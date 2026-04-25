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
}

ROLE_PATTERN = re.compile(
    r"\b(co-founder|cofounder|founder|ceo|cto|cpo|owner|director|основатель|сооснователь|фаундер|владелец|директор)\b",
    re.IGNORECASE,
)

CONTACT_PATTERN = re.compile(r"@[A-Za-z0-9_\.]+")
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

COMPANY_PATTERNS = [
    re.compile(
        r"(?:мы\s+из\s+компании|мы\s+из|компания)\s+([A-ZА-Я][A-Za-zА-Яа-я0-9&\.\-\+\s]{1,60}?)(?=(?:[\.\,\!\?\;\:]|\s+я\b|\s+i\b|\s+контакт\b|\s+мой\s+контакт\b|\s+my\s+contact\b|$))",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:from\s+company|from)\s+([A-Z][A-Za-z0-9&\.\-\+\s]{1,60}?)(?=(?:[\.\,\!\?\;\:]|\s+i\b|\s+contact\b|\s+my\s+contact\b|$))",
        re.IGNORECASE,
    ),
]

USE_CASE_PATTERNS = [
    re.compile(r"(?:нужна|нужно|нужен)\s+([^\.!\?\n]+)", re.IGNORECASE),
    re.compile(r"(?:хотим|хочу)\s+([^\.!\?\n]+)", re.IGNORECASE),
    re.compile(r"(?:ищем)\s+([^\.!\?\n]+)", re.IGNORECASE),
    re.compile(r"(?:интересует)\s+([^\.!\?\n]+)", re.IGNORECASE),
    re.compile(
        r"(?:we\s+need|need|want\s+to|looking\s+for)\s+([^\.!\?\n]+)", re.IGNORECASE),
]

NOISE_PATTERNS = [
    re.compile(r"(?:мой|наш|my)\s+контакт.*$", re.IGNORECASE),
    re.compile(r"(?:контакт|contact)\s+@[A-Za-z0-9_\.]+.*$", re.IGNORECASE),
    re.compile(
        r"(?:контакт|contact)\s+[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}.*$", re.IGNORECASE),
]


def _clean(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = re.sub(r"\s+", " ", value).strip(" \n\t\r.,;:!?-")
    return value or None


def _extract_company(text: str) -> Optional[str]:
    for pattern in COMPANY_PATTERNS:
        match = pattern.search(text)
        if match:
            return _clean(match.group(1))
    return None


def _extract_role(text: str) -> Optional[str]:
    match = ROLE_PATTERN.search(text)
    if not match:
        return None

    raw = match.group(1).lower().strip()
    return ROLE_MAP.get(raw, raw)


def _extract_contact(text: str) -> Optional[str]:
    match = CONTACT_PATTERN.search(text)
    if match:
        return _clean(match.group(0))

    match = EMAIL_PATTERN.search(text)
    if match:
        return _clean(match.group(0))

    return None


def _cleanup_use_case(value: str) -> Optional[str]:
    value = value.strip()

    for pattern in NOISE_PATTERNS:
        value = pattern.sub("", value)

    value = re.sub(r"\s+", " ", value).strip(" \n\t\r.,;:!?-")
    return value or None


def _extract_use_case(text: str) -> Optional[str]:
    for pattern in USE_CASE_PATTERNS:
        match = pattern.search(text)
        if match:
            cleaned = _cleanup_use_case(match.group(1))
            if cleaned:
                return cleaned

    return None


def extract_fields(message_text: str) -> dict:
    text = message_text.strip()

    company = _extract_company(text)
    role = _extract_role(text)
    contact = _extract_contact(text)
    use_case = _extract_use_case(text)

    return {
        "company": company,
        "role": role,
        "contact": contact,
        "use_case": use_case,
    }


# aliases so existing imports do not break
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
