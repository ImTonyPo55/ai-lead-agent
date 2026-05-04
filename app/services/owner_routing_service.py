from __future__ import annotations

from typing import Any

from app.services.campaign_intelligence_service import build_campaign_intelligence


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

    intelligence = build_campaign_intelligence(lead)
    return int(intelligence.get("score") or 0)


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

    intelligence = build_campaign_intelligence(lead)
    missing_fields = intelligence.get("missing_fields") or []
    pricing_tier = _clean(intelligence.get("pricing_tier"))
    use_case = _clean(getattr(lead, "use_case", None)).casefold()
    text = " ".join(
        part
        for part in (
            use_case,
            _clean(getattr(lead, "notes", None)).casefold(),
        )
        if part
    )

    if missing_fields:
        return {
            "owner": "Unassigned",
            "team": "Intake",
            "reason": "Missing key qualification fields",
        }

    if any(signal in text for signal in ("crm", "cdp", "api", "integration", "gdpr", "analytics")):
        return {
            "owner": "Tony",
            "team": "Tech / Support",
            "reason": "Technical integration mentioned",
        }

    if pricing_tier == "DIY Tier":
        return {
            "owner": "Tony",
            "team": "Sales",
            "reason": "DIY campaign package",
        }

    if pricing_tier == "Done-With-You Tier":
        return {
            "owner": "Tony",
            "team": "Sales / Delivery",
            "reason": "Done-With-You campaign package",
        }

    if pricing_tier == "Enterprise Tier":
        return {
            "owner": "Tony",
            "team": "Enterprise",
            "reason": "Enterprise campaign package",
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
