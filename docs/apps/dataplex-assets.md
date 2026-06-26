---
title: Dataplex assets app
description: Learn how to crawl Dataplex and publish to Atlan for discovery.
---

# Dataplex assets app

The Dataplex assets app crawls Dataplex assets and publishes to Atlan. Build it with the `AtlanKnowledgeCatalog` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Dataplex assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanKnowledgeCatalog

    client = AtlanClient()

    response = (
        AtlanKnowledgeCatalog(client)
        .basic(
            network_connectivity="...",  # (1)
            psc_host="...",  # (2)
            service_account_json="...",  # (3)
            project_id="...",  # (4)
        )
        .connection(  # (5)
            name="production-dataplex",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="dataplex-prod")  # (6)
    )
    print(response.slug, response.run_id)
    ```

    1. Network Connectivity.
    2. PSC Hostname.
    3. Service Account JSON.
    4. Home Project Id.
    5. Display name + at least one admin (role, group, or user).
    6. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    AtlanKnowledgeCatalog(client).gcp_wif(service_account_email="...", wif_pool_provider_id="...", atlan_oauth_id="...", atlan_oauth_secret="...", project_id="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanKnowledgeCatalog(client)
        .basic(...)
        .connection(name="production-dataplex", admin_roles=[...])
        .exclude_aspect_types({...})  # (1)
        .exclude_projects_optional({...})  # (2)
        .include_aspect_types({...})  # (3)
        .include_projects_optional({...})  # (4)
        .ingest_data_profiling_metadata('yes')  # (5)
        .ingest_data_quality_metadata('yes')  # (6)
        .ingest_knowledge_catalog_aspect_metadata('yes')  # (7)
        .preflight_check("...")  # (8)
        .run(name="dataplex-prod")
    )
    ```

    1. Exclude Aspect Types — Select Aspect Types to exclude. These aspects will be skipped during extraction.
    2. Exclude Projects (Optional) — Select GCP projects to exclude from ingestion.
    3. Include Aspect Types — Select specific Aspect Types to include. If specified, ONLY these aspects will be extracted. Leave empty to extract all aspects.
    4. Include Projects (Optional) — Select GCP projects to include. If empty, all accessible projects are ingested.
    5. Ingest Data Profiling Metadata? — When enabled, fetches DATA_PROFILE scan results from Knowledge Catalog and writes per-column profiling metrics (missing values, distinct values, top values, min/max/mean, etc.) to Atlan column assets.
    6. Ingest Data Quality Metadata? — When enabled, fetches DATA_QUALITY scan results from Knowledge Catalog and writes DQ scores, rules, and dimension breakdowns to Atlan table and column assets.
    7. Ingest Knowledge Catalog Aspect Metadata? — When enabled, discovers all Knowledge Catalog Aspect Types across accessible GCP projects and writes per-asset aspect metadata to Atlan assets.
    8. preflight_check
