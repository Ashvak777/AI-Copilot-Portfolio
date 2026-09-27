# Agentic Workflow Architecture

**Sanitized Reference Architecture**

Orchestrator decides among knowledge, structured data, APIs, workflows, specialist agents, or refusal—with human approval for high-risk writes.

```mermaid
flowchart TB
  User["User"] --> CS["Copilot Studio"]
  CS --> Orch["Orchestrator Agent\nAzure OpenAI tool calling"]

  Orch --> K["Knowledge Tool\nRAG / SharePoint"]
  Orch --> D["Data Tool\nDataverse / Databricks API"]
  Orch --> A["Action Tool\nREST / MCP"]
  Orch --> PA["Power Automate\nWorkflows"]
  Orch --> Spec["Specialist Agent"]
  Orch --> HITL{"High-risk write?"}

  HITL -->|Yes| Approver["Human Approval"]
  HITL -->|No| Exec["Execute Tool"]
  Approver -->|Approved| Exec
  Approver -->|Rejected| Deny["Return denial"]

  K --> Resp["Unified Response + Audit"]
  D --> Resp
  A --> Resp
  PA --> Resp
  Spec --> Resp
  Exec --> Resp
  Deny --> Resp
  Resp --> User
```

## Design notes

- Scope each tool identity to the minimum APIs and tables required.
- Log every tool invocation with user identity and correlation ID.
- Prefer MCP or curated OpenAPI connectors over ad-hoc credential use in prompts.
