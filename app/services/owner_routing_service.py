from __future__ import annotations

from typing import Any


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _score(lead: Any, latest_handoff: Any = None) -> int:
    explicit_score = getattr(lead, "score", None)
    try:
        if explicit_score is not None:
            return int(explicit_score)
    except (TypeError, ValueError):
        pass

    score = 0
    if _clean(getattr(lead, "company", None)):
        score += 25
    if _clean(getattr(lead, "contact", None)):
        score += 25
    if _clean(getattr(lead, "use_case", None)):
        score += 25
    if _clean(getattr(lead, "role", None)):
        score += 10
    if latest_handoff is not None:
        score += 15

    return min(score, 100)


def _team_for_owner(owner: str) -> str:
    if owner == "Tony":
        return "Sales"
    if owner == "Support Lead":
        return "Customer Success"
    return "Intake"


def _event_payload(event: Any) -> dict:
    payload = getattr(event, "payload", None)
    if isinstance(payload, dict):
        return payload
    return {}


def _latest_owner_event(events: Any) -> dict:
    if not events:
        return {}

    for event in events:
        if getattr(event, "event_type", None) == "owner_assigned":
            return _event_payload(event)

    return {}


def recommend_owner(lead: Any, latest_handoff: Any = None) -> dict:
    existing_owner = _clean(getattr(latest_handoff, "assigned_to", None))
    if existing_owner:
        return {
            "owner": existing_owner,
            "team": _team_for_owner(existing_owner),
            "reason": "Existing handoff owner",
        }

    score = _score(lead, latest_handoff)
    priority = _clean(getattr(lead, "priority", None))
    use_case = _clean(getattr(lead, "use_case", None)).casefold()

    if score >= 90 or priority == "High" or (not priority and score >= 80):
        return {
            "owner": "Tony",
            "team": "Sales",
            "reason": "High-priority qualified lead",
        }

    if "crm" in use_case or "routing" in use_case:
        return {
            "owner": "Tony",
            "team": "Sales",
            "reason": "CRM automation request",
        }

    if "support" in use_case or "customer" in use_case:
        return {
            "owner": "Support Lead",
            "team": "Customer Success",
            "reason": "Customer support automation request",
        }

    return {
        "owner": "Unassigned",
        "team": "Intake",
        "reason": "Needs manual review",
    }


def resolve_owner_routing(
    lead: Any,
    latest_handoff: Any = None,
    events: Any = None,
) -> dict:
    event_payload = _latest_owner_event(events)
    event_owner = _clean(event_payload.get("owner"))
    event_team = _clean(event_payload.get("team"))
    event_reason = _clean(event_payload.get("reason"))
    handoff_owner = _clean(getattr(latest_handoff, "assigned_to", None))
    lead_owner = _clean(getattr(lead, "assigned_to", None)) or _clean(
        getattr(lead, "assignee", None)
    )

    if handoff_owner:
        return {
            "owner": handoff_owner,
            "team": event_team or _team_for_owner(handoff_owner),
            "reason": event_reason or "Existing handoff owner",
        }

    if lead_owner:
        return {
            "owner": lead_owner,
            "team": event_team or _team_for_owner(lead_owner),
            "reason": event_reason or "Existing lead owner",
        }

    if event_owner:
        return {
            "owner": event_owner,
            "team": event_team or _team_for_owner(event_owner),
            "reason": event_reason or "Latest owner assignment event",
        }

    return recommend_owner(lead, latest_handoff)
