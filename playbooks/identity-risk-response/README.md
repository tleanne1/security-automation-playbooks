# Identity Risk Investigation & Response

## Overview

Identity Risk Investigation & Response is a security orchestration reference design for investigating potentially compromised user identities and coordinating controlled response actions.

The workflow combines identity risk signals with authentication context, endpoint telemetry, security alerts, and account information to help an analyst determine whether suspicious identity activity represents legitimate behavior, elevated risk, or probable account compromise.

Potentially disruptive identity actions remain analyst-controlled.

## Security Problem

Identity alerts rarely provide enough context on their own to determine whether an account is compromised.

An analyst may need to investigate:

- Risky or anomalous sign-ins
- Unusual authentication locations
- New or unfamiliar IP addresses
- Impossible-travel indicators
- Unfamiliar devices
- Authentication failures
- Privileged account activity
- Related endpoint alerts
- Related security incidents
- Existing identity risk signals

Manually gathering this context across multiple security platforms increases investigation time and can lead to inconsistent response decisions.

## Objectives

The workflow is designed to:

1. Receive an identity-related security alert.
2. Extract the affected identity and authentication context.
3. Enrich the investigation with identity, sign-in, endpoint, and security telemetry.
4. Correlate related risk signals and activity.
5. Determine an appropriate investigation path.
6. Escalate probable account compromise.
7. Present response options to an analyst.
8. Require approval before sensitive identity actions.
9. Record the investigation and response outcome.

## High-Level Workflow

```mermaid
flowchart TD
    A[Identity Security Alert] --> B[Validate Alert]
    B --> C[Extract User & Authentication Context]

    C --> D[Identity Enrichment]
    C --> E[Sign-In Analysis]
    C --> F[Endpoint Context]
    C --> G[Related Security Alerts]

    D --> H[Correlate Evidence]
    E --> H
    F --> H
    G --> H

    H --> I{Risk Assessment}

    I -->|Low| J[Document / Monitor]
    I -->|Medium| K[Analyst Investigation]
    I -->|High| L[Potential Account Compromise]

    L --> M[Prepare Response Options]

    M --> N{Analyst Approval}

    N -->|Approved| O[Controlled Identity Response]
    N -->|Rejected| P[Continue Investigation]

    O --> Q[Record Outcome]
    P --> Q
    K --> Q
    J --> Q
