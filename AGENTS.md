## Security

> Follow these security guidelines for every change to the pyatlan SDK.

### Contact

- **Security Team:** #bu-security-and-it on Slack

### Quickstart for Agents

atlan-python (pyatlan) is Atlan's Python SDK, providing typed wrappers around the Atlan REST API. Key modules:

- `pyatlan/client/atlan.py` — `AtlanClient` (Pydantic `BaseSettings`); initialised with `base_url` and `api_key`; uses `httpx` with `PyatlanSyncTransport` / async variant; supports impersonation via `ImpersonationClient`.
- `pyatlan/client/transport.py` — `PyatlanSyncTransport` and async variant wrap `httpx.HTTPTransport` with retry logic; `trust_env=True` by default to respect `HTTPS_PROXY` env.
- `pyatlan/client/credential.py` — manages credential objects (Vault-stored secrets).
- `pyatlan/client/token.py` — manages API tokens (long-lived service account keys).
- `pyatlan/cache/` — caches for tags, groups, roles, custom metadata.

Review every change for:

- **API key logging** — `AtlanClient` holds `api_key` (set as `Authorization: Bearer <key>` on every request); it must never appear in log output, error messages, or exception tracebacks; wrap all `httpx` error handling to strip `Authorization` from logged request details; the `api_key` field must be excluded from any Pydantic model `dict()` / `model_dump()` used for logging.
- **Impersonation token safety** — `ImpersonationClient` generates short-lived impersonation JWTs; these tokens must not be logged; the target user's identity (email/username) may be logged but not the token value.
- **TLS verification** — `PyatlanSyncTransport` must never pass `verify=False` to `httpx.HTTPTransport`; if users need to use custom CA bundles, accept a path to the bundle, not a `False` flag.
- **`base_url` validation** — `base_url` is validated as `HttpUrl` via Pydantic; ensure validation rejects non-HTTPS URLs in production builds (the `HttpUrl` type allows HTTP by default — add a validator if HTTPS is required).
- **Proxy credential exposure** — `trust_env=True` means `HTTPS_PROXY` is honoured; proxy credentials embedded in the URL (e.g., `http://user:pass@proxy`) must not be echoed in log output; strip credentials from proxy URLs before logging.
- **Credential object sensitivity** — `CredentialClient` returns objects with `username` and potentially `password` fields; these must not be logged; use repr/str exclusion for credential model classes.

### Security Invariants

- **[MUST]** `api_key` must never appear in log output, error messages, or exception tracebacks.
- **[MUST]** Impersonation JWT values must not be logged.
- **[MUST]** `verify=False` must not be used in any httpx transport.
- **[MUST]** `base_url` must be validated as HTTPS.
- **[MUST]** All direct dependency versions in `pyproject.toml` pinned exactly.

### Data Classification

- **CONFIDENTIAL:** `api_key`, impersonation tokens, credential object passwords, service account secrets
- **INTERNAL:** `base_url`, user email addresses, workspace IDs, asset GUIDs
- **PUBLIC:** SDK version, API endpoint names, asset type names

### Review Checklist

- [ ] `api_key` absent from all log output and exception messages; `Authorization` header stripped from error logs
- [ ] Impersonation JWT token values absent from all log output
- [ ] `verify=False` not present in any `httpx.HTTPTransport` or client config
- [ ] `base_url` validated as HTTPS (not just HTTP-or-HTTPS via Pydantic `HttpUrl`)
- [ ] Proxy URLs stripped of credentials before logging
- [ ] `CredentialClient` response objects not logged with `password` field
- [ ] All direct dependencies in `pyproject.toml` pinned exactly
