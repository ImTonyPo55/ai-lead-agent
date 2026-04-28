from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Literal

from pydantic import BaseModel, Field

from app.services.llm_service import llm_extract_fields


CRITICAL_FIELDS = ["company", "contact", "use_case"]


class AgentDecision(BaseModel):
    intent: str = "other"
    next_action: Literal[
        "ask_followup",
        "qualify_lead",
        "create_handoff",
        "update_lead",
        "reply_only",
        "noop",
    ] = "noop"
    should_ask_followup: bool = False
    should_create_handoff: bool = False
    should_update_lead: bool = False
    should_create_new_lead: bool = False
    confidence: float = 0.0
    missing_fields: List[str] = Field(default_factory=list)
    reply_text: str = ""
    notes: str = ""


def _clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return " ".join(str(value).strip().split())


def _has_value(value: Optional[str]) -> bool:
    return bool(_clean_text(value))


def _missing_fields(extracted: Optional[Dict[str, Any]]) -> List[str]:
    data = extracted or {}
    missing: List[str] = []

    for field in CRITICAL_FIELDS:
        if not _has_value(data.get(field)):
            missing.append(field)

    return missing


def _followup_question(missing_fields: List[str]) -> str:
    if not missing_fields:
        return "Спасибо. Данных достаточно — продолжаю квалификацию лида."

    mapping = {
        "company": "название компании",
        "contact": "лучший контакт для связи",
        "use_case": "какую задачу вы хотите решить",
    }

    parts = [mapping[field] for field in missing_fields if field in mapping]

    if not parts:
        return (
            "Спасибо. Чтобы корректно квалифицировать запрос, "
            "уточните, пожалуйста, недостающие данные."
        )

    if len(parts) == 1:
        return (
            "Спасибо. Чтобы подготовить лид к передаче в работу, "
            f"уточните, пожалуйста: {parts[0]}."
        )

    if len(parts) == 2:
        return (
            "Спасибо. Чтобы подготовить лид к передаче в работу, "
            f"уточните, пожалуйста: {parts[0]} и {parts[1]}."
        )

    return (
        "Спасибо. Чтобы подготовить лид к передаче в работу, "
        f"уточните, пожалуйста: {parts[0]}, {parts[1]} и {parts[2]}."
    )


def build_agent_prompt(
    message_text: str,
    extracted: Optional[Dict[str, Any]] = None,
    current_lead: Optional[Dict[str, Any]] = None,
) -> str:
    cleaned_message = _clean_text(message_text)
    extracted = extracted or {}
    current_lead = current_lead or {}

    return f"""
You are an agent decision engine for inbound B2B lead qualification.

Your job is to decide the next best action after a user message.

Return ONLY valid JSON with these keys:
- intent
- next_action
- should_ask_followup
- should_create_handoff
- should_update_lead
- should_create_new_lead
- confidence
- missing_fields
- reply_text
- notes

Allowed next_action values:
- ask_followup
- qualify_lead
- create_handoff
- update_lead
- reply_only
- noop

Rules:
1. If company/contact/use_case are missing, ask a focused follow-up.
2. If enough data is present, qualify the lead.
3. If the lead is qualified and not yet handed off, create handoff.
4. Be concise.
5. reply_text must be short and usable as an assistant reply.
6. Do not invent fields that are absent in the message or current lead.
7. Confidence must be a float between 0 and 1.

MESSAGE:
{cleaned_message}

EXTRACTED:
{json.dumps(extracted, ensure_ascii=False)}

CURRENT_LEAD:
{json.dumps(current_lead, ensure_ascii=False)}
""".strip()


def _parse_agent_decision_json(raw_text: Optional[str]) -> Optional[AgentDecision]:
    if not raw_text:
        return None

    text = str(raw_text).strip()
    if not text:
        return None

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None

        try:
            data = json.loads(text[start: end + 1])
        except json.JSONDecodeError:
            return None

    if not isinstance(data, dict):
        return None

    try:
        return AgentDecision.model_validate(data)
    except Exception:
        return None


def rule_based_agent_decide(
    message_text: str,
    extracted: Optional[Dict[str, Any]] = None,
    current_lead: Optional[Dict[str, Any]] = None,
) -> AgentDecision:
    _ = _clean_text(message_text)
    extracted = extracted or {}
    current_lead = current_lead or {}

    missing_fields = _missing_fields(extracted)
    lead_exists = bool(current_lead)

    if missing_fields:
        return AgentDecision(
            intent="lead_followup",
            next_action="ask_followup",
            should_ask_followup=True,
            should_create_handoff=False,
            should_update_lead=lead_exists,
            should_create_new_lead=not lead_exists,
            confidence=0.78,
            missing_fields=missing_fields,
            reply_text=_followup_question(missing_fields),
            notes="Critical lead fields are missing.",
        )

    return AgentDecision(
        intent="qualified_lead",
        next_action="create_handoff",
        should_ask_followup=False,
        should_create_handoff=True,
        should_update_lead=True,
        should_create_new_lead=not lead_exists,
        confidence=0.92,
        missing_fields=[],
        reply_text=(
            "Готово. Я извлёк ключевые данные, квалифицировал лид "
            "и подготовил его к передаче в работу."
        ),
        notes="Lead has enough data for qualification and handoff.",
    )


def llm_agent_decide(
    message_text: str,
    extracted: Optional[Dict[str, Any]] = None,
    current_lead: Optional[Dict[str, Any]] = None,
) -> Optional[AgentDecision]:
    try:
        prompt = build_agent_prompt(
            message_text=message_text,
            extracted=extracted,
            current_lead=current_lead,
        )

        raw_result = llm_extract_fields(prompt)
    except Exception:
        return None

    if not raw_result:
        return None

    if isinstance(raw_result, str):
        return _parse_agent_decision_json(raw_result)

    if not isinstance(raw_result, dict):
        return None

    for key in ("raw_text", "output_text"):
        parsed = _parse_agent_decision_json(raw_result.get(key))
        if parsed is not None:
            return parsed

    required_keys = {
        "intent",
        "next_action",
        "should_ask_followup",
        "should_create_handoff",
        "should_update_lead",
        "should_create_new_lead",
        "confidence",
        "missing_fields",
        "reply_text",
        "notes",
    }
    if not required_keys.issubset(raw_result.keys()):
        return None

    try:
        return AgentDecision.model_validate(raw_result)
    except Exception:
        return None


def agent_decide(
    message_text: str,
    extracted: Optional[Dict[str, Any]] = None,
    current_lead: Optional[Dict[str, Any]] = None,
    use_llm: bool = False,
) -> AgentDecision:
    if use_llm:
        llm_decision = llm_agent_decide(
            message_text=message_text,
            extracted=extracted,
            current_lead=current_lead,
        )
        if llm_decision is not None:
            return llm_decision

    return rule_based_agent_decide(
        message_text=message_text,
        extracted=extracted,
        current_lead=current_lead,
    )
