from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import Handoff
from app.db.session import get_db

router = APIRouter(prefix="/handoffs", tags=["handoffs"])


class UpdateHandoffRequest(BaseModel):
    assigned_to: str | None = None
    status: str | None = None


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

    allowed_statuses = {"pending", "in_progress", "done"}

    if payload.status is not None and payload.status not in allowed_statuses:
        return {
            "status": "error",
            "message": "Invalid status. Use: pending, in_progress, done",
        }

    if payload.assigned_to is not None:
        handoff.assigned_to = payload.assigned_to

    if payload.status is not None:
        handoff.status = payload.status

    db.add(handoff)
    db.commit()
    db.refresh(handoff)

    return {
        "status": "ok",
        "handoff_id": handoff.id,
        "lead_id": handoff.lead_id,
        "reason": handoff.reason,
        "assigned_to": handoff.assigned_to,
        "handoff_status": handoff.status,
        "created_at": str(handoff.created_at),
    }
