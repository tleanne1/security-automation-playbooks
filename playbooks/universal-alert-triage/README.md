# Universal Alert Triage & Enrichment

## Overview

Universal Alert Triage & Enrichment is a vendor-neutral SOAR workflow designed to automate the initial investigation of security alerts while preserving analyst control over security-sensitive response actions.

The workflow accepts alerts from multiple security sources, normalizes incoming telemetry into a consistent structure, extracts relevant entities and indicators, performs contextual enrichment, evaluates risk, and routes the alert to the appropriate investigation or escalation path.

This project demonstrates the architecture and engineering patterns behind a production-oriented security orchestration workflow without exposing proprietary playbooks, customer data, credentials, or internal infrastructure.

## Security Problem

Security operations teams receive alerts from multiple security products with different schemas, severity models, entity formats, and levels of context.

Analysts frequently have to perform the same initial tasks:

- Review the incoming alert
- Identify affected users, hosts, IP addresses, URLs, domains, and other indicators
- Gather additional context from security tools
- Determine whether the alert warrants further investigation
- Establish priority and severity
- Escalate suspicious activity
- Decide whether response actions are appropriate

Performing these steps manually increases investigation time and makes triage less consistent.

This workflow automates the repeatable portions of that process while keeping consequential response decisions under analyst control.

## Objectives

The workflow is designed to:

1. Accept security alerts from different telemetry sources.
2. Normalize alert data into a common investigation model.
3. Extract security-relevant entities and indicators.
4. Enrich those entities using available security integrations.
5. Evaluate the combined alert and enrichment context.
6. Assign an investigation path based on risk.
7. Escalate alerts requiring analyst attention.
8. Require human approval before disruptive response actions.

## High-Level Workflow

```mermaid
flowchart TD
    A[Security Alert] --> B[Validate Input]
    B --> C[Normalize Alert]
    C --> D[Extract Entities & IOCs]
    D --> E[Enrichment]

    E --> F[Identity Context]
    E --> G[Endpoint Context]
    E --> H[Threat Intelligence]
    E --> I[Email / Cloud Context]

    F --> J[Correlate Findings]
    G --> J
    H --> J
    I --> J

    J --> K[Risk & Severity Evaluation]

    K -->|Low Risk| L[Document & Close / Monitor]
    K -->|Medium Risk| M[Analyst Investigation]
    K -->|High Risk| N[Escalate Incident]

    N --> O{Response Action Required?}
    O -->|No| P[Continue Investigation]
    O -->|Yes| Q[Analyst Approval]
    Q -->|Approved| R[Execute Controlled Response]
    Q -->|Rejected| P

    R --> S[Record Outcome]
    P --> S
    M --> S
    L --> S
