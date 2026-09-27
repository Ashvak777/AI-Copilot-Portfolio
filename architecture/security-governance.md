# Security & Governance Architecture

**Sanitized Reference Architecture**

Controls ensuring Copilot and agents do not exceed the authenticated user’s entitlements.

```mermaid
flowchart TB
  User["Authenticated User"] --> Entra["Microsoft Entra ID"]
  Entra --> CA["Conditional Access"]
  CA --> App["Copilot Studio / AI App"]

  App --> Policy["Policy Engine\nRBAC · Tool Allow-list · DLP"]
  Policy --> ReadTools["Read Tools\nLeast-privilege MI / OAuth"]
  Policy --> WriteTools["Write Tools\nSeparate identity + approval"]

  ReadTools --> Data["SharePoint · Dataverse · Fabric · APIs"]
  WriteTools --> HITL["Human Approval Gate"]
  HITL --> Data

  Data --> Purview["Purview Classification / Lineage"]
  App --> Audit["Audit Logging"]
  ReadTools --> Audit
  WriteTools --> Audit

  subgraph Envs["Environment Isolation"]
    Dev["Dev"]
    Test["Test"]
    UAT["UAT"]
    Prod["Prod"]
  end

  App -.-> Envs
```

## Principle

An AI agent should never provide access to information or operations that the authenticated user would not normally be authorized to access.
