from sqlalchemy.orm import Session

from app.db.models import EventLog


def log_event(db: Session, lead_id: int, event_type: str, payload: dict) -> EventLog:
    event = EventLog(
        lead_id=lead_id,
        event_type=event_type,
        payload=payload,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
