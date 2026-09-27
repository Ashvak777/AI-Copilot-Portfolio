# Reference Implementation — Power Automate Integration Pattern

## Intent

Copilot Studio collects slots → calls a cloud flow → flow validates, calls API, returns structured status.

```text
Trigger: When Power Virtual Agents / Copilot calls a flow
  → Initialize correlationId (GUID)
  → Scope: Validate inputs (category, summary length)
  → HTTP / Custom connector: POST /service-requests
       Authorization: Bearer @{token}
  → On success:
       Compose response JSON { id, status, message }
  → On failure:
       Log correlationId + statusCode
       Return user-safe error { status: "failed", message, correlationId }
  → Respond to Copilot
```

## Reliability

- Use retry policy on transient `408/429/5xx`.
- Keep approval actions for high-priority or externally visible creates.
- Bind connection references per environment; use environment variables for base URLs.
