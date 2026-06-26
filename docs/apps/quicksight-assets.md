---
title: QuickSight assets app
description: Learn how to crawl QuickSight and publish to Atlan for discovery.
---

# QuickSight assets app

The QuickSight assets app crawls QuickSight assets and publishes to Atlan. Build it with the `AtlanQuicksight` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Iam authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="QuickSight assets crawling with iam auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanQuicksight

    client = AtlanClient()

    response = (
        AtlanQuicksight(client)
        .iam(
            username="...",  # (1)
            password="...",  # (2)
            region="...",  # (3)
            accountid="...",  # (4)
        )
        .connection(  # (5)
            name="production-quicksight",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="quicksight-prod")  # (6)
    )
    print(response.slug, response.run_id)
    ```

    1. AWS Access Key.
    2. AWS Secret Key.
    3. Region.
    4. AWS Account ID.
    5. Display name + at least one admin (role, group, or user).
    6. `.run()` creates and submits a run; use `.create()` to create without running.

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanQuicksight(client)
        .iam(...)
        .connection(name="production-quicksight", admin_roles=[...])
        .exclude_folders({...})  # (1)
        .fetch_all_assets_without_folder(True)  # (2)
        .include_folders({...})  # (3)
        .run(name="quicksight-prod")
    )
    ```

    1. Exclude Folders — Selected folders will not be processed.
    2. Fetch all assets without folder? — Fetch assets not linked to any folder, including datasets, analyses & dashboards.
    3. Include Folders — Selected folders will be processed. Exclude gets preference over include.
