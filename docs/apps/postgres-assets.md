---
title: PostgreSQL assets app
description: Learn how to crawl PostgreSQL and publish to Atlan for discovery.
---

# PostgreSQL assets app

The PostgreSQL assets app crawls PostgreSQL assets and publishes to Atlan. Build it with the `PostgresCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="PostgreSQL assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PostgresCrawler

    client = AtlanClient()

    response = (
        PostgresCrawler(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            database="...",  # (3)
            host="...",  # (4)
            port=0,  # (5)
        )
        .connection(  # (6)
            name="production-postgres",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="postgres-prod")  # (7)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Database.
    4. Host.
    5. Port.
    6. Display name + at least one admin (role, group, or user).
    7. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    PostgresCrawler(client).iam_role(username="...", aws_role_arn="...", aws_region="...", database="...")
    PostgresCrawler(client).iam_user(username="...", password="...", username_2="...", aws_region="...", database="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        PostgresCrawler(client)
        .basic(...)
        .connection(name="production-postgres", admin_roles=[...])
        .advanced_config('default')  # (1)
        .control_config('default')  # (2)
        .custom_config("...")  # (3)
        .enable_source_level_filtering('true')  # (4)
        .exclude_metadata({...})  # (5)
        .exclude_regex_for_tables_views("...")  # (6)
        .include_metadata({...})  # (7)
        .run(name="postgres-prod")
    )
    ```

    1. Advanced Config — Set advanced configuration of the crawler.
    2. Control Config — Controls custom experimental feature flags for the crawler.
    3. Custom Config — Custom JSON config controlling experimental feature flags.
    4. Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source.
    5. Exclude Metadata — Selected databases and schemas won't be extracted.
    6. Exclude regex for tables & views — Regex of tables & views to ignore.
    7. Include Metadata — Only the selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config.
