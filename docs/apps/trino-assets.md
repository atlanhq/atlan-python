---
title: Trino assets app
description: Learn how to crawl Trino and publish to Atlan for discovery.
---

# Trino assets app

The Trino assets app crawls Trino assets and publishes to Atlan. Build it with the `AtlanTrino` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Trino assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanTrino

    client = AtlanClient()

    response = (
        AtlanTrino(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            enable_tls_https="...",  # (3)
            disable_ssl_verification="...",  # (4)
            host="...",  # (5)
            port=0,  # (6)
        )
        .connection(  # (7)
            name="production-trino",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="trino-prod")  # (8)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Enable TLS/HTTPS.
    4. Disable SSL verification.
    5. Host.
    6. Port.
    7. Display name + at least one admin (role, group, or user).
    8. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanTrino(client).jwt(jwt_token="...", enable_tls_https="...", disable_ssl_verification="...", host="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanTrino(client)
        .basic(...)
        .connection(name="production-trino", admin_roles=[...])
        .exclude_metadata({...})  # (1)
        .include_metadata({...})  # (2)
        .run(name="trino-prod")
    )
    ```

    1. Exclude Metadata
    2. Include Metadata
