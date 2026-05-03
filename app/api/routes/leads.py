from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import Lead, Message, Handoff, EventLog
from app.db.session import get_db
from app.services.event_service import format_event, log_event

router = APIRouter(prefix="/leads", tags=["leads"])


class UpdateLeadRequest(BaseModel):
    name: str | None = None
    company: str | None = None
    role: str | None = None
    contact: str | None = None
    use_case: str | None = None
    request_type: str | None = None
    industry: str | None = None
    market: str | None = None
    budget: str | None = None
    timeline: str | None = None
    notes: str | None = None
    status: str | None = None


def _latest_handoff(db: Session, lead_id: int) -> Handoff | None:
    return (
        db.query(Handoff)
        .filter(Handoff.lead_id == lead_id)
        .order_by(Handoff.id.desc())
        .first()
    )


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
        reason="auto_created_from_lead_patch",
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

    return handoff.id, True


@router.get("")
def list_leads(db: Session = Depends(get_db)) -> list[dict]:
    leads = db.query(Lead).order_by(Lead.id.desc()).all()

    items = []
    for lead in leads:
        latest_handoff = _latest_handoff(db, lead.id)
        items.append(
            {
                "id": lead.id,
                "name": lead.name,
                "company": lead.company,
                "role": lead.role,
                "contact": lead.contact,
                "use_case": lead.use_case,
                "status": lead.status,
                "handoff_id": latest_handoff.id if latest_handoff else None,
                "handoff_status": latest_handoff.status if latest_handoff else None,
                "created_at": str(lead.created_at),
            }
        )

    return items


@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)) -> dict:
    lead = db.get(Lead, lead_id)
    if lead is None:
        return {
            "status": "error",
            "message": f"Lead {lead_id} not found",
        }

    return {
        "status": "ok",
        "id": lead.id,
        "name": lead.name,
        "company": lead.company,
        "role": lead.role,
        "contact": lead.contact,
        "use_case": lead.use_case,
        "request_type": lead.request_type,
        "industry": lead.industry,
        "market": lead.market,
        "budget": lead.budget,
        "timeline": lead.timeline,
        "notes": lead.notes,
        "lead_status": lead.status,
        "created_at": str(lead.created_at),
        "updated_at": str(lead.updated_at),
    }


@router.patch("/{lead_id}")
def update_lead(
    lead_id: int,
    payload: UpdateLeadRequest,
    db: Session = Depends(get_db),
) -> dict:
    lead = db.get(Lead, lead_id)
    if lead is None:
        return {
            "status": "error",
            "message": f"Lead {lead_id} not found",
        }

    allowed_statuses = {"new", "needs_followup", "qualified"}

    if payload.status is not None and payload.status not in allowed_statuses:
        return {
            "status": "error",
            "message": "Invalid status. Use: new, needs_followup, qualified",
        }

    previous_status = lead.status

    if payload.name is not None:
        lead.name = payload.name
    if payload.company is not None:
        lead.company = payload.company
    if payload.role is not None:
        lead.role = payload.role
    if payload.contact is not None:
        lead.contact = payload.contact
    if payload.use_case is not None:
        lead.use_case = payload.use_case
    if payload.request_type is not None:
        lead.request_type = payload.request_type
    if payload.industry is not None:
        lead.industry = payload.industry
    if payload.market is not None:
        lead.market = payload.market
    if payload.budget is not None:
        lead.budget = payload.budget
    if payload.timeline is not None:
        lead.timeline = payload.timeline
    if payload.notes is not None:
        lead.notes = payload.notes
    if payload.status is not None:
        lead.status = payload.status

    db.add(lead)
    db.commit()
    db.refresh(lead)

    if previous_status != "qualified" and lead.status == "qualified":
        log_event(
            db,
            lead.id,
            "lead_qualified",
            {"previous_status": previous_status, "status": lead.status},
        )

    handoff_id, handoff_created = create_handoff_if_needed(db, lead)

    return {
        "status": "ok",
        "lead_id": lead.id,
        "handoff_id": handoff_id,
        "handoff_created": handoff_created,
        "name": lead.name,
        "company": lead.company,
        "role": lead.role,
        "contact": lead.contact,
        "use_case": lead.use_case,
        "request_type": lead.request_type,
        "industry": lead.industry,
        "market": lead.market,
        "budget": lead.budget,
        "timeline": lead.timeline,
        "notes": lead.notes,
        "lead_status": lead.status,
        "created_at": str(lead.created_at),
        "updated_at": str(lead.updated_at),
    }


@router.get("/{lead_id}/messages")
def get_lead_messages(lead_id: int, db: Session = Depends(get_db)) -> dict:
    lead = db.get(Lead, lead_id)
    if lead is None:
        return {
            "status": "error",
            "message": f"Lead {lead_id} not found",
        }

    messages = (
        db.query(Message)
        .filter(Message.lead_id == lead_id)
        .order_by(Message.id.asc())
        .all()
    )

    return {
        "status": "ok",
        "lead_id": lead_id,
        "messages": [
            {
                "id": message.id,
                "lead_id": message.lead_id,
                "sender": message.sender,
                "text": message.text,
                "detected_intent": message.detected_intent,
            }
            for message in messages
        ],
    }


@router.get("/{lead_id}/summary")
def get_lead_summary(lead_id: int, db: Session = Depends(get_db)) -> dict:
    lead = db.get(Lead, lead_id)
    if lead is None:
        return {
            "status": "error",
            "message": f"Lead {lead_id} not found",
        }

    latest_message = (
        db.query(Message)
        .filter(Message.lead_id == lead_id)
        .order_by(Message.id.desc())
        .first()
    )

    latest_handoff = _latest_handoff(db, lead_id)

    score = 0

    if lead.company:
        score += 25
    if lead.contact:
        score += 25
    if lead.use_case:
        score += 25
    if lead.role:
        score += 10
    if latest_handoff:
        score += 15

    score = min(score, 100)

    if score >= 75:
        priority = "High"
    elif score >= 40:
        priority = "Medium"
    else:
        priority = "Low"

    message_count = db.query(Message).filter(
        Message.lead_id == lead_id).count()

    try:
        events = (
            db.query(EventLog)
            .filter(EventLog.lead_id == lead_id)
            .order_by(EventLog.id.desc())
            .limit(8)
            .all()
        )
    except Exception:
        db.rollback()
        events = []

    return {
        "status": "ok",
        "score": score,
        "priority": priority,
        "lead": {
            "id": lead.id,
            "name": lead.name,
            "company": lead.company,
            "role": lead.role,
            "contact": lead.contact,
            "use_case": lead.use_case,
            "lead_status": lead.status,
        },
        "handoff": {
            "id": latest_handoff.id if latest_handoff else None,
            "assigned_to": latest_handoff.assigned_to if latest_handoff else None,
            "handoff_status": latest_handoff.status if latest_handoff else None,
            "reason": latest_handoff.reason if latest_handoff else None,
        },
        "conversation": {
            "message_count": message_count,
            "last_message_id": latest_message.id if latest_message else None,
            "last_sender": latest_message.sender if latest_message else None,
            "last_text": latest_message.text if latest_message else None,
            "last_intent": latest_message.detected_intent if latest_message else None,
        },
        "events": [format_event(event) for event in events],
    }
