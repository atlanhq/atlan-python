---
title: Google Dataplex assets app
description: Learn how to crawl Google Dataplex (Knowledge Catalog) assets and publish them to Atlan.
---

# Google Dataplex assets app

The Dataplex assets app crawls Google Dataplex / Knowledge Catalog metadata (aspect
types, data profiling, and data quality) and publishes it to Atlan. Build it with
the `AtlanKnowledgeCatalog` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Dataplex supports two authentication methods: **service account** (`basic`) and
**Workload Identity Federation** (`gcp_wif`).

## Service account

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Dataplex crawling with a service account"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanKnowledgeCatalog

    client = AtlanClient()

    response = (
        AtlanKnowledgeCatalog(client)
        .basic( # (1)
            service_account_json=sa_json, # (2)
            project_id="my-project", # (3)
        )
        .connection(
            name="production-dataplex",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_projects_optional({"my-project": {}}) # (4)
        .run(name="dataplex-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Service-account auth; the JSON key is vaulted.
    2. **Required.** The service-account JSON key (as a string; keep `\n` escaped).
    3. **Required.** The home GCP project id. For private connectivity, pass
       `network_connectivity=...` and `psc_host=...` (both optional).
    4. **Step 3 — Metadata.** GCP projects to include. Empty = all accessible
       projects.

## Workload Identity Federation

=== ":lang-python: Python"

    ```python linenums="1" title="Dataplex crawling with WIF"
    (
        AtlanKnowledgeCatalog(client)
        .gcp_wif(
            service_account_email="svc@my-project.iam.gserviceaccount.com", # (1)
            wif_pool_provider_id="...", # (2)
            atlan_oauth_id="...", # (3)
            atlan_oauth_secret="••••••", # (4)
            project_id="my-project", # (5)
        )
        .connection(name="production-dataplex", admin_roles=[...])
        .run(name="dataplex-prod")
    )
    ```

    1. **Required.** The service-account email.
    2. **Required.** The WIF pool provider id.
    3. **Required.** Atlan OAuth client id.
    4. **Required.** Atlan OAuth client secret.
    5. **Required.** The home GCP project id.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Dataplex metadata configuration"
    (
        AtlanKnowledgeCatalog(client)
        .basic(service_account_json=sa_json, project_id="my-project")
        .connection(name="production-dataplex", admin_roles=[...])
        .include_projects_optional({"my-project": {}}) # (1)
        .exclude_projects_optional({"sandbox-project": {}}) # (2)
        .include_aspect_types({"my-aspect": {}}) # (3)
        .exclude_aspect_types({"noisy-aspect": {}}) # (4)
        .ingest_knowledge_catalog_aspect_metadata(True) # (5)
        .ingest_data_profiling_metadata(True) # (6)
        .ingest_data_quality_metadata(True) # (7)
        .run(name="dataplex-prod")
    )
    ```

    1. GCP projects to include (empty = all accessible projects).
    2. GCP projects to exclude.
    3. Aspect types to include — if set, **only** these aspects are extracted.
    4. Aspect types to exclude.
    5. Discover Knowledge Catalog aspect types and write per-asset aspect metadata.
    6. Fetch `DATA_PROFILE` scan results and write per-column profiling metrics.
    7. Fetch `DATA_QUALITY` scan results and write DQ scores, rules, and dimensions.
