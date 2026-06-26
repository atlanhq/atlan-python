---
title: MySQL assets app
description: Learn how to crawl MySQL assets and publish them to Atlan for discovery.
---

# MySQL assets app

The MySQL assets app crawls MySQL databases, tables, views, and columns and
publishes them to Atlan. Build it with the `AtlanMysql` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

MySQL supports three authentication methods: **basic** and two AWS RDS IAM methods
(**IAM role**, **IAM user**). The port is optional and defaults to `3306`.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="MySQL crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanMysql

    client = AtlanClient()

    response = (
        AtlanMysql(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            host="mydb.abc123.us-east-1.rds.amazonaws.com", # (4)
        )
        .connection(
            name="production-mysql",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"analytics": ["*"]}) # (5)
        .run(name="mysql-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** Host. The port (`port=`) is optional and defaults to `3306`.
    5. Databases/schemas to crawl, as `{database: [schema, ...]}`.

## AWS RDS IAM authentication

=== ":lang-python: Python"

    ```python linenums="1" title="MySQL on RDS with IAM auth"
    # IAM role
    AtlanMysql(client).iam_role(
        username="db_user", # (1)
        aws_role_arn="arn:aws:iam::123456789012:role/atlan", # (2)
        aws_external_id="...", # (3)
        host="mydb.abc123.us-east-1.rds.amazonaws.com",
    )

    # IAM user
    AtlanMysql(client).iam_user(
        username="AKIA...", # (4)
        password="••••••", # (5)
        username_2="db_user", # (6)
        host="mydb.abc123.us-east-1.rds.amazonaws.com",
    )
    ```

    1. **Required.** Database user.
    2. **Required.** The IAM role ARN to assume.
    3. *Optional.* AWS external id.
    4. **Required.** AWS access key id.
    5. **Required.** AWS secret access key.
    6. **Required.** Database user (distinct from the AWS access key).

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="MySQL metadata configuration"
    (
        AtlanMysql(client)
        .basic(username="atlan_user", password="••••••", host="...")
        .connection(name="production-mysql", admin_roles=[...])
        .include_metadata({"analytics": ["*"]}) # (1)
        .exclude_metadata({"analytics": ["tmp"]}) # (2)
        .exclude_regex_for_tables_views(".*_tmp$") # (3)
        .run(name="mysql-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude.
    3. Regex to exclude temporary tables and views.
