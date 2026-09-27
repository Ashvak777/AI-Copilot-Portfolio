# Project 03 — Agentic AI Workflow

**Sanitized Reference Architecture** · Decide, retrieve, call tools, or escalate

---

## 1. Business Problem

Enterprise users ask mixed questions: some need document knowledge, some need structured data, some need an API call or workflow, and some require a specialist process. A single FAQ bot fails; hard-coded topics do not scale.

The organization needed an agent that can **choose the right action path** under policy constraints.

---

## 2. Solution

An agentic orchestration layer (Copilot Studio with Azure OpenAI tool calling / generative orchestration) that decides whether to:

1. Search enterprise knowledge (RAG)
2. Retrieve structured data (Dataverse / SQL / Fabric-backed APIs)
3. Call an enterprise API
4. Trigger a Power Automate workflow
5. Delegate to a specialized agent
6. Return a direct grounded answer

```text
User intent
  → Orchestrator agent
      ├─ Knowledge tool (RAG / SharePoint)
      ├─ Data tool (Dataverse / Databricks query API)
      ├─ Action tool (REST / MCP / Power Automate)
      ├─ Specialist agent
      └─ Human approval (high-risk writes)
  → Unified response + audit trail
```

---

## 3. What the Agent Does

| Decision | Example |
|----------|---------|
| Knowledge search | “What is the retention policy for X?” → RAG + citations |
| Structured data | “What is the status of request 12345?” → Dataverse / API read |
| API call | “Get the latest rate for product Y” → REST with OAuth |
| Workflow | “Open a service request for Z” → Power Automate create |
| Delegate | Compliance-specific follow-up → specialized agent |
| Answer | Clarification or refusal when tools are insufficient |

---

## 4. Technical Architecture

### Orchestration

- **Planner / orchestrator** selects tools based on intent, confidence, and policy.
- **Tool schemas** describe inputs/outputs (see [`samples/api-patterns/agent-tool-schema.json`](../../samples/api-patterns/agent-tool-schema.json)).
- **MCP-based integrations** may expose standardized tool surfaces to enterprise systems alongside custom connectors.
- **Power Automate** remains a reliable bridge for approvals, notifications, and Platform-native actions.
- **SharePoint / Dataverse / Databricks** supply knowledge and analytical data through approved interfaces—not ad-hoc database credentials in the prompt.

### Why narrowly scoped permissions matter

Agents amplify whatever credentials they hold. Broad service accounts turn a prompt-injection or logic error into a data-exfiltration or unauthorized-write risk. Each tool should use least-privilege app registrations, table-level or API-scope limits, and separate identities for read vs write.

### Human approval

High-risk write operations (payments, master-data changes, irreversible deletes, externally visible communications) require human approval steps before execution.

Diagram: [Agentic workflow](../../architecture/agentic-workflow.md).

---

## 5. Integration Map

| System | Role in agentic flow |
|--------|----------------------|
| Copilot Studio | User experience and orchestration |
| Azure OpenAI | Reasoning / tool selection / grounded synthesis |
| Power Automate | Workflows, approvals, Platform connectors |
| REST APIs / MCP | Enterprise application actions |
| SharePoint | Unstructured knowledge |
| Dataverse | Operational entities |
| Databricks | Analytical / curated data access via governed APIs |
| SAP (where present) | Line-of-business reads/writes via integration layer only |

---

## 6. Security & Governance

- Tool allow-lists; no arbitrary code execution from the model
- Input validation and schema enforcement on every tool call
- Prompt-injection hardening: treat retrieved content and user text as untrusted for instruction override
- Identity propagation and RBAC on each backend
- Full logging of tool invocations (who, what tool, correlation ID, outcome)
- See [Project 06](../06-ai-security-governance/)

---

## 7. Business Value

- One entry point for knowledge, data, and actions
- Lower topic maintenance vs purely scripted bots
- Controlled expansion of automation with approval gates
- Clear audit story for regulated environments

---

## Representative Environments

Banking and insurance programs have used agentic workflows combining Copilot Studio, Azure AI/OpenAI, SharePoint, SAP integration layers, Databricks, Dataverse, MCP/API integrations, RAG, evaluation, and ALM—presented here only as sanitized patterns.
