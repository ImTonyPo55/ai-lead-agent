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

    return handoff.id, True


@router.post("/message")
def chat_message(payload: ChatMessageRequest, db: Session = Depends(get_db)) -> dict:
    if payload.lead_id:
        lead = db.get(Lead, payload.lead_id)
        if lead is None:
            return {
                "status": "error",
                "message": f"Lead {payload.lead_id} not found",
            }
    else:
        lead = Lead()
        db.add(lead)
        db.commit()
        db.refresh(lead)

    company = extract_company(payload.message)
    role = extract_role(payload.message)
    contact = extract_contact(payload.message)
    use_case = extract_use_case(payload.message)

    if company and not lead.company:
        lead.company = company

    if role and not lead.role:
        lead.role = role

    if contact and not lead.contact:
        lead.contact = contact

    if use_case and not lead.use_case:
        lead.use_case = use_case

    lead.status = calculate_lead_status(lead)

    db.add(lead)
    db.commit()
    db.refresh(lead)

    intent = detect_intent(payload.message)
    reply = build_followup_reply(lead, intent)

    user_message = Message(
        lead_id=lead.id,
        sender=SenderType.USER.value,
        text=payload.message,
        detected_intent=intent,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    assistant_message = Message(
        lead_id=lead.id,
        sender=SenderType.ASSISTANT.value,
        text=reply,
        detected_intent=intent,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    handoff_id, handoff_created = create_handoff_if_needed(db, lead)

    return {
        "status": "ok",
        "lead_id": lead.id,
        "message_id": user_message.id,
        "assistant_message_id": assistant_message.id,
        "lead_status": lead.status,
        "handoff_id": handoff_id,
        "handoff_created": handoff_created,
        "intent": intent,
        "company": lead.company,
        "role": lead.role,
        "contact": lead.contact,
        "use_case": lead.use_case,
        "reply": reply,
    }
