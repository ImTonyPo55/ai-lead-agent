from __future__ import annotations

from typing import Any

from app.services.action_queue_service import get_action_status
from app.services.campaign_intelligence_service import build_campaign_intelligence
from app.services.owner_routing_service import resolve_owner_routing


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _display(value: Any) -> str:
    return _clean(value) or "-"


def _timestamp(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _summary(
    lead: Any,
    latest_handoff: Any = None,
    campaign_summary: str | None = None,
    recommended_mechanic: str | None = None,
) -> str:
    if campaign_summary:
        return campaign_summary

    company = _display(getattr(lead, "company", None))
    contact = _display(getattr(lead, "contact", None))
    handoff_status = _display(getattr(latest_handoff, "status", None))
    goal = _display(getattr(lead, "use_case", None))
    mechanic = _display(recommended_mechanic)

    return (
        f"{company} is a qualified campaign lead for {goal}. "
        f"Best game for this campaign: {mechanic}; primary contact is {contact}; handoff status is {handoff_status}."
    )


def _qualification_reason(
    lead: Any,
    latest_handoff: Any = None,
    missing_fields: Any = None,
) -> str:
    missing = list(missing_fields or [])

    if not missing:
        if not _clean(getattr(lead, "company", None)):
            missing.append("company")
        if not _clean(getattr(lead, "contact", None)):
            missing.append("contact")
        if not _clean(getattr(lead, "use_case", None)):
            missing.append("campaign need")

    if missing:
        return f"Missing required campaign handoff fields: {', '.join(missing)}."

    if latest_handoff is not None:
        return "Qualified because company, contact and campaign goal are available, and a handoff is created."

    return "Qualified because company, contact and campaign goal are available."


def build_crm_handoff_payload(
    lead: Any,
    latest_handoff: Any,
    latest_message: Any,
    campaign_intelligence: dict,
    owner_routing: dict,
    action_queue: dict,
    qualification_status: str,
    handoff_status: str | None,
) -> dict | None:
    if campaign_intelligence.get("missing_fields"):
        return None
    if qualification_status not in {
        "ready_to_handoff",
        "active_handoff",
        "completed_handoff",
    }:
        return None

    qualification_reason = _qualification_reason(
        lead,
        latest_handoff,
        campaign_intelligence.get("missing_fields"),
    )

    return {
        "lead_id": getattr(lead, "id", None),
        "handoff_id": getattr(latest_handoff, "id", None),
        "company": _clean(getattr(lead, "company", None)) or None,
        "contact": _clean(getattr(lead, "contact", None)) or None,
        "role": _clean(getattr(lead, "role", None)) or None,
        "campaign_need": _clean(getattr(lead, "use_case", None)) or None,
        "client_type": campaign_intelligence["client_type"],
        "campaign_goal": campaign_intelligence["campaign_goal"],
        "platform": campaign_intelligence["platform"],
        "recommended_mechanic": campaign_intelligence["recommended_mechanic"],
        "best_game": campaign_intelligence["recommended_mechanic"],
        "recommended_tier": campaign_intelligence["pricing_tier"],
        "pricing_tier": campaign_intelligence["pricing_tier"],
        "score": campaign_intelligence["score"],
        "priority": campaign_intelligence["priority"],
        "owner": owner_routing["owner"],
        "team": owner_routing["team"],
        "next_action": campaign_intelligence["recommended_next_action"],
        "qualification_reason": qualification_reason,
        "qualification_status": qualification_status,
        "handoff_status": handoff_status,
        "source_message": _clean(getattr(latest_message, "text", None)) or None,
        "created_at": _timestamp(
            getattr(latest_handoff, "created_at", None)
            or getattr(lead, "created_at", None)
        ),
        "updated_at": _timestamp(
            getattr(lead, "updated_at", None)
            or getattr(latest_handoff, "created_at", None)
            or getattr(lead, "created_at", None)
        ),
    }


def build_handoff_package(
    lead: Any,
    latest_handoff: Any = None,
    latest_message: Any = None,
    events: Any = None,
) -> dict:
    company = _clean(getattr(lead, "company", None)) or None
    role = _clean(getattr(lead, "role", None)) or None
    contact = _clean(getattr(lead, "contact", None)) or None
    use_case = _clean(getattr(lead, "use_case", None)) or None
    handoff_status = _clean(getattr(latest_handoff, "status", None)) or None
    campaign_intelligence = build_campaign_intelligence(lead, latest_message)
    score = campaign_intelligence["score"]
    priority = campaign_intelligence["priority"]
    client_type = campaign_intelligence["client_type"]
    campaign_goal = campaign_intelligence["campaign_goal"]
    platform = campaign_intelligence["platform"]
    recommended_mechanic = campaign_intelligence["recommended_mechanic"]
    mechanic_reason = campaign_intelligence["mechanic_reason"]
    pricing_tier = campaign_intelligence["pricing_tier"]
    qualification_status = campaign_intelligence["qualification_status"]
    if handoff_status in {"in_progress", "active_handoff"}:
        qualification_status = "active_handoff"
    elif handoff_status in {"done", "completed", "completed_handoff"}:
        qualification_status = "completed_handoff"
    elif latest_handoff is not None:
        qualification_status = "ready_to_handoff"
    lead_status = qualification_status
    missing_fields = campaign_intelligence["missing_fields"]
    recommended_next_action = campaign_intelligence["recommended_next_action"]
    campaign_summary = campaign_intelligence["campaign_summary"]
    copy_ready_followup = campaign_intelligence["copy_text"]
    next_question = campaign_intelligence["next_question"]
    owner_routing = resolve_owner_routing(lead, latest_handoff, events)
    action_queue = get_action_status(lead, latest_handoff, events)

    crm_payload = build_crm_handoff_payload(
        lead=lead,
        latest_handoff=latest_handoff,
        latest_message=latest_message,
        campaign_intelligence=campaign_intelligence,
        owner_routing=owner_routing,
        action_queue=action_queue,
        qualification_status=qualification_status,
        handoff_status=handoff_status,
    )
    package_copy_text = "\n".join(
        [
            "MechanicFlow AI campaign handoff package",
            f"Lead ID: {_display(getattr(lead, 'id', None))}",
            f"Campaign summary: {_display(campaign_summary)}",
            f"Company: {_display(company)}",
            f"Role: {_display(role)}",
            f"Contact: {_display(contact)}",
            f"Client type: {_display(client_type)}",
            f"Campaign goal: {_display(campaign_goal)}",
            f"Platform: {_display(platform)}",
            f"Recommended game mechanic: {_display(recommended_mechanic)}",
            f"Why it fits: {_display(mechanic_reason)}",
            f"Suggested tier: {_display(pricing_tier)}",
            f"Qualification status: {_display(qualification_status)}",
            f"Missing fields: {_display(', '.join(missing_fields))}",
            f"Lead status: {_display(lead_status)}",
            f"Handoff status: {_display(handoff_status)}",
            f"Owner: {_display(owner_routing['owner'])}",
            f"Team: {_display(owner_routing['team'])}",
            f"Routing reason: {_display(owner_routing['reason'])}",
            f"Action status: {_display(action_queue['label'])}",
            f"Next action: {_display(action_queue['next_action'])}",
            f"Score: {score}",
            f"Priority: {priority}",
            f"Summary: {_summary(lead, latest_handoff, campaign_summary, recommended_mechanic)}",
            f"Qualification reason: {_qualification_reason(lead, latest_handoff, missing_fields)}",
            f"Recommended next action: {recommended_next_action}",
            f"Copy-ready follow-up: {_display(copy_ready_followup)}",
        ]
    )

    return {
        "lead_id": getattr(lead, "id", None),
        "company": company,
        "role": role,
        "contact": contact,
        "use_case": use_case,
        "campaign_summary": campaign_summary,
        "client_type": client_type,
        "client_type_label": campaign_intelligence["client_type_label"],
        "campaign_goal": campaign_goal,
        "campaign_goal_label": campaign_intelligence["campaign_goal_label"],
        "platform": platform,
        "recommended_mechanic": recommended_mechanic,
        "best_game": recommended_mechanic,
        "mechanic_reason": mechanic_reason,
        "recommended_mechanic_reason": mechanic_reason,
        "pricing_tier": pricing_tier,
        "recommended_package": pricing_tier,
        "qualification_status": qualification_status,
        "missing_fields": missing_fields,
        "next_question": next_question,
        "lead_status": lead_status,
        "handoff_status": handoff_status,
        "owner": owner_routing["owner"],
        "team": owner_routing["team"],
        "routing_reason": owner_routing["reason"],
        "action_status": action_queue["status"],
        "next_action": action_queue["next_action"],
        "score": score,
        "priority": priority,
        "summary": _summary(lead, latest_handoff, campaign_summary, recommended_mechanic),
        "qualification_reason": _qualification_reason(lead, latest_handoff, missing_fields),
        "recommended_next_action": recommended_next_action,
        "crm_payload": crm_payload,
        "campaign_intelligence": campaign_intelligence,
        "copy_text": copy_ready_followup,
        "copy_ready_followup": copy_ready_followup,
        "package_copy_text": package_copy_text,
    }
