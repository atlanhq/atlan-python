---
title: Databricks miner app
description: Learn how to mine query history from Databricks and publish to Atlan for discovery.
---

# Databricks miner app

The Databricks miner app mines query history from Databricks to generate lineage and usage metrics and publishes to Atlan. Build it with the `DatabricksMiner` builder.

A miner does not create a connection or take a credential — it runs against an
**existing** connection and reuses that connection's own credential.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from Databricks"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import DatabricksMiner

    client = AtlanClient()

    response = (
        DatabricksMiner(client)
        .connection(qualified_name="default/databricks/1700000000")  # (1)
        .cloned_catalog_name("...")  # (2)
        .cloned_catalog_name_for_popularity("...")  # (3)
        .cloned_schema_name("...")  # (4)
        .cloned_schema_name_for_popularity("...")  # (5)
        .enable_file_path_lineage('false')  # (6)
        .excluded_users([...])  # (7)
        .extraction_catalog_for_popularity('system-table')  # (8)
        .extraction_catalog_type('system-table')  # (9)
        .fetch_query_history_and_calculate_popularity('false')  # (10)
        .lineage_extraction_method('system-table')  # (11)
        .popularity_window_days(0.0)  # (12)
        .set_sql_warehouse_popularity("...")  # (13)
        .sql_warehouse_id("...")  # (14)
        .start_date(0.0)  # (15)
        .run(name="databricks-miner")  # (16)
    )
    ```

    1. The exact `qualifiedName` of the existing connection to mine; its credential is reused.
    2. Cloned Catalog Name — Name of the catalog that contains the cloned schema for lineage
    3. Cloned Catalog Name for Popularity — Name of the catalog that contains the cloned schema for popularity
    4. Cloned Schema Name — Name of the schema that contains the cloned tables for lineage
    5. Cloned Schema Name for Popularity — Name of the schema that contains the cloned tables for popularity
    6. Enable File Path Lineage — Control lineage tracking at the file-path level for volumes and external locations.
    7. Excluded Users — List of users whose queries should be excluded while calculating usage metrics for assets.
    8. Extraction Catalog for Popularity — Select the catalog to use for popularity extraction. By default uses 'system' catalog and 'query' schema. To use cloned catalog, select 'Cloned Catalog'.
    9. Extraction Catalog Type — Select the catalog to use for extraction. By default uses 'system' catalog and 'access' schema. To use cloned catalog, select 'Cloned Catalog'.
    10. Fetch Query History and Calculate Popularity — Aggregate query-history counts into popularity scores. Requires `system.access.query_history`.
    11. Lineage Extraction Method — Determines the method used to fetch the lineage. `System Table` reads lineage from `system.access.*`. `Offline` skips extraction (used when lineage is pre-computed upstream).
    12. Popularity Window (days) — Lookback window in days for popularity computation. 30 = last month.
    13. SQL Warehouse ID — Warehouse ID used by Statement Execution API for popularity extraction.
    14. SQL Warehouse ID — Warehouse ID used by Statement Execution API for lineage extraction.
    15. Start Date — Queries from this date onwards are fetched for Query History mining and popularity calculation. This does not change lineage extraction.
    16. Always pass an explicit unique `name` for miners (a bare run defaults to the app id and collides).
