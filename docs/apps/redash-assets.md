---
title: Redash assets app
description: Learn how to crawl Redash and publish to Atlan for discovery.
---

# Redash assets app

The Redash assets app crawls Redash assets and publishes to Atlan. Build it with the `AtlanRedash` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Api Key authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Redash assets crawling with api_key auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanRedash

    client = AtlanClient()

    response = (
        AtlanRedash(client)
        .api_key(
            password="...",  # (1)
            host="...",  # (2)
            port=0,  # (3)
        )
        .connection(  # (4)
            name="production-redash",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="redash-prod")  # (5)
    )
    print(response.slug, response.run_id)
    ```

    1. API Key.
    2. Host.
    3. Port.
    4. Display name + at least one admin (role, group, or user).
    5. `.run()` creates and submits a run; use `.create()` to create without running.

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanRedash(client)
        .api_key(...)
        .connection(name="production-redash", admin_roles=[...])
        .advanced_config('default')  # (1)
        .alternate_host_url("...")  # (2)
        .exclude_dashboards_with_tags({...})  # (3)
        .exclude_queries_with_tags({...})  # (4)
        .include_dashboards_with_tags({...})  # (5)
        .include_dashboards_without_tags('true')  # (6)
        .include_queries_with_tags({...})  # (7)
        .include_queries_without_tags('true')  # (8)
        .include_unpublished_queries('true')  # (9)
        .run(name="redash-prod")
    )
    ```

    1. Advanced Config — Controls advanced asset inclusion features.
    2. Alternate Host URL — Protocol and host used in the 'View in Redash' link.
    3. Exclude dashboards with tags — Dashboards having selected tags will not be crawled.
    4. Exclude queries with tags — Queries having selected tags will not be crawled.
    5. Include dashboards with tags — Dashboards having selected tags will be crawled. Exclude gets preference over include.
    6. Include dashboards without tags — Include dashboards that do not have any tags associated to them.
    7. Include queries with tags — Queries having selected tags will be crawled. Exclude gets preference over include.
    8. Include queries without tags — Include queries that do not have any tags associated to them.
    9. Include unpublished queries — Select whether unpublished queries should be fetched.
