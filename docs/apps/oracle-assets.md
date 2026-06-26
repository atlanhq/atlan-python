---
title: Oracle assets app
description: Learn how to crawl Oracle assets and publish them to Atlan for discovery.
---

# Oracle assets app

The Oracle assets app crawls Oracle databases, schemas, tables, views, and columns
and publishes them to Atlan. Build it with the `OracleCrawler` builder, which
mirrors the "new app" wizard: **Credential → Connection → Metadata**.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Oracle crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import OracleCrawler

    client = AtlanClient()

    response = (
        OracleCrawler(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            sid="ORCL", # (4)
            database_name="ORCL", # (5)
            host="oracle.example.com", # (6)
        )
        .connection( # (7)
            name="production-oracle",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"ORCL": ["HR", "SALES"]}) # (8)
        .run(name="oracle-prod") # (9)
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** The Oracle SID or service name.
    5. **Required.** The default database name.
    6. **Required.** The Oracle host. The port (`port=`) is optional and defaults to
       `1521`.
    7. **Step 2 — Connection.** Display name + at least one admin.
    8. **Step 3 — Metadata.** Schemas to crawl, as `{database: [schema, ...]}`.
    9. `.run(name=...)` creates **and** submits a run.

    For TLS/wallet connections, also pass the optional `protocol="TCPS"`,
    `oracle_wallet=...`, and `wallet_password=...` arguments.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Oracle metadata configuration"
    (
        OracleCrawler(client)
        .basic(username="atlan_user", password="••••••", sid="ORCL", database_name="ORCL", host="...")
        .connection(name="production-oracle", admin_roles=[...])
        .include_metadata({"ORCL": ["HR"]}) # (1)
        .exclude_metadata({"ORCL": ["TEMP"]}) # (2)
        .exclude_regex_for_tables_views(".*_TMP$") # (3)
        .advanced_config("default") # (4)
        .run(name="oracle-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude — exclude takes precedence over include.
    3. Regex of tables/views to ignore.
    4. Controls experimental crawler features.
