---
title: Oracle assets app
description: Learn how to crawl Oracle and publish to Atlan for discovery.
---

# Oracle assets app

The Oracle assets app crawls Oracle assets and publishes to Atlan. Build it with the `OracleCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Oracle assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import OracleCrawler

    client = AtlanClient()

    response = (
        OracleCrawler(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            sid="...",  # (3)
            database_name="...",  # (4)
            protocol="...",  # (5)
            oracle_wallet="...",  # (6)
            wallet_password="...",  # (7)
            host="...",  # (8)
            port=0,  # (9)
        )
        .connection(  # (10)
            name="production-oracle",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="oracle-prod")  # (11)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. SID / Service Name.
    4. Default Database Name.
    5. Protocol.
    6. Oracle wallet.
    7. Wallet password.
    8. Host.
    9. Port.
    10. Display name + at least one admin (role, group, or user).
    11. `.run()` creates and submits a run; use `.create()` to create without running.

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        OracleCrawler(client)
        .basic(...)
        .connection(name="production-oracle", admin_roles=[...])
        .advanced_config('default')  # (1)
        .exclude_metadata({...})  # (2)
        .exclude_regex_for_tables_views("...")  # (3)
        .include_metadata({...})  # (4)
        .run(name="oracle-prod")
    )
    ```

    1. Advanced Config — Controls custom experimental features for the crawler.
    2. Exclude Metadata — Selected databases and schemas won't be extracted.
    3. Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string.
    4. Include Metadata — Only the selected databases and schemas will be extracted. Exclude takes precedence over include for shared databases/schemas.
