# Reference Implementation — Evaluation Scoring Rubric

| Metric | Score 1 | Score 3 | Score 5 |
|--------|---------|---------|---------|
| Groundedness | Unsupported claims | Mostly supported; minor gaps | Fully supported by retrieved context; citations correct |
| Relevance | Off-topic | Partially answers | Directly answers the asked question |
| Completeness | Missing key required facts | Covers main point; omits secondary detail | Covers all must-include facts present in sources |
| Latency | Fail SLA | Near SLA | Comfortably within p95 target |

**Release guidance:** Block promotion if groundedness or relevance mean score drops below the agreed threshold on the regression set, or if refusal cases incorrectly answer.
