---
title: Teradata assets app
description: Learn how to crawl Teradata and publish to Atlan for discovery.
---

# Teradata assets app

The Teradata assets app crawls Teradata assets and publishes to Atlan. Build it with the `TeradataCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Teradata assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import TeradataCrawler

    client = AtlanClient()

    response = (
        TeradataCrawler(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            host="...",  # (3)
            port=0,  # (4)
        )
        .connection(  # (5)
            name="production-teradata",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="teradata-prod")  # (6)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Host.
    4. Port.
    5. Display name + at least one admin (role, group, or user).
    6. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    TeradataCrawler(client).ldap(username="...", password="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        TeradataCrawler(client)
        .basic(...)
        .connection(name="production-teradata", admin_roles=[...])
        .advanced_config('default')  # (1)
        .enable_source_level_filtering('true')  # (2)
        .exclude_metadata({...})  # (3)
        .exclude_regex_for_tables_views("...")  # (4)
        .include_metadata({...})  # (5)
        .run(name="teradata-prod")
    )
    ```

    1. Advanced Config — Controls custom experimental features for the crawler
    2. Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source. Schemas selected in the include filter will be fetched.
    3. Exclude Metadata — Selected databases and schemas won't be extracted.
    4. Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string.
    5. Include Metadata — Only the selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config.
