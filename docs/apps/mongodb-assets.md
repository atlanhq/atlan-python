---
title: MongoDB assets app
description: Learn how to crawl MongoDB Atlas assets and publish them to Atlan for discovery.
---

# MongoDB assets app

The MongoDB assets app crawls MongoDB Atlas databases and collections and publishes
them to Atlan. Build it with the `MongodbAtlas` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="MongoDB crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import MongodbAtlas

    client = AtlanClient()

    response = (
        MongodbAtlas(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            native_host="demo-cluster.m1fmuci.mongodb.net", # (4)
            default_database="my_db", # (5)
            authsource="admin", # (6)
            ssl="true", # (7)
            host="atlas-sql-....a.query.mongodb.net", # (8)
        )
        .connection(
            name="production-mongodb",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_databases("analytics,sales") # (9)
        .run(name="mongodb-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** The MongoDB native host (the cluster host).
    5. **Required.** The default database.
    6. **Required.** The authentication database (e.g. `admin`).
    7. **Required.** Whether to use SSL (`"true"` / `"false"`).
    8. **Required.** The Atlas SQL host. The port (`port=`) is optional. Advanced:
       pass `connection_string=...` to override the individual fields.
    9. **Step 3 — Metadata.** Comma-separated database name patterns (regex).

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="MongoDB metadata configuration"
    (
        MongodbAtlas(client)
        .basic(username="atlan_user", password="••••••", native_host="...",
               default_database="my_db", authsource="admin", ssl="true", host="...")
        .connection(name="production-mongodb", admin_roles=[...])
        .include_databases("analytics,sales") # (1)
        .exclude_databases("tmp.*") # (2)
        .run(name="mongodb-prod")
    )
    ```

    1. Comma-separated database name patterns (regex) to include.
    2. Comma-separated database name patterns (regex) to exclude — wins over include.
