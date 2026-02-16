## SDK Compatibility

This repository depends on `atlanhq/application-sdk`. When reviewing changes, consider:

- **SDK API usage**: pyatlan uses SDK base classes and services. Any change to how
  these are called or extended must match the SDK's current API surface.
- **Version compatibility**: When the SDK dependency version changes, verify that
  pyatlan's usage is compatible with the new version's interfaces.
- **Behavioral assumptions**: Changes that rely on specific SDK behavior (e.g.,
  ObjectStore path normalization, Dapr service defaults, Temporal workflow semantics)
  should be validated against the SDK's documented or tested behavior.

## Key Integration Points

- `pyatlan.client` — SDK client wrappers and API interactions
- `pyatlan.model` — Data models that may extend or interact with SDK types
- `pyatlan.events` — Event handling that integrates with SDK EventStore
- `pyatlan.cache` — Caching layer that may use SDK StateStore
