import json
import os
import re
from typing import Optional

from openai import APIConnectionError, APIStatusError, OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")


def _extract_json_block(text: str) -> Optional[str]:
    text = text.strip()

    if text.startswith("{") and text.endswith("}"):
        return text

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return None


def _clean_str(value) -> Optional[str]:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _normalize_result(data: dict) -> dict:
    company = _clean_str(data.get("company"))
    role = _clean_str(data.get("role"))
    contact = _clean_str(data.get("contact"))
    use_case = _clean_str(data.get("use_case"))

    try:
        confidence = float(data.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(0.0, min(confidence, 1.0))

    missing_fields = []
    if not company:
        missing_fields.append("company")
    if not role:
        missing_fields.append("role")
    if not contact:
        missing_fields.append("contact")
    if not use_case:
        missing_fields.append("use_case")

    return {
        "company": company,
        "role": role,
        "contact": contact,
        "use_case": use_case,
        "extraction_method": "llm_v1",
        "confidence": round(confidence, 2),
        "missing_fields": missing_fields,
        "is_qualified_candidate": bool(company and use_case and (contact or role)),
    }


def is_llm_available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def llm_extract_fields(message_text: str) -> Optional[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    client = OpenAI(
        api_key=api_key,
        timeout=20.0,
        max_retries=1,
    )

    prompt = f"""
You are an extraction engine for inbound B2B lead messages.

Extract these fields from the message:
- company
- role
- contact
- use_case
- confidence

Rules:
- Return ONLY valid JSON.
- If a field is missing, use null.
- confidence must be a number from 0 to 1.
- Preserve the original language when useful.
- Do not add commentary.
- Do not wrap JSON in markdown fences.

JSON shape:
{{
  "company": "string or null",
  "role": "string or null",
  "contact": "string or null",
  "use_case": "string or null",
  "confidence": 0.0
}}

Message:
{message_text}
""".strip()

    try:
        response = client.responses.create(
            model=DEFAULT_MODEL,
            input=prompt,
        )

        raw_text = (response.output_text or "").strip()
        json_block = _extract_json_block(raw_text)
        if not json_block:
            return None

        parsed = json.loads(json_block)
        if not isinstance(parsed, dict):
            return None

        return _normalize_result(parsed)

    except (APIConnectionError, APIStatusError, json.JSONDecodeError, ValueError, TypeError):
        return None
