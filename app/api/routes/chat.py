from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Lead, Message, SenderType, Handoff
from app.db.session import get_db
from app.schemas.chat import ChatMessageRequest
from app.services.extract_service import (
    extract_company,
    extract_contact,
    extract_role,
    extract_use_case,
)
from app.services.intent_service import detect_intent
from app.services.knowledge_service import answer_from_knowledge_base
from app.services.event_service import log_event
from app.services.telegram_service import notify_handoff_created
router = APIRouter(prefix="/chat", tags=["chat"])


def build_reply_by_intent(intent: str) -> str:
    if intent == "pricing":
        return "Стоимость зависит от сценария, объёма и интеграций."
    if intent == "demo_request":
        return "Да, можем показать демо."
    if intent == "consultation_request":
        return "Да, можно организовать консультацию."
    if intent == "integration_question":
        return "Да, это можно обсудить как интеграционный сценарий."
    if intent == "partnership":
        return "Понял, это похоже на запрос по партнёрству."
    if intent == "support":
        return "Понял, это похоже на запрос в поддержку."
    return "Понял ваш запрос."


def build_followup_reply(lead: Lead, intent: str) -> str:
    base_reply = build_reply_by_intent(intent)

    if not lead.company:
        return f"{base_reply} Подскажите, пожалуйста, название компании."

    if not lead.role:
        return f"{base_reply} Подскажите, пожалуйста, вашу роль в компании."

    if not lead.use_case:
        return f"{base_reply} Опишите, пожалуйста, какую задачу хотите решить."

    if not lead.contact:
        return f"{base_reply} Оставьте, пожалуйста, удобный контакт для связи."

    return f"{base_reply} Спасибо, базовую информацию получил."


def calculate_lead_status(lead: Lead) -> str:
    if lead.company and lead.role and lead.use_case and lead.contact:
        return "qualified"
    return "needs_followup"


def create_handoff_if_needed(db: Session, lead: Lead) -> tuple[int | None, bool]:
    if lead.status != "qualified":
        return None, False

    existing_handoff = (
        db.query(Handoff)
        .filter(Handoff.lead_id == lead.id)
        .first()
    )
    if existing_handoff:
        return existing_handoff.id, False

    handoff = Handoff(
        lead_id=lead.id,
        reason="auto_created_from_chat",
    )
    db.add(handoff)
    db.commit()
    db.refresh(handoff)
    log_event(
        db,
        lead.id,
        "handoff_created",
        {"handoff_id": handoff.id, "reason": handoff.reason},
    )
    telegram_sent = notify_handoff_created(lead, handoff)
    log_event(
        db,
        lead.id,
        "telegram_notification_sent" if telegram_sent else "telegram_notification_failed",
        {"handoff_id": handoff.id, "success": telegram_sent},
    )

    return handoff.id, True


@router.post("/message")
def chat_message(payload: ChatMessageRequest, db: Session = Depends(get_db)) -> dict:
    import re
    from app.services.agent_service import agent_decide
    from app.services.action_executor import apply_agent_decision

    if payload.lead_id:
        lead = db.get(Lead, payload.lead_id)
        if lead is None:
            return {
                "status": "error",
                "message": f"Lead {payload.lead_id} not found",
            }
        current_lead = {
            "id": lead.id,
            "company": lead.company,
            "role": lead.role,
            "contact": lead.contact,
            "use_case": lead.use_case,
            "status": lead.status,
        }
    else:
        lead = Lead()
        db.add(lead)
        db.commit()
        db.refresh(lead)
        log_event(db, lead.id, "lead_created", {"source": "chat"})
        current_lead = None

    company = extract_company(payload.message)
    if company:
        normalized_company = company.strip()

        if normalized_company.lower().strip(".,!?:;") in {
            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "good morning",
            "good afternoon",
            "good evening",
        }:
            normalized_company = ""

        normalized_company = re.sub(
            r"(?i)[\s\.,;:]+best(?:\s+contact.*)?$",
            "",
            normalized_company,
        ).strip(" .,!?:;")

        normalized_company = re.sub(
            r"(?i)[\s\.,;:]+contact(?:\s+is.*)?$",
            "",
            normalized_company,
        ).strip(" .,!?:;")

        company = normalized_company or None

    role = extract_role(payload.message)
    contact = extract_contact(payload.message)
    use_case = extract_use_case(payload.message)

    extracted = {
        "company": company,
        "role": role,
        "contact": contact,
        "use_case": use_case,
    }

    if current_lead:
        for field in ("company", "role", "contact", "use_case"):
            if not extracted.get(field) and current_lead.get(field):
                extracted[field] = current_lead[field]

    decision = agent_decide(
        message_text=payload.message,
        extracted=extracted,
        current_lead=current_lead,
        use_llm=True,
    )

    previous_status = lead.status

    action_result = apply_agent_decision(
        db=db,
        lead=lead,
        extracted=extracted,
        decision=decision,
        create_handoff_fn=create_handoff_if_needed,
    )

    if previous_status != "qualified" and action_result["lead_status"] == "qualified":
        log_event(
            db,
            lead.id,
            "lead_qualified",
            {"previous_status": previous_status, "status": action_result["lead_status"]},
        )

    intent = decision.intent
    knowledge_reply = answer_from_knowledge_base(payload.message)
    reply = decision.reply_text or build_followup_reply(lead, intent)

    if knowledge_reply and decision.intent != "qualified_lead":
        reply = f"{knowledge_reply}\n\n{reply}"

    user_message = Message(
        lead_id=lead.id,
        sender=SenderType.USER.value,
        text=payload.message,
        detected_intent=intent,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    log_event(
        db,
        lead.id,
        "message_received",
        {
            "message_id": user_message.id,
            "intent": intent,
            "text": payload.message[:160],
        },
    )

    assistant_message = Message(
        lead_id=lead.id,
        sender=SenderType.ASSISTANT.value,
        text=reply,
        detected_intent=intent,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {
        "status": "ok",
        "lead_id": lead.id,
        "message_id": user_message.id,
        "assistant_message_id": assistant_message.id,
        "lead_status": action_result["lead_status"],
        "handoff_id": action_result["handoff_id"],
        "handoff_created": action_result["handoff_created"],
        "intent": intent,
        "company": action_result["company"],
        "role": action_result["role"],
        "contact": action_result["contact"],
        "use_case": action_result["use_case"],
        "reply": reply,
        "next_action": decision.next_action,
        "should_ask_followup": decision.should_ask_followup,
        "should_create_handoff": decision.should_create_handoff,
        "should_update_lead": decision.should_update_lead,
        "should_create_new_lead": decision.should_create_new_lead,
        "missing_fields": decision.missing_fields,
        "confidence": decision.confidence,
        "notes": decision.notes,
        "lead_changed": action_result["lead_changed"],
    }
