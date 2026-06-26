---
title: Microsoft SQL Server assets app
description: Learn how to crawl Microsoft SQL Server assets and publish them to Atlan for discovery.
---

# Microsoft SQL Server assets app

The Microsoft SQL Server assets app crawls SQL Server databases, schemas, tables,
views, and columns and publishes them to Atlan. Build it with the `AtlanMssql`
builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

SQL Server supports three authentication methods: **basic** (SQL auth), **NTLM**
(Windows auth), and **Azure AD service principal**. The port is optional and
defaults to `1433`.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="SQL Server crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanMssql

    client = AtlanClient()

    response = (
        AtlanMssql(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            database="AdventureWorks", # (4)
            enable_ssl=True, # (5)
            host="sqlserver.example.com", # (6)
        )
        .connection(
            name="production-mssql",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"AdventureWorks": ["dbo", "sales"]}) # (7)
        .run(name="mssql-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** SQL Server authentication; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** Database to connect to.
    5. *Optional.* Encrypt the connection (TLS).
    6. *Optional.* Host. The port (`port=`) is optional and defaults to `1433`.
    7. Schemas to crawl, as `{database: [schema, ...]}`.

## NTLM (Windows) and Azure AD authentication

=== ":lang-python: Python"

    ```python linenums="1" title="NTLM and Azure AD service principal"
    # NTLM (Windows domain)
    AtlanMssql(client).ntlm(
        username="atlan_user", # (1)
        password="••••••",
        domain="CORP", # (2)
        database="AdventureWorks",
    )

    # Azure AD service principal
    AtlanMssql(client).azure_ad_sp(
        aad_principal_id="...", # (3)
        aad_principal_secret="...", # (4)
        tenant_id="...", # (5)
        database="AdventureWorks",
    )
    ```

    1. **Required.** Username (+ `password`).
    2. **Required.** The Windows domain.
    3. **Required.** Azure AD principal application id.
    4. **Required.** Azure AD principal secret.
    5. **Required.** Azure AD tenant id. `enable_ssl`, `host`, `port` are optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="SQL Server metadata configuration"
    (
        AtlanMssql(client)
        .basic(username="atlan_user", password="••••••", database="AdventureWorks", host="...")
        .connection(name="production-mssql", admin_roles=[...])
        .include_metadata({"AdventureWorks": ["dbo"]}) # (1)
        .exclude_metadata({"AdventureWorks": ["tmp"]}) # (2)
        .exclude_regex_for_tables_views(".*_tmp$") # (3)
        .agent_name("my-offline-agent") # (4)
        .run(name="mssql-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude.
    3. Regex of tables/views to ignore.
    4. Name of an offline agent installed on the same network as the database (for
       agent-based extraction).
