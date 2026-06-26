---
title: MongoDB assets app
description: Learn how to crawl MongoDB and publish to Atlan for discovery.
---

# MongoDB assets app

The MongoDB assets app crawls MongoDB assets and publishes to Atlan. Build it with the `MongodbatlasAtlas` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="MongoDB assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import MongodbatlasAtlas

    client = AtlanClient()

    response = (
        MongodbatlasAtlas(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            native_host="...",  # (3)
            default_database="...",  # (4)
            authsource="...",  # (5)
            ssl="...",  # (6)
            connection_string="...",  # (7)
            host="...",  # (8)
            port=0,  # (9)
        )
        .connection(  # (10)
            name="production-mongodb",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="mongodb-prod")  # (11)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. MongoDB native host.
    4. Default database.
    5. Authentication database.
    6. SSL.
    7. Connection string (advanced — overrides above fields).
    8. Host.
    9. Port.
    10. Display name + at least one admin (role, group, or user).
    11. `.run()` creates and submits a run; use `.create()` to create without running.

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        MongodbatlasAtlas(client)
        .basic(...)
        .connection(name="production-mongodb", admin_roles=[...])
        .exclude_databases("...")  # (1)
        .include_databases("...")  # (2)
        .run(name="mongodb-prod")
    )
    ```

    1. Exclude Databases — Comma-separated database name patterns (regex). Wins over include.
    2. Include Databases — Comma-separated database name patterns (regex).
