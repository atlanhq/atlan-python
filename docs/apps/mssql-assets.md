---
title: Microsoft SQL Server assets app
description: Learn how to crawl Microsoft SQL Server and publish to Atlan for discovery.
---

# Microsoft SQL Server assets app

The Microsoft SQL Server assets app crawls Microsoft SQL Server assets and publishes to Atlan. Build it with the `AtlanMssql` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Azure Ad Sp authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Microsoft SQL Server assets crawling with azure_ad_sp auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanMssql

    client = AtlanClient()

    response = (
        AtlanMssql(client)
        .azure_ad_sp(
            aad_principal_id="...",  # (1)
            aad_principal_secret="...",  # (2)
            tenant_id="...",  # (3)
            database="...",  # (4)
            enable_ssl="...",  # (5)
            host="...",  # (6)
            port=0,  # (7)
        )
        .connection(  # (8)
            name="production-mssql",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="mssql-prod")  # (9)
    )
    print(response.slug, response.run_id)
    ```

    1. Azure AD Principal Application ID.
    2. Azure AD Principal Secret.
    3. Azure AD Tenant ID.
    4. Database.
    5. Encrypt Connection.
    6. Host.
    7. Port.
    8. Display name + at least one admin (role, group, or user).
    9. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanMssql(client).basic(username="...", password="...", database="...")
    AtlanMssql(client).ntlm(username="...", password="...", domain="...", database="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanMssql(client)
        .azure_ad_sp(...)
        .connection(name="production-mssql", admin_roles=[...])
        .agent_name("...")  # (1)
        .exclude_metadata({...})  # (2)
        .exclude_regex_for_tables_views("...")  # (3)
        .include_metadata({...})  # (4)
        .run(name="mssql-prod")
    )
    ```

    1. Agent Name — Name of the offline agent installed on the same network as the database.
    2. Exclude Metadata
    3. Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string.
    4. Include Metadata
