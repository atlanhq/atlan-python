---
title: Teradata assets app
description: Learn how to crawl Teradata assets and publish them to Atlan for discovery.
---

# Teradata assets app

The Teradata assets app crawls Teradata databases, tables, views, and columns and
publishes them to Atlan. Build it with the `TeradataCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Teradata supports two authentication methods: **basic** (TD2) and **LDAP**.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Teradata crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import TeradataCrawler

    client = AtlanClient()

    response = (
        TeradataCrawler(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            host="teradata.example.com", # (4)
        )
        .connection(
            name="production-teradata",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"my_db": ["*"]}) # (5)
        .run(name="teradata-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password (TD2) auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. *Optional.* Host. The port (`port=`) is optional.
    5. Databases/schemas to crawl, as `{database: [schema, ...]}`.

## LDAP authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Teradata crawling with LDAP"
    (
        TeradataCrawler(client)
        .ldap(username="atlan_user", password="••••••", host="teradata.example.com") # (1)
        .connection(name="production-teradata", admin_roles=[...])
        .run(name="teradata-prod")
    )
    ```

    1. LDAP auth — same parameters as basic; `host` and `port` are optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Teradata metadata configuration"
    (
        TeradataCrawler(client)
        .basic(username="atlan_user", password="••••••", host="...")
        .connection(name="production-teradata", admin_roles=[...])
        .include_metadata({"my_db": ["*"]}) # (1)
        .exclude_metadata({"my_db": ["staging"]}) # (2)
        .exclude_regex_for_tables_views(".*_tmp$") # (3)
        .enable_source_level_filtering(False) # (4)
        .advanced_config("...") # (5)
        .run(name="teradata-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude — exclude takes priority over include.
    3. Regex of tables/views to ignore.
    4. Apply schema-level filtering at the source (only include-filter schemas are
       fetched).
    5. Controls experimental crawler features.
