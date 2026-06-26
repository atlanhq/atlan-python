---
title: MySQL assets app
description: Learn how to crawl MySQL and publish to Atlan for discovery.
---

# MySQL assets app

The MySQL assets app crawls MySQL assets and publishes to Atlan. Build it with the `AtlanMysql` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="MySQL assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanMysql

    client = AtlanClient()

    response = (
        AtlanMysql(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            host="...",  # (3)
            port=0,  # (4)
        )
        .connection(  # (5)
            name="production-mysql",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="mysql-prod")  # (6)
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
    AtlanMysql(client).iam_role(username="...", aws_role_arn="...", host="...")
    AtlanMysql(client).iam_user(username="...", password="...", username_2="...", host="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanMysql(client)
        .basic(...)
        .connection(name="production-mysql", admin_roles=[...])
        .exclude_metadata({...})  # (1)
        .exclude_regex_for_tables_views("...")  # (2)
        .include_metadata({...})  # (3)
        .run(name="mysql-prod")
    )
    ```

    1. Exclude Metadata
    2. Exclude regex for tables & views — Regular expression to exclude temporary tables and views.
    3. Include Metadata
