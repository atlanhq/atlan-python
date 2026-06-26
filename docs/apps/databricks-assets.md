---
title: Databricks assets app
description: Learn how to crawl Databricks assets and publish them to Atlan for discovery.
---

# Databricks assets app

The Databricks assets app crawls Unity Catalog assets from Databricks and publishes
them to Atlan. Build it with the `DatabricksCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection. To re-crawl, re-run the existing
    workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Personal access token

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To crawl Databricks using a personal access token:

=== ":lang-python: Python"

    ```python linenums="1" title="Databricks crawling with a personal access token"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import DatabricksCrawler

    client = AtlanClient()

    response = (
        DatabricksCrawler(client)
        .basic( # (1)
            password="dapi...", # (2)
            http_path="/sql/1.0/warehouses/abc123", # (3)
            host="dbc-1234.cloud.databricks.com", # (4)
        )
        .connection(
            name="production-databricks",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .extraction_strategy("system-tables") # (5)
        .asset_selection( # (6)
            include_hierarchy={"my_catalog": ["sales", "marketing"]},
        )
        .nested_columns("true") # (7)
        .run(name="databricks-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Personal-access-token auth; the token is vaulted.
    2. The Databricks personal access token.
    3. The SQL warehouse HTTP path.
    4. The Databricks workspace host.
    5. **Step 3 — Metadata.** `system-tables` (recommended) queries Unity Catalog's
       `system.information_schema`; `rest-api` uses the Databricks SDK.
    6. Asset selection — see [Asset selection](#asset-selection) below.
    7. Parse `STRUCT`/`ARRAY`/`MAP` columns into nested child columns.

## Service principal (AWS / Azure)

To authenticate with a service principal instead of a token:

=== ":lang-python: Python"

    ```python linenums="1" title="Databricks crawling with a service principal"
    # AWS
    DatabricksCrawler(client).aws_service(
        client_id="...", client_secret="...", host="dbc-1234.cloud.databricks.com",
    )

    # Azure
    DatabricksCrawler(client).azure_service(
        client_id="...", client_secret="...", tenant_id="...",
        host="adb-1234.azuredatabricks.net",
    )
    ```

## Asset selection

The `asset_selection(...)` method mirrors the UI's multi-mode picker. Combine any
of the four modes (all optional):

=== ":lang-python: Python"

    ```python linenums="1" title="Asset selection — hierarchy and regex"
    (
        DatabricksCrawler(client)
        .basic(password="dapi...", http_path="...", host="...")
        .connection(name="production-databricks", admin_roles=[...])
        .asset_selection(
            include_hierarchy={"my_catalog": ["sales"]}, # (1)
            exclude_hierarchy={"my_catalog": ["staging"]}, # (2)
            include_regex={"schema": "prod_.*"}, # (3)
            exclude_regex={"table": ".*_tmp$"}, # (4)
        )
        .run(name="databricks-prod")
    )
    ```

    1. **Include by hierarchy** — `{catalog: [schema, ...]}` (sent as an object).
    2. **Exclude by hierarchy** — same shape; exclude takes priority over include.
    3. **Include by regex** — `{asset_type: regex}` for `schema` or `table`.
    4. **Exclude by regex** — same; `{"table": ...}` excludes matching tables/views.

## Other metadata options

=== ":lang-python: Python"

    ```python linenums="1" title="Additional Databricks configuration"
    (
        DatabricksCrawler(client)
        .basic(password="dapi...", http_path="...", host="...")
        .connection(name="production-databricks", admin_roles=[...])
        .import_tags("true") # (1)
        .enable_view_lineage("true") # (2)
        .import_ai_models("true") # (3)
        .incremental_extraction("true") # (4)
        .run(name="databricks-prod")
    )
    ```

    1. Sync Unity Catalog tags to Atlan.
    2. Build column-level lineage for views from their definitions.
    3. Import Databricks ML model and model-version metadata.
    4. Only extract assets changed since the last successful run.
