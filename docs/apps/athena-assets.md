---
title: Athena assets app
description: Learn how to crawl Athena and publish to Atlan for discovery.
---

# Athena assets app

The Athena assets app crawls Athena assets and publishes to Atlan. Build it with the `AtlanAthena` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Athena assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanAthena

    client = AtlanClient()

    response = (
        AtlanAthena(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            s3_output_location="...",  # (3)
            workgroup="...",  # (4)
            host="...",  # (5)
            port=0,  # (6)
        )
        .connection(  # (7)
            name="production-athena",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="athena-prod")  # (8)
    )
    print(response.slug, response.run_id)
    ```

    1. AWS Access Key.
    2. AWS Secret Key.
    3. S3 Output Location.
    4. Workgroup.
    5. Host.
    6. Port.
    7. Display name + at least one admin (role, group, or user).
    8. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanAthena(client).role(s3_output_location="...", host="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanAthena(client)
        .basic(...)
        .connection(name="production-athena", admin_roles=[...])
        .advanced_config('default')  # (1)
        .enable_source_level_filtering('true')  # (2)
        .exclude_metadata({...})  # (3)
        .exclude_regex_for_tables_views("...")  # (4)
        .include_metadata({...})  # (5)
        .run(name="athena-prod")
    )
    ```

    1. Advanced Config — Set advanced configuration of the crawler
    2. Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source. Schemas selected in the include filter will be fetched.
    3. Exclude Metadata
    4. Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string
    5. Include Metadata
