---
title: Metabase assets app
description: Learn how to crawl Metabase and publish to Atlan for discovery.
---

# Metabase assets app

The Metabase assets app crawls Metabase assets and publishes to Atlan. Build it with the `AtlanMetabase` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Metabase assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanMetabase

    client = AtlanClient()

    response = (
        AtlanMetabase(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            host="...",  # (3)
            port=0,  # (4)
        )
        .connection(  # (5)
            name="production-metabase",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="metabase-prod")  # (6)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Host.
    4. Port.
    5. Display name + at least one admin (role, group, or user).
    6. `.run()` creates and submits a run; use `.create()` to create without running.

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanMetabase(client)
        .basic(...)
        .connection(name="production-metabase", admin_roles=[...])
        .exclude_collections({...})  # (1)
        .include_collections({...})  # (2)
        .run(name="metabase-prod")
    )
    ```

    1. Exclude collections
    2. Include collections
