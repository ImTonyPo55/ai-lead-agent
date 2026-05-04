from __future__ import annotations

import re
from typing import Optional


def _clean(value: str) -> str:
    return " ".join(str(value).strip().split())


def _normalize(value: str) -> str:
    return _clean(value).casefold()


def _has_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def answer_from_knowledge_base(message_text: str) -> Optional[str]:
    """
    Demo-ready knowledge base for MechanicFlow AI.

    Returns short FAQ answers for common product questions.
    Can combine several answers when the user asks about multiple topics.
    Returns None when no FAQ topic is detected.
    """
    text = _normalize(message_text)

    if not text:
        return None

    answers: list[str] = []

    has_price = _has_any(
        text,
        ("price", "pricing", "cost", "how much", "стоимость", "цена", "сколько стоит", "precio", "costo"),
    )
    has_timeline = _has_any(
        text,
        ("timeline", "how long", "eta", "срок", "сроки", "как долго", "cuánto tiempo", "plazo"),
    )
    has_crm = _has_any(
        text,
        ("crm", "hubspot", "salesforce", "pipedrive", "amo", "битрикс", "bitrix"),
    )
    has_channels = _has_any(
        text,
        ("telegram", "whatsapp", "tg", "direct", "instagram", "инстаграм", "телеграм", "ватсап"),
    )
    has_demo = _has_any(
        text,
        ("demo", "show me", "presentation", "демо", "показать", "презентация"),
    )
    has_handoff = _has_any(
        text,
        ("handoff", "sales", "manager", "assign", "передача", "менеджер", "продажи", "назначить"),
    )
    has_security = _has_any(
        text,
        ("security", "data", "privacy", "безопасность", "данные", "конфиденциальность"),
    )

    if has_price:
        answers.append(
            "Стоимость зависит от сценария, количества входящих каналов и нужных интеграций. "
            "Для MVP обычно начинаем с короткого discovery: какие каналы подключаем, какие поля собираем "
            "и куда передаём квалифицированные лиды."
        )

    if has_crm:
        answers.append(
            "CRM можно подключить отдельным шагом: агент готовит company, role, contact, use case, статус квалификации "
            "и handoff-данные, а затем передаёт лид в CRM или sales-процесс."
        )

    if has_channels:
        answers.append(
            "Агент можно подключить к Telegram, WhatsApp, Instagram Direct, email или web-форме. "
            "Для MVP лучше начать с одного канала и потом расширять интеграции."
        )

    if has_timeline:
        answers.append(
            "Базовый MVP собирается поэтапно: сначала приём сообщений, извлечение данных, follow-up, квалификация "
            "и handoff. После этого добавляются CRM, Telegram, WhatsApp или email-интеграции."
        )

    if has_demo:
        answers.append(
            "В демо агент принимает свободное сообщение, извлекает ключевые поля, задаёт follow-up при нехватке данных "
            "и готовит квалифицированный лид к передаче в работу."
        )

    if has_handoff:
        answers.append(
            "Handoff срабатывает, когда у лида достаточно данных для передачи: компания, контакт и сценарий. "
            "После этого лид получает статус готового к передаче в работу."
        )

    if has_security:
        answers.append(
            "На MVP-этапе агент работает только с данными, которые пользователь сам отправляет в сообщении. "
            "Для production-версии можно добавить роли доступа, логирование и правила хранения данных."
        )

    if not answers and re.search(r"\b(can you help|можете помочь|pueden ayudar)\b", text):
        answers.append(
            "Да, могу помочь. Опишите, пожалуйста, какой входящий поток нужно автоматизировать, "
            "какие данные собирать и куда передавать квалифицированные лиды."
        )

    if not answers:
        return None

    return "\n\n".join(answers)
