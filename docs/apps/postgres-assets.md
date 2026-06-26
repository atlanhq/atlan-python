---
title: PostgreSQL assets app
description: Learn how to crawl PostgreSQL assets and publish them to Atlan for discovery.
---

# PostgreSQL assets app

The PostgreSQL assets app crawls PostgreSQL databases, schemas, tables, views, and
columns and publishes them to Atlan. Build it with the `PostgresCrawler` builder,
which mirrors the "new app" wizard: **Credential → Connection → Metadata**.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

PostgreSQL supports three authentication methods: **basic** (username/password) and
two AWS RDS IAM methods (**IAM role** and **IAM user**). The port is optional and
defaults to `5432`.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="PostgreSQL crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PostgresCrawler

    client = AtlanClient()

    response = (
        PostgresCrawler(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            database="analytics", # (4)
            host="mydb.abc123.us-east-1.rds.amazonaws.com", # (5)
        )
        .connection( # (6)
            name="production-postgres",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"analytics": ["public", "sales"]}) # (7)
        .run(name="postgres-prod") # (8)
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Database username.
    3. **Required.** Password.
    4. **Required.** Database to connect to.
    5. *Optional.* Database host. The port (`port=`) is optional and defaults to `5432`.
    6. **Step 2 — Connection.** Display name + at least one admin.
    7. **Step 3 — Metadata.** Schemas to crawl, as `{database: [schema, ...]}`. Omit
       to crawl everything. Exclude takes priority over include.
    8. `.run(name=...)` creates **and** submits a run; use `.create(name=...)` to
       create without running.

## AWS RDS IAM authentication

For PostgreSQL on AWS RDS, authenticate with an IAM role or IAM user:

=== ":lang-python: Python"

    ```python linenums="1" title="PostgreSQL on RDS with IAM auth"
    # IAM role
    PostgresCrawler(client).iam_role(
        username="db_user", # (1)
        aws_role_arn="arn:aws:iam::123456789012:role/atlan", # (2)
        aws_region="us-east-1", # (3)
        database="analytics", # (4)
        aws_external_id="...", # (5)
        host="mydb.abc123.us-east-1.rds.amazonaws.com",
    )

    # IAM user
    PostgresCrawler(client).iam_user(
        username="AKIA...", # (6)
        password="••••••", # (7)
        username_2="db_user", # (8)
        aws_region="us-east-1",
        database="analytics",
        host="mydb.abc123.us-east-1.rds.amazonaws.com",
    )
    ```

    1. **Required.** Database username.
    2. **Required.** The IAM role ARN to assume.
    3. **Required.** AWS region. `rds_port` and `port` are optional.
    4. **Required.** Database to connect to.
    5. *Optional.* AWS external id for the role.
    6. **Required.** AWS access key.
    7. **Required.** AWS secret key.
    8. **Required.** The database username (distinct from the AWS access key).

## Configuration options

All metadata options are **optional** — set only what you need:

=== ":lang-python: Python"

    ```python linenums="1" title="PostgreSQL metadata configuration"
    (
        PostgresCrawler(client)
        .basic(username="atlan_user", password="••••••", database="analytics", host="...")
        .connection(name="production-postgres", admin_roles=[...])
        .include_metadata({"analytics": ["public"]}) # (1)
        .exclude_metadata({"analytics": ["staging"]}) # (2)
        .exclude_regex_for_tables_views(".*_tmp$") # (3)
        .enable_source_level_filtering(False) # (4)
        .advanced_config("default") # (5)
        .control_config("custom") # (6)
        .custom_config('{"flag": true}') # (7)
        .run(name="postgres-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude — exclude takes priority over include.
    3. Regex of tables/views to ignore.
    4. Apply schema-level filtering at the source (only the include-filter schemas
       are fetched).
    5. Set the crawler's advanced configuration.
    6. Switch advanced config to `custom` to enable experimental feature flags.
    7. Custom feature-flag config as a JSON string (used when `control_config` is
       `custom`).
