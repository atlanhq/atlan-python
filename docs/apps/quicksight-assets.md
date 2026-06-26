---
title: QuickSight assets app
description: Learn how to crawl Amazon QuickSight assets and publish them to Atlan for discovery.
---

# QuickSight assets app

The QuickSight assets app crawls Amazon QuickSight dashboards, analyses, datasets,
and folders and publishes them to Atlan. Build it with the `AtlanQuicksight`
builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## IAM authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="QuickSight crawling with IAM credentials"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanQuicksight

    client = AtlanClient()

    response = (
        AtlanQuicksight(client)
        .iam( # (1)
            username="AKIA...", # (2)
            password="••••••", # (3)
            region="us-east-1", # (4)
            accountid="123456789012", # (5)
        )
        .connection(
            name="production-quicksight",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_folders({"folder-id-1": {}}) # (6)
        .run(name="quicksight-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** AWS access key/secret auth; the secret is vaulted.
    2. **Required.** AWS access key.
    3. **Required.** AWS secret key.
    4. **Required.** AWS region.
    5. **Required.** AWS account id.
    6. **Step 3 — Metadata.** Folders to crawl (`{folder_id: {}}`). Omit to crawl all
       folders.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="QuickSight metadata configuration"
    (
        AtlanQuicksight(client)
        .iam(username="AKIA...", password="••••••", region="us-east-1", accountid="123456789012")
        .connection(name="production-quicksight", admin_roles=[...])
        .include_folders({"folder-id-1": {}}) # (1)
        .exclude_folders({"folder-id-2": {}}) # (2)
        .fetch_all_assets_without_folder(True) # (3)
        .run(name="quicksight-prod")
    )
    ```

    1. Folders to include (`{folder_id: {}}`). Exclude takes priority over include.
    2. Folders to exclude.
    3. Also fetch assets not linked to any folder (datasets, analyses, dashboards).
