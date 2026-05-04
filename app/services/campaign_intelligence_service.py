from __future__ import annotations

import re
from typing import Any


CLIENT_TYPE_LABELS = {
    "ecommerce_brand": "eCommerce brand",
    "agency": "Agency",
    "retail_brand": "Retail brand",
    "mobile_app": "Mobile app",
    "product_brand": "Product brand",
    "gaming_studio": "Gaming studio",
    "enterprise_brand": "Enterprise brand",
    "unknown": "Unknown",
}

CAMPAIGN_GOAL_LABELS = {
    "lead_capture": "lead capture",
    "retention": "retention",
    "repeat_purchase": "repeat purchase",
    "holiday_promo": "holiday promotion",
    "loyalty": "loyalty",
    "product_launch": "product launch",
    "engagement": "engagement",
    "unknown": "campaign discovery",
}

MECHANIC_REASONS = {
    "Advent Calendar": (
        "A seasonal calendar creates repeated visits, daily incentives and a clear structure for holiday offers."
    ),
    "Spin-to-Win": (
        "Spin-to-Win is a fast, simple mechanic for email capture, offer reveal and first-purchase activation."
    ),
    "Wheel of Fortune": (
        "A wheel mechanic gives returning shoppers a clear reward loop and can motivate repeat purchases."
    ),
    "Rewards Campaign": (
        "Rewards campaigns support retention by giving customers a visible reason to come back and redeem benefits."
    ),
    "Quiz / Lead Magnet": (
        "A quiz captures intent data while giving the launch a useful recommendation or lead magnet flow."
    ),
    "Memory Match": (
        "Memory Match creates a lightweight engagement loop that keeps the campaign interactive and brand-led."
    ),
    "Campaign Discovery Package": (
        "Discovery is the safest next step when the campaign goal, platform or offer is not specific enough yet."
    ),
}

EXPLICIT_MECHANICS = (
    ("Spin-to-Win", ("spin-to-win", "spin to win", "spin wheel", "wheel popup")),
    ("Advent Calendar", ("advent", "advent calendar", "christmas", "holiday", "seasonal promo")),
    ("Memory Match", ("memory match", "matching game", "pairs game")),
    ("Wheel of Fortune", ("wheel of fortune", "fortune wheel")),
    ("Quiz / Lead Magnet", ("lead magnet quiz", "product quiz", "quiz")),
    ("Rewards Campaign", ("rewards", "loyalty", "points", "retention", "returning customers")),
)

CAMPAIGN_SIGNALS = (
    "campaign",
    "promo game",
    "game",
    "playable",
    "gamified",
    "gamification",
    "lead capture",
    "retention",
    "loyalty",
    "holiday",
    "advent",
    "spin",
    "quiz",
    "rewards",
)

TECHNICAL_SIGNALS = (
    "crm",
    "cdp",
    "api",
    "integration",
    "integrations",
    "analytics",
    "gdpr",
    "consent",
    "webhook",
)

COMPLEX_ROLLOUT_SIGNALS = (
    "enterprise",
    "global brand",
    "multiple markets",
    "multi-market",
    "multimarket",
    "multi-country",
    "global rollout",
    "complex rollout",
)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _context_text(lead: Any, latest_message: Any = None) -> str:
    parts = [
        getattr(lead, "company", None),
        getattr(lead, "role", None),
        getattr(lead, "contact", None),
        getattr(lead, "use_case", None),
        getattr(lead, "notes", None),
        getattr(latest_message, "text", None),
    ]
    return " ".join(_clean(part) for part in parts if _clean(part)).casefold()


def _has_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def _has_complex_rollout(text: str) -> bool:
    return _has_any(text, COMPLEX_ROLLOUT_SIGNALS) or bool(
        re.search(r"\b\d+\s+(countries|markets)\b", text)
    )


def _has_technical_integration(text: str) -> bool:
    return _has_any(text, TECHNICAL_SIGNALS)


def _has_campaign_signal(text: str) -> bool:
    return _has_any(text, CAMPAIGN_SIGNALS)


def detect_explicit_mechanic(text: str) -> str | None:
    for mechanic, keywords in EXPLICIT_MECHANICS:
        if _has_any(text, keywords):
            return mechanic
    return None


def detect_client_type(text: str) -> str:
    if _has_complex_rollout(text):
        return "enterprise_brand"
    if _has_any(text, ("agency", "client", "campaign for a client", "for a retail client")):
        return "agency"
    if _has_any(text, ("mobile app", "ios", "android", "in-app", "in app", "sdk", "app retention")):
        return "mobile_app"
    if _has_any(text, ("gaming studio", "game studio", "studio")):
        return "gaming_studio"
    if _has_any(text, ("product launch", "new product", "product quiz", "lead magnet")):
        return "product_brand"
    if _has_any(text, ("shopify", "shopify store", "ecommerce", "e-commerce", "cart", "online store")):
        return "ecommerce_brand"
    if _has_any(text, ("retail", "retail brand", "stores", "loyalty", "promo codes", "retail client")):
        return "retail_brand"
    if _has_any(
        text,
        (
            "shopify",
            "store",
            "ecommerce",
            "e-commerce",
            "cart",
            "email list",
            "repeat purchases",
            "returning customers",
            "repeat buyers",
        ),
    ):
        return "ecommerce_brand"
    return "unknown"


def detect_campaign_goal(text: str) -> str:
    if _has_any(text, ("christmas", "holiday", "advent", "advent calendar", "seasonal", "seasonal promo")):
        return "holiday_promo"
    if _has_any(text, ("launch", "new product")):
        return "product_launch"
    if _has_any(text, ("repeat purchase", "repeat purchases", "repeat buyers")):
        return "repeat_purchase"
    if _has_any(text, ("returning customers", "retention", "churn")):
        return "retention"
    if _has_any(text, ("rewards", "loyalty", "points")):
        return "loyalty"
    if _has_any(
        text,
        ("lead capture", "collect emails", "email list", "signups", "sign ups", "subscribers", "popup", "leads"),
    ):
        return "lead_capture"
    if _has_any(text, ("engagement", "activation")):
        return "engagement"
    return "unknown"


def detect_platform(text: str) -> str:
    if "shopify" in text:
        return "Shopify"
    if "woocommerce" in text or "woo commerce" in text:
        return "WooCommerce"
    if "magento" in text or "adobe commerce" in text:
        return "Magento"
    if "bigcommerce" in text:
        return "BigCommerce"
    if "klaviyo" in text:
        return "Klaviyo"
    if _has_any(text, ("mobile app", "ios", "android", "in-app", "in app", "sdk")):
        return "Mobile app"
    if _has_any(text, ("instagram", "direct")):
        return "Instagram"
    if "tiktok" in text or "tik tok" in text:
        return "TikTok"
    if _has_any(text, ("website", "web form", "landing page")):
        return "Website"
    if _has_any(text, ("ecommerce", "e-commerce", "online store", "storefront")):
        return "eCommerce"
    return "unknown"


def recommend_mechanic(client_type: str, campaign_goal: str, text: str = "") -> str:
    explicit_mechanic = detect_explicit_mechanic(text)
    if explicit_mechanic:
        return explicit_mechanic

    if campaign_goal == "holiday_promo":
        return "Advent Calendar"
    if campaign_goal == "lead_capture":
        return "Spin-to-Win"
    if campaign_goal == "repeat_purchase":
        return "Wheel of Fortune"
    if campaign_goal in {"retention", "loyalty"}:
        return "Rewards Campaign"
    if campaign_goal == "product_launch":
        return "Quiz / Lead Magnet"
    if campaign_goal == "engagement":
        return "Memory Match"
    if client_type == "agency":
        return "Campaign Discovery Package"
    return "Campaign Discovery Package"


def recommend_pricing_tier(
    client_type: str,
    campaign_goal: str,
    platform: str,
    mechanic: str,
    text: str,
) -> str:
    explicit_mechanic = detect_explicit_mechanic(text)
    is_vague = campaign_goal == "unknown" and not explicit_mechanic

    if is_vague:
        return "Discovery Tier"
    if (
        client_type == "enterprise_brand"
        or _has_complex_rollout(text)
        or _has_any(
            text,
            (
                "crm integration",
                "cdp",
                "api integration",
                "integration",
                "loyalty platform",
                "loyalty program",
                "multi-country",
                "large-scale rollout",
                "large scale rollout",
                "global rollout",
                "advanced analytics",
                "custom backend",
                "millions of users",
                "complex integration",
                "complex integrations",
                "complex stack",
                "sso",
                "security",
                "procurement",
                "sap",
                "salesforce",
                "hubspot",
                "gdpr",
                "consent",
                "analytics",
            ),
        )
    ):
        return "Enterprise Tier"
    if campaign_goal in {"retention", "loyalty"} or _has_any(
        text,
        ("rewards", "returning customers", "retention campaign"),
    ):
        return "Done-With-You Tier"
    if client_type == "agency" or _has_any(
        text,
        (
            "branded client campaign",
            "campaign for a client",
            "customization",
            "customisation",
            "custom design",
            "design support",
            "integration support",
            "brand campaign",
        ),
    ):
        return "Done-With-You Tier"
    if campaign_goal == "product_launch" and mechanic == "Quiz / Lead Magnet":
        return "Done-With-You Tier"
    if (
        client_type == "ecommerce_brand"
        and platform in {"Shopify", "eCommerce"}
        and mechanic in {"Spin-to-Win", "Wheel of Fortune", "Memory Match"}
        and campaign_goal in {"lead_capture", "repeat_purchase", "engagement"}
    ):
        return "DIY Tier"
    if platform == "Shopify" and campaign_goal == "lead_capture" and mechanic == "Spin-to-Win":
        return "DIY Tier"
    return "Discovery Tier"


def recommend_next_action(
    company: str,
    contact: str,
    use_case: str,
    client_type: str,
    campaign_goal: str,
    platform: str,
    mechanic: str = "",
    pricing_tier: str = "",
    text: str = "",
) -> str:
    explicit_mechanic = bool(detect_explicit_mechanic(text))
    is_vague = campaign_goal == "unknown" and not explicit_mechanic

    if not company:
        return "Ask for company name"
    if not contact:
        return "Ask for decision-maker contact"
    if is_vague:
        return "Ask for primary campaign goal and target audience"
    if pricing_tier == "Enterprise Tier" or client_type == "enterprise_brand":
        return "Book discovery call and confirm CRM/CDP integration requirements"
    if client_type == "agency":
        return "Confirm client brand, timeline, and preferred mechanic"
    if campaign_goal == "unknown" or not use_case:
        return "Ask for primary campaign goal"
    if company and contact and use_case and mechanic and pricing_tier:
        return "Prepare CRM handoff and confirm campaign objective"
    return "Ask for primary campaign goal"


def _qualification_score(
    company: str,
    contact: str,
    client_type: str,
    campaign_goal: str,
    platform: str,
    mechanic: str,
    pricing_tier: str,
    explicit_mechanic: bool,
    vague_campaign: bool,
) -> int:
    if not company or not contact:
        return 35 if company or contact else 20

    if vague_campaign or pricing_tier == "Discovery Tier":
        return 55 if _has_campaign_signal(mechanic.casefold()) else 50

    if explicit_mechanic and campaign_goal != "unknown" and client_type != "unknown":
        score = 90
        if platform != "unknown":
            score += 7
        if pricing_tier != "Discovery Tier":
            score += 3
        return min(score, 100)

    if campaign_goal != "unknown" and mechanic != "Campaign Discovery Package":
        score = 72
        if client_type != "unknown":
            score += 8
        if platform != "unknown":
            score += 5
        return min(score, 89)

    return 45


def _priority(score: int) -> str:
    if score >= 90:
        return "High"
    if score >= 70:
        return "Medium"
    return "Low"


def _missing_fields(
    company: str,
    contact: str,
    use_case: str,
    client_type: str,
    campaign_goal: str,
    pricing_tier: str,
    explicit_mechanic: bool,
    vague_campaign: bool,
) -> list[str]:
    missing: list[str] = []

    if not company:
        missing.append("company")
    if not contact:
        missing.append("contact")
    if not use_case and campaign_goal == "unknown" and not explicit_mechanic:
        missing.append("campaign_need")
    if client_type == "unknown":
        missing.append("client_type")
    if vague_campaign:
        missing.append("campaign_goal")
    if not pricing_tier:
        missing.append("pricing_tier")

    return missing


def can_create_campaign_handoff(intelligence: dict) -> bool:
    return bool(
        intelligence.get("company")
        and intelligence.get("contact")
        and intelligence.get("client_type") != "unknown"
        and (
            intelligence.get("campaign_goal") != "unknown"
            or intelligence.get("explicit_mechanic")
        )
        and intelligence.get("pricing_tier")
        and intelligence.get("pricing_tier") != "Discovery Tier"
    )


def lead_status_from_campaign_intelligence(
    intelligence: dict,
    latest_handoff: Any = None,
) -> str:
    handoff_status = _clean(getattr(latest_handoff, "status", None))
    if handoff_status in {"in_progress", "active_handoff"}:
        return "active_handoff"
    if handoff_status in {"done", "completed", "completed_handoff"}:
        return "completed_handoff"
    if latest_handoff is not None:
        return "ready_to_handoff"
    if can_create_campaign_handoff(intelligence):
        return "ready_to_handoff"
    if intelligence.get("missing_fields"):
        return "needs_followup"
    return "new"


def build_next_question(intelligence: dict) -> str:
    missing = intelligence.get("missing_fields") or []
    if "contact" in missing:
        return "Who is the best decision-maker contact for this campaign?"
    if "company" in missing:
        return "Which company or brand is this campaign for?"
    if "campaign_goal" in missing or "campaign_need" in missing:
        return (
            "Can you confirm the main campaign goal: lead capture, retention, "
            "product launch, holiday promo, or loyalty?"
        )
    if "client_type" in missing:
        return "Is this for an eCommerce brand, retail brand, agency client, mobile app, or enterprise brand?"
    return "What is the most important campaign detail we should confirm before handoff?"


def build_campaign_summary(company: str, campaign_goal: str, mechanic: str, platform: str) -> str:
    company_display = company or "This campaign lead"
    goal_display = CAMPAIGN_GOAL_LABELS.get(campaign_goal, campaign_goal)
    platform_part = "" if platform == "unknown" else f" on {platform}"
    return f"{company_display} needs a gamified marketing campaign for {goal_display}{platform_part}. Best game for this campaign: {mechanic}."


def build_copy_ready_followup(
    campaign_goal: str,
    mechanic: str,
    platform: str,
    next_action: str,
    pricing_tier: str = "",
    is_vague: bool = False,
) -> str:
    if is_vague or pricing_tier == "Discovery Tier":
        return (
            "Thanks — to recommend the right game mechanic, can you confirm the main campaign goal: "
            "lead capture, retention, product launch, holiday promo, or loyalty?"
        )

    goal_display = CAMPAIGN_GOAL_LABELS.get(campaign_goal, "your campaign goal")
    goal_part = goal_display if platform == "unknown" else f"{platform} {goal_display}"
    platform_part = "confirm your platform and target offer" if platform == "unknown" else "confirm the target offer"
    return (
        f"Thanks — based on your {goal_part} goal, I’d recommend a {mechanic} campaign. "
        f"Next step: {platform_part} so we can prepare the campaign package."
    )


def build_campaign_intelligence(lead: Any, latest_message: Any = None) -> dict:
    text = _context_text(lead, latest_message)
    company = _clean(getattr(lead, "company", None))
    contact = _clean(getattr(lead, "contact", None))
    use_case = _clean(getattr(lead, "use_case", None))
    client_type = detect_client_type(text)
    campaign_goal = detect_campaign_goal(text)
    platform = detect_platform(text)
    explicit_mechanic_value = detect_explicit_mechanic(text)
    explicit_mechanic = bool(explicit_mechanic_value)
    mechanic = recommend_mechanic(client_type, campaign_goal, text)
    mechanic_reason = MECHANIC_REASONS[mechanic]
    pricing_tier = recommend_pricing_tier(client_type, campaign_goal, platform, mechanic, text)
    vague_campaign = _has_campaign_signal(text) and campaign_goal == "unknown" and not explicit_mechanic
    missing_fields = _missing_fields(
        company=company,
        contact=contact,
        use_case=use_case,
        client_type=client_type,
        campaign_goal=campaign_goal,
        pricing_tier=pricing_tier,
        explicit_mechanic=explicit_mechanic,
        vague_campaign=vague_campaign,
    )
    qualification_score = _qualification_score(
        company=company,
        contact=contact,
        client_type=client_type,
        campaign_goal=campaign_goal,
        platform=platform,
        mechanic=mechanic,
        pricing_tier=pricing_tier,
        explicit_mechanic=explicit_mechanic,
        vague_campaign=vague_campaign,
    )
    next_action = recommend_next_action(
        company=company,
        contact=contact,
        use_case=use_case,
        client_type=client_type,
        campaign_goal=campaign_goal,
        platform=platform,
        mechanic=mechanic,
        pricing_tier=pricing_tier,
        text=text,
    )
    result = {
        "company": company,
        "contact": contact,
        "campaign_need": use_case,
        "use_case": use_case,
        "explicit_mechanic": explicit_mechanic,
        "explicit_mechanic_value": explicit_mechanic_value,
        "client_type": client_type,
        "client_type_label": CLIENT_TYPE_LABELS[client_type],
        "campaign_goal": campaign_goal,
        "campaign_goal_label": CAMPAIGN_GOAL_LABELS[campaign_goal],
        "platform": platform,
        "recommended_mechanic": mechanic,
        "best_game": mechanic,
        "mechanic_reason": mechanic_reason,
        "pricing_tier": pricing_tier,
        "recommended_package": pricing_tier,
        "recommended_next_action": next_action,
        "qualification_score": qualification_score,
        "score": qualification_score,
        "priority": _priority(qualification_score),
        "missing_fields": missing_fields,
        "vague_campaign": vague_campaign,
        "discovery_reason": (
            "Campaign goal and target audience need confirmation before package recommendation."
            if vague_campaign
            else ""
        ),
        "campaign_summary": build_campaign_summary(company, campaign_goal, mechanic, platform),
    }
    result["can_create_handoff"] = can_create_campaign_handoff(result)
    result["qualification_status"] = lead_status_from_campaign_intelligence(result)
    result["lead_status"] = result["qualification_status"]
    result["next_question"] = build_next_question(result) if missing_fields else ""
    if missing_fields and not vague_campaign:
        result["copy_text"] = f"Thanks — {result['next_question']}"
    else:
        result["copy_text"] = build_copy_ready_followup(
            campaign_goal,
            mechanic,
            platform,
            next_action,
            pricing_tier=pricing_tier,
            is_vague=vague_campaign,
        )

    return result
