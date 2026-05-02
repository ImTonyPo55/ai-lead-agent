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
    Simple demo-ready knowledge base for AI Lead Agent.

    Returns a short assistant answer when the user asks a common product/FAQ question.
    Returns None when the message should go through normal lead qualification.
    """
    text = _normalize(message_text)

    if not text:
        return None

    if _has_any(text, ("price", "pricing", "cost", "how much", "стоимость", "цена", "сколько стоит", "precio", "costo")):
        return (
            "Стоимость зависит от сценария, количества каналов и нужных интеграций. "
            "Для MVP обычно начинаем с короткого discovery: какие входящие каналы, какие поля нужно собирать "
            "и куда передавать лиды."
        )

    if _has_any(text, ("timeline", "how long", "eta", "срок", "сроки", "как долго", "cuánto tiempo", "plazo")):
        return (
            "Базовый MVP можно собрать быстро: сначала входящие сообщения, извлечение данных, follow-up, "
            "квалификация и handoff. После этого добавляются интеграции с CRM, Telegram, WhatsApp или email."
        )

    if _has_any(text, ("crm", "hubspot", "salesforce", "pipedrive", "amo", "битрикс", "bitrix")):
        return (
            "Да, агент может готовить лид к передаче в CRM: извлекать компанию, роль, контакт, сценарий, "
            "статус квалификации и причину handoff. Интеграция подключается отдельным шагом после MVP."
        )

    if _has_any(text, ("telegram", "whatsapp", "tg", "direct", "instagram", "инстаграм", "телеграм", "ватсап")):
        return (
            "Да, агент можно подключить к Telegram, WhatsApp, Instagram Direct или web-форме. "
            "В MVP лучше начать с одного канала, доказать качество квалификации и потом расширять интеграции."
        )

    if _has_any(text, ("demo", "show me", "presentation", "демо", "показать", "презентация")):
        return (
            "Да, можно показать демо. В демо агент принимает свободное сообщение, извлекает ключевые поля, "
            "задаёт follow-up при нехватке данных и готовит квалифицированный лид к передаче в работу."
        )

    if _has_any(text, ("handoff", "sales", "manager", "assign", "передача", "менеджер", "продажи", "назначить")):
        return (
            "Handoff срабатывает, когда у лида достаточно данных для передачи: компания, контакт и сценарий. "
            "После этого лид получает статус готового к передаче в работу."
        )

    if _has_any(text, ("security", "data", "privacy", "безопасность", "данные", "конфиденциальность")):
        return (
            "На MVP-этапе агент работает только с данными, которые пользователь сам отправляет в сообщении. "
            "Для production-версии можно добавить ограничения доступа, логирование, хранение истории и правила обработки данных."
        )

    if re.search(r"\b(can you help|можете помочь|pueden ayudar)\b", text):
        return (
            "Да, могу помочь. Опишите, пожалуйста, какой входящий поток нужно автоматизировать, "
            "какие данные собирать и куда передавать квалифицированные лиды."
        )

    return None
