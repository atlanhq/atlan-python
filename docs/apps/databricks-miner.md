---
title: Databricks miner app
description: Learn how to mine query history from Databricks to generate lineage and usage metrics.
---

# Databricks miner app

The Databricks miner app mines lineage and query history from Databricks Unity
Catalog system tables to generate lineage and usage (popularity) metrics. Build it
with the `DatabricksMiner` builder.

A miner does **not** create a connection or take a credential — it runs against an
**existing** Databricks connection and reuses that connection's own credential, so
you only supply the connection's `qualifiedName`.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine lineage and query history from Databricks"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import DatabricksMiner

    client = AtlanClient()

    response = (
        DatabricksMiner(client)
        .connection( # (1)
            qualified_name="default/databricks/1700000000",
        )
        .lineage_extraction_method("system-table") # (2)
        .sql_warehouse_id("abc123def456") # (3)
        .fetch_query_history_and_calculate_popularity(True) # (4)
        .start_date(1704067200) # (5)
        .popularity_window_days(30) # (6)
        .run(name="databricks-prod-miner") # (7)
    )
    print(response.slug, response.run_id)
    ```

    1. **Required.** The exact `qualifiedName` of the existing Databricks connection
       to mine. Its credential is reused — no credential step is needed.
    2. *Optional.* `system-table` reads lineage from `system.access.*`; `offline`
       skips extraction (when lineage is pre-computed upstream).
    3. *Optional.* The SQL warehouse id used by the Statement Execution API for
       lineage extraction.
    4. *Optional.* Aggregate query-history counts into popularity scores (requires
       `system.access.query_history`).
    5. *Optional.* Fetch queries from this date onwards for query-history mining and
       popularity (does not affect lineage extraction).
    6. *Optional.* Lookback window in days for popularity (30 = last month).
    7. **Always pass an explicit `name` for miners** — a bare `.run()` defaults to the
       app id (`databricks-miner`) and a second run would collide.

## Popularity from a cloned catalog

If you mine from a cloned catalog/schema rather than the `system` catalog, all of
these are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Popularity / lineage from a cloned catalog"
    (
        DatabricksMiner(client)
        .connection(qualified_name="default/databricks/1700000000")
        .extraction_catalog_type("cloned-catalog") # (1)
        .cloned_catalog_name("my_clone") # (2)
        .cloned_schema_name("access_clone") # (3)
        .extraction_catalog_for_popularity("cloned-catalog") # (4)
        .cloned_catalog_name_for_popularity("my_clone") # (5)
        .cloned_schema_name_for_popularity("query_clone") # (6)
        .set_sql_warehouse_popularity("abc123def456") # (7)
        .excluded_users(["svc-account"]) # (8)
        .enable_file_path_lineage(False) # (9)
        .run(name="databricks-prod-miner")
    )
    ```

    1. Catalog to use for lineage extraction (`system` by default, or `cloned-catalog`).
    2. Name of the catalog containing the cloned schema for lineage.
    3. Name of the schema containing the cloned tables for lineage.
    4. Catalog to use for popularity extraction.
    5. Name of the catalog containing the cloned schema for popularity.
    6. Name of the schema containing the cloned tables for popularity.
    7. The SQL warehouse id used for popularity extraction.
    8. Users whose queries to exclude from usage metrics.
    9. Track lineage at the file-path level for volumes and external locations.
