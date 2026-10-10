# Security Automation & SOAR Engineering
[![Security Automation Tests](https://github.com/tleanne1/security-automation-playbooks/actions/workflows/security-tests.yml/badge.svg)](https://github.com/tleanne1/security-automation-playbooks/actions/workflows/security-tests.yml)

A cybersecurity engineering portfolio focused on security orchestration, automated investigation and response, SOAR playbook development, security integrations, and human-in-the-loop automation.

This repository contains vendor-neutral reference implementations and case studies based on security automation patterns I have designed and worked with across SOAR, SIEM, EDR, identity, vulnerability management, and AI-assisted security operations.

## Focus Areas

- Security Automation & Orchestration (SOAR)
- Playbook & Workflow Engineering
- Alert Triage & Enrichment
- Incident Investigation & Response
- Detection & Response Engineering
- Identity Security
- Email Security
- Endpoint Security
- Vulnerability Management
- Security Data Normalization & Enrichment
- REST API & Security Platform Integrations
- Human-in-the-Loop Response Automation
- AI-Assisted Security Operations

## Security Automation Playbooks
## Security Automation Playbooks

| Workflow | Security Domain | Capabilities | Status |
| --- | --- | --- | --- |
| [Universal Alert Triage & Enrichment](playbooks/universal-alert-triage/) | SOC / Incident Response | Normalization, entity extraction, explainable risk scoring, triage & escalation | **Working Implementation** |
| [Identity Risk Investigation & Response](playbooks/identity-risk-response/) | Identity Security | Identity enrichment, risk correlation, investigation & controlled response | **Case Study** |
| [Email Security Investigation & Response](playbooks/email-security-investigation/) | Email Security | IOC enrichment, evidence correlation, phishing investigation & remediation | **Case Study** |
| [Endpoint Investigation & Response](playbooks/endpoint-investigation-response/) | Endpoint Security | Endpoint enrichment, evidence correlation, containment & response | **Case Study** |
| [Vulnerability Investigation & Remediation](playbooks/vulnerability-remediation/) | Vulnerability Management | Asset correlation, risk prioritization, remediation & verification | **Case Study** |

### Featured Implementation

The [Universal Alert Triage & Enrichment](playbooks/universal-alert-triage/) project includes an executable Python reference implementation with:

- Synthetic security telemetry
- Input validation and normalization
- Security entity extraction
- Explainable risk scoring
- Investigation routing
- Human-in-the-loop response controls
- Automated pytest coverage
- GitHub Actions CI

The remaining projects are security engineering case studies documenting investigation architecture, integration requirements, failure handling, response boundaries, and security controls across identity, email, endpoint, and vulnerability operations.

## Architecture Principles

The workflows in this repository are designed around several core security engineering principles:

**Human oversight**

Security-critical response actions should support analyst review and approval where appropriate rather than assuming unrestricted autonomous execution.

**Evidence-driven automation**

Automated decisions should be supported by security telemetry, enrichment results, investigation context, and clearly defined decision logic.

**Controlled response**

Investigation and response workflows should separate data collection and analysis from potentially disruptive actions such as containment, account changes, or remediation.

**Integration-aware design**

Production security automation depends on more than workflow logic. Authentication, permissions, connector health, API behavior, telemetry availability, command support, and platform limitations are treated as part of the engineering problem.

**Testability**

Workflows should support repeatable testing using controlled inputs, expected outputs, documented decision paths, and observable results.

## Technology Areas

The portfolio demonstrates patterns involving technologies and concepts such as:

- D3 Security
- Microsoft Defender XDR
- Microsoft Defender for Endpoint
- Microsoft Sentinel
- Microsoft Entra ID
- Microsoft Defender for Office 365
- Tenable
- Python
- REST APIs
- JSON
- Webhooks
- SIEM / EDR / SOAR integrations
- Security telemetry normalization
- Agentic AI and LLM-assisted security workflows

## SOAR & Security Automation Engineering

My security automation work includes hands-on workflow engineering, platform evaluation, integration analysis, testing, and troubleshooting across enterprise security environments.

### D3 Security

Hands-on engineering experience includes:

- Investigation and incident playbook development
- Alert triage and enrichment workflows
- Microsoft security integration mapping
- Workflow import and portability validation
- Utility-command and data-transformation workflows
- Playbook testing and runtime validation
- Connector and authentication troubleshooting
- Response-action dependency analysis
- Human-in-the-loop response design
- Security telemetry normalization

### SOAR Platform Evaluation

I have also evaluated security orchestration platforms, including **Torq**, against areas such as:

- Integration coverage
- Workflow capabilities
- API support
- Security use cases
- Implementation constraints
- Automation architecture
- Operational fit

Platform evaluation and hands-on implementation experience are represented separately throughout this portfolio to avoid overstating implementation depth.

## Repository Structure

```text
security-automation-playbooks/
├── playbooks/
│   ├── universal-alert-triage/
│   ├── identity-risk-response/
│   ├── email-security-investigation/
│   ├── endpoint-investigation-response/
│   └── vulnerability-remediation/
├── integrations/
│   ├── microsoft-security/
│   └── security-data-normalization/
├── automation/
│   └── python/
├── architecture/
└── docs/
```

## Portfolio Approach

These projects focus on the engineering behind security automation:

1. Define the security problem and investigation objective.
2. Identify required telemetry, entities, integrations, and permissions.
3. Normalize and enrich security data.
4. Build investigation and decision logic.
5. Define escalation and response paths.
6. Introduce analyst approval for security-sensitive actions.
7. Test expected, edge, and failure conditions.
8. Document operational dependencies and limitations.

Each completed playbook will include architecture documentation, workflow logic, synthetic sample data, testing methodology, security considerations, and implementation notes.

## Security & Data Handling

This repository is a personal engineering portfolio.

All examples are sanitized and use synthetic or non-sensitive data. No customer data, employer-confidential information, production credentials, internal infrastructure details, or proprietary workflow exports are included.

The implementations are intended to demonstrate security engineering concepts, architecture, workflow design, and automation methodology rather than reproduce any organization's production environment.

## About

I'm a Forward Deployment Engineer with a cybersecurity background focused on security automation, AI-assisted security operations, enterprise integrations, and secure workflow engineering.

My work spans cybersecurity engineering, SOAR, detection and response, vulnerability management, security integrations, agentic AI, Python automation, and human-in-the-loop security systems.

For additional projects, visit my GitHub profile.
