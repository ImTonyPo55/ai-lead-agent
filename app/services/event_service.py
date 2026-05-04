from typing import Any

from sqlalchemy.orm import Session

from app.db.models import EventLog


EVENT_LABELS = {
    "lead_created": "Лид создан",
    "message_received": "Получено сообщение",
    "lead_qualified": "Лид квалифицирован",
    "handoff_created": "Передача создана",
    "telegram_notification_sent": "Telegram-уведомление отправлено",
    "telegram_notification_failed": "Ошибка Telegram-уведомления",
    "telegram_notification_skipped": "Telegram-уведомление не отправлено",
    "handoff_moved_to_in_progress": "Передача взята в работу",
    "handoff_completed": "Передача завершена",
    "crm_export_simulated": "CRM-экспорт подготовлен",
    "owner_assigned": "Ответственный назначен",
    "action_contacted": "Связались с лидом",
    "action_waiting_reply": "Ждём ответ от лида",
    "action_closed": "Действие закрыто",
}

STATUS_LABELS = {
    "new": "новый",
    "needs_followup": "требует уточнения",
    "qualified": "квалифицирован",
    "pending": "готов к передаче",
    "in_progress": "в работе",
    "done": "завершено",
    "completed": "завершено",
}

PUBLIC_PAYLOAD_KEYS = {
    "source",
    "message_id",
    "intent",
    "text",
    "previous_status",
    "status",
    "handoff_id",
    "reason",
    "success",
    "target",
    "owner",
    "team",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _short(value: Any, limit: int = 120) -> str:
    text = _clean(value)
    if len(text) <= limit:
        return text
    return f"{text[:limit - 3]}..."


def _status(value: Any) -> str:
    text = _clean(value)
    return STATUS_LABELS.get(text, text)


def _safe_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {}


def _public_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: _short(value, 180)
        for key, value in payload.items()
        if key in PUBLIC_PAYLOAD_KEYS and value is not None
    }


def format_event_details(event_type: str, payload: dict[str, Any] | None = None) -> str:
    payload = _safe_payload(payload)

    if event_type == "lead_created":
        source = _short(payload.get("source"))
        return f"Источник: {source}" if source else ""

    if event_type == "message_received":
        text = _short(payload.get("text"))
        intent = _short(payload.get("intent"))
        if text and intent:
            return f"{text} · intent: {intent}"
        return text or (f"intent: {intent}" if intent else "")

    if event_type == "lead_qualified":
        previous_status = _status(payload.get("previous_status"))
        status = _status(payload.get("status"))
        if previous_status and status:
            return f"{previous_status} → {status}"
        return status

    if event_type == "handoff_created":
        handoff_id = _short(payload.get("handoff_id"))
        reason = _short(payload.get("reason"))
        parts = []
        if handoff_id:
            parts.append(f"handoff #{handoff_id}")
        if reason:
            parts.append(reason)
        return " · ".join(parts)

    if event_type in {
        "telegram_notification_sent",
        "telegram_notification_failed",
        "telegram_notification_skipped",
    }:
        handoff_id = _short(payload.get("handoff_id"))
        return f"handoff #{handoff_id}" if handoff_id else ""

    if event_type in {"handoff_moved_to_in_progress", "handoff_completed"}:
        handoff_id = _short(payload.get("handoff_id"))
        previous_status = _status(payload.get("previous_status"))
        status = _status(payload.get("status"))
        parts = []
        if handoff_id:
            parts.append(f"handoff #{handoff_id}")
        if previous_status and status:
            parts.append(f"{previous_status} → {status}")
        elif status:
            parts.append(status)
        return " · ".join(parts)

    if event_type == "crm_export_simulated":
        handoff_id = _short(payload.get("handoff_id"))
        target = _short(payload.get("target"))
        status = _short(payload.get("status"))
        parts = []
        if handoff_id:
            parts.append(f"handoff #{handoff_id}")
        if target:
            parts.append(target)
        if status:
            parts.append(status)
        return " · ".join(parts)

    if event_type == "owner_assigned":
        owner = _short(payload.get("owner"))
        team = _short(payload.get("team"))
        reason = _short(payload.get("reason"))
        return " · ".join(part for part in (owner, team, reason) if part)

    if event_type in {"action_contacted", "action_waiting_reply", "action_closed"}:
        previous_status = _short(payload.get("previous_status"))
        status = _short(payload.get("status"))
        owner = _short(payload.get("owner"))
        team = _short(payload.get("team"))
        parts = []
        if previous_status and status:
            parts.append(f"{previous_status} → {status}")
        elif status:
            parts.append(status)
        parts.extend(part for part in (owner, team) if part)
        return " · ".join(parts)

    return ""


def format_event(event: EventLog) -> dict[str, Any]:
    payload = _public_payload(_safe_payload(event.payload))
    return {
        "id": event.id,
        "event_type": event.event_type,
        "label": EVENT_LABELS.get(event.event_type, "Событие CRM"),
        "details": format_event_details(event.event_type, payload),
        "payload": payload,
        "created_at": str(event.created_at),
    }


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
