---
title: Snowflake assets app
description: Learn how to crawl Snowflake assets and publish them to Atlan for discovery.
---

# Snowflake assets app

The Snowflake assets app crawls Snowflake databases, schemas, tables, views,
columns (and optionally tags and stages) and publishes them to Atlan for
discovery. Build it with the `SnowflakeCrawler` builder, which mirrors the
"new app" wizard: **Credential → Connection → Metadata**.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets within it — running it
    repeatedly with the same settings can produce duplicate assets. To re-crawl,
    re-run the **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Snowflake supports four authentication methods: **basic**, **key-pair**,
**Okta SSO**, and **Microsoft Entra ID**. All four accept an optional `role` and
`warehouse` (the role/warehouse Atlan uses to run extraction queries) and default
the port to `443`.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To crawl Snowflake with a username and password:

=== ":lang-python: Python"

    ```python linenums="1" title="Snowflake crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import SnowflakeCrawler

    client = AtlanClient()

    response = (
        SnowflakeCrawler(client)
        .basic( # (1)
            username="ATLAN_USER", # (2)
            password="••••••", # (3)
            role="ATLAN_ROLE", # (4)
            warehouse="COMPUTE_WH", # (5)
            host="abc12345.snowflakecomputing.com", # (6)
        )
        .connection( # (7)
            name="production-snowflake",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .extraction_method("account-usage") # (8)
        .include_metadata({"ANALYTICS": ["PUBLIC", "SALES"]}) # (9)
        .run(name="snowflake-prod") # (10)
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted and
       never persisted in the workflow.
    2. **Required.** The Snowflake username.
    3. **Required.** The password.
    4. *Optional.* The role Atlan assumes when extracting (e.g. a read-only role).
    5. *Optional.* The warehouse used to run extraction queries.
    6. *Optional.* Your Snowflake account host. The port (`port=`) is optional and
       defaults to `443`.
    7. **Step 2 — Connection.** Display name + at least one admin (role, group, or
       user). The builder mints the connection qualified name.
    8. **Step 3 — Metadata.** `account-usage` queries Snowflake's `ACCOUNT_USAGE`
       views (fast, recommended); `information-schema` queries each database's
       information schema directly.
    9. Databases/schemas to crawl, as `{database: [schema, ...]}`. Omit to crawl
       everything. Exclude takes priority over include.
    10. `.run(name=...)` creates **and** submits a run; use `.create(name=...)` to
        create without running.

## Key-pair authentication

To authenticate with an encrypted private key instead of a password:

=== ":lang-python: Python"

    ```python linenums="1" title="Snowflake crawling with key-pair auth"
    (
        SnowflakeCrawler(client)
        .keypair(
            username="ATLAN_USER", # (1)
            password=encrypted_private_key, # (2)
            private_key_password="••••••", # (3)
            role="ATLAN_ROLE", # (4)
            warehouse="COMPUTE_WH",
            host="abc12345.snowflakecomputing.com",
        )
        .connection(name="production-snowflake", admin_roles=[...])
        .run(name="snowflake-prod")
    )
    ```

    1. **Required.** The Snowflake username.
    2. **Required.** The encrypted private key (PEM contents), passed as `password`.
    3. *Optional.* The passphrase for the encrypted private key.
    4. *Optional.* `role`, `warehouse`, `host`, and `port` behave as in basic auth.

## Okta SSO authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Snowflake crawling with Okta SSO"
    (
        SnowflakeCrawler(client)
        .okta(
            username="ATLAN_USER", # (1)
            password="••••••", # (2)
            authenticator="https://my-org.okta.com", # (3)
            role="ATLAN_ROLE",
            warehouse="COMPUTE_WH",
            host="abc12345.snowflakecomputing.com",
        )
        .connection(name="production-snowflake", admin_roles=[...])
        .run(name="snowflake-prod")
    )
    ```

    1. **Required.** The Snowflake username.
    2. **Required.** The password.
    3. **Required.** The Okta authenticator URL for your organization.
       `role` / `warehouse` / `host` / `port` are optional (as in basic auth).

## Microsoft Entra ID authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Snowflake crawling with Microsoft Entra ID"
    (
        SnowflakeCrawler(client)
        .entra_id(
            username=client_id, # (1)
            password=client_secret, # (2)
            tenant_id="...", # (3)
            oauth_scope="session:role:ATLAN_ROLE", # (4)
            warehouse="COMPUTE_WH",
            host="abc12345.snowflakecomputing.com",
        )
        .connection(name="production-snowflake", admin_roles=[...])
        .run(name="snowflake-prod")
    )
    ```

    1. **Required.** The Entra ID application **Client ID**, passed as `username`.
    2. **Required.** The application **Client Secret**, passed as `password`.
    3. **Required.** Your Entra ID tenant id.
    4. **Required.** The OAuth scope to request. `role` / `warehouse` / `host` /
       `port` are optional (as in basic auth).

## Configuration options

Every wizard metadata toggle is available on the builder. All of these are
**optional** — set only the ones you need:

=== ":lang-python: Python"

    ```python linenums="1" title="Snowflake metadata configuration"
    (
        SnowflakeCrawler(client)
        .basic(username="ATLAN_USER", password="••••••", host="abc12345.snowflakecomputing.com")
        .connection(name="production-snowflake", admin_roles=[...])
        # what to crawl
        .include_metadata({"ANALYTICS": ["PUBLIC"]}) # (1)
        .exclude_metadata({"ANALYTICS": ["STAGING"]}) # (2)
        .exclude_regex_for_tables_views(".*_TMP$") # (3)
        .exclude_views(False) # (4)
        .exclude_tables_with_empty_data(False) # (5)
        # account-usage source (only relevant when extraction_method="account-usage")
        .database_name("SNOWFLAKE") # (6)
        .schema_name("ACCOUNT_USAGE") # (7)
        # enrichment
        .view_definition_lineage(True) # (8)
        .import_tags(True) # (9)
        .import_stages(True) # (10)
        .enable_incremental_extraction(False) # (11)
        # advanced
        .control_config("custom") # (12)
        .custom_config('{"flag": true}') # (13)
        .run(name="snowflake-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude — exclude takes priority over include.
    3. Regex of tables/views to ignore.
    4. Exclude all views.
    5. Exclude tables (and their columns) that contain no data.
    6. Database to read `ACCOUNT_USAGE` data from (defaults to `SNOWFLAKE`).
    7. Schema to read account-usage data from (defaults to `ACCOUNT_USAGE`).
    8. Build column-level lineage for views from their definitions.
    9. Sync Snowflake tags to Atlan.
    10. Import internal and external named stages.
    11. Only extract schemas changed since the last successful run.
    12. Switch advanced config to `custom` to enable experimental feature flags.
    13. Custom feature-flag config as a JSON string (used when `control_config` is
        `custom`).
