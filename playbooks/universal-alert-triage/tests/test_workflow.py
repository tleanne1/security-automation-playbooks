"""Tests for the Universal Alert Triage & Enrichment reference workflow."""

import sys
from pathlib import Path

import pytest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from normalize_alert import AlertValidationError, normalize_alert
from triage_alert import triage_alert


def sample_alert() -> dict:
    """Return a synthetic suspicious sign-in alert."""

    return {
        "alert_id": "ALT-2026-001",
        "source": "identity-provider",
        "alert_type": "suspicious_sign_in",
        "title": "Suspicious Sign-In Activity",
        "timestamp": "2026-10-10T14:32:18Z",
        "severity": "high",
        "status": "new",
        "description": (
            "A user account authenticated from an unusual "
            "location and IP address."
        ),
        "entities": {
            "user": {
                "user_id": "USR-1042",
                "display_name": "Jordan Lee",
                "email": "jordan.lee@example.com",
            },
            "source_ip": {
                "address": "203.0.113.42",
            },
            "device": {
                "device_id": "DEV-2048",
                "hostname": "FIN-LT-042",
                "managed": True,
            },
        },
        "detection": {
            "risk_level": "high",
            "risk_signals": [
                "unusual_location",
                "new_ip_address",
            ],
        },
    }


def test_alert_normalization():
    alert = sample_alert()

    normalized = normalize_alert(alert)

    assert normalized["schema_version"] == "1.0"
    assert normalized["event"]["id"] == "ALT-2026-001"
    assert normalized["event"]["severity"] == "high"
    assert normalized["entities"]["source_ip"] == "203.0.113.42"
    assert normalized["entities"]["device"]["managed"] is True


def test_missing_required_field_is_rejected():
    alert = sample_alert()
    del alert["alert_id"]

    with pytest.raises(AlertValidationError):
        normalize_alert(alert)


def test_high_risk_alert_is_escalated():
    normalized = normalize_alert(sample_alert())

    decision = triage_alert(normalized)

    assert decision["risk"] == "high"
    assert decision["route"] == "escalate"
    assert decision["analyst_review"] is True
    assert decision["response_approval_required"] is True


def test_decision_contains_explanation():
    normalized = normalize_alert(sample_alert())

    decision = triage_alert(normalized)

    assert decision["decision_reasons"]
    assert any(
        "Suspicious signals detected" in reason
        for reason in decision["decision_reasons"]
    )


def test_low_risk_alert_is_monitored():
    alert = sample_alert()

    alert["severity"] = "low"
    alert["detection"]["risk_level"] = "low"
    alert["detection"]["risk_signals"] = []

    normalized = normalize_alert(alert)
    decision = triage_alert(normalized)

    assert decision["risk"] == "low"
    assert decision["route"] == "monitor"
    assert decision["analyst_review"] is False
    assert decision["response_approval_required"] is False


def test_unmanaged_device_increases_risk():
    alert = sample_alert()

    alert["severity"] = "low"
    alert["detection"]["risk_level"] = "low"
    alert["detection"]["risk_signals"] = []
    alert["entities"]["device"]["managed"] = False

    normalized = normalize_alert(alert)
    decision = triage_alert(normalized)

    assert decision["risk_score"] == 3
    assert "Alert involves an unmanaged device" in decision["decision_reasons"]
