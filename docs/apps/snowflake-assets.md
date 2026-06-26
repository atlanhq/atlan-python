---
title: Snowflake assets app
description: Learn how to crawl Snowflake and publish to Atlan for discovery.
---

# Snowflake assets app

The Snowflake assets app crawls Snowflake assets and publishes to Atlan. Build it with the `SnowflakeCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Snowflake assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import SnowflakeCrawler

    client = AtlanClient()

    response = (
        SnowflakeCrawler(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            role="...",  # (3)
            warehouse="...",  # (4)
            host="...",  # (5)
            port=0,  # (6)
        )
        .connection(  # (7)
            name="production-snowflake",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="snowflake-prod")  # (8)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Role.
    4. Warehouse.
    5. Host.
    6. Port.
    7. Display name + at least one admin (role, group, or user).
    8. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    SnowflakeCrawler(client).entra_id(username="...", password="...", tenant_id="...", oauth_scope="...")
    SnowflakeCrawler(client).keypair(username="...", password="...")
    SnowflakeCrawler(client).okta(username="...", password="...", authenticator="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        SnowflakeCrawler(client)
        .basic(...)
        .connection(name="production-snowflake", admin_roles=[...])
        .asset_selection({...})  # (1)
        .control_config('default')  # (2)
        .custom_config("...")  # (3)
        .database_name("...")  # (4)
        .enable_incremental_extraction(True)  # (5)
        .exclude_metadata({...})  # (6)
        .exclude_regex_for_tables_views("...")  # (7)
        .exclude_tables_with_empty_data(True)  # (8)
        .exclude_views(True)  # (9)
        .extraction_method('information-schema')  # (10)
        .import_semantic_views(True)  # (11)
        .import_stages(True)  # (12)
        .import_tags(True)  # (13)
        .include_metadata({...})  # (14)
        .preflight_check("...")  # (15)
        .schema_name("...")  # (16)
        .view_definition_lineage(True)  # (17)
        .run(name="snowflake-prod")
    )
    ```

    1. Asset selection — Select the assets you want to crawl, or filter out the ones you don't.
    2. Control Config — Controls custom experimental feature flags for the crawler
    3. Custom Config — Custom JSON config controlling experimental feature flags for the crawler
    4. Database Name — Database name to extract account usage data from. Defaults to SNOWFLAKE
    5. Enable Incremental Extraction — Enable or Disable Schema Incremental Extraction on source.
    6. Exclude Metadata — Selected databases and schemas wont be extracted.
    7. Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string
    8. Exclude tables with empty data — Excludes tables and their corresponding columns when the table contains no data.
    9. Exclude views — Excludes all views
    10. Extraction method — Determines the method the package will use to extract metadata from Snowflake. Please refer to the docs [here](https://docs.atlan.com/apps/connectors/data-warehouses/snowflake/how-tos/set-up-snowflake#choose-metadata-fetching-method).
    11. Import Semantic Views — Import semantic views, logical tables, dimensions, metrics and facts from snowflake to atlan
    12. Import Stages — Import internal and external named stages from snowflake to atlan
    13. Import Tags — Syncing tags from snowflake to atlan
    14. Include Metadata — Only the selected databases will be extracted. Exclude gets preference over include for common databases, if present, in the config.
    15. preflight_check
    16. Schema Name — Schema name to extract account usage data from. Defaults to ACCOUNT_USAGE
    17. View Definition Lineage — Enable view definition lineage while crawling
