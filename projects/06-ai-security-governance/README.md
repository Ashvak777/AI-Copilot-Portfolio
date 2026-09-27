# Project 06 — AI Security & Governance

**Sanitized Reference Architecture** · Framework for enterprise Copilot and Azure AI

---

## 1. Business Problem

AI assistants and agents introduce new pathways to data and actions. Without deliberate controls, organizations risk oversharing, unauthorized writes, weak audit trails, and non-compliance with Responsible AI expectations—especially in banking, insurance, and regulatory contexts.

---

## 2. Solution

A layered governance framework covering identity, authorization, data protection, model/prompt risk, environments, and operations.

**Core principle:** An AI agent should never provide access to information or operations that the authenticated user would not normally be authorized to access.

Diagram: [Security & governance](../../architecture/security-governance.md).

---

## 3. Control Areas

### Identity & access

| Control | Practice |
|---------|----------|
| Microsoft Entra ID | Authenticate users and apps; conditional access as required |
| Authorization / RBAC | Role-based access to Copilot, Fabric, Dataverse, Azure resources |
| RLS | Row-level security in semantic models and data APIs |
| Least privilege | Separate read/write tool identities; minimal API scopes |
| Managed identities | Prefer over long-lived secrets for Azure resources |
| OAuth 2.0 | Standardized token acquisition for APIs and connectors |

### Secrets & connectors

- Azure Key Vault for remaining secrets and certificates
- Connection references per environment; no secrets in solution XML or source control
- Connector governance: approved connectors only; DLP policies in Power Platform

### Data protection

| Control | Practice |
|---------|----------|
| DLP | Restrict exfiltration paths for sensitive content |
| Microsoft Purview | Classification, labeling, catalog, lineage |
| Sensitive-data controls | Minimize PII in prompts/logs; redaction patterns |
| Audit logging | Who asked what, which tools ran, which sources retrieved |

### Responsible AI & prompt risk

- Groundedness requirements and refusal behavior
- Prompt-injection protection: isolate system policy from user/retrieved content
- Evaluation gates before production promotion
- Human review for high-risk scenarios

### Environment isolation

```text
Development → Test → UAT → Production
```

Separate environments, identities, connectors, and data samples. Production corpora and credentials never used in personal developer tenants.

---

## 4. Validation Flow (Reference)

See [`samples/api-patterns/security-validation-flow.md`](../../samples/api-patterns/security-validation-flow.md) for a concise check sequence before an agent tool executes.

---

## 5. Operating Model

- Security + platform owners approve connector and app-registration designs
- AI evaluation results attached to release evidence
- Incident runbooks for suspected prompt abuse or data leakage
- Periodic access reviews for agent identities and high-privilege connectors

---

## 6. Business Value

- Reduces likelihood that AI becomes an entitlement bypass
- Provides auditability for regulated reviews
- Enables safer expansion from Q&A to agentic actions
- Aligns Copilot delivery with existing enterprise IAM and Purview programs
