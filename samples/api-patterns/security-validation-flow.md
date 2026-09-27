# Reference Implementation — Security Validation Flow

Sequence checked before an agent tool executes a write (or sensitive read).

```text
1. Authenticate caller (Entra ID token present and valid)
2. Resolve user identity and group membership
3. Authorize tool for this user/role (allow-list)
4. Validate tool arguments against schema (type, length, pattern)
5. Apply resource-level AuthZ (record ACL / RLS / API scope)
6. If write is high-risk → require human approval artifact
7. Execute with least-privilege identity (delegated or managed identity)
8. Log correlation ID, tool name, outcome (success/deny/error)
9. Return user-safe result (no secrets, no stack traces)
```

**Principle:** Deny by default when any step fails.
