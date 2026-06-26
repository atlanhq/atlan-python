---
title: Trino assets app
description: Learn how to crawl Trino assets and publish them to Atlan for discovery.
---

# Trino assets app

The Trino assets app crawls Trino catalogs, schemas, tables, views, and columns and
publishes them to Atlan. Build it with the `AtlanTrino` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Trino supports two authentication methods: **basic** (username/password) and **JWT**.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Trino crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanTrino

    client = AtlanClient()

    response = (
        AtlanTrino(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            enable_tls_https=True, # (4)
            disable_ssl_verification=False, # (5)
            host="trino.example.com", # (6)
        )
        .connection(
            name="production-trino",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"my_catalog": ["public"]}) # (7)
        .run(name="trino-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** Enable TLS/HTTPS for the connection.
    5. **Required.** Whether to disable SSL certificate verification.
    6. **Required.** The Trino host. The port (`port=`) is optional.
    7. Catalogs/schemas to crawl, as `{catalog: [schema, ...]}`.

## JWT authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Trino crawling with a JWT"
    (
        AtlanTrino(client)
        .jwt(
            jwt_token="eyJ...", # (1)
            enable_tls_https=True, # (2)
            disable_ssl_verification=False, # (3)
            host="trino.example.com",
        )
        .connection(name="production-trino", admin_roles=[...])
        .run(name="trino-prod")
    )
    ```

    1. **Required.** The JWT token.
    2. **Required.** Enable TLS/HTTPS.
    3. **Required.** Whether to disable SSL verification. `port` is optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Trino metadata configuration"
    (
        AtlanTrino(client)
        .basic(username="atlan_user", password="••••••", enable_tls_https=True,
               disable_ssl_verification=False, host="...")
        .connection(name="production-trino", admin_roles=[...])
        .include_metadata({"my_catalog": ["public"]}) # (1)
        .exclude_metadata({"my_catalog": ["staging"]}) # (2)
        .run(name="trino-prod")
    )
    ```

    1. Catalogs/schemas to include, as `{catalog: [schema, ...]}`.
    2. Catalogs/schemas to exclude.
