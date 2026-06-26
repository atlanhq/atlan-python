---
title: Anaplan assets app
description: Learn how to crawl Anaplan and publish to Atlan for discovery.
---

# Anaplan assets app

The Anaplan assets app crawls Anaplan assets and publishes to Atlan. Build it with the `Anaplan` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Anaplan assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import Anaplan

    client = AtlanClient()

    response = (
        Anaplan(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            host="...",  # (3)
        )
        .connection(  # (4)
            name="production-anaplan",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="anaplan-prod")  # (5)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Host.
    4. Display name + at least one admin (role, group, or user).
    5. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    Anaplan(client).ca_cert(username="...", password="...", ca_certificate="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        Anaplan(client)
        .basic(...)
        .connection(name="production-anaplan", admin_roles=[...])
        .exclude_empty_modules(True)  # (1)
        .exclude_metadata({...})  # (2)
        .include_metadata({...})  # (3)
        .ingest_system_dimensions('proxy')  # (4)
        .run(name="anaplan-prod")
    )
    ```

    1. Exclude Empty Modules — Exclude modules that have no line items.
    2. Exclude Metadata
    3. Include Metadata
    4. Ingest System Dimensions? — Ingest System Dimensions (Time and Versions) as a proxy, individually, or not at all.
