# Project 07 — Copilot ALM / Production Deployment

**Sanitized Reference Architecture** · Repeatable promotion to production

---

## 1. Business Problem

Copilot Studio agents, Power Automate flows, and Dataverse customizations developed only in a maker portal are hard to review, regress, and roll back. Regulated enterprises need the same discipline as application releases: versioning, environments, automated deployment, and monitoring.

---

## 2. Solution

A production lifecycle for Power Platform + Copilot solutions:

```text
Development
  → Source control
  → Test
  → UAT
  → Production
```

Packaged as Power Platform solutions (preferably **managed** in higher environments), deployed via Azure DevOps or GitHub Actions with environment variables and connection references.

---

## 3. Lifecycle Components

| Element | Purpose |
|---------|---------|
| Unmanaged solution (Dev) | Active development |
| Source control | Solution export / unpacked YAML or zip artifacts |
| Managed solution (Test/UAT/Prod) | Controlled deployment surface |
| Environment variables | URLs, feature flags, non-secret configuration |
| Connection references | Bind connectors per environment without hardcoding |
| CI/CD pipeline | Build validation → deploy → smoke tests |
| Versioning | Semantic or build-number version on solution |
| Testing | Topic/flow tests, RAG evaluation suite, UAT scripts |
| Rollback | Redeploy prior managed solution version; feature flags |
| Monitoring | Flow failures, Copilot analytics, App Insights / Log Analytics |
| Adoption analytics | Usage, containment, escalation rates |

---

## 4. CI/CD Sketch

```text
Commit / PR
  → Validate solution (pac / pipelines)
  → Run automated checks (including AI evaluation where applicable)
  → Deploy to Test
  → Deploy to UAT (approval gate)
  → Deploy to Production (approval gate)
  → Post-deploy health checks
```

Pipelines use service principals with least privilege on each environment. Secrets stay in the pipeline secret store or Key Vault—not in the repository.

---

## 5. Testing Strategy

| Layer | Examples |
|-------|----------|
| Component | Flow unit paths, connector mocks |
| Conversation | Golden dialog scripts for critical intents |
| RAG quality | Groundedness / relevance regression set |
| Security | Negative tests for unauthorized retrieval/actions |
| UAT | Business sign-off on scenarios |

---

## 6. Operations

- Alert on elevated flow failure rates and auth errors
- Track adoption and deflection metrics for stakeholders
- Change calendar for model/prompt updates with evaluation evidence
- Document rollback owners and RTO expectations

Related: [Project 06 — Security](../06-ai-security-governance/), [samples/evaluation](../../samples/evaluation/).

---

## 7. Business Value

- Predictable releases suitable for regulated change management
- Faster recovery via versioned managed solutions
- Evidence for audit: what changed, who approved, what was tested
- Separates experimentation in Dev from production reliability
