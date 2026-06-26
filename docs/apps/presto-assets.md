---
title: Presto assets app
description: Learn how to crawl Presto assets and publish them to Atlan for discovery.
---

# Presto assets app

The Presto assets app crawls Presto catalogs, schemas, tables, views, and columns
and publishes them to Atlan. Build it with the `AtlanPresto` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Presto crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanPresto

    client = AtlanClient()

    response = (
        AtlanPresto(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            host="presto.example.com", # (4)
        )
        .connection(
            name="production-presto",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"my_catalog": ["public"]}) # (5)
        .run(name="presto-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** The Presto host. The port (`port=`) is optional.
    5. Catalogs/schemas to crawl, as `{catalog: [schema, ...]}`.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Presto metadata configuration"
    (
        AtlanPresto(client)
        .basic(username="atlan_user", password="••••••", host="...")
        .connection(name="production-presto", admin_roles=[...])
        .include_metadata({"my_catalog": ["public"]}) # (1)
        .exclude_metadata({"my_catalog": ["staging"]}) # (2)
        .run(name="presto-prod")
    )
    ```

    1. Catalogs/schemas to include in extraction, as `{catalog: [schema, ...]}`.
    2. Catalogs/schemas to exclude from extraction.
