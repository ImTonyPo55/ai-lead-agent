from __future__ import annotations

from typing import Any


CLIENT_TYPE_LABELS = {
    "ecommerce_brand": "eCommerce brand",
    "agency": "Agency",
    "retail_brand": "Retail brand",
    "mobile_app": "Mobile app",
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


def detect_client_type(text: str) -> str:
    if _has_any(text, ("enterprise", "global brand", "multiple markets", "multi-market", "multimarket")):
        return "enterprise_brand"
    if _has_any(text, ("agency", "client", "campaign for a client")):
        return "agency"
    if _has_any(text, ("mobile app", "in-app", "in app", "app retention")):
        return "mobile_app"
    if _has_any(text, ("retail", "retail brand", "stores", "loyalty", "promo codes")):
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
    if _has_any(text, ("christmas", "holiday", "advent", "seasonal")):
        return "holiday_promo"
    if _has_any(text, ("launch", "new product")):
        return "product_launch"
    if _has_any(text, ("repeat purchase", "repeat purchases", "repeat buyers")):
        return "repeat_purchase"
    if _has_any(text, ("returning customers", "retention", "churn")):
        return "retention"
    if _has_any(text, ("points", "rewards", "loyalty")):
        return "loyalty"
    if _has_any(text, ("collect emails", "email list", "signups", "sign ups", "leads", "lead capture")):
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
    if _has_any(text, ("mobile app", "in-app", "in app")):
        return "Mobile app"
    if _has_any(text, ("instagram", "direct")):
        return "Instagram"
    if "tiktok" in text or "tik tok" in text:
        return "TikTok"
    if _has_any(text, ("website", "web form", "landing page")):
        return "Website"
    return "unknown"


def recommend_mechanic(client_type: str, campaign_goal: str) -> str:
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
    if (
        client_type == "enterprise_brand"
        or campaign_goal == "loyalty"
        or _has_any(text, ("multi-market", "multiple markets", "complex integration", "complex integrations"))
    ):
        return "Enterprise Tier"
    if client_type == "agency" or _has_any(text, ("branded client campaign", "campaign for a client")):
        return "Done-With-You Tier"
    if platform == "Shopify" and (campaign_goal == "lead_capture" or mechanic == "Spin-to-Win"):
        return "DIY Tier"
    if campaign_goal == "unknown" and client_type == "unknown":
        return "Discovery Tier"
    return "Discovery Tier"


def recommend_next_action(
    company: str,
    contact: str,
    use_case: str,
    client_type: str,
    campaign_goal: str,
    platform: str,
) -> str:
    if client_type == "enterprise_brand":
        return "Route to strategy call"
    if not contact:
        return "Ask for contact handle or email"
    if campaign_goal == "unknown" or not use_case:
        return "Ask for primary campaign goal"
    if platform == "unknown":
        return "Ask which platform or ecommerce stack they use"
    if company and contact and use_case:
        return "Prepare CRM handoff and confirm campaign objective"
    return "Ask for primary campaign goal"


def build_campaign_summary(company: str, campaign_goal: str, mechanic: str, platform: str) -> str:
    company_display = company or "This campaign lead"
    goal_display = CAMPAIGN_GOAL_LABELS.get(campaign_goal, campaign_goal)
    platform_part = "" if platform == "unknown" else f" on {platform}"
    return f"{company_display} needs a gamified marketing campaign for {goal_display}{platform_part}. Recommended mechanic: {mechanic}."


def build_copy_ready_followup(
    campaign_goal: str,
    mechanic: str,
    platform: str,
    next_action: str,
) -> str:
    goal_display = CAMPAIGN_GOAL_LABELS.get(campaign_goal, "your campaign goal")
    platform_part = "confirm your platform and target offer" if platform == "unknown" else f"confirm the target offer for {platform}"
    return (
        f"Thanks — based on your goal, I’d recommend a {mechanic} campaign for {goal_display}. "
        f"Next step: {platform_part} so we can prepare the campaign package. {next_action}."
    )


def build_campaign_intelligence(lead: Any, latest_message: Any = None) -> dict:
    text = _context_text(lead, latest_message)
    company = _clean(getattr(lead, "company", None))
    contact = _clean(getattr(lead, "contact", None))
    use_case = _clean(getattr(lead, "use_case", None))
    client_type = detect_client_type(text)
    campaign_goal = detect_campaign_goal(text)
    platform = detect_platform(text)
    mechanic = recommend_mechanic(client_type, campaign_goal)
    mechanic_reason = MECHANIC_REASONS[mechanic]
    pricing_tier = recommend_pricing_tier(client_type, campaign_goal, platform, mechanic, text)
    next_action = recommend_next_action(
        company=company,
        contact=contact,
        use_case=use_case,
        client_type=client_type,
        campaign_goal=campaign_goal,
        platform=platform,
    )

    return {
        "client_type": client_type,
        "client_type_label": CLIENT_TYPE_LABELS[client_type],
        "campaign_goal": campaign_goal,
        "campaign_goal_label": CAMPAIGN_GOAL_LABELS[campaign_goal],
        "platform": platform,
        "recommended_mechanic": mechanic,
        "mechanic_reason": mechanic_reason,
        "pricing_tier": pricing_tier,
        "recommended_next_action": next_action,
        "campaign_summary": build_campaign_summary(company, campaign_goal, mechanic, platform),
        "copy_text": build_copy_ready_followup(campaign_goal, mechanic, platform, next_action),
    }
