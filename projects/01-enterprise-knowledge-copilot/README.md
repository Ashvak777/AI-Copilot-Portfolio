# Project 01 — Enterprise Knowledge Copilot

**Sanitized Reference Architecture** · Internal knowledge assistant with grounded answers and citations

---

## 1. Business Problem

Employees in regulated organizations spend significant time searching SharePoint libraries, policy portals, and approved knowledge bases. Answers are inconsistent, hard to verify, and often bypass access controls when content is copied into informal channels.

The organization needed a conversational assistant that:

- Answers from approved enterprise knowledge only
- Respects the user’s existing entitlements
- Returns citations so answers can be verified
- Reduces unsupported or fabricated statements

---

## 2. Solution

An **Enterprise Knowledge Copilot** built with Microsoft Copilot Studio, backed by a RAG pipeline on Azure AI / Azure OpenAI and enterprise content sources (SharePoint, approved document stores, Dataverse knowledge where applicable).

```text
Employee
  → Copilot Studio (Entra ID auth)
  → Orchestration / grounding instructions
  → RAG retrieval (vector + optional keyword/metadata)
  → Azure OpenAI (grounded generation)
  → Response with citations
```

---

## 3. What the Agent Does

| Capability | Behavior |
|------------|----------|
| Policy / procedure Q&A | Retrieves relevant chunks and summarizes with citations |
| Document discovery | Points users to source locations they are entitled to open |
| Clarifying questions | Asks for product, region, or document type when ambiguous |
| Refusal | Declines when no grounded source is found or access is denied |
| Escalation | Routes to human support for sensitive or out-of-scope topics |

---

## 4. Technical Architecture

### Ingestion

1. Approved content is registered (SharePoint libraries, curated document sets, selected Dataverse records).
2. Documents are preprocessed (format normalization, OCR where required, PII/sensitivity tagging).
3. Content is chunked with overlap tuned for policy-style documents (often smaller chunks for precise citations).
4. Embeddings are generated and stored in a vector index with metadata (source, ACL hints, department, doc type, effective date).

### Retrieval & Generation

1. User query is authenticated via Microsoft Entra ID.
2. Query embedding + optional filters (metadata, security trimming) drive semantic retrieval.
3. Top-k chunks are re-ranked for relevance.
4. Prompt construction injects retrieved context, citation IDs, and strict grounding rules.
5. Azure OpenAI produces an answer that must reference retrieved sources; empty retrieval yields a controlled “no source” response.

See also: [Enterprise Copilot architecture](../../architecture/enterprise-copilot-architecture.md) and [Enterprise RAG](../../architecture/rag-architecture.md).

---

## 5. Integration

| Component | Role |
|-----------|------|
| Copilot Studio | Conversational UX, topics, orchestration |
| SharePoint | Primary document knowledge source |
| Dataverse | Structured knowledge / configuration where used |
| Azure OpenAI | Embeddings and grounded completion |
| Vector index | Semantic retrieval store |
| Entra ID | Authentication and group-based access |

---

## 6. Security & Governance

- Authenticate every session with Entra ID; no anonymous enterprise knowledge access.
- Apply authorization-aware retrieval: filter chunks by what the user (or their groups) may see.
- Prefer user-delegated access to source systems over “god” service accounts where feasible.
- Use managed identity for Azure resources; store secrets in Key Vault.
- Log queries and retrieval IDs for audit (content of answers may be retention-controlled).
- Align classification with Microsoft Purview labels where available.
- Prompt instructions forbid inventing citations or answering outside retrieved context.

---

## 7. Hallucination Reduction

- Grounding-first prompts and “answer only from context” rules
- Mandatory citations when content is used
- Thresholds on retrieval score; refuse below threshold
- Evaluation of groundedness / relevance before major releases
- Periodic content freshness and ACL sync checks

---

## 8. Business Value

- Faster access to approved procedures and policies
- Consistent answers tied to verifiable sources
- Reduced risk of informal, uncontrolled knowledge sharing
- Foundation for later agentic actions (see Projects 02–03) on the same identity and content model

---

## Representative Environments

Patterns of this type have been delivered in regulatory/insurance and banking contexts using Copilot Studio, Azure AI/OpenAI, SharePoint, Dataverse, RAG, embeddings, vector search, prompt engineering, RBAC, Purview, and AI evaluation—without exposing client-specific content models here.
