---
title: Teradata miner app
description: Learn how to mine query history from Teradata to generate lineage and usage metrics.
---

# Teradata miner app

The Teradata miner app mines query history from Teradata to generate lineage and
usage metrics. Build it with the `TeradataMiner` builder.

A miner does **not** create a connection or take a credential — it runs against an
**existing** Teradata connection and reuses that connection's own credential, so you
only supply the connection's `qualifiedName`.

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
        .connection( # (1)
            qualified_name="default/teradata/1700000000",
        )
        .start_date(1704067200) # (2)
        .cross_connection(False) # (3)
        .run(name="teradata-prod-miner") # (4)
    )
    print(response.slug, response.run_id)
    ```

    1. **Required.** The exact `qualifiedName` of the existing Teradata connection to
       mine. Its credential is reused — no credential step is needed.
    2. *Optional.* Earliest date (epoch seconds) from which to mine query history.
       The miner extracts up to two weeks of history; set `0` to use the full window.
    3. *Optional.* Search for lineage across all connections on Atlan instead of just
       the selected connection. Defaults to `false`.
    4. **Always pass an explicit `name` for miners** — a bare `.run()` defaults to the
       app id (`teradata-miner`) and a second run would collide.

## Advanced config

=== ":lang-python: Python"

    ```python linenums="1" title="Custom feature-flag config"
    (
        TeradataMiner(client)
        .connection(qualified_name="default/teradata/1700000000")
        .start_date(0)
        .advanced_config("...") # (1)
        .custom_config('{"flag": true}') # (2)
        .run(name="teradata-prod-miner")
    )
    ```

    1. Set advanced configuration of the miner.
    2. Custom feature-flag config as a JSON string.
