---
title: Athena assets app
description: Learn how to crawl Amazon Athena assets and publish them to Atlan for discovery.
---

# Athena assets app

The Athena assets app crawls Amazon Athena databases, tables, views, and columns and
publishes them to Atlan. Build it with the `AtlanAthena` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Athena supports two authentication methods: **access key/secret** and **IAM role**.
The port is optional and defaults to `443`.

## Access key authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Athena crawling with access key/secret"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanAthena

    client = AtlanClient()

    response = (
        AtlanAthena(client)
        .basic( # (1)
            username="AKIA...", # (2)
            password="••••••", # (3)
            s3_output_location="s3://my-athena-results/", # (4)
            workgroup="primary", # (5)
            host="athena.us-east-1.amazonaws.com", # (6)
        )
        .connection(
            name="production-athena",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"my_catalog": ["default"]}) # (7)
        .run(name="athena-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** AWS access key/secret auth; the secret is vaulted.
    2. **Required.** AWS access key.
    3. **Required.** AWS secret key.
    4. **Required.** The S3 location where Athena writes query results.
    5. *Optional.* The Athena workgroup.
    6. **Required.** The Athena host. The port (`port=`) defaults to `443`.
    7. Databases/schemas to crawl, as `{database: [schema, ...]}`.

## IAM role authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Athena crawling with an IAM role"
    (
        AtlanAthena(client)
        .role(
            aws_role_arn="arn:aws:iam::123456789012:role/atlan", # (1)
            aws_external_id="...", # (2)
            s3_output_location="s3://my-athena-results/", # (3)
            workgroup="primary",
            host="athena.us-east-1.amazonaws.com",
        )
        .connection(name="production-athena", admin_roles=[...])
        .run(name="athena-prod")
    )
    ```

    1. *Optional.* The IAM role ARN to assume.
    2. *Optional.* AWS external id for the role.
    3. **Required.** The S3 output location. `workgroup` and `port` are optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Athena metadata configuration"
    (
        AtlanAthena(client)
        .basic(username="AKIA...", password="••••••", s3_output_location="s3://...", host="...")
        .connection(name="production-athena", admin_roles=[...])
        .include_metadata({"my_catalog": ["default"]}) # (1)
        .exclude_metadata({"my_catalog": ["staging"]}) # (2)
        .exclude_regex_for_tables_views(".*_tmp$") # (3)
        .enable_source_level_filtering(False) # (4)
        .advanced_config("default") # (5)
        .run(name="athena-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude.
    3. Regex of tables/views to ignore.
    4. Apply schema-level filtering at the source (only include-filter schemas are
       fetched).
    5. Set the crawler's advanced configuration.
