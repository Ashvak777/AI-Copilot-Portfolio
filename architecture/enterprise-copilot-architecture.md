# Enterprise Copilot Architecture

**Sanitized Reference Architecture**

Employee-facing knowledge assistant: Copilot Studio orchestration with RAG grounding on Azure OpenAI and enterprise content sources.

```mermaid
flowchart LR
  subgraph Identity["Identity"]
    Entra["Microsoft Entra ID"]
  end

  subgraph Channel["Experience"]
    User["Employee"]
    CS["Copilot Studio"]
  end

  subgraph Orchestration["Orchestration"]
    Topics["Topics / Generative Orchestration"]
    Ground["Grounding Instructions"]
  end

  subgraph RAG["Retrieval"]
    EmbedQ["Query Embedding"]
    Vec["Vector Index"]
    Meta["Metadata / ACL Filter"]
    Rerank["Re-rank Top-k"]
  end

  subgraph Models["Azure AI"]
    AOAI["Azure OpenAI"]
  end

  subgraph Sources["Enterprise Knowledge"]
    SP["SharePoint"]
    DV["Dataverse"]
    Docs["Approved Documents"]
  end

  User --> Entra
  Entra --> CS
  CS --> Topics
  Topics --> Ground
  Ground --> EmbedQ
  EmbedQ --> Vec
  Vec --> Meta
  Meta --> Rerank
  SP --> Vec
  DV --> Vec
  Docs --> Vec
  Rerank --> AOAI
  Ground --> AOAI
  AOAI --> CS
  CS --> User
```

## Information flow

1. User authenticates with Entra ID and opens Copilot Studio.
2. Orchestration applies grounding rules and builds a retrieval query.
3. Vector search returns candidates; ACL/metadata filters enforce authorization.
4. Azure OpenAI generates an answer constrained to retrieved context.
5. Response returns to the user with citations to permitted sources.
