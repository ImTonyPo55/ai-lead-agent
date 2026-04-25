def detect_intent(message: str) -> str:
    text = message.lower()

    pricing_keywords = ["цена", "стоимость",
                        "сколько стоит", "тариф", "pricing", "price"]
    demo_keywords = ["демо", "demo", "показать", "презентация"]
    consultation_keywords = ["консультация",
                             "созвон", "звонок", "call", "meeting"]
    integration_keywords = ["интеграция", "api", "webhook", "sdk"]
    partnership_keywords = ["партнерство", "партнёрство",
                            "сотрудничество", "partner", "partnership"]
    support_keywords = ["ошибка", "не работает",
                        "support", "помощь", "проблема"]

    if any(word in text for word in pricing_keywords):
        return "pricing"
    if any(word in text for word in demo_keywords):
        return "demo_request"
    if any(word in text for word in consultation_keywords):
        return "consultation_request"
    if any(word in text for word in integration_keywords):
        return "integration_question"
    if any(word in text for word in partnership_keywords):
        return "partnership"
    if any(word in text for word in support_keywords):
        return "support"

    return "other"
