---
title: Supported apps
description: Explore how to create and run connector app workflows in Atlan.
---

# Supported apps

Atlan **apps** are connector workflows — crawlers, miners, and enrichment jobs — that
crawl your sources and publish assets to Atlan for discovery. Each app has a typed,
UI-equivalent **builder** that walks the same three steps as the "new app" wizard
(**Credential → Connection → Metadata**), so you can create and run it without
knowing the underlying payload.

For the full lifecycle — create, run, list, update, schedule, and delete — see
[Manage apps](manage-apps.md). Each app page below shows how to build the workflow
from scratch, covering every authentication method and configuration option.

??? tip "Can't find the app you're looking for? :thinking:"

    === ":lang-python: Python"
        <!-- md:python 9.8.0 -->
        <!-- md:flag experimental -->

        If a connector doesn't have a builder yet, you can still create and run it by
        passing a raw `inputs` dict (matching the app's input contract) directly to
        `client.app.create()`. :tada:

        ```python linenums="1" title="app_create_example.py"
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient()

        response = client.app.create(
            app_id="bigquery-crawler",
            name="my-workflow",
            inputs={...},  # values matching the app's input contract
            run=True,
        )
        ```

        Use `client.app.get_input_contract("<app-id>")` to discover the available
        input keys, types, and defaults for any app.

## Connectors

1. [Anaplan assets](./anaplan-assets.md)
2. [Apache Kafka assets](./apache-kafka-assets.md)
3. [Athena assets](./athena-assets.md)
4. [BigQuery assets](./bigquery-assets.md)
5. [BigQuery miner](./bigquery-miner.md)
6. [Confluent Kafka assets](./confluent-kafka-assets.md)
7. [Databricks assets](./databricks-assets.md)
8. [Databricks miner](./databricks-miner.md)
9. [Dataplex assets](./dataplex-assets.md)
10. [DynamoDB assets](./dynamodb-assets.md)
11. [Glue assets](./glue-assets.md)
12. [Hive assets](./hive-assets.md)
13. [Metabase assets](./metabase-assets.md)
14. [Microsoft SQL Server assets](./mssql-assets.md)
15. [MongoDB assets](./mongodb-assets.md)
16. [MySQL assets](./mysql-assets.md)
17. [Oracle assets](./oracle-assets.md)
18. [Oracle miner](./oracle-miner.md)
19. [PostgreSQL assets](./postgres-assets.md)
20. [PostgreSQL miner](./postgres-miner.md)
21. [Power BI assets](./powerbi-assets.md)
22. [Power BI miner](./powerbi-miner.md)
23. [Presto assets](./presto-assets.md)
24. [QuickSight assets](./quicksight-assets.md)
25. [Redash assets](./redash-assets.md)
26. [Sigma assets](./sigma-assets.md)
27. [Snowflake assets](./snowflake-assets.md)
28. [Snowflake miner](./snowflake-miner.md)
29. [Tableau assets](./tableau-assets.md)
30. [Teradata assets](./teradata-assets.md)
31. [Teradata miner](./teradata-miner.md)
32. [Trino assets](./trino-assets.md)
33. [dbt assets](./dbt-assets.md)
