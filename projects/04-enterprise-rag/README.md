# Project 04 — Enterprise RAG Architecture

**Sanitized Reference Architecture** · Financial-services style knowledge retrieval (generic)

---

## 1. Business Problem

Generative models alone are unsuitable for regulated Q&A: they lack current enterprise content, cannot prove sources, and may invent details. Enterprises need a retrieval-augmented pipeline that is measurable, authorization-aware, and operable at scale.

---

## 2. Solution

An end-to-end RAG architecture:

```text
Documents / enterprise data
  → Ingestion
  → Preprocessing
  → Chunking
  → Embeddings
  → Vector index
  → Retrieval (+ optional metadata filters)
  → Prompt / context construction
  → Azure OpenAI
  → Grounded answer + citations
  → Evaluation
```

---

## 3. Pipeline Detail

### Ingestion & preprocessing

- Pull from approved repositories (e.g., policy libraries, product guides—**sanitized financial-services examples only**).
- Normalize formats (PDF, DOCX, HTML); extract text; attach sensitivity labels.
- Drop or segregate content that fails classification or licensing checks.

### Chunking

- Choose chunk size/overlap by document type (policies vs FAQs vs tables).
- Preserve headings and section paths in metadata for better citations.
- Avoid chunks that mix unrelated products or jurisdictions.

### Embeddings & vector index

- Generate embeddings with an Azure OpenAI embedding model (or approved equivalent).
- Store vectors with metadata: `doc_id`, `source_uri`, `acl_group`, `product`, `region`, `effective_date`, `chunk_index`.

### Retrieval

- Semantic (vector) search for meaning; optional hybrid with keyword for identifiers (policy numbers, product codes).
- Metadata filtering before or after ANN search (product, region, language).
- Authorization-aware filtering so users only retrieve permitted chunks.
- Re-rank top-k for relevance; enforce minimum score thresholds.

### Prompt construction & grounding

- System instructions: answer only from supplied context; cite chunk IDs; refuse if insufficient.
- Include citation markers mapped to source URIs the user can open.
- Separate untrusted retrieved text from system policy (prompt-injection considerations).

### Evaluation

| Metric | Intent |
|--------|--------|
| Groundedness | Answer supported by retrieved context |
| Relevance | Answer addresses the user question |
| Completeness | Key facts covered when present in sources |
| Latency | p50 / p95 end-to-end response time |

Reference dataset sketch: [`samples/evaluation/`](../../samples/evaluation/).

---

## 4. Technical Considerations

| Topic | Practice |
|-------|----------|
| Chunk size | Tune empirically; oversize chunks dilute retrieval; undersize loses context |
| Relevance | Hybrid search + re-ranking + metadata |
| Hallucination controls | Thresholds, forced citations, refusal paths |
| Prompt injection | Never let retrieved content override system rules or tool policy |
| AuthZ-aware retrieval | Filter by Entra groups / document ACLs at query time |
| Freshness | Incremental re-index on document change events |

Pseudocode reference: [`samples/rag-patterns/retrieve_and_ground.py`](../../samples/rag-patterns/retrieve_and_ground.py).

Diagram: [RAG architecture](../../architecture/rag-architecture.md).

---

## 5. Security & Governance

- Index stores only approved corpora; separate indexes by sensitivity tier when required.
- Managed identities for index and model endpoints; Key Vault for any remaining secrets.
- Audit retrieval IDs with user identity for investigations.
- Purview labels influence what may enter the index.

---

## 6. Business Value

- Defensible, citation-backed answers for policy and product questions
- Measurable quality via evaluation datasets and release gates
- Reusable retrieval layer for Copilot Studio and other channels
