from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import EventLog, Handoff, Lead, Message
from app.db.session import get_db
from app.services.event_service import log_event
from app.services.handoff_package_service import build_handoff_package
from app.services.owner_routing_service import resolve_owner_routing

router = APIRouter(prefix="/handoffs", tags=["handoffs"])

HANDOFF_STATUSES = {"pending", "in_progress", "done"}
HANDOFF_STATUS_ALIASES = {"completed": "done"}


class UpdateHandoffRequest(BaseModel):
    assigned_to: str | None = None
    status: str | None = None


class AssignOwnerRequest(BaseModel):
    owner: str
    team: str | None = None


def _normalize_handoff_status(status: str | None) -> str | None:
    if status is None:
        return None
    return HANDOFF_STATUS_ALIASES.get(status, status)


def _log_handoff_status_event(db: Session, handoff: Handoff, previous_status: str | None) -> None:
    if previous_status == handoff.status:
        return

    if handoff.status == "in_progress":
        event_type = "handoff_moved_to_in_progress"
    elif handoff.status == "done":
        event_type = "handoff_completed"
    else:
        return

    log_event(
        db,
        handoff.lead_id,
        event_type,
        {
            "handoff_id": handoff.id,
            "previous_status": previous_status,
            "status": handoff.status,
        },
    )


def _handoff_response(handoff: Handoff) -> dict:
    return {
        "status": "ok",
        "handoff_id": handoff.id,
        "lead_id": handoff.lead_id,
        "reason": handoff.reason,
        "assigned_to": handoff.assigned_to,
        "handoff_status": handoff.status,
        "created_at": str(handoff.created_at),
    }


def _update_latest_handoff_status(lead_id: int, status: str, db: Session) -> dict:
    status = _normalize_handoff_status(status) or status
    handoff = (
        db.query(Handoff)
        .filter(Handoff.lead_id == lead_id)
        .order_by(Handoff.id.desc())
        .first()
    )
    if handoff is None:
        return {
            "status": "error",
            "message": f"Handoff for lead {lead_id} not found",
        }

    previous_status = handoff.status
    handoff.status = status
    db.add(handoff)
    db.commit()
    db.refresh(handoff)
    _log_handoff_status_event(db, handoff, previous_status)

    return _handoff_response(handoff)


def _latest_handoff(db: Session, lead_id: int) -> Handoff | None:
    return (
        db.query(Handoff)
        .filter(Handoff.lead_id == lead_id)
        .order_by(Handoff.id.desc())
        .first()
    )


def _latest_message(db: Session, lead_id: int) -> Message | None:
    return (
        db.query(Message)
        .filter(Message.lead_id == lead_id)
        .order_by(Message.id.desc())
        .first()
    )


def _latest_owner_event(db: Session, lead_id: int) -> EventLog | None:
    return (
        db.query(EventLog)
        .filter(EventLog.lead_id == lead_id, EventLog.event_type == "owner_assigned")
        .order_by(EventLog.id.desc())
        .first()
    )


def _clean(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


@router.get("")
def list_handoffs(db: Session = Depends(get_db)) -> list[dict]:
    handoffs = db.query(Handoff).order_by(Handoff.id.desc()).all()

    items = []
    for handoff in handoffs:
        lead = db.get(Lead, handoff.lead_id)
        owner_event = _latest_owner_event(db, handoff.lead_id)
        owner_routing = resolve_owner_routing(
            lead,
            handoff,
            [owner_event] if owner_event is not None else [],
        )
        assigned_to = owner_routing["owner"]
        if assigned_to == "Unassigned":
            assigned_to = None

        items.append(
            {
                "id": handoff.id,
                "lead_id": handoff.lead_id,
                "reason": handoff.reason,
                "assigned_to": assigned_to,
                "owner_routing": owner_routing,
                "status": handoff.status,
                "handoff_status": handoff.status,
                "created_at": str(handoff.created_at),
            }
        )

    return items


@router.get("/{handoff_id}")
def get_handoff(handoff_id: int, db: Session = Depends(get_db)) -> dict:
    handoff = db.get(Handoff, handoff_id)
    if handoff is None:
        return {
            "status": "error",
            "message": f"Handoff {handoff_id} not found",
        }

    return {
        "status": "ok",
        "id": handoff.id,
        "lead_id": handoff.lead_id,
        "reason": handoff.reason,
        "assigned_to": handoff.assigned_to,
        "handoff_status": handoff.status,
        "created_at": str(handoff.created_at),
    }


@router.patch("/{handoff_id}")
def update_handoff(
    handoff_id: int,
    payload: UpdateHandoffRequest,
    db: Session = Depends(get_db),
) -> dict:
    handoff = db.get(Handoff, handoff_id)
    if handoff is None:
        return {
            "status": "error",
            "message": f"Handoff {handoff_id} not found",
        }

    allowed_statuses = HANDOFF_STATUSES | set(HANDOFF_STATUS_ALIASES)

    if payload.status is not None and payload.status not in allowed_statuses:
        return {
            "status": "error",
            "message": "Invalid status. Use: pending, in_progress, done",
        }

    previous_status = handoff.status

    if payload.assigned_to is not None:
        handoff.assigned_to = payload.assigned_to

    if payload.status is not None:
        handoff.status = _normalize_handoff_status(payload.status) or payload.status

    db.add(handoff)
    db.commit()
    db.refresh(handoff)
    _log_handoff_status_event(db, handoff, previous_status)

    return _handoff_response(handoff)


@router.post("/{lead_id}/in-progress")
@router.post("/{lead_id}/start")
@router.post("/{lead_id}/in_progress")
def set_handoff_in_progress(lead_id: int, db: Session = Depends(get_db)) -> dict:
    return _update_latest_handoff_status(lead_id, "in_progress", db)


@router.post("/{lead_id}/done")
@router.post("/{lead_id}/complete")
def set_handoff_done(lead_id: int, db: Session = Depends(get_db)) -> dict:
    return _update_latest_handoff_status(lead_id, "done", db)


@router.post("/{lead_id}/assign")
def assign_handoff_owner(
    lead_id: int,
    payload: AssignOwnerRequest,
    db: Session = Depends(get_db),
) -> dict:
    handoff = _latest_handoff(db, lead_id)
    if handoff is None:
        return {
            "status": "error",
            "message": f"Handoff for lead {lead_id} not found",
        }

    owner = _clean(payload.owner) or "Unassigned"
    team = _clean(payload.team) or "Intake"

    if hasattr(handoff, "assigned_to"):
        handoff.assigned_to = None if owner == "Unassigned" else owner
        db.add(handoff)
        db.commit()
        db.refresh(handoff)

    log_event(
        db,
        lead_id,
        "owner_assigned",
        {
            "owner": owner,
            "team": team,
            "reason": "Manual owner assignment",
            "handoff_id": handoff.id,
        },
    )

    return {
        "status": "ok",
        "lead_id": lead_id,
        "owner": owner,
        "team": team,
        "handoff_id": handoff.id,
    }


@router.post("/{lead_id}/export-crm")
def export_handoff_to_crm(lead_id: int, db: Session = Depends(get_db)) -> dict:
    lead = db.get(Lead, lead_id)
    if lead is None:
        return {
            "status": "error",
            "message": f"Lead {lead_id} not found",
        }

    latest_handoff = _latest_handoff(db, lead_id)
    if latest_handoff is None:
        return {
            "status": "error",
            "message": f"Handoff for lead {lead_id} not found",
        }

    handoff_package = build_handoff_package(
        lead,
        latest_handoff=latest_handoff,
        latest_message=_latest_message(db, lead_id),
        events=[_latest_owner_event(db, lead_id)],
    )
    log_event(
        db,
        lead_id,
        "crm_export_simulated",
        {
            "handoff_id": latest_handoff.id,
            "target": "demo_crm",
            "status": "ok",
        },
    )

    return {
        "status": "ok",
        "message": "CRM export simulated",
        "lead_id": lead.id,
        "handoff_status": latest_handoff.status,
        "crm_payload": handoff_package["crm_payload"],
    }
