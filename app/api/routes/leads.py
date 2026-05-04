from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import Lead, Message, Handoff, EventLog
from app.db.session import get_db
from app.services.action_queue_service import get_action_status
from app.services.campaign_intelligence_service import build_campaign_intelligence
from app.services.event_service import format_event, log_event
from app.services.handoff_package_service import build_handoff_package
from app.services.owner_routing_service import recommend_owner, resolve_owner_routing

router = APIRouter(prefix="/leads", tags=["leads"])

ACTION_EVENT_TYPES = {"action_contacted", "action_waiting_reply", "action_closed"}


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


def _latest_owner_event(db: Session, lead_id: int) -> EventLog | None:
    return (
        db.query(EventLog)
        .filter(EventLog.lead_id == lead_id, EventLog.event_type == "owner_assigned")
        .order_by(EventLog.id.desc())
        .first()
    )


def _latest_action_event(db: Session, lead_id: int) -> EventLog | None:
    return (
        db.query(EventLog)
        .filter(EventLog.lead_id == lead_id, EventLog.event_type.in_(ACTION_EVENT_TYPES))
        .order_by(EventLog.id.desc())
        .first()
    )


def _latest_routing_events(db: Session, lead_id: int) -> list[EventLog]:
    events = []
    owner_event = _latest_owner_event(db, lead_id)
    action_event = _latest_action_event(db, lead_id)
    if owner_event is not None:
        events.append(owner_event)
    if action_event is not None:
        events.append(action_event)
    return events


def create_handoff_if_needed(db: Session, lead: Lead) -> tuple[int | None, bool]:
    intelligence = build_campaign_intelligence(lead)
    if not intelligence.get("can_create_handoff"):
        next_status = intelligence.get("lead_status") or "needs_followup"
        if lead.status not in {
            "active_handoff",
            "completed_handoff",
            "in_progress",
            "done",
        } and lead.status != next_status:
            lead.status = next_status
            db.add(lead)
            db.commit()
            db.refresh(lead)
        return None, False

    existing_handoff = (
        db.query(Handoff)
        .filter(Handoff.lead_id == lead.id)
        .first()
    )
    if existing_handoff:
        if lead.status not in {
            "ready_to_handoff",
            "active_handoff",
            "completed_handoff",
            "in_progress",
            "done",
        }:
            lead.status = "ready_to_handoff"
            db.add(lead)
            db.commit()
            db.refresh(lead)
        return existing_handoff.id, False

    owner_routing = recommend_owner(lead)
    handoff = Handoff(
        lead_id=lead.id,
        reason="auto_created_from_lead_patch",
    )
    if hasattr(handoff, "assigned_to") and owner_routing["owner"] != "Unassigned":
        handoff.assigned_to = owner_routing["owner"]
    db.add(handoff)
    db.commit()
    db.refresh(handoff)
    lead.status = "ready_to_handoff"
    db.add(lead)
    db.commit()
    db.refresh(lead)
    log_event(
        db,
        lead.id,
        "handoff_created",
        {"handoff_id": handoff.id, "reason": handoff.reason},
    )
    log_event(
        db,
        lead.id,
        "owner_assigned",
        {
            "owner": owner_routing["owner"],
            "team": owner_routing["team"],
            "reason": owner_routing["reason"],
            "handoff_id": handoff.id,
        },
    )

    return handoff.id, True


@router.get("")
def list_leads(db: Session = Depends(get_db)) -> list[dict]:
    leads = db.query(Lead).order_by(Lead.id.desc()).all()

    items = []
    for lead in leads:
        latest_handoff = _latest_handoff(db, lead.id)
        routing_events = _latest_routing_events(db, lead.id)
        action_queue = get_action_status(lead, latest_handoff, routing_events)
        handoff_package = build_handoff_package(
            lead,
            latest_handoff=latest_handoff,
            events=routing_events,
        )
        items.append(
            {
                "id": lead.id,
                "name": lead.name,
                "company": lead.company,
                "role": lead.role,
                "contact": lead.contact,
                "use_case": lead.use_case,
                "client_type": handoff_package["client_type"],
                "campaign_goal": handoff_package["campaign_goal"],
                "platform": handoff_package["platform"],
                "recommended_mechanic": handoff_package["recommended_mechanic"],
                "mechanic_reason": handoff_package["mechanic_reason"],
                "pricing_tier": handoff_package["pricing_tier"],
                "qualification_status": handoff_package["qualification_status"],
                "missing_fields": handoff_package["missing_fields"],
                "recommended_package": handoff_package["recommended_package"],
                "score": handoff_package["score"],
                "priority": handoff_package["priority"],
                "status": handoff_package["qualification_status"],
                "lead_status": handoff_package["qualification_status"],
                "handoff_id": latest_handoff.id if latest_handoff else None,
                "handoff_status": latest_handoff.status if latest_handoff else None,
                "action_queue": action_queue,
                "action_status": action_queue["status"],
                "action_label": action_queue["label"],
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

    allowed_statuses = {
        "new",
        "needs_followup",
        "needs_follow_up",
        "qualified",
        "ready_to_handoff",
        "active_handoff",
        "completed_handoff",
        "in_progress",
        "done",
    }

    if payload.status is not None and payload.status not in allowed_statuses:
        return {
            "status": "error",
            "message": "Invalid status. Use: new, needs_followup, qualified, ready_to_handoff, active_handoff, completed_handoff",
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

    if previous_status not in {"qualified", "ready_to_handoff"} and lead.status == "ready_to_handoff":
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
    latest_user_message = (
        db.query(Message)
        .filter(Message.lead_id == lead_id, Message.sender == "user")
        .order_by(Message.id.desc())
        .first()
    )

    latest_handoff = _latest_handoff(db, lead_id)

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
    latest_owner_event = _latest_owner_event(db, lead_id)
    latest_action_event = _latest_action_event(db, lead_id)
    routing_events = [
        event for event in (latest_owner_event, latest_action_event) if event is not None
    ] + [
        event for event in events
        if event.event_type != "owner_assigned" and event.event_type not in ACTION_EVENT_TYPES
    ]
    owner_routing = resolve_owner_routing(lead, latest_handoff, routing_events)
    action_queue = get_action_status(lead, latest_handoff, routing_events)
    handoff_package = build_handoff_package(
        lead,
        latest_handoff=latest_handoff,
        latest_message=latest_user_message,
        events=routing_events,
    )
    score = handoff_package["score"]
    priority = handoff_package["priority"]

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
            "campaign_summary": handoff_package["campaign_summary"],
            "client_type": handoff_package["client_type"],
            "campaign_goal": handoff_package["campaign_goal"],
            "platform": handoff_package["platform"],
            "recommended_mechanic": handoff_package["recommended_mechanic"],
            "mechanic_reason": handoff_package["mechanic_reason"],
            "pricing_tier": handoff_package["pricing_tier"],
            "qualification_status": handoff_package["qualification_status"],
            "missing_fields": handoff_package["missing_fields"],
            "recommended_package": handoff_package["recommended_package"],
            "next_question": handoff_package["next_question"],
            "recommended_next_action": handoff_package["recommended_next_action"],
            "lead_status": handoff_package["qualification_status"],
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
        "owner_routing": owner_routing,
        "action_queue": action_queue,
        "handoff_package": handoff_package,
        "events": [format_event(event) for event in events],
    }
