---
title: Glue assets app
description: Learn how to crawl Glue and publish to Atlan for discovery.
---

# Glue assets app

The Glue assets app crawls Glue assets and publishes to Atlan. Build it with the `AtlanGlue` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Iam authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Glue assets crawling with iam auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanGlue

    client = AtlanClient()

    response = (
        AtlanGlue(client)
        .iam(
            username="...",  # (1)
            password="...",  # (2)
            region="...",  # (3)
        )
        .connection(  # (4)
            name="production-glue",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="glue-prod")  # (5)
    )
    print(response.slug, response.run_id)
    ```

    1. AWS Access Key.
    2. AWS Secret Key.
    3. Region.
    4. Display name + at least one admin (role, group, or user).
    5. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanGlue(client).role(region="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanGlue(client)
        .iam(...)
        .connection(name="production-glue", admin_roles=[...])
        .catalog_id("...")  # (1)
        .exclude_metadata({...})  # (2)
        .exclude_table_regex("...")  # (3)
        .include_metadata({...})  # (4)
        .run(name="glue-prod")
    )
    ```

    1. Catalog ID — The Glue Data Catalog ID to crawl. Use 'AwsDataCatalog' for the default catalog. For S3 Table Buckets (federated catalogs), use '<account_id>:s3tablescatalog/<bucket_name>'.
    2. Exclude Metadata — Selected databases won't be extracted.
    3. Exclude table regex — Regex of tables to exclude. Defaults to empty string and includes all tables.
    4. Include Metadata — Only the selected databases will be extracted. Exclude gets preference over include for common databases, if present, in the config.
