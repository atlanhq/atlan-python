---
title: Snowflake miner app
description: Learn how to mine query history from Snowflake and publish to Atlan for discovery.
---

# Snowflake miner app

The Snowflake miner app mines query history from Snowflake to generate lineage and usage metrics and publishes to Atlan. Build it with the `SnowflakeMiner` builder.

A miner does not create a connection or take a credential — it runs against an
**existing** connection and reuses that connection's own credential.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from Snowflake"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import SnowflakeMiner

    client = AtlanClient()

    response = (
        SnowflakeMiner(client)
        .connection(qualified_name="default/snowflake/1700000000")  # (1)
        .advanced_config('default')  # (2)
        .calculate_popularity(True)  # (3)
        .custom_config("...")  # (4)
        .database_name("...")  # (5)
        .excluded_users([...])  # (6)
        .popularity_window_days(0.0)  # (7)
        .preflight_check("...")  # (8)
        .schema_name("...")  # (9)
        .snowflake_database('default')  # (10)
        .start_date(0.0)  # (11)
        .run(name="snowflake-miner")  # (12)
    )
    ```

    1. The exact `qualifiedName` of the existing connection to mine; its credential is reused.
    2. Advanced Config — Controls custom experimental feature flags for the miner
    3. Calculate popularity — Enable popularity metrics generated using mined data.
    4. Custom Config — Custom JSON config controlling experimental feature flags for the miner
    5. Database Name — Snowflake database name to be used
    6. Excluded Users — List of users who should be excluded while calculating usage metrics for assets
    7. Popularity Window (days) — Number of days to consider for calculating popularity.
    8. preflight_check
    9. Schema Name — Account Usage schema name in the Snowflake database
    10. Snowflake Database — Optionally provide details of the cloned version of the snowflake database
    11. Start date
    12. Always pass an explicit unique `name` for miners (a bare run defaults to the app id and collides).
