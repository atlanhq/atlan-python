## Security

> Follow these security guidelines for every change to the pyatlan SDK.

### Contact

- **Security Team:** #bu-security-and-it on Slack

### Quickstart for Agents

pyatlan is Atlan's Python SDK. It wraps the Atlan REST API using `httpx`, handles API key auth, and provides typed models for all Atlan entities. Review every change for:

- **API key logging** — the `api_key` (and impersonation tokens from `ImpersonationClient`) must never appear in log output or error messages; log only the `base_url` and response status codes.
- **`verify=False` in httpx transport** — TLS certificate verification must not be disabled; `trust_env=True` is correct for proxy support.
- **Proxy credential leakage** — if proxy credentials are configured via environment variables (`HTTPS_PROXY`), they must not be echoed in log output.
- **User-supplied URL validation** — `base_url` must be validated as HTTPS before constructing the client.

### Security Invariants

- **[MUST]** `api_key` and impersonation tokens must never appear in log output.
- **[MUST]** TLS certificate verification must not be disabled (`verify=False` is forbidden).
- **[MUST]** `base_url` must be validated as HTTPS.

### Review Checklist

- [ ] `api_key` and impersonation tokens absent from all log output and error messages
- [ ] `verify=False` not used in any httpx transport or session
- [ ] `base_url` validated as HTTPS before client construction
- [ ] All direct dependencies in `pyproject.toml` pinned exactly
