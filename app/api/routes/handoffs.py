from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import Handoff
from app.db.session import get_db
from app.services.event_service import log_event

router = APIRouter(prefix="/handoffs", tags=["handoffs"])


class UpdateHandoffRequest(BaseModel):
    assigned_to: str | None = None
    status: str | None = None


def _log_handoff_status_event(db: Session, handoff: Handoff, previous_status: str | None) -> None:
    if previous_status == handoff.status:
        return

    if handoff.status == "in_progress":
        event_type = "handoff_moved_to_in_progress"
    elif handoff.status in {"done", "completed"}:
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


@router.get("")
def list_handoffs(db: Session = Depends(get_db)) -> list[dict]:
    handoffs = db.query(Handoff).order_by(Handoff.id.desc()).all()

    return [
        {
            "id": handoff.id,
            "lead_id": handoff.lead_id,
            "reason": handoff.reason,
            "assigned_to": handoff.assigned_to,
            "status": handoff.status,
            "created_at": str(handoff.created_at),
        }
        for handoff in handoffs
    ]


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

    allowed_statuses = {"pending", "in_progress", "done", "completed"}

    if payload.status is not None and payload.status not in allowed_statuses:
        return {
            "status": "error",
            "message": "Invalid status. Use: pending, in_progress, done, completed",
        }

    previous_status = handoff.status

    if payload.assigned_to is not None:
        handoff.assigned_to = payload.assigned_to

    if payload.status is not None:
        handoff.status = payload.status

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
