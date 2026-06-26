---
title: DynamoDB assets app
description: Learn how to crawl DynamoDB and publish to Atlan for discovery.
---

# DynamoDB assets app

The DynamoDB assets app crawls DynamoDB assets and publishes to Atlan. Build it with the `AtlanDynamodb` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Assume Role authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="DynamoDB assets crawling with assume_role auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanDynamodb

    client = AtlanClient()

    response = (
        AtlanDynamodb(client)
        .assume_role(
            aws_role_arn="...",  # (1)
            aws_external_id="...",  # (2)
            session_name="...",  # (3)
            region="...",  # (4)
            endpoint_url="...",  # (5)
        )
        .connection(  # (6)
            name="production-dynamodb",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="dynamodb-prod")  # (7)
    )
    print(response.slug, response.run_id)
    ```

    1. AWS Role ARN.
    2. AWS External ID.
    3. Session Name.
    4. AWS Region.
    5. Custom Endpoint URL.
    6. Display name + at least one admin (role, group, or user).
    7. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanDynamodb(client).iam_user(username="...", password="...", region="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanDynamodb(client)
        .assume_role(...)
        .connection(name="production-dynamodb", admin_roles=[...])
        .exclude_tables_regex("...")  # (1)
        .include_tables_regex("...")  # (2)
        .run(name="dynamodb-prod")
    )
    ```

    1. Exclude tables regex — Pipe-separated regex matched against table names. Example: .*_TMP|.*_TEMP|TMP.*|TEMP.*
    2. Include tables regex — Pipe-separated regex matched against table names. Example: Employee.*
