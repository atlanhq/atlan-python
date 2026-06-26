---
title: Redash assets app
description: Learn how to crawl Redash assets and publish them to Atlan for discovery.
---

# Redash assets app

The Redash assets app crawls Redash queries and dashboards and publishes them to
Atlan. Build it with the `AtlanRedash` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## API key

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Redash crawling with an API key"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanRedash

    client = AtlanClient()

    response = (
        AtlanRedash(client)
        .api_key( # (1)
            password="••••••", # (2)
            host="redash.example.com", # (3)
        )
        .connection(
            name="production-redash",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="redash-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** API-key auth; the key is vaulted.
    2. **Required.** The Redash API key.
    3. **Required.** The Redash host. The port (`port=`) is optional.

## Configuration options

Redash filters queries and dashboards **by tag**. All options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Redash metadata configuration"
    (
        AtlanRedash(client)
        .api_key(password="••••••", host="redash.example.com")
        .connection(name="production-redash", admin_roles=[...])
        .include_queries_with_tags(["prod"]) # (1)
        .exclude_queries_with_tags(["draft"]) # (2)
        .include_queries_without_tags(True) # (3)
        .include_unpublished_queries(False) # (4)
        .include_dashboards_with_tags(["prod"]) # (5)
        .exclude_dashboards_with_tags(["draft"]) # (6)
        .include_dashboards_without_tags(True) # (7)
        .alternate_host_url("https://redash.mycompany.com") # (8)
        .advanced_config("...") # (9)
        .run(name="redash-prod")
    )
    ```

    1. Crawl queries having these tags. Exclude takes priority over include.
    2. Skip queries having these tags.
    3. Also include queries that have no tags.
    4. Whether to fetch unpublished queries.
    5. Crawl dashboards having these tags. Exclude takes priority over include.
    6. Skip dashboards having these tags.
    7. Also include dashboards that have no tags.
    8. Protocol + host used in the "View in Redash" links.
    9. Controls advanced asset-inclusion features.
