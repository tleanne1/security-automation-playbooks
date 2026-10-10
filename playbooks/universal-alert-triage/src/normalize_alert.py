"""Normalize security alerts into a common investigation schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "alert_id",
    "source",
    "alert_type",
    "title",
    "timestamp",
    "severity",
)


class AlertValidationError(ValueError):
    """Raised when an incoming security alert fails validation."""


def validate_alert(alert: dict[str, Any]) -> None:
    """Validate fields required for downstream investigation."""

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if not alert.get(field)
    ]

    if missing_fields:
        raise AlertValidationError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )


def normalize_severity(severity: str) -> str:
    """Convert source severity values into a common severity model."""

    severity_map = {
        "informational": "informational",
        "info": "informational",
        "low": "low",
        "medium": "medium",
        "moderate": "medium",
        "high": "high",
        "critical": "critical",
        "severe": "critical",
    }

    return severity_map.get(str(severity).strip().lower(), "unknown")


def extract_entities(alert: dict[str, Any]) -> dict[str, Any]:
    """Extract investigation entities while tolerating missing data."""

    entities = alert.get("entities") or {}

    user = entities.get("user") or {}
    source_ip = entities.get("source_ip") or {}
    device = entities.get("device") or {}

    return {
        "user": {
            "user_id": user.get("user_id"),
            "display_name": user.get("display_name"),
            "email": user.get("email"),
        },
        "source_ip": source_ip.get("address"),
        "device": {
            "device_id": device.get("device_id"),
            "hostname": device.get("hostname"),
            "managed": device.get("managed"),
        },
    }


def normalize_alert(alert: dict[str, Any]) -> dict[str, Any]:
    """Transform a source alert into the common investigation schema."""

    validate_alert(alert)

    detection = alert.get("detection") or {}

    normalized = {
        "schema_version": "1.0",
        "event": {
            "id": alert["alert_id"],
            "source": alert["source"],
            "type": alert["alert_type"],
            "title": alert["title"],
            "timestamp": alert["timestamp"],
            "severity": normalize_severity(alert["severity"]),
            "status": alert.get("status", "unknown"),
            "description": alert.get("description"),
        },
        "entities": extract_entities(alert),
        "detection": {
            "risk_level": normalize_severity(
                detection.get("risk_level", "unknown")
            ),
            "risk_signals": detection.get("risk_signals", []),
        },
    }

    return normalized


def load_json(path: Path) -> dict[str, Any]:
    """Load an alert from a JSON file."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    """Normalize the portfolio's synthetic suspicious sign-in alert."""

    project_dir = Path(__file__).resolve().parent.parent
    input_path = project_dir / "sample-data" / "suspicious-signin-alert.json"

    alert = load_json(input_path)
    normalized = normalize_alert(alert)

    print(json.dumps(normalized, indent=2))


if __name__ == "__main__":
    main()
