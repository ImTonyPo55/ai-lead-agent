from __future__ import annotations

import os
import ssl
import urllib.parse
import urllib.request
from typing import Any

import certifi

from app.services.handoff_package_service import build_handoff_package


def _field(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _owner_team(owner_routing: Any = None) -> tuple[str, str]:
    if isinstance(owner_routing, dict):
        owner = _field(owner_routing.get("owner"))
        team = _field(owner_routing.get("team"))
        return owner or "Unassigned", team or "Intake"

    owner = _field(getattr(owner_routing, "owner", None))
    team = _field(getattr(owner_routing, "team", None))
    return owner or "Unassigned", team or "Intake"


def notify_handoff_created(
    lead: Any,
    handoff: Any = None,
    owner_routing: Any = None,
) -> bool:
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            return False

        handoff_id = getattr(handoff, "id", None) if handoff is not None else None
        owner, team = _owner_team(owner_routing)
        handoff_package = build_handoff_package(lead, latest_handoff=handoff)
        message = "\n".join(
            [
                "🔥 New campaign lead",
                "",
                f"Company: {_field(getattr(lead, 'company', None))}",
                f"Contact: {_field(getattr(lead, 'contact', None))}",
                f"Client type: {_field(handoff_package.get('client_type'))}",
                f"Goal: {_field(handoff_package.get('campaign_goal'))}",
                f"Mechanic: {_field(handoff_package.get('recommended_mechanic'))}",
                f"Tier: {_field(handoff_package.get('pricing_tier'))}",
                f"Owner: {owner}",
                f"Team: {team}",
                f"Handoff: {_field(handoff_id)}",
            ]
        )

        data = urllib.parse.urlencode(
            {
                "chat_id": chat_id,
                "text": message,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data,
            method="POST",
        )
        context = ssl.create_default_context(cafile=certifi.where())

        with urllib.request.urlopen(request, timeout=5, context=context) as response:
            return 200 <= response.status < 300
    except Exception:
        return False


def notify_action_updated(
    lead: Any,
    handoff: Any = None,
    action_queue: Any = None,
) -> bool:
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            return False

        owner, team = _owner_team(action_queue)
        if isinstance(action_queue, dict):
            action = _field(action_queue.get("label")) or _field(action_queue.get("status"))
            next_action = _field(action_queue.get("next_action"))
        else:
            action = _field(getattr(action_queue, "label", None)) or _field(
                getattr(action_queue, "status", None)
            )
            next_action = _field(getattr(action_queue, "next_action", None))

        lead_label = (
            _field(getattr(lead, "company", None))
            or _field(getattr(lead, "contact", None))
            or f"lead_id {_field(getattr(lead, 'id', None))}"
        )
        message = "\n".join(
            [
                "⚡ Lead action updated",
                "",
                f"Lead: {lead_label}",
                f"Owner: {owner}",
                f"Team: {team}",
                f"Action: {action}",
                f"Next: {next_action}",
            ]
        )

        data = urllib.parse.urlencode(
            {
                "chat_id": chat_id,
                "text": message,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data,
            method="POST",
        )
        context = ssl.create_default_context(cafile=certifi.where())

        with urllib.request.urlopen(request, timeout=5, context=context) as response:
            return 200 <= response.status < 300
    except Exception:
        return False
