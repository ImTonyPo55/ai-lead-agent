from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Tuple

from sqlalchemy.orm import Session


def _clean(value: Optional[str]) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _compact_key(value: str) -> str:
    return "".join(char for char in value.casefold() if char.isalnum())


def _should_update_use_case(lead: Any, use_case: str, company: str) -> bool:
    if not use_case:
        return False

    existing_use_case = _clean(getattr(lead, "use_case", None))
    if existing_use_case:
        return False

    if company and _compact_key(use_case) == _compact_key(company):
        return False

    return True


def update_lead_fields(lead: Any, extracted: Optional[Dict[str, Any]] = None) -> bool:
    extracted = extracted or {}
    changed = False

    company = _clean(extracted.get("company"))
    role = _clean(extracted.get("role"))
    contact = _clean(extracted.get("contact"))
    use_case = _clean(extracted.get("use_case"))

    if company and not getattr(lead, "company", None):
        lead.company = company
        changed = True

    if role and not getattr(lead, "role", None):
        lead.role = role
        changed = True

    if contact and not getattr(lead, "contact", None):
        lead.contact = contact
        changed = True

    if _should_update_use_case(lead, use_case, company):
        lead.use_case = use_case
        changed = True

    return changed


def apply_agent_status(lead: Any, decision: Any) -> bool:
    current_status = getattr(lead, "status", None)
    next_action = getattr(decision, "next_action", "noop")
    should_create_handoff = bool(
        getattr(decision, "should_create_handoff", False))
    should_ask_followup = bool(getattr(decision, "should_ask_followup", False))

    new_status = current_status

    if should_ask_followup or next_action == "ask_followup":
        new_status = "needs_followup"
    elif should_create_handoff or next_action in {"qualify_lead", "create_handoff"}:
        new_status = "qualified"

    if new_status and new_status != current_status:
        lead.status = new_status
        return True

    return False


def maybe_create_handoff(
    db: Session,
    lead: Any,
    decision: Any,
    create_handoff_fn: Optional[Callable[[
        Session, Any], Tuple[Optional[int], bool]]] = None,
) -> Tuple[Optional[int], bool]:
    should_create_handoff = bool(
        getattr(decision, "should_create_handoff", False))

    if not should_create_handoff:
        return None, False

    if create_handoff_fn is None:
        return None, False

    return create_handoff_fn(db, lead)


def apply_agent_decision(
    db: Session,
    lead: Any,
    extracted: Optional[Dict[str, Any]],
    decision: Any,
    create_handoff_fn: Optional[Callable[[
        Session, Any], Tuple[Optional[int], bool]]] = None,
) -> Dict[str, Any]:
    lead_changed = False

    if update_lead_fields(lead, extracted):
        lead_changed = True

    if apply_agent_status(lead, decision):
        lead_changed = True

    if lead_changed:
        db.add(lead)
        db.commit()
        db.refresh(lead)

    handoff_id, handoff_created = maybe_create_handoff(
        db=db,
        lead=lead,
        decision=decision,
        create_handoff_fn=create_handoff_fn,
    )

    return {
        "lead_changed": lead_changed,
        "handoff_id": handoff_id,
        "handoff_created": handoff_created,
        "lead_status": getattr(lead, "status", None),
        "company": getattr(lead, "company", None),
        "role": getattr(lead, "role", None),
        "contact": getattr(lead, "contact", None),
        "use_case": getattr(lead, "use_case", None),
    }
