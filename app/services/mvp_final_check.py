from __future__ import annotations

from app.api.routes.ui import portfolio_page, ui_page
from app.main import app
from app.services.campaign_regression_check import CASES, _actual


REQUIRED_ROUTES = {"/", "/ui", "/ui/", "/health", "/portfolio"}

REQUIRED_UI_STRINGS = (
    "MechanicFlow AI",
    "Campaign handoff package",
    "Follow-up package",
    "Technical summary JSON",
    "ready for handoff",
    "needs follow-up",
    "Export to CRM",
    "Move to work",
    "Complete handoff",
    "Portfolio / Case Study",
    "How to test this demo",
)

REQUIRED_PORTFOLIO_STRINGS = (
    "MechanicFlow AI",
    "AI lead qualification and CRM-ready handoff agent for campaign requests",
    "Problem",
    "Solution",
    "Core Workflow",
    "What the Agent Extracts",
    "What the Agent Outputs",
    "Tech Stack",
    "Automation level",
    "Current status",
    "Known MVP Limitations",
    "Use Cases",
    "Business Value",
    "Open Live Demo",
    "Open App UI",
)


def _check_routes() -> None:
    routes = {getattr(route, "path", "") for route in app.routes}
    missing = sorted(REQUIRED_ROUTES - routes)
    if missing:
        raise SystemExit(f"Missing production routes: {', '.join(missing)}")


def _check_ui_labels() -> None:
    html = ui_page()
    missing = [text for text in REQUIRED_UI_STRINGS if text not in html]
    if missing:
        raise SystemExit(f"Missing UI labels: {', '.join(missing)}")


def _check_portfolio_page() -> None:
    html = portfolio_page()
    missing = [text for text in REQUIRED_PORTFOLIO_STRINGS if text not in html]
    if missing:
        raise SystemExit(f"Missing portfolio content: {', '.join(missing)}")


def _check_campaign_regression() -> None:
    failures: list[str] = []
    for case in CASES:
        actual = _actual(case)
        for key, expected_value in case.expected.items():
            if actual.get(key) != expected_value:
                failures.append(
                    f"{case.name}: {key} expected {expected_value!r}, got {actual.get(key)!r}"
                )
        if not actual["crm_payload_has_expected_fields"]:
            failures.append(f"{case.name}: CRM payload fields do not match the contract")

    if failures:
        raise SystemExit("MVP regression failed:\n- " + "\n- ".join(failures))


def main() -> None:
    _check_routes()
    _check_ui_labels()
    _check_portfolio_page()
    _check_campaign_regression()
    print("MVP final check OK")


if __name__ == "__main__":
    main()
