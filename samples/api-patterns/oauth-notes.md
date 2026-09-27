# Reference Implementation — OAuth 2.0 Notes for Agents

## Preferred patterns

| Pattern | When |
|---------|------|
| Delegated (authorization code / OBO) | Action should run as the signed-in user |
| Application permissions + managed identity | Backend-to-backend with no user context; still enforce AuthZ in the API |
| Separate app registrations | Split read vs write and Prod vs non-Prod |

## Practices

- Request minimum scopes (`service_requests.read` vs `.write`).
- Store client secrets in Key Vault or pipeline secret stores—never in Copilot topics or source control.
- Rotate credentials on a schedule; prefer certificate or federated credentials where possible.
- Validate audience and issuer on every API call.
