---
title: Tableau assets app
description: Learn how to crawl Tableau assets and publish them to Atlan for discovery.
---

# Tableau assets app

The Tableau assets app crawls Tableau projects, workbooks, worksheets, dashboards,
datasources, and fields and publishes them to Atlan. Build it with the
`AtlanTableau` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Tableau supports three authentication methods: **basic**, **personal access token**,
and **JWT**. All three accept an optional `default_site` and a
`self_signed_ssl_certificate`, and require `protocol` and `host`.

## Personal access token

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Tableau crawling with a personal access token"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanTableau

    client = AtlanClient()

    response = (
        AtlanTableau(client)
        .personal_access_token( # (1)
            username="my-pat-name", # (2)
            password="••••••", # (3)
            protocol="https", # (4)
            host="prod-useast-b.online.tableau.com", # (5)
            default_site="my-site", # (6)
        )
        .connection(
            name="production-tableau",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_projects({"40e6b97a-...": {}, "bd1f0402-...": {}}) # (7)
        .run(name="tableau-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Personal-access-token auth; the secret is vaulted.
    2. **Required.** The PAT name.
    3. **Required.** The PAT secret.
    4. **Required.** SSL/protocol (e.g. `https`).
    5. **Required.** The Tableau host. The port (`port=`) is optional.
    6. *Optional.* The Tableau site. `self_signed_ssl_certificate` is also optional.
    7. **Step 3 — Metadata.** Projects to crawl, keyed by project id
       (`{project_id: {}}`). Omit to crawl all projects.

## Basic and JWT authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Basic and JWT auth"
    # Basic (username/password)
    AtlanTableau(client).basic(
        username="atlan_user", password="••••••",
        protocol="https", host="prod-useast-b.online.tableau.com",
    )

    # JWT (connected app)
    AtlanTableau(client).jwt(
        username="atlan_user", # (1)
        client_id="6c93f350-...", # (2)
        private_id="6ae86656-...", # (3)
        private_key="••••••", # (4)
        protocol="https",
        host="prod-useast-b.online.tableau.com",
    )
    ```

    1. **Required.** Username (the JWT `sub` claim).
    2. **Required.** Client ID (the `iss` claim).
    3. **Required.** Secret ID (the `kid` claim).
    4. **Required.** The secret. `default_site` / `self_signed_ssl_certificate` /
       `port` are optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Tableau metadata configuration"
    (
        AtlanTableau(client)
        .personal_access_token(username="my-pat", password="••••••", protocol="https", host="...")
        .connection(name="production-tableau", admin_roles=[...])
        .include_projects({"40e6b97a-...": {}}) # (1)
        .exclude_projects({"99999999-...": {}}) # (2)
        .exclude_projects_regex(".*_archive$") # (3)
        .crawl_hidden_datasource_fields(True) # (4)
        .crawl_unpublished_worksheets_and_dashboards(True) # (5)
        .crawl_embedded_dashboards(False) # (6)
        .alternate_host_url("https://tableau.mycompany.com") # (7)
        .incremental_mode(False) # (8)
        .force_full_field_extraction(False) # (9)
        .run(name="tableau-prod")
    )
    ```

    1. Projects to include, keyed by project id (`{project_id: {}}`).
    2. Projects to exclude, same shape.
    3. Exclude projects whose names match this regex.
    4. Crawl hidden datasource fields.
    5. Crawl unpublished (hidden) worksheets and dashboards.
    6. Create relationships for embedded dashboards (increases runtime).
    7. Protocol + host used in the "View in Tableau" links.
    8. **v3-only.** Only fetch metadata changed since the last successful run.
    9. **v3-only.** Force a full field extraction even with incremental mode on (to
       re-seed the incremental cache).
