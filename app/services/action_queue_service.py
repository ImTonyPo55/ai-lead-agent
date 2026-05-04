from __future__ import annotations

from typing import Any

from app.services.owner_routing_service import resolve_owner_routing

ACTION_LABELS = {
    "new": "Новое действие",
    "contacted": "Связались",
    "waiting_reply": "Ждём ответ",
    "closed": "Действие закрыто",
}

NEXT_ACTIONS = {
    "new": "Contact the lead and confirm the business need",
    "contacted": "Wait for reply or send follow-up",
    "waiting_reply": "Monitor reply and prepare next follow-up",
    "closed": "No active follow-up action",
}

EVENT_STATUS = {
    "action_contacted": "contacted",
    "action_waiting_reply": "waiting_reply",
    "action_closed": "closed",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _latest_action_status(events: Any) -> str:
    if not events:
        return "new"

    for event in events:
        status = EVENT_STATUS.get(getattr(event, "event_type", None))
        if status:
            return status

    return "new"


def get_action_status(
    lead: Any,
    latest_handoff: Any = None,
    events: Any = None,
) -> dict:
    status = _latest_action_status(events)
    lead_status = _clean(getattr(lead, "status", None))
    reason = (
        "Qualified lead with handoff package"
        if lead_status == "qualified" and latest_handoff is not None
        else "Needs review"
    )
    owner_routing = resolve_owner_routing(lead, latest_handoff, events)

    return {
        "status": status,
        "label": ACTION_LABELS.get(status, ACTION_LABELS["new"]),
        "next_action": NEXT_ACTIONS.get(status, NEXT_ACTIONS["new"]),
        "reason": reason,
        "owner": owner_routing.get("owner") or "Unassigned",
        "team": owner_routing.get("team") or "Intake",
    }
