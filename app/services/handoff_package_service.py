from __future__ import annotations

from typing import Any

from app.services.action_queue_service import get_action_status
from app.services.owner_routing_service import resolve_owner_routing


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _display(value: Any) -> str:
    return _clean(value) or "-"


def _score(lead: Any, latest_handoff: Any = None) -> int:
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


def _priority(score: int) -> str:
    if score >= 80:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def _summary(lead: Any, latest_handoff: Any = None) -> str:
    company = _display(getattr(lead, "company", None))
    role = _display(getattr(lead, "role", None))
    use_case = _display(getattr(lead, "use_case", None))
    contact = _display(getattr(lead, "contact", None))
    handoff_status = _display(getattr(latest_handoff, "status", None))

    return (
        f"{company} is a qualified B2B lead for {use_case}. "
        f"Primary contact is {contact}; role is {role}; handoff status is {handoff_status}."
    )


def _qualification_reason(lead: Any, latest_handoff: Any = None) -> str:
    missing = []

    if not _clean(getattr(lead, "company", None)):
        missing.append("company")
    if not _clean(getattr(lead, "contact", None)):
        missing.append("contact")
    if not _clean(getattr(lead, "use_case", None)):
        missing.append("use case")

    if missing:
        return f"Missing required CRM handoff fields: {', '.join(missing)}."

    if latest_handoff is not None:
        return "Qualified because company, contact and use case are available, and a handoff is created."

    return "Qualified because company, contact and use case are available."


def build_handoff_package(
    lead: Any,
    latest_handoff: Any = None,
    latest_message: Any = None,
    events: Any = None,
) -> dict:
    score = _score(lead, latest_handoff)
    priority = _priority(score)
    company = _clean(getattr(lead, "company", None)) or None
    role = _clean(getattr(lead, "role", None)) or None
    contact = _clean(getattr(lead, "contact", None)) or None
    use_case = _clean(getattr(lead, "use_case", None)) or None
    lead_status = _clean(getattr(lead, "status", None)) or None
    handoff_status = _clean(getattr(latest_handoff, "status", None)) or None
    owner_routing = resolve_owner_routing(lead, latest_handoff, events)
    action_queue = get_action_status(lead, latest_handoff, events)

    recommended_next_action = (
        "Send to CRM and assign owner"
        if contact and use_case
        else "Request missing info before CRM export"
    )
    crm_payload = {
        "company": company,
        "contact": contact,
        "role": role,
        "use_case": use_case,
        "priority": priority,
        "score": score,
        "source": "AI Lead Agent",
        "handoff_status": handoff_status,
        "owner": owner_routing["owner"],
        "team": owner_routing["team"],
        "action_status": action_queue["status"],
        "next_action": action_queue["next_action"],
    }
    copy_text = "\n".join(
        [
            "AI Lead Agent handoff package",
            f"Lead ID: {_display(getattr(lead, 'id', None))}",
            f"Company: {_display(company)}",
            f"Role: {_display(role)}",
            f"Contact: {_display(contact)}",
            f"Use case: {_display(use_case)}",
            f"Lead status: {_display(lead_status)}",
            f"Handoff status: {_display(handoff_status)}",
            f"Owner: {_display(owner_routing['owner'])}",
            f"Team: {_display(owner_routing['team'])}",
            f"Routing reason: {_display(owner_routing['reason'])}",
            f"Action status: {_display(action_queue['label'])}",
            f"Next action: {_display(action_queue['next_action'])}",
            f"Score: {score}",
            f"Priority: {priority}",
            f"Summary: {_summary(lead, latest_handoff)}",
            f"Qualification reason: {_qualification_reason(lead, latest_handoff)}",
            f"Recommended next action: {recommended_next_action}",
        ]
    )

    return {
        "lead_id": getattr(lead, "id", None),
        "company": company,
        "role": role,
        "contact": contact,
        "use_case": use_case,
        "lead_status": lead_status,
        "handoff_status": handoff_status,
        "owner": owner_routing["owner"],
        "team": owner_routing["team"],
        "routing_reason": owner_routing["reason"],
        "action_status": action_queue["status"],
        "next_action": action_queue["next_action"],
        "score": score,
        "priority": priority,
        "summary": _summary(lead, latest_handoff),
        "qualification_reason": _qualification_reason(lead, latest_handoff),
        "recommended_next_action": recommended_next_action,
        "crm_payload": crm_payload,
        "copy_text": copy_text,
    }
