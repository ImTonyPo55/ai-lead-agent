from __future__ import annotations

import os
import ssl
import urllib.parse
import urllib.request
from typing import Any

import certifi


def _field(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def notify_handoff_created(lead: Any, handoff: Any = None) -> bool:
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            return False

        handoff_id = getattr(handoff, "id", None) if handoff is not None else None
        message = "\n".join(
            [
                "🔥 New qualified lead",
                "",
                f"Company: {_field(getattr(lead, 'company', None))}",
                f"Role: {_field(getattr(lead, 'role', None))}",
                f"Contact: {_field(getattr(lead, 'contact', None))}",
                f"Use case: {_field(getattr(lead, 'use_case', None))}",
                f"Status: {_field(getattr(lead, 'status', None))}",
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
