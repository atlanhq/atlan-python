---
title: Oracle miner app
description: Learn how to mine query history from Oracle to generate lineage and usage metrics.
---

# Oracle miner app

The Oracle miner app mines query history (from Oracle's AWR) to generate lineage and
usage metrics. Build it with the `OracleMiner` builder.

A miner does **not** create a connection or take a credential — it runs against an
**existing** Oracle connection and reuses that connection's own credential, so you
only supply the connection's `qualifiedName`.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from Oracle"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import OracleMiner

    client = AtlanClient()

    response = (
        OracleMiner(client)
        .connection( # (1)
            qualified_name="default/oracle/1700000000",
        )
        .start_date(-3) # (2)
        .run(name="oracle-prod-miner") # (3)
    )
    print(response.slug, response.run_id)
    ```

    1. **Required.** The exact `qualifiedName` of the existing Oracle connection to
       mine. Its credential is reused — no credential step is needed.
    2. *Optional.* How far back to mine, as a **negative-day offset** (e.g. `-3` =
       three days ago), which the miner converts to an AWR cutoff timestamp.
    3. **Always pass an explicit `name` for miners** — a bare `.run()` defaults to
       the app id (`oracle-miner`) and a second run would collide.
