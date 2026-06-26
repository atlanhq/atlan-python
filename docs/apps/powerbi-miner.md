---
title: Power BI miner app
description: Learn how to mine Power BI activity to generate usage and popularity metrics.
---

# Power BI miner app

The Power BI miner app mines Power BI activity events to generate usage and
popularity metrics. Build it with the `PowerbiMiner` builder.

A miner does **not** create a connection or take a credential — it runs against an
**existing** Power BI connection and reuses that connection's own credential, so you
only supply the connection's `qualifiedName`.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine activity from Power BI"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PowerbiMiner

    client = AtlanClient()

    response = (
        PowerbiMiner(client)
        .connection( # (1)
            qualified_name="default/powerbi/1700000000",
        )
        .start_date(1704067200) # (2)
        .excluded_users("svc-account-1,svc-account-2") # (3)
        .run(name="powerbi-prod-miner") # (4)
    )
    print(response.slug, response.run_id)
    ```

    1. **Required.** The exact `qualifiedName` of the existing Power BI connection to
       mine. Its credential is reused — no credential step is needed.
    2. *Optional.* Earliest date from which to mine activity events. The Power BI API
       only retains the **last 14 days**; the default uses that full window.
    3. *Optional.* Comma-separated user IDs (typically service accounts) whose
       activity should not count toward popularity.
    4. **Always pass an explicit `name` for miners** — a bare `.run()` defaults to the
       app id (`powerbi-miner`) and a second run would collide.

## Advanced config

=== ":lang-python: Python"

    ```python linenums="1" title="Advanced miner configuration"
    (
        PowerbiMiner(client)
        .connection(qualified_name="default/powerbi/1700000000")
        .advanced_config("...") # (1)
        .run(name="powerbi-prod-miner")
    )
    ```

    1. Set advanced configuration of the miner.
