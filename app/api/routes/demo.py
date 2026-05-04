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
        company="Bloom Retail",
        role="Growth Lead",
        contact="@bloom_growth",
        use_case="holiday promo game to collect emails and boost repeat purchases",
        status="qualified",
    )

    lead_in_progress = Lead(
        company="UrbanFit",
        role="CMO",
        contact="@urbanfit_cmo",
        use_case="spin-to-win campaign for Shopify lead capture",
        notes="Prepare campaign mechanic recommendation and CRM handoff",
        status="qualified",
    )

    lead_followup = Lead(
        company="FreshBox",
        role="Growth Lead",
        contact="@freshbox_growth",
        use_case="retention campaign with rewards for returning customers",
        status="needs_followup",
    )

    lead_agency = Lead(
        company="Nova Agency",
        role="Director",
        contact="@nova_agency",
        use_case="branded Advent Calendar campaign for a client",
        status="qualified",
    )

    lead_launch = Lead(
        company="GameLaunch Studio",
        role="CMO",
        contact="@gamelaunch_cmo",
        use_case="quiz lead magnet for a new product launch",
        status="qualified",
    )

    db.add_all([lead_done, lead_in_progress, lead_followup, lead_agency, lead_launch])
    db.flush()

    messages = [
        Message(
            lead_id=lead_done.id,
            sender="user",
            text="We are Bloom Retail. Need a holiday promo game to collect emails and boost repeat purchases. Contact @bloom_growth",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_done.id,
            sender="assistant",
            text="The campaign lead is qualified and ready for a gamified mechanic handoff.",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_in_progress.id,
            sender="user",
            text="We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo",
            detected_intent="integration_question",
        ),
        Message(
            lead_id=lead_in_progress.id,
            sender="assistant",
            text="Spin-to-win is recommended for Shopify lead capture and first-purchase activation.",
            detected_intent="integration_question",
        ),
        Message(
            lead_id=lead_followup.id,
            sender="user",
            text="We are FreshBox. Need a retention campaign with rewards for returning customers. Contact @freshbox_growth",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_followup.id,
            sender="assistant",
            text="Please confirm the campaign owner and launch timing.",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_agency.id,
            sender="user",
            text="We are Nova Agency. Need a branded Advent Calendar campaign for a client. Contact @nova_agency",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_agency.id,
            sender="assistant",
            text="Advent Calendar is recommended for a branded seasonal client campaign.",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_launch.id,
            sender="user",
            text="We are GameLaunch Studio. Need a quiz lead magnet for a new product launch. Contact @gamelaunch_cmo",
            detected_intent="other",
        ),
        Message(
            lead_id=lead_launch.id,
            sender="assistant",
            text="Quiz / Lead Magnet is recommended for product launch intent capture.",
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
        Handoff(
            lead_id=lead_agency.id,
            reason="auto_created_from_chat",
            assigned_to="Tony",
            status="pending",
        ),
        Handoff(
            lead_id=lead_launch.id,
            reason="auto_created_from_chat",
            assigned_to="Tony",
            status="pending",
        ),
    ]

    db.add_all(handoffs)
    db.commit()

    return {
        "status": "ok",
        "deleted_before_seed": deleted,
        "seeded": {
            "leads": 5,
            "messages": 10,
            "handoffs": 4,
        },
        "seeded_lead_ids": [
            lead_in_progress.id,
            lead_done.id,
            lead_followup.id,
            lead_agency.id,
            lead_launch.id,
        ],
    }
