---
title: Power BI assets app
description: Learn how to crawl Power BI and publish to Atlan for discovery.
---

# Power BI assets app

The Power BI assets app crawls Power BI assets and publishes to Atlan. Build it with the `PowerbiCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Power BI assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PowerbiCrawler

    client = AtlanClient()

    response = (
        PowerbiCrawler(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            tenant_id="...",  # (3)
            client_id="...",  # (4)
            client_secret="...",  # (5)
            host="...",  # (6)
            port=0,  # (7)
        )
        .connection(  # (8)
            name="production-powerbi",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="powerbi-prod")  # (9)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Tenant ID.
    4. Client ID.
    5. Client Secret.
    6. Host.
    7. Port.
    8. Display name + at least one admin (role, group, or user).
    9. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    PowerbiCrawler(client).service_principal(tenant_id="...", client_id="...", client_secret="...", admin_api="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        PowerbiCrawler(client)
        .basic(...)
        .connection(name="production-powerbi", admin_roles=[...])
        .attach_endorsements_from_power_bi('metastore')  # (1)
        .enable_incremental_extraction(True)  # (2)
        .enable_odbc_dsn_connectivity_mapping('true')  # (3)
        .exclude_dashboard_and_reports_regex("...")  # (4)
        .exclude_workspaces({...})  # (5)
        .fetch_report_definition_extracts(True)  # (6)
        .include_dashboard_and_reports_regex("...")  # (7)
        .include_workspaces({...})  # (8)
        .odbc_dsn_config_mapping({...})  # (9)
        .sql_connection_info_note("...")  # (10)
        .run(name="powerbi-prod")
    )
    ```

    1. Attach Endorsements from Power BI — The workflow automatically certifies the assets endorsed in Power BI
    2. Enable Incremental Extraction — Enable or Disable Incremental Extraction on Source.
    3. Enable ODBC DSN Connectivity Mapping
    4. Exclude Dashboard and Reports Regex — Dashboards and Reports that match the regex will be excluded. Defaults to empty string.
    5. Exclude Workspaces — Selected workspaces will not be processed.
    6. Fetch Report Definition Extracts — Whether to fetch Power BI report definition extracts
    7. Include Dashboard and Reports Regex — Dashboards and Reports that match the regex will be included. Defaults to empty string.
    8. Include Workspaces — Selected workspaces will be processed.
    9. odbc_dsn_config_mapping
    10. sql_connection_info_note
