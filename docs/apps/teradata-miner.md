---
title: Teradata miner app
description: Learn how to mine query history from Teradata and publish to Atlan for discovery.
---

# Teradata miner app

The Teradata miner app mines query history from Teradata to generate lineage and usage metrics and publishes to Atlan. Build it with the `TeradataMiner` builder.

A miner does not create a connection or take a credential — it runs against an
**existing** connection and reuses that connection's own credential.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from Teradata"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import TeradataMiner

    client = AtlanClient()

    response = (
        TeradataMiner(client)
        .connection(qualified_name="default/teradata/1700000000")  # (1)
        .advanced_config('default')  # (2)
        .cross_connection('true')  # (3)
        .custom_config("...")  # (4)
        .set_control_config_strategy('default')  # (5)
        .start_date("...")  # (6)
        .run(name="teradata-miner")  # (7)
    )
    ```

    1. The exact `qualifiedName` of the existing connection to mine; its credential is reused.
    2. Advanced Config — Set advanced configuration of the miner
    3. Cross Connection — Enable searching for lineage across all available connections on Atlan instead of the selected connection. Defaults to false.
    4. Custom Config — Custom JSON config controlling experimental feature flags.
    5. Advanced Config — Controls custom experimental feature flags for the miner
    6. Start date — Earliest date (epoch seconds) from which to mine query history. The miner extracts up to two weeks of history. Set 0 to use the full window.
    7. Always pass an explicit unique `name` for miners (a bare run defaults to the app id and collides).
