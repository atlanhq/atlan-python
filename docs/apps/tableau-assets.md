---
title: Tableau assets app
description: Learn how to crawl Tableau and publish to Atlan for discovery.
---

# Tableau assets app

The Tableau assets app crawls Tableau assets and publishes to Atlan. Build it with the `AtlanTableau` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Tableau assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanTableau

    client = AtlanClient()

    response = (
        AtlanTableau(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            default_site="...",  # (3)
            protocol="...",  # (4)
            self_signed_ssl_certificate="...",  # (5)
            host="...",  # (6)
            port=0,  # (7)
        )
        .connection(  # (8)
            name="production-tableau",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="tableau-prod")  # (9)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Site.
    4. SSL.
    5. SSL Certificate.
    6. Host.
    7. Port.
    8. Display name + at least one admin (role, group, or user).
    9. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanTableau(client).jwt(username="...", client_id="...", private_id="...", private_key="...", protocol="...", host="...")
    AtlanTableau(client).personal_access_token(username="...", password="...", protocol="...", host="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanTableau(client)
        .basic(...)
        .connection(name="production-tableau", admin_roles=[...])
        .alternate_host_url("...")  # (1)
        .crawl_embedded_dashboards(True)  # (2)
        .crawl_hidden_datasource_fields(True)  # (3)
        .crawl_unpublished_worksheets_and_dashboards(True)  # (4)
        .exclude_projects({...})  # (5)
        .exclude_projects_regex("...")  # (6)
        .force_full_field_extraction(True)  # (7)
        .include_projects({...})  # (8)
        .incremental_mode(True)  # (9)
        .run(name="tableau-prod")
    )
    ```

    1. Alternate Host URL — Protocol and host name to use in the link for the 'View in Tableau' button.
    2. Crawl Embedded Dashboards — Default behaviour does not create relationships between embedded dashboards. Selecting 'Yes' will create them; this can increase workflow runtime.
    3. Crawl Hidden Datasource Fields — Default behaviour is to crawl all datasource fields, including hidden ones. Selecting 'No' will exclude fields marked hidden in Tableau Desktop.
    4. Crawl Unpublished Worksheets and Dashboards — Default behaviour is to crawl all worksheets and dashboards, including hidden ones. Selecting 'No' will exclude assets marked hidden in Tableau Desktop.
    5. Exclude Projects — Selected projects will not be processed.
    6. Exclude Projects Regex — Projects whose names match the regex will not be processed. Defaults to empty string.
    7. Force Full Field Extraction — v3-only. When enabled, ignores the incremental marker and performs a full field extraction even if Incremental Mode is on. Use this to re-seed the incremental field cache. Has no effect when Incremental Mode is off.
    8. Include Projects — Selected projects will be processed (empty = all projects).
    9. Incremental Mode — v3-only. When enabled, only fetches metadata changed since the last successful run.
