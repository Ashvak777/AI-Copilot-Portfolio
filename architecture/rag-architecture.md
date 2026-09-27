# Enterprise RAG Architecture

**Sanitized Reference Architecture**

End-to-end retrieval-augmented generation for regulated knowledge Q&A.

```mermaid
flowchart TB
  subgraph Ingest["Ingestion"]
    Src["Documents / Enterprise Data"]
    Prep["Preprocess / Classify"]
    Chunk["Chunk + Metadata"]
    Emb["Generate Embeddings"]
    Idx["Vector Index"]
  end

  subgraph Query["Query Time"]
    UQ["User Question"]
    Auth["Entra ID + AuthZ Filter"]
    QEmb["Embed Query"]
    Ret["Semantic / Hybrid Retrieve"]
    MF["Metadata Filter"]
    Ctx["Prompt + Context Assembly"]
    LLM["Azure OpenAI"]
    Ans["Grounded Answer + Citations"]
  end

  subgraph Eval["Evaluation"]
    G["Groundedness"]
    R["Relevance"]
    C["Completeness"]
    L["Latency"]
  end

  Src --> Prep --> Chunk --> Emb --> Idx
  UQ --> Auth --> QEmb --> Ret
  Idx --> Ret
  Ret --> MF --> Ctx --> LLM --> Ans
  Ans --> G
  Ans --> R
  Ans --> C
  Ans --> L
```

## Design notes

- Prefer authorization-aware retrieval before generation.
- Keep system instructions separate from retrieved text to reduce prompt-injection risk.
- Use evaluation gates before promoting index or prompt changes to production.
