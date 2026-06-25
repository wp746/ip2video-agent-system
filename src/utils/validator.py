"""Input validation."""

from __future__ import annotations

from typing import Any, Dict


def validate_input(data: Dict[str, Any]) -> None:
    if "ip_input" not in data:
        raise ValueError("Missing required field: ip_input")
    ip_input = data["ip_input"]
    for field in ("name", "description"):
        if not ip_input.get(field):
            raise ValueError(f"Missing required ip_input.{field}")
