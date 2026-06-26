---
title: Glue assets app
description: Learn how to crawl AWS Glue Data Catalog assets and publish them to Atlan for discovery.
---

# Glue assets app

The Glue assets app crawls the AWS Glue Data Catalog (databases, tables, columns)
and publishes it to Atlan. Build it with the `AtlanGlue` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Glue supports two authentication methods: **access key/secret** (`iam`) and **IAM
role** (`role`).

## Access key authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Glue crawling with access key/secret"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanGlue

    client = AtlanClient()

    response = (
        AtlanGlue(client)
        .iam( # (1)
            username="AKIA...", # (2)
            password="••••••", # (3)
            region="us-east-1", # (4)
        )
        .connection(
            name="production-glue",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"my_database": {}}) # (5)
        .run(name="glue-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** AWS access key/secret auth; the secret is vaulted.
    2. **Required.** AWS access key.
    3. **Required.** AWS secret key.
    4. **Required.** AWS region.
    5. **Step 3 — Metadata.** Databases to crawl. Omit to crawl everything.

## IAM role authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Glue crawling with an IAM role"
    (
        AtlanGlue(client)
        .role(
            aws_role_arn="arn:aws:iam::123456789012:role/atlan", # (1)
            aws_external_id="...", # (2)
            region="us-east-1", # (3)
        )
        .connection(name="production-glue", admin_roles=[...])
        .run(name="glue-prod")
    )
    ```

    1. *Optional.* The IAM role ARN to assume.
    2. *Optional.* AWS external id for the role.
    3. **Required.** AWS region.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Glue metadata configuration"
    (
        AtlanGlue(client)
        .iam(username="AKIA...", password="••••••", region="us-east-1")
        .connection(name="production-glue", admin_roles=[...])
        .catalog_id("AwsDataCatalog") # (1)
        .include_metadata({"my_database": {}}) # (2)
        .exclude_metadata({"tmp_database": {}}) # (3)
        .exclude_table_regex(".*_tmp$") # (4)
        .run(name="glue-prod")
    )
    ```

    1. The Glue Data Catalog id. Use `AwsDataCatalog` for the default catalog; for S3
       Table Buckets use `<account_id>:s3tablescatalog/<bucket_name>`.
    2. Databases to include. Exclude takes priority over include.
    3. Databases to exclude.
    4. Regex of tables to exclude (defaults to including all tables).
