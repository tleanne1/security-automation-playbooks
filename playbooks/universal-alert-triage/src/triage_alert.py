"""Risk evaluation and routing logic for normalized security alerts."""

from __future__ import annotations

from typing import Any


SEVERITY_SCORES = {
    "informational": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
    "unknown": 1,
}

HIGH_RISK_SIGNALS = {
    "impossible_travel",
    "malicious_ip",
    "known_malware",
    "credential_compromise",
    "privileged_account",
}

SUSPICIOUS_SIGNALS = {
    "unusual_location",
    "new_ip_address",
    "unmanaged_device",
    "anonymous_ip",
    "unfamiliar_sign_in",
}


def calculate_risk_score(alert: dict[str, Any]) -> tuple[int, list[str]]:
    """
    Calculate an explainable risk score.

    Returns both the numeric score and the reasons that contributed
    to the decision so an analyst can understand the routing outcome.
    """

    event = alert.get("event") or {}
    detection = alert.get("detection") or {}
    entities = alert.get("entities") or {}

    score = 0
    reasons: list[str] = []

    severity = event.get("severity", "unknown")
    severity_score = SEVERITY_SCORES.get(severity, 1)

    score += severity_score

    if severity_score >= 3:
        reasons.append(f"Alert severity is {severity}")

    risk_level = detection.get("risk_level", "unknown")
    risk_score = SEVERITY_SCORES.get(risk_level, 1)

    score += risk_score

    if risk_score >= 3:
        reasons.append(f"Detection risk level is {risk_level}")

    risk_signals = set(detection.get("risk_signals") or [])

    high_risk_matches = risk_signals & HIGH_RISK_SIGNALS
    suspicious_matches = risk_signals & SUSPICIOUS_SIGNALS

    if high_risk_matches:
        score += 3
        reasons.append(
            "High-risk signal detected: "
            + ", ".join(sorted(high_risk_matches))
        )

    if suspicious_matches:
        score += len(suspicious_matches)
        reasons.append(
            "Suspicious signals detected: "
            + ", ".join(sorted(suspicious_matches))
        )

    device = entities.get("device") or {}

    if device.get("managed") is False:
        score += 1
        reasons.append("Alert involves an unmanaged device")

    return score, reasons


def determine_route(score: int) -> dict[str, Any]:
    """Map the risk score to an investigation and response path."""

    if score >= 10:
        return {
            "risk": "critical",
            "route": "escalate",
            "analyst_review": True,
            "response_approval_required": True,
        }

    if score >= 7:
        return {
            "risk": "high",
            "route": "escalate",
            "analyst_review": True,
            "response_approval_required": True,
        }

    if score >= 4:
        return {
            "risk": "medium",
            "route": "analyst_investigation",
            "analyst_review": True,
            "response_approval_required": False,
        }

    return {
        "risk": "low",
        "route": "monitor",
        "analyst_review": False,
        "response_approval_required": False,
    }


def triage_alert(alert: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a normalized alert and return an explainable triage decision."""

    score, reasons = calculate_risk_score(alert)
    decision = determine_route(score)

    return {
        "risk_score": score,
        **decision,
        "decision_reasons": reasons,
    }
