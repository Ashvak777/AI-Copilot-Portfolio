# Project 05 — Copilot + Microsoft Fabric

**Sanitized Reference Architecture** · Governed data layer for analytics and AI

---

## 1. Business Problem

AI and Copilot experiences that query raw operational tables inherit inconsistent definitions, poor data quality, and unclear ownership. Business users then receive conflicting numbers from chat, reports, and spreadsheets.

The organization needed a **governed analytics foundation** so Copilot and Power BI consume the same curated business data.

---

## 2. Solution

Microsoft Fabric as the enterprise data layer:

```text
Sources
  → Fabric ingestion (pipelines / Dataflows / ADF patterns)
  → Lakehouse
      → Bronze (raw)
      → Silver (cleansed / conformed)
      → Gold (business-ready)
  → Semantic model
  → Power BI / Copilot / downstream AI
```

---

## 3. What This Enables

| Consumer | Consumes |
|----------|----------|
| Power BI | Semantic models on Gold |
| Copilot experiences | Curated metrics and descriptions aligned to the model |
| Downstream AI | APIs or datasets built from Gold—not ad-hoc raw extracts |
| Operations | Pipelines, data quality checks, lineage |

---

## 4. Technical Architecture

### Medallion layers

| Layer | Purpose |
|-------|---------|
| Bronze | Land source data with minimal transformation; preserve lineage |
| Silver | Cleanse, deduplicate, conform keys and reference data |
| Gold | Business entities and metrics ready for reporting and AI |

### Platform components

- **Fabric Lakehouse** — unified storage and SQL analytics endpoint
- **Dataflows / pipelines** — ingestion and transformation
- **Azure Data Factory** — hybrid or complex orchestration where used alongside Fabric
- **Databricks** — advanced transforms or ML feature prep when part of the estate
- **Semantic models** — measures, relationships, RLS roles
- **Power BI** — visualization and governed self-service
- **SQL / Python** — transformation and quality logic

Diagram: [Fabric + AI architecture](../../architecture/fabric-ai-architecture.md).

---

## 5. Why AI Should Prefer Curated Data

Raw tables often contain:

- Multiple conflicting definitions of “customer,” “balance,” or “claim”
- Incomplete history and late-arriving facts
- Columns not approved for broad consumption
- No RLS or unclear sensitivity

Gold layers and semantic models encode **business logic and data quality rules** once. Copilot and other AI consumers then reason over trusted metrics instead of inventing joins across operational schemas.

---

## 6. Security & Governance

- Workspace and item-level permissions in Fabric
- RLS in semantic models for row-scoped access
- Classification and lineage via Microsoft Purview where integrated
- Separate workspaces / capacities for Dev / Test / Prod
- Document which entities are AI-approved for grounding

---

## 7. Business Value

- One governed definition of metrics across BI and AI
- Faster, safer enablement of Copilot on enterprise data
- Clear ownership and quality gates before AI consumption
- Reduced reconciliation between “chat answers” and official reports
