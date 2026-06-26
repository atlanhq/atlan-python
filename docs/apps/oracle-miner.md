---
title: Oracle miner app
description: Learn how to mine query history from Oracle and publish to Atlan for discovery.
---

# Oracle miner app

The Oracle miner app mines query history from Oracle to generate lineage and usage metrics and publishes to Atlan. Build it with the `OracleMiner` builder.

A miner does not create a connection or take a credential — it runs against an
**existing** connection and reuses that connection's own credential.

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
        .connection(qualified_name="default/oracle/1700000000")  # (1)
        .start_date(0.0)  # (2)
        .run(name="oracle-miner")  # (3)
    )
    ```

    1. The exact `qualifiedName` of the existing connection to mine; its credential is reused.
    2. Start date — Pick how far back to mine query history. The widget returns a negative-day offset (e.g. -3 = three days ago) which the miner converts to an AWR cutoff timestamp. Mirrors MSSQL v3 miner's date widget.
    3. Always pass an explicit unique `name` for miners (a bare run defaults to the app id and collides).
