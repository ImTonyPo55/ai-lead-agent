import re
from typing import Optional

from app.services.llm_service import is_llm_available, llm_extract_fields


ROLE_MAP = {
    "founder": "Founder",
    "cofounder": "Co-founder",
    "co-founder": "Co-founder",
    "ceo": "CEO",
    "cto": "CTO",
    "cpo": "CPO",
    "owner": "Owner",
    "director": "Director",
    "основатель": "Founder",
    "сооснователь": "Co-founder",
    "фаундер": "Founder",
    "владелец": "Owner",
    "директор": "Director",
    "fundador": "Founder",
    "cofundador": "Co-founder",
    "dueño": "Owner",
    "dueno": "Owner",
    "director general": "Director",
    "directora": "Director",
}

ROLE_PATTERN = re.compile(
    r"\b(" + "|".join(sorted((re.escape(k)
                              for k in ROLE_MAP.keys()), key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

CONTACT_PATTERN = re.compile(r"(?<!\w)@[A-Za-z0-9_]{3,32}\b")
EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?:(?:\+?\d[\d\s().-]{7,}\d))")

COMPANY_PATTERNS = [
    re.compile(
        r"(?:\bwe are\b|\bwe're\b|\bi am from\b|\bi'm from\b|\bfrom company\b|\bcompany[:\s])\s+([A-Z][A-Za-z0-9&.\- ]{1,60})",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\bмы из\b|\bиз компании\b|\bкомпания[:\s])\s+([A-ZА-ЯЁ][A-Za-zА-Яа-яЁё0-9&.\- ]{1,60})",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\bsomos de\b|\bsoy de\b|\bempresa[:\s]|\bde la empresa\b)\s+([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ0-9&.\- ]{1,60})",
        re.IGNORECASE,
    ),
    re.compile(
        r"^\s*([A-Z][A-Za-z0-9&.\- ]{1,60}?)\s+here\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"^\s*([A-ZА-ЯЁ][A-Za-zА-Яа-яЁё0-9&.\- ]{1,60}?)(?:,\s*(?:i am|i'm|я|soy|somos|need|нуж|buscamos|necesitamos)|[,.]\s|$)",
        re.IGNORECASE,
    ),
]

USE_CASE_PATTERNS = [
    re.compile(
        r"(?:\bneed\b|\blooking for\b|\bneed help with\b|\binterested in\b|\bwant\b)\s+(.+?)(?:$|[.!?]\s*|\bcontact\b)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\bнужен\b|\bнужна\b|\bнужно\b|\bнужны\b|\bищем\b|\bинтересует\b|\bхотим\b)\s+(.+?)(?:$|[.!?]\s*|\bконтакт\b)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:\bnecesitamos\b|\bbuscamos\b|\bqueremos\b|\bnos interesa\b)\s+(.+?)(?:$|[.!?]\s*|\bcontacto\b)",
        re.IGNORECASE,
    ),
]

NOISE_PATTERNS = [
    re.compile(r"\b(?:contact|контакт|contacto)[:\s].*$", re.IGNORECASE),
    re.compile(
        r"\b(?:founder|cofounder|co-founder|ceo|cto|cpo|owner|director|основатель|сооснователь|фаундер|владелец|директор|fundador|cofundador|dueño|dueno|directora)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:we are|we're|мы из|somos de|soy de|company|компания|empresa)\b", re.IGNORECASE),
]

USE_CASE_HINTS = (
    "automation",
    "automate",
    "crm",
    "lead",
    "leads",
    "inbound",
    "sales",
    "telegram",
    "whatsapp",
    "integration",
    "integrations",
    "ai",
    "agent",
    "agents",
    "support",
    "analytics",
    "dashboard",
    "workflow",
    "qualification",
    "routing",
    "product",
    "growth",
    "автоматизация",
    "заявок",
    "лидов",
    "входящих",
    "телеграм",
    "интегра",
    "агент",
    "бот",
    "панель",
    "аналитика",
    "маршрутизация",
    "automatización",
    "entrantes",
    "integración",
    "agente",
    "ventas",
    "panel",
    "enrutamiento",
)

BAD_COMPANY_VALUES = {
    "we",
    "we are",
    "company",
    "компания",
    "empresa",
    "founder",
    "ceo",
    "owner",
    "director",
    "основатель",
    "фаундер",
    "fundador",
}


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _clean_str(value) -> Optional[str]:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _normalize_role(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    raw = _clean(value)
    lowered = raw.lower()

    exact_map = {
        "founder": "Founder",
        "cofounder": "Co-founder",
        "co-founder": "Co-founder",
        "ceo": "CEO",
        "cto": "CTO",
        "cpo": "CPO",
        "owner": "Owner",
        "director": "Director",
        "fundador": "Founder",
        "cofundador": "Co-founder",
        "основатель": "Founder",
        "сооснователь": "Co-founder",
    }

    if lowered in exact_map:
        return exact_map[lowered]

    if "product" in lowered and "growth" in lowered:
        return "Product & Growth Lead"
    if "product" in lowered:
        return "Product Lead"
    if "growth" in lowered:
        return "Growth Lead"
    if "sales" in lowered:
        return "Sales Lead"
    if "marketing" in lowered:
        return "Marketing Lead"

    return raw


def _cleanup_company(value: str) -> Optional[str]:
    value = _clean(value)
    value = value.strip(" \n\t\r,.;:!?-—")
    value = re.sub(r"\b(contact|контакт|contacto)\b.*$",
                   "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\b(i am from|i'm from|from company|мы из|из компании|somos de|soy de)\b.*$",
                   "", value, flags=re.IGNORECASE).strip()
    value = value.strip(" \n\t\r,.;:!?-—")

    if not value:
        return None
    if value.lower() in BAD_COMPANY_VALUES:
        return None
    if len(value) < 2 or len(value) > 64:
        return None

    return value


def _extract_company(text: str) -> Optional[str]:
    for pattern in COMPANY_PATTERNS:
        match = pattern.search(text)
        if match:
            company = _cleanup_company(match.group(1))
            if company:
                return company
    return None


def _extract_role(text: str) -> Optional[str]:
    match = ROLE_PATTERN.search(text)
    if not match:
        return None
    raw = match.group(1).lower()
    return ROLE_MAP.get(raw, raw)


def _extract_contact(text: str) -> Optional[str]:
    match = CONTACT_PATTERN.search(text)
    if match:
        return _clean(match.group(0))

    match = EMAIL_PATTERN.search(text)
    if match:
        return _clean(match.group(0))

    match = PHONE_PATTERN.search(text)
    if match:
        return _clean(match.group(0))

    return None


def _cleanup_use_case(value: str) -> Optional[str]:
    value = value.strip()

    value = re.sub(r"^[,.;:\s-]+", "", value)
    value = re.sub(r"\b(?:best way to reach me is|contact|контакт|contacto)\b.*$",
                   "", value, flags=re.IGNORECASE)

    value = re.sub(r"\bthem\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\bit\b", "", value, flags=re.IGNORECASE)

    for pattern in NOISE_PATTERNS:
        value = pattern.sub("", value)

    value = re.sub(r"\s+", " ", value).strip(" \n\t\r,.;:!?-—")
    return value or None


def _score_sentence(sentence: str) -> int:
    lowered = sentence.lower()
    return sum(1 for hint in USE_CASE_HINTS if hint in lowered)


def _extract_use_case(text: str) -> Optional[str]:
    for pattern in USE_CASE_PATTERNS:
        match = pattern.search(text)
        if match:
            value = _cleanup_use_case(match.group(1))
            if value:
                return value

    chunks = [_clean(chunk)
              for chunk in re.split(r"[\n.;]+", text) if _clean(chunk)]
    scored = [(chunk, _score_sentence(chunk)) for chunk in chunks]
    scored = [item for item in scored if item[1] > 0]

    if not scored:
        return None

    scored.sort(key=lambda item: item[1], reverse=True)
    return _cleanup_use_case(scored[0][0])


def _normalize_use_case(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    raw = _clean(value)
    lowered = raw.lower()

    # 1. Явные хорошие каноничные варианты
    canonical_map = {
        "inbound b2b lead automation": "Inbound B2B lead automation",
        "telegram and crm integration": "Telegram and CRM integration",
        "whatsapp and crm integration": "WhatsApp and CRM integration",
        "автоматизация входящих b2b-заявок": "Автоматизация входящих B2B-заявок",
        "automatización de leads entrantes": "Automatización de leads entrantes",
    }
    if lowered in canonical_map:
        return canonical_map[lowered]

    # 2. Главный pitch-ready сценарий для нашего демо
    has_telegram = "telegram" in lowered
    has_whatsapp = "whatsapp" in lowered
    has_crm = "crm" in lowered
    has_inbound = any(x in lowered for x in (
        "inbound", "entrantes", "входящих"))
    has_qualify = any(x in lowered for x in ("qualif", "квалиф", "calific"))
    has_cleanup = any(x in lowered for x in (
        "clean", "cleanup", "clean up", "очист", "limpiar"))
    has_push_or_route = any(x in lowered for x in (
        "push", "route", "routing", "маршрут", "enrut"))

    if has_telegram and has_whatsapp and has_crm and (has_qualify or has_cleanup or has_push_or_route or has_inbound):
        return "Inbound lead qualification and CRM routing from Telegram and WhatsApp"

    if has_telegram and has_crm and (has_qualify or has_inbound):
        return "Inbound lead qualification and CRM routing from Telegram"

    if has_whatsapp and has_crm and (has_qualify or has_inbound):
        return "Inbound lead qualification and CRM routing from WhatsApp"

    if has_inbound and has_crm and (has_qualify or has_push_or_route):
        return "Inbound lead qualification and CRM routing"

    # 3. Чистка кривых формулировок
    raw = re.sub(r"^(them|it|this|that)\s+", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s+", " ", raw).strip(" \n\t\r,.;:!?-—")

    if not raw:
        return None

    return raw[0].upper() + raw[1:] if len(raw) > 1 else raw.upper()


def _use_case_quality(value: Optional[str]) -> int:
    if not value:
        return -100

    lowered = value.lower()
    score = 0

    if lowered == "inbound lead qualification and crm routing from telegram and whatsapp":
        score += 100

    if "crm" in lowered:
        score += 15
    if "telegram" in lowered:
        score += 8
    if "whatsapp" in lowered:
        score += 8
    if "qualification" in lowered or "qualif" in lowered:
        score += 8
    if "routing" in lowered:
        score += 6

    if lowered.startswith(("them ", "it ", "this ", "that ")):
        score -= 20

    if len(value) > 90:
        score -= 5

    return score


def _pick_best_use_case(rule_value: Optional[str], llm_value: Optional[str]) -> Optional[str]:
    rule_norm = _normalize_use_case(rule_value)
    llm_norm = _normalize_use_case(llm_value)

    if not rule_norm:
        return llm_norm
    if not llm_norm:
        return rule_norm

    if _use_case_quality(llm_norm) > _use_case_quality(rule_norm):
        return llm_norm

    return rule_norm


def _build_result(
    company: Optional[str],
    role: Optional[str],
    contact: Optional[str],
    use_case: Optional[str],
    extraction_method: str,
    confidence: float,
) -> dict:
    company = _clean_str(company)
    role = _normalize_role(role)
    contact = _clean_str(contact)
    use_case = _normalize_use_case(use_case)

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
        "extraction_method": extraction_method,
        "confidence": round(max(0.0, min(confidence, 0.95)), 2),
        "missing_fields": missing_fields,
        "is_qualified_candidate": bool(company and use_case and (contact or role)),
    }


def _extract_rules_v2(text: str) -> dict:
    company = _extract_company(text)
    role = _extract_role(text)
    contact = _extract_contact(text)
    use_case = _extract_use_case(text)

    fields_found = sum(bool(x) for x in (company, role, contact, use_case))
    confidence = 0.35 + (fields_found * 0.15)

    if company and use_case:
        confidence += 0.10
    if contact:
        confidence += 0.05

    return _build_result(
        company=company,
        role=role,
        contact=contact,
        use_case=use_case,
        extraction_method="rules_v2",
        confidence=confidence,
    )


def _should_try_llm(rule_result: dict) -> bool:
    if not is_llm_available():
        return False

    if (
        rule_result.get("is_qualified_candidate")
        and rule_result.get("confidence", 0) >= 0.85
        and len(rule_result.get("missing_fields", [])) == 0
    ):
        return False

    return True


def _llm_improves(rule_result: dict, llm_result: Optional[dict]) -> bool:
    if not llm_result:
        return False

    rule_missing = sum(1 for key in ("company", "role",
                       "contact", "use_case") if not rule_result.get(key))
    llm_missing = sum(1 for key in ("company", "role",
                      "contact", "use_case") if not llm_result.get(key))

    if llm_missing < rule_missing:
        return True

    if not rule_result.get("is_qualified_candidate") and llm_result.get("is_qualified_candidate"):
        return True

    if llm_result.get("confidence", 0) > rule_result.get("confidence", 0) + 0.15:
        return True

    return False


def _merge_results(rule_result: dict, llm_result: dict) -> dict:
    company = rule_result.get("company") or llm_result.get("company")
    role = llm_result.get("role") or rule_result.get("role")
    contact = rule_result.get("contact") or llm_result.get("contact")
    use_case = _pick_best_use_case(rule_result.get(
        "use_case"), llm_result.get("use_case"))
    confidence = max(rule_result.get("confidence", 0.0),
                     llm_result.get("confidence", 0.0))

    return _build_result(
        company=company,
        role=role,
        contact=contact,
        use_case=use_case,
        extraction_method="rules_v2+llm_fallback",
        confidence=confidence,
    )


def extract_fields(message_text: str) -> dict:
    text = _clean(message_text)
    rule_result = _extract_rules_v2(text)

    if not _should_try_llm(rule_result):
        return rule_result

    llm_result = llm_extract_fields(text)

    if not _llm_improves(rule_result, llm_result):
        return rule_result

    return _merge_results(rule_result, llm_result)


def extract_company(message_text: str) -> Optional[str]:
    return extract_fields(message_text).get("company")


def extract_role(message_text: str) -> Optional[str]:
    return extract_fields(message_text).get("role")


def extract_contact(message_text: str) -> Optional[str]:
    return extract_fields(message_text).get("contact")


def extract_use_case(message_text: str) -> Optional[str]:
    return extract_fields(message_text).get("use_case")


def extract_lead_fields(message_text: str) -> dict:
    return extract_fields(message_text)


def extract_lead_data(message_text: str) -> dict:
    return extract_fields(message_text)


def extract_from_message(message_text: str) -> dict:
    return extract_fields(message_text)


def extract_message_fields(message_text: str) -> dict:
    return extract_fields(message_text)


def extract_structured_data(message_text: str) -> dict:
    return extract_fields(message_text)
