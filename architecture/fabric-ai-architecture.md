# Microsoft Fabric + Copilot Architecture

**Sanitized Reference Architecture**

Medallion lakehouse and semantic models as the governed substrate for Power BI and AI.

```mermaid
flowchart LR
  subgraph Sources["Sources"]
    OPS["Operational Systems"]
    Files["Files / APIs"]
    Ext["External Feeds"]
  end

  subgraph Fabric["Microsoft Fabric"]
    Ing["Pipelines / Dataflows"]
    LH["Lakehouse"]
    B["Bronze"]
    S["Silver"]
    G["Gold"]
    SM["Semantic Model"]
  end

  subgraph Consumers["Consumers"]
    PBI["Power BI"]
    Copilot["Copilot / Downstream AI"]
  end

  subgraph Gov["Governance"]
    Purview["Microsoft Purview"]
    RLS["RLS / Workspace RBAC"]
  end

  OPS --> Ing
  Files --> Ing
  Ext --> Ing
  Ing --> LH
  LH --> B --> S --> G --> SM
  SM --> PBI
  SM --> Copilot
  Purview -.-> LH
  RLS -.-> SM
```

## Design notes

- AI should consume Gold / semantic-model outputs, not raw Bronze tables, whenever possible.
- Encode business logic and quality rules once in the lakehouse and model layers.
- Apply RLS so conversational access cannot exceed report-level entitlements.
