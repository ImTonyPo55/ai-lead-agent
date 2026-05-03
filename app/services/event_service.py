from typing import Any

from sqlalchemy.orm import Session

from app.db.models import EventLog


def log_event(
    db: Session,
    lead_id: int,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> EventLog | None:
    try:
        event = EventLog(
            lead_id=lead_id,
            event_type=event_type,
            payload=payload or {},
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    except Exception:
        db.rollback()
        return None
