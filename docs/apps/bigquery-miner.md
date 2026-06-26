---
title: BigQuery miner app
description: Learn how to mine query history from BigQuery to generate lineage and usage metrics.
---

# BigQuery miner app

The BigQuery miner app mines query history from BigQuery to generate lineage and
usage (popularity) metrics. Build it with the `BigqueryMiner` builder.

Unlike crawlers, a miner does **not** create a connection or take a credential.
It runs against an **existing** BigQuery connection and reuses that connection's
own credential — so you only supply the connection's `qualifiedName`.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To mine query history from an existing BigQuery connection:

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from BigQuery"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import BigqueryMiner

    client = AtlanClient()

    response = (
        BigqueryMiner(client) # (1)
        .connection( # (2)
            qualified_name="default/bigquery/1700000000",
        )
        .start_date(1704067200) # (3)
        .calculate_popularity("true") # (4)
        .popularity_window_days(30) # (5)
        .excluded_users(["system@my-project.iam.gserviceaccount.com"]) # (6)
        .run(name="bigquery-prod-miner") # (7)
    )
    print(response.slug, response.run_id)
    ```

    1. Base configuration for a new BigQuery miner. You must provide a `client`.
    2. The exact `qualifiedName` of the **existing** BigQuery connection to mine. The
       builder resolves that connection's credential automatically — no credential
       step is needed.
    3. The date (as an epoch) from which to start mining query history.
    4. Generate popularity metrics from the mined query history.
    5. Number of days of history to consider when calculating popularity.
    6. Optionally exclude users (e.g. service accounts) from usage metrics.
    7. **Always pass an explicit `name` for miners.** A miner has no connection
       display name to derive one from, so a bare `.run()` would default the
       workflow name to the app id (`bigquery-miner`) and a second run would collide
       (`409 already exists`).

## Region

By default the miner mines from the connection's region. To target a specific
BigQuery region:

=== ":lang-python: Python"

    ```python linenums="1" title="Mine from a custom region"
    (
        BigqueryMiner(client)
        .connection(qualified_name="default/bigquery/1700000000")
        .start_date(1704067200)
        .region("custom") # (1)
        .custom_big_query_region("region-us") # (2)
        .run(name="bigquery-prod-miner")
    )
    ```

    1. Switch region selection to `custom`.
    2. The BigQuery region to mine from.

## Advanced config

=== ":lang-python: Python"

    ```python linenums="1" title="Custom feature-flag config"
    (
        BigqueryMiner(client)
        .connection(qualified_name="default/bigquery/1700000000")
        .start_date(1704067200)
        .control_config("custom") # (1)
        .custom_config('{"flag": true}') # (2)
        .run(name="bigquery-prod-miner")
    )
    ```

    1. Switch advanced config to `custom`.
    2. Supply experimental feature-flag config as a JSON string.
