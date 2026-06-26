---
title: PostgreSQL miner app
description: Learn how to mine query history from PostgreSQL to generate lineage and usage metrics.
---

# PostgreSQL miner app

The PostgreSQL miner app mines query history from PostgreSQL to generate lineage and
usage metrics. Build it with the `PostgresMiner` builder.

A miner does **not** create a connection or take a credential — it runs against an
**existing** PostgreSQL connection and reuses that connection's own credential, so
you only supply the connection's `qualifiedName`.

## Source extraction

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Mine query history from PostgreSQL"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PostgresMiner

    client = AtlanClient()

    response = (
        PostgresMiner(client)
        .connection( # (1)
            qualified_name="default/postgres/1700000000",
        )
        .run(name="postgres-prod-miner") # (2)
    )
    print(response.slug, response.run_id)
    ```

    1. **Required.** The exact `qualifiedName` of the existing PostgreSQL connection
       to mine. The builder resolves that connection's credential automatically — no
       credential step is needed.
    2. **Always pass an explicit `name` for miners.** A miner has no connection
       display name to derive one from, so a bare `.run()` would default the workflow
       name to the app id (`postgres-miner`) and a second run would collide
       (`409 already exists`).
