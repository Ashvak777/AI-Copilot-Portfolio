# Project 02 — Service / Process Automation Agent

**Sanitized Reference Architecture** · Beyond Q&A: intent-driven enterprise actions

---

## 1. Business Problem

Service desks and operations teams receive high volumes of routine requests: status checks, form submissions, validations, and simple updates in enterprise systems. Manual handling creates backlog, inconsistent data entry, and slow feedback to employees or customers.

The organization needed an agent that can **take action**—not only answer questions—while preserving approvals, audit trails, and API security.

---

## 2. Solution

A Copilot Studio agent that detects intent, orchestrates Power Automate (and/or REST APIs via custom connectors), interacts with Dataverse or other backends, and returns a structured status or reference number.

```text
User
  → Copilot Studio (intent / topic routing)
  → Power Automate / API (OAuth)
  → Dataverse or enterprise backend
  → Business action + logging
  → Structured response (status / reference ID)
```

---

## 3. What the Agent Does

Example business capabilities (sanitized):

| Capability | Outcome |
|------------|---------|
| Retrieve information | Look up case, request, or record status the user is allowed to see |
| Submit service requests | Create a ticket or Dataverse row with validated fields |
| Initiate workflows | Start an approval or fulfillment flow |
| Perform validations | Check required fields, eligibility rules, or file rules |
| Update systems | Write only through approved APIs with scoped permissions |
| Return status | Provide transaction/reference ID and next steps |

**Measurable automation example (adjacent pattern):** A Python-based file-validation process reduced processing time from approximately three days to approximately ten minutes—illustrating the class of operational gains targeted when agents and automation replace manual validation loops.

---

## 4. Technical Architecture

1. **Conversation & intent** — Copilot Studio topics / generative orchestration classify the request and collect slots (IDs, dates, categories).
2. **Action layer** — Power Automate cloud flows or custom connectors call REST APIs with OAuth 2.0.
3. **System of record** — Dataverse, or enterprise APIs (CRM, ITSM, line-of-business).
4. **Response shaping** — Flow returns structured JSON; the agent presents a clear status message.
5. **Human-in-the-loop** — High-impact writes pause for approval before commit.

See [Agentic workflow architecture](../../architecture/agentic-workflow.md) for multi-tool extensions.

---

## 5. Integration Patterns

| Pattern | Notes |
|---------|--------|
| Power Automate | Preferred orchestration for Power Platform ALM and connectors |
| Custom connectors | Wrap internal REST APIs with OpenAPI definitions |
| OAuth 2.0 | Delegated user or application permissions, least privilege |
| Dataverse | Transactional store for requests, audit, and agent configuration |
| Error handling | Catch blocks, user-safe messages, correlation IDs |
| Retries | Transient HTTP retries with backoff; poison-message logging |
| Logging | Flow run history + Application Insights / central logging where used |

Reference pattern notes: [`samples/power-automate-patterns/`](../../samples/power-automate-patterns/), [`samples/api-patterns/`](../../samples/api-patterns/).

---

## 6. Security & Governance

- Authenticate the user; propagate identity to backends when the API supports OBO / delegated calls.
- Scope connector and app registrations to the minimum APIs and tables required.
- Separate read tools from write tools; require approval for destructive or high-value updates.
- Do not expose raw error payloads or stack traces to end users.
- Environment isolation: Dev / Test / Prod connections and connection references.

---

## 7. Deployment / ALM

Solutions package the Copilot agent components, flows, connection references, and environment variables. Promotion follows the ALM path in [Project 07](../07-copilot-alm/).

---

## 8. Business Value

- Shorter cycle time for routine service requests
- Fewer hand-offs for status and validation work
- Consistent data capture into systems of record
- Auditable automation with clear reference IDs
