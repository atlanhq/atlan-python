---
title: DynamoDB assets app
description: Learn how to crawl Amazon DynamoDB assets and publish them to Atlan for discovery.
---

# DynamoDB assets app

The DynamoDB assets app crawls Amazon DynamoDB tables (and their inferred schema)
and publishes them to Atlan. Build it with the `AtlanDynamodb` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

DynamoDB supports two authentication methods: **IAM user** (access key/secret) and
**assume role**.

## IAM user authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="DynamoDB crawling with access key/secret"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanDynamodb

    client = AtlanClient()

    response = (
        AtlanDynamodb(client)
        .iam_user( # (1)
            username="AKIA...", # (2)
            password="••••••", # (3)
            region="us-east-1", # (4)
        )
        .connection(
            name="production-dynamodb",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_tables_regex("Employee.*") # (5)
        .run(name="dynamodb-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** AWS access key/secret auth; the secret is vaulted.
    2. **Required.** AWS access key.
    3. **Required.** AWS secret key.
    4. **Required.** AWS region. A custom `endpoint_url` is optional.
    5. **Step 3 — Metadata.** Pipe-separated regex matched against table names.

## Assume role authentication

=== ":lang-python: Python"

    ```python linenums="1" title="DynamoDB crawling with an assumed role"
    (
        AtlanDynamodb(client)
        .assume_role(
            aws_role_arn="arn:aws:iam::123456789012:role/atlan", # (1)
            region="us-east-1", # (2)
            aws_external_id="...", # (3)
            session_name="atlan-session", # (4)
        )
        .connection(name="production-dynamodb", admin_roles=[...])
        .run(name="dynamodb-prod")
    )
    ```

    1. **Required.** The IAM role ARN to assume.
    2. **Required.** AWS region.
    3. *Optional.* AWS external id for the role.
    4. *Optional.* Session name. A custom `endpoint_url` is also optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="DynamoDB metadata configuration"
    (
        AtlanDynamodb(client)
        .iam_user(username="AKIA...", password="••••••", region="us-east-1")
        .connection(name="production-dynamodb", admin_roles=[...])
        .include_tables_regex("Employee.*|Orders.*") # (1)
        .exclude_tables_regex(".*_TMP|.*_TEMP") # (2)
        .run(name="dynamodb-prod")
    )
    ```

    1. Pipe-separated regex of table names to include.
    2. Pipe-separated regex of table names to exclude.
