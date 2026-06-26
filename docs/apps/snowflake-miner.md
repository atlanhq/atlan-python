---
title: Snowflake miner app
description: Learn how to mine query history from Snowflake to generate lineage and usage metrics.
---

# Snowflake miner app

The Snowflake miner app mines query history from Snowflake to generate lineage and
usage (popularity) metrics. Build it with the `SnowflakeMiner` builder.

Unlike a crawler, a miner does **not** create a connection or take a credential. It
runs against an **existing** Snowflake connection and reuses that connection's own
credential — so you only supply the connection's `qualifiedName`.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To mine query history from an existing Snowflake connection:

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from Snowflake"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import SnowflakeMiner

    client = AtlanClient()

    response = (
        SnowflakeMiner(client)
        .connection( # (1)
            qualified_name="default/snowflake/1700000000",
        )
        .start_date(1704067200) # (2)
        .calculate_popularity(True) # (3)
        .popularity_window_days(30) # (4)
        .excluded_users(["SYSTEM", "ATLAN_SERVICE"]) # (5)
        .run(name="snowflake-prod-miner") # (6)
    )
    print(response.slug, response.run_id)
    ```

    1. **Required.** The exact `qualifiedName` of the existing Snowflake connection
       to mine. The builder resolves that connection's credential automatically — no
       credential step is needed.
    2. *Optional.* The date (as an epoch) from which to start mining query history.
    3. *Optional.* Generate popularity metrics from the mined query history.
    4. *Optional.* Number of days of history to consider when calculating popularity.
    5. *Optional.* Users (e.g. service accounts) to exclude from usage metrics.
    6. **Always pass an explicit `name` for miners.** A miner has no connection
       display name to derive one from, so a bare `.run()` would default the workflow
       name to the app id (`snowflake-miner`) and a second run would collide
       (`409 already exists`).

## Account-usage source

By default the miner reads from Snowflake's `SNOWFLAKE.ACCOUNT_USAGE`. To point it at
a different database/schema (e.g. a clone) — all of these are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Mine from a cloned account-usage database"
    (
        SnowflakeMiner(client)
        .connection(qualified_name="default/snowflake/1700000000")
        .snowflake_database("cloned") # (1)
        .database_name("SNOWFLAKE_CLONE") # (2)
        .schema_name("ACCOUNT_USAGE") # (3)
        .start_date(1704067200)
        .run(name="snowflake-prod-miner")
    )
    ```

    1. Use a `cloned` Snowflake database instead of the `default`.
    2. The Snowflake database name to mine from.
    3. The account-usage schema name in that database.

## Advanced config

=== ":lang-python: Python"

    ```python linenums="1" title="Custom feature-flag config"
    (
        SnowflakeMiner(client)
        .connection(qualified_name="default/snowflake/1700000000")
        .start_date(1704067200)
        .advanced_config("custom") # (1)
        .custom_config('{"flag": true}') # (2)
        .run(name="snowflake-prod-miner")
    )
    ```

    1. Switch advanced config to `custom` to enable experimental feature flags.
    2. Custom feature-flag config as a JSON string (used when `advanced_config` is
       `custom`).
