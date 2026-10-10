"""Run the Universal Alert Triage & Enrichment reference workflow."""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC_DIR))

from normalize_alert import AlertValidationError, load_json, normalize_alert
from triage_alert import triage_alert


def print_header(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def format_value(value: object) -> str:
    if value is None or value == "":
        return "Not available"
    return str(value)


def run_workflow(alert_path: Path) -> int:
    """Process an alert through normalization and triage."""

    try:
        raw_alert = load_json(alert_path)
        normalized = normalize_alert(raw_alert)
        decision = triage_alert(normalized)
    except FileNotFoundError:
        print(f"ERROR: Alert file not found: {alert_path}")
        return 1
    except AlertValidationError as exc:
        print(f"ERROR: Alert validation failed: {exc}")
        return 1

    event = normalized["event"]
    entities = normalized["entities"]

    user = entities.get("user") or {}
    device = entities.get("device") or {}

    print_header("UNIVERSAL ALERT TRIAGE & ENRICHMENT")

    print(f"Alert:       {format_value(event.get('title'))}")
    print(f"Alert ID:    {format_value(event.get('id'))}")
    print(f"Source:      {format_value(event.get('source'))}")
    print(f"Severity:    {format_value(event.get('severity')).upper()}")

    print_header("ENTITIES")

    print(f"User:        {format_value(user.get('email'))}")
    print(f"Source IP:   {format_value(entities.get('source_ip'))}")
    print(f"Endpoint:    {format_value(device.get('hostname'))}")
    print(f"Managed:     {format_value(device.get('managed'))}")

    print_header("TRIAGE DECISION")

    print(f"Risk Score:  {decision['risk_score']}")
    print(f"Risk:        {decision['risk'].upper()}")
    print(f"Route:       {decision['route'].upper()}")

    print()
    print("Decision Evidence:")

    if decision["decision_reasons"]:
        for reason in decision["decision_reasons"]:
            print(f"  - {reason}")
    else:
        print("  - No elevated risk indicators identified")

    print()
    print(
        "Analyst Review:             "
        + ("REQUIRED" if decision["analyst_review"] else "NOT REQUIRED")
    )

    print(
        "Response Approval Required: "
        + (
            "YES"
            if decision["response_approval_required"]
            else "NO"
        )
    )

    print(
        "Automated Disruptive Action: "
        + (
            "BLOCKED PENDING APPROVAL"
            if decision["response_approval_required"]
            else "NOT REQUESTED"
        )
    )

    print_header("WORKFLOW COMPLETE")

    return 0


def main() -> None:
    project_dir = Path(__file__).resolve().parent

    default_alert = (
        project_dir
        / "sample-data"
        / "suspicious-signin-alert.json"
    )

    alert_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_alert

    raise SystemExit(run_workflow(alert_path))


if __name__ == "__main__":
    main()
