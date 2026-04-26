import re
from typing import Optional


ROLE_MAP = {
    "founder": "founder",
    "cofounder": "cofounder",
    "co-founder": "cofounder",
    "ceo": "CEO",
    "cto": "CTO",
    "cpo": "CPO",
    "owner": "owner",
    "director": "director",
    "основатель": "founder",
    "сооснователь": "cofounder",
    "фаундер": "founder",
    "владелец": "owner",
    "директор": "director",
    "fundador": "founder",
    "cofundador": "cofounder",
    "dueño": "owner",
    "dueno": "owner",
    "director general": "director",
    "directora": "director",
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
        r"^\s*([A-ZА-ЯЁ][A-Za-zА-Яа-яЁё0-9&.\- ]{1,60}?)(?:,\s*(?:i am|i'm|я|soy|somos|need|нуж|buscamos|necesitamos)|[,.]\s|$)",
        re.IGNORECASE,
    ),
]

USE_CASE_PATTERNS = [
    re.compile(
        r"(?:\bneed\b|\blooking for\b|\bneed help with\b|\binterested in\b|\bwant\b)\s+(.+?)(?:$|[.!?]\s*|\bcontact\b)", re.IGNORECASE),
    re.compile(
        r"(?:\bнужен\b|\bнужна\b|\bнужно\b|\bнужны\b|\bищем\b|\bинтересует\b|\bхотим\b)\s+(.+?)(?:$|[.!?]\s*|\bконтакт\b)", re.IGNORECASE),
    re.compile(
        r"(?:\bnecesitamos\b|\bbuscamos\b|\bqueremos\b|\bnos interesa\b)\s+(.+?)(?:$|[.!?]\s*|\bcontacto\b)", re.IGNORECASE),
]

NOISE_PATTERNS = [
    re.compile(r"\b(?:contact|контакт|contacto)[:\s].*$", re.IGNORECASE),
    re.compile(r"\b(?:i am|i'm|я|soy|somos)\b.*$", re.IGNORECASE),
    re.compile(r"\b(?:founder|cofounder|co-founder|ceo|cto|cpo|owner|director|основатель|сооснователь|фаундер|владелец|директор|fundador|cofundador|dueño|dueno|directora)\b", re.IGNORECASE),
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
    "автоматизация",
    "заявок",
    "лидов",
    "входящих",
    "crm",
    "телеграм",
    "whatsapp",
    "интегра",
    "агент",
    "бот",
    "панель",
    "аналитика",
    "automatización",
    "leads",
    "entrantes",
    "integración",
    "agente",
    "bot",
    "ventas",
    "panel",
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


def _cleanup_company(value: str) -> Optional[str]:
    value = _clean(value)
    value = value.strip(" \n\t\r,.;:!?-—")
    value = re.sub(r"\b(contact|контакт|contacto)\b.*$",
                   "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\b(i am|i'm|я|soy|somos)\b.*$", "",
                   value, flags=re.IGNORECASE).strip()
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

    chunks = [
        _clean(chunk)
        for chunk in re.split(r"[\n.;]+", text)
        if _clean(chunk)
    ]

    scored = [(chunk, _score_sentence(chunk)) for chunk in chunks]
    scored = [item for item in scored if item[1] > 0]

    if not scored:
        return None

    scored.sort(key=lambda item: item[1], reverse=True)
    return _cleanup_use_case(scored[0][0])


def extract_fields(message_text: str) -> dict:
    text = _clean(message_text)

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

    confidence = round(min(confidence, 0.95), 2)

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
        "extraction_method": "rules_v2",
        "confidence": confidence,
        "missing_fields": missing_fields,
        "is_qualified_candidate": bool(company and use_case and (contact or role)),
    }


def extract_company(message_text: str) -> Optional[str]:
    return _extract_company(message_text.strip())


def extract_role(message_text: str) -> Optional[str]:
    return _extract_role(message_text.strip())


def extract_contact(message_text: str) -> Optional[str]:
    return _extract_contact(message_text.strip())


def extract_use_case(message_text: str) -> Optional[str]:
    return _extract_use_case(message_text.strip())


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
