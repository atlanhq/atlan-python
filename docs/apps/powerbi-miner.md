---
title: Power BI miner app
description: Learn how to mine query history from Power BI and publish to Atlan for discovery.
---

# Power BI miner app

The Power BI miner app mines query history from Power BI to generate lineage and usage metrics and publishes to Atlan. Build it with the `PowerbiMiner` builder.

A miner does not create a connection or take a credential — it runs against an
**existing** connection and reuses that connection's own credential.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from Power BI"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PowerbiMiner

    client = AtlanClient()

    response = (
        PowerbiMiner(client)
        .connection(qualified_name="default/powerbi/1700000000")  # (1)
        .advanced_config('default')  # (2)
        .excluded_users("...")  # (3)
        .start_date(0.0)  # (4)
        .run(name="powerbi-miner")  # (5)
    )
    ```

    1. The exact `qualifiedName` of the existing connection to mine; its credential is reused.
    2. Advanced Config — Set advanced configuration of the miner
    3. Excluded Users — Comma-separated list of user IDs (typically service accounts) whose activity should not count toward popularity.
    4. Start date — Earliest date from which to mine activity events. The Power BI API only retains the last 14 days; the default uses that full window.
    5. Always pass an explicit unique `name` for miners (a bare run defaults to the app id and collides).
