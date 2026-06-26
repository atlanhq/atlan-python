---
title: Metabase assets app
description: Learn how to crawl Metabase assets and publish them to Atlan for discovery.
---

# Metabase assets app

The Metabase assets app crawls Metabase collections, dashboards, and questions and
publishes them to Atlan. Build it with the `AtlanMetabase` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Metabase crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanMetabase

    client = AtlanClient()

    response = (
        AtlanMetabase(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            host="metabase.example.com", # (4)
        )
        .connection(
            name="production-metabase",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_collections({"collection-id-1": {}}) # (5)
        .run(name="metabase-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. *Optional.* Host. The port (`port=`) is optional.
    5. **Step 3 — Metadata.** Collections to crawl (`{collection_id: {}}`). Omit to
       crawl all collections.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Metabase metadata configuration"
    (
        AtlanMetabase(client)
        .basic(username="atlan_user", password="••••••", host="metabase.example.com")
        .connection(name="production-metabase", admin_roles=[...])
        .include_collections({"collection-id-1": {}}) # (1)
        .exclude_collections({"collection-id-2": {}}) # (2)
        .run(name="metabase-prod")
    )
    ```

    1. Collections to include (`{collection_id: {}}`).
    2. Collections to exclude.
