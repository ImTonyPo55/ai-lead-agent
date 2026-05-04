from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from app.services.campaign_intelligence_service import build_campaign_intelligence
from app.services.extract_service import extract_company, extract_contact, extract_use_case
from app.services.handoff_package_service import build_handoff_package
from app.services.owner_routing_service import recommend_owner


@dataclass(frozen=True)
class Case:
    name: str
    message: str
    expected: dict[str, Any]


CASES = [
    Case(
        name="UrbanFit",
        message="We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo",
        expected={
            "company": "UrbanFit",
            "contact": "@urbanfit_cmo",
            "client_type": "ecommerce_brand",
            "campaign_goal": "lead_capture",
            "platform": "Shopify",
            "recommended_mechanic": "Spin-to-Win",
            "pricing_tier": "DIY Tier",
            "qualification_status": "ready_to_handoff",
            "missing_fields": [],
            "can_create_handoff": True,
            "owner": "Tony",
            "team": "Sales",
            "has_crm_payload": True,
        },
    ),
    Case(
        name="NoContactFit",
        message="We are NoContactFit. Need a spin-to-win campaign for Shopify lead capture.",
        expected={
            "company": "NoContactFit",
            "contact": "",
            "client_type": "ecommerce_brand",
            "campaign_goal": "lead_capture",
            "platform": "Shopify",
            "recommended_mechanic": "Spin-to-Win",
            "pricing_tier": "DIY Tier",
            "qualification_status": "needs_followup",
            "missing_fields": ["contact"],
            "can_create_handoff": False,
            "owner": "Unassigned",
            "team": "Intake",
            "has_crm_payload": False,
        },
    ),
    Case(
        name="Nova Agency",
        message="We are Nova Agency. Need a branded Advent Calendar campaign for a client. Contact @nova_agency",
        expected={
            "company": "Nova Agency",
            "contact": "@nova_agency",
            "client_type": "agency",
            "campaign_goal": "holiday_promo",
            "platform": "unknown",
            "recommended_mechanic": "Advent Calendar",
            "pricing_tier": "Done-With-You Tier",
            "qualification_status": "ready_to_handoff",
            "missing_fields": [],
            "can_create_handoff": True,
            "owner": "Tony",
            "team": "Sales / Delivery",
            "has_crm_payload": True,
        },
    ),
    Case(
        name="FreshBox",
        message="We are FreshBox. Need a retention campaign with rewards for returning customers. Contact @freshbox_growth",
        expected={
            "company": "FreshBox",
            "contact": "@freshbox_growth",
            "client_type": "ecommerce_brand",
            "campaign_goal": "retention",
            "platform": "unknown",
            "recommended_mechanic": "Rewards Campaign",
            "pricing_tier": "Done-With-You Tier",
            "qualification_status": "ready_to_handoff",
            "missing_fields": [],
            "can_create_handoff": True,
            "owner": "Tony",
            "team": "Sales / Delivery",
            "has_crm_payload": True,
        },
    ),
    Case(
        name="GameLaunch Studio",
        message="We are GameLaunch Studio. Need a quiz lead magnet for a new product launch. Contact @gamelaunch_cmo",
        expected={
            "company": "GameLaunch Studio",
            "contact": "@gamelaunch_cmo",
            "client_type": "gaming_studio",
            "campaign_goal": "product_launch",
            "platform": "unknown",
            "recommended_mechanic": "Quiz / Lead Magnet",
            "pricing_tier": "Done-With-You Tier",
            "qualification_status": "ready_to_handoff",
            "missing_fields": [],
            "can_create_handoff": True,
            "owner": "Tony",
            "team": "Sales / Delivery",
            "has_crm_payload": True,
        },
    ),
]


def _lead_from_message(message: str) -> SimpleNamespace:
    return SimpleNamespace(
        company=extract_company(message),
        contact=extract_contact(message),
        use_case=extract_use_case(message),
        role=None,
        notes=None,
        status="new",
    )


def _actual(case: Case) -> dict[str, Any]:
    lead = _lead_from_message(case.message)
    intelligence = build_campaign_intelligence(
        lead,
        latest_message=SimpleNamespace(text=case.message),
    )
    owner = recommend_owner(lead)
    fake_handoff = None
    if intelligence["can_create_handoff"]:
        fake_handoff = SimpleNamespace(
            id=100,
            status="pending",
            assigned_to=None,
            created_at="2026-01-01 00:00:00",
        )
    package = build_handoff_package(
        lead,
        latest_handoff=fake_handoff,
        latest_message=SimpleNamespace(text=case.message),
    )
    crm_payload = package.get("crm_payload")
    expected_crm_fields = {
        "company",
        "contact",
        "role",
        "client_type",
        "campaign_goal",
        "platform",
        "campaign_need",
        "recommended_mechanic",
        "pricing_tier",
        "qualification_status",
        "score",
        "priority",
        "owner",
        "team",
        "next_action",
        "handoff_id",
        "created_at",
    }
    return {
        "company": lead.company or "",
        "contact": lead.contact or "",
        "client_type": intelligence["client_type"],
        "campaign_goal": intelligence["campaign_goal"],
        "platform": intelligence["platform"],
        "recommended_mechanic": intelligence["recommended_mechanic"],
        "pricing_tier": intelligence["pricing_tier"],
        "qualification_status": intelligence["qualification_status"],
        "missing_fields": intelligence["missing_fields"],
        "can_create_handoff": intelligence["can_create_handoff"],
        "owner": owner["owner"],
        "team": owner["team"],
        "has_crm_payload": bool(crm_payload),
        "crm_payload_has_expected_fields": (
            not crm_payload
            or set(crm_payload) == expected_crm_fields
        ),
    }


def main() -> None:
    failures: list[str] = []
    print("case | status | mechanic | tier | handoff | crm_payload | owner/team")
    print("-" * 92)

    for case in CASES:
        actual = _actual(case)
        for key, expected_value in case.expected.items():
            if actual.get(key) != expected_value:
                failures.append(
                    f"{case.name}: {key} expected {expected_value!r}, got {actual.get(key)!r}"
                )
        if not actual["crm_payload_has_expected_fields"]:
            failures.append(f"{case.name}: CRM payload fields do not match the contract")

        print(
            f"{case.name} | {actual['qualification_status']} | "
            f"{actual['recommended_mechanic']} | {actual['pricing_tier']} | "
            f"{actual['can_create_handoff']} | {actual['has_crm_payload']} | "
            f"{actual['owner']} / {actual['team']}"
        )

    lifecycle_lead = _lead_from_message(CASES[0].message)
    lifecycle_checks = {
        "pending": "ready_to_handoff",
        "in_progress": "active_handoff",
        "done": "completed_handoff",
    }
    for handoff_status, expected_status in lifecycle_checks.items():
        package = build_handoff_package(
            lifecycle_lead,
            latest_handoff=SimpleNamespace(
                id=200,
                status=handoff_status,
                assigned_to="Tony",
                created_at="2026-01-01 00:00:00",
            ),
            latest_message=SimpleNamespace(text=CASES[0].message),
        )
        actual_status = package["qualification_status"]
        if actual_status != expected_status:
            failures.append(
                f"lifecycle {handoff_status}: expected {expected_status!r}, got {actual_status!r}"
            )

    print("lifecycle | pending->ready_to_handoff | in_progress->active_handoff | done->completed_handoff")

    if failures:
        print("\nFAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("\nOK")


if __name__ == "__main__":
    main()
