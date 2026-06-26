---
title: PostgreSQL miner app
description: Learn how to mine query history from PostgreSQL and publish to Atlan for discovery.
---

# PostgreSQL miner app

The PostgreSQL miner app mines query history from PostgreSQL to generate lineage and usage metrics and publishes to Atlan. Build it with the `PostgresMiner` builder.

A miner does not create a connection or take a credential — it runs against an
**existing** connection and reuses that connection's own credential.

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
        .connection(qualified_name="default/postgres/1700000000")  # (1)
        .run(name="postgres-miner")  # (2)
    )
    ```

    1. The exact `qualifiedName` of the existing connection to mine; its credential is reused.
    2. Always pass an explicit unique `name` for miners (a bare run defaults to the app id and collides).
