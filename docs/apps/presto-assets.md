---
title: Presto assets app
description: Learn how to crawl Presto and publish to Atlan for discovery.
---

# Presto assets app

The Presto assets app crawls Presto assets and publishes to Atlan. Build it with the `AtlanPresto` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Presto assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanPresto

    client = AtlanClient()

    response = (
        AtlanPresto(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            host="...",  # (3)
            port=0,  # (4)
        )
        .connection(  # (5)
            name="production-presto",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="presto-prod")  # (6)
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
        AtlanPresto(client)
        .basic(...)
        .connection(name="production-presto", admin_roles=[...])
        .exclude_metadata({...})  # (1)
        .include_metadata({...})  # (2)
        .run(name="presto-prod")
    )
    ```

    1. Exclude Metadata — Select the catalogs and schemas to exclude from extraction.
    2. Include Metadata — Select the catalogs and schemas to include in extraction.
