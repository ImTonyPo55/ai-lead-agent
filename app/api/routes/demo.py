from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import EventLog, Handoff, Lead, Message
from app.db.session import get_db

router = APIRouter(prefix="/demo", tags=["demo"])


def _clear_demo_tables(db: Session) -> dict:
    deleted_event_logs = db.query(EventLog).delete()
    deleted_handoffs = db.query(Handoff).delete()
    deleted_messages = db.query(Message).delete()
    deleted_leads = db.query(Lead).delete()

    db.commit()

    return {
        "event_logs": deleted_event_logs,
        "handoffs": deleted_handoffs,
        "messages": deleted_messages,
        "leads": deleted_leads,
    }


@router.post("/reset")
def reset_demo_data(db: Session = Depends(get_db)) -> dict:
    deleted = _clear_demo_tables(db)

    return {
        "status": "ok",
        "deleted": deleted,
    }


@router.post("/seed")
def seed_demo_data(db: Session = Depends(get_db)) -> dict:
    deleted = _clear_demo_tables(db)

    lead_done = Lead(
        company="Nova Growth",
        role="founder",
        contact="@nova_founder",
        use_case="автоматизация входящих B2B-заявок",
        status="qualified",
    )

    lead_in_progress = Lead(
        company="We2 Digital",
        role="founder",
        contact="@tony_new",
        use_case="AI lead intake + CRM",
        notes="Важно показать demo на следующей встрече",
        status="qualified",
    )

    lead_followup = Lead(
        company="Test Patch Co",
        role="CEO",
        contact="@patch_test",
        use_case="Нужен AI lead intake",
        status="needs_followup",
    )

    db.add_all([lead_done, lead_in_progress, lead_followup])
    db.flush()

    messages = [
        Message(
            lead_id=lead_done.id,
            sender="user",
            text="Мы из компании Nova Growth. Я founder. Нужна автоматизация входящих B2B-заявок. Контакт @nova_founder",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_done.id,
            sender="assistant",
            text="Понял ваш запрос. Спасибо, базовую информацию получил.",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_in_progress.id,
            sender="user",
            text="Нужна ещё интеграция с CRM",
            detected_intent="integration_question",
        ),
        Message(
            lead_id=lead_in_progress.id,
            sender="assistant",
            text="Да, это можно обсудить как интеграционный сценарий.",
            detected_intent="integration_question",
        ),
        Message(
            lead_id=lead_followup.id,
            sender="user",
            text="Я founder, мой контакт @patch_test",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_followup.id,
            sender="assistant",
            text="Опишите, пожалуйста, какую задачу хотите решить.",
            detected_intent="other",
        ),
    ]

    db.add_all(messages)
    db.flush()

    handoffs = [
        Handoff(
            lead_id=lead_done.id,
            reason="auto_created_from_chat",
            assigned_to="Tony",
            status="done",
        ),
        Handoff(
            lead_id=lead_in_progress.id,
            reason="auto_created_from_chat",
            assigned_to="Tony",
            status="in_progress",
        ),
    ]

    db.add_all(handoffs)
    db.commit()

    return {
        "status": "ok",
        "deleted_before_seed": deleted,
        "seeded": {
            "leads": 3,
            "messages": 6,
            "handoffs": 2,
        },
        "seeded_lead_ids": [
            lead_in_progress.id,
            lead_done.id,
            lead_followup.id,
        ],
    }
