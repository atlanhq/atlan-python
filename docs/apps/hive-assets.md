---
title: Hive assets app
description: Learn how to crawl Hive and publish to Atlan for discovery.
---

# Hive assets app

The Hive assets app crawls Hive assets and publishes to Atlan. Build it with the `HiveCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Hive assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import HiveCrawler

    client = AtlanClient()

    response = (
        HiveCrawler(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            default_schema="...",  # (3)
            database_name="...",  # (4)
            host="...",  # (5)
            port=0,  # (6)
        )
        .connection(  # (7)
            name="production-hive",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="hive-prod")  # (8)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Default schema.
    4. Database name.
    5. Host.
    6. Port.
    7. Display name + at least one admin (role, group, or user).
    8. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    HiveCrawler(client).kerberos(principal="...", service_name="...", keytab_file="...", krb5_conf_file="...", kerberos_type="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        HiveCrawler(client)
        .basic(...)
        .connection(name="production-hive", admin_roles=[...])
        .advanced_config('default')  # (1)
        .allow_partial_success(True)  # (2)
        .exclude_metadata({...})  # (3)
        .include_metadata({...})  # (4)
        .run(name="hive-prod")
    )
    ```

    1. Advanced Config — Advanced configuration for the workflow. Do not edit if unsure.
    2. Allow partial success — Enable this if you are aware of permission limitations and still want Atlan to ingest remaining assets. If unsure, don't enable this.
    3. Exclude Metadata
    4. Include Metadata
