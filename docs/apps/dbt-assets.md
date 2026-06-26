---
title: dbt assets app
description: Learn how to crawl dbt assets (dbt Cloud or dbt Core) and publish them to Atlan.
---

# dbt assets app

The dbt assets app ingests dbt metadata — models, sources, tests, and their lineage
— and publishes it to Atlan. Build it with the `AtlanDbt` builder. dbt supports two
**sources**, selected with `.source(...)`:

- **dbt Cloud** (`.source("api")`) — pull metadata from the dbt Cloud API.
- **dbt Core** (`.source("objectstore")`) — read pre-extracted artifacts from cloud
  object storage (AWS / GCP / Azure).

## dbt Cloud (API)

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To ingest from dbt Cloud using an API token:

=== ":lang-python: Python"

    ```python linenums="1" title="dbt Cloud ingestion"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanDbt

    client = AtlanClient()

    response = (
        AtlanDbt(client)
        .source("api") # (1)
        .api( # (2)
            password="dbtc_...", # (3)
            host="https://abc123.us1.dbt.com", # (4)
        )
        .connection( # (5)
            name="production-dbt",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({ # (6)
            "24670": {"117312": {}, "133741": {}}
        })
        .enrich_metadata_in_materialized_assets(True) # (7)
        .run(name="dbt-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. Select the dbt Cloud source.
    2. **Step 1 — Credential.** dbt Cloud API auth; the token is vaulted.
    3. Your dbt Cloud API token (Service Token).
    4. Your dbt Cloud access URL (the host for your dbt Cloud account region).
    5. **Step 2 — Connection.** Display name + at least one admin.
    6. **Step 3 — Metadata.** The include filter is **nested** —
       `{account_id: {job_id: {}}}` — and is sent as a JSON string the worker parses.
       A flat `{account_id: [job_ids]}` list will not work. Omit to include everything.
    7. Add enrichment to the dbt assets' materialized (warehouse) assets too.

## dbt Core (object storage)

To ingest from dbt artifacts stored in cloud object storage, select the
`objectstore` source and provide object-store credentials (`.aws(...)`,
`.gcp(...)`, or `.azure(...)`):

=== ":lang-python: Python"

    ```python linenums="1" title="dbt Core ingestion from object storage"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanDbt

    client = AtlanClient()

    response = (
        AtlanDbt(client)
        .source("objectstore") # (1)
        .manifest_source("external") # (2)
        .aws( # (3)
            # object-store credential fields (bucket/region/keys)
        )
        .object_storage_prefix("artifacts/apps/dbt/workflows/my-run/metadata") # (4)
        .connection(
            name="production-dbt",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_folder_filter("project_a|project_b") # (5)
        .run(name="dbt-core-prod")
    )
    ```

    1. Select the object-storage (dbt Core) source.
    2. Read artifacts from an external bucket. Use `"atlan"` to read from Atlan's own
       object storage (no extra credential needed).
    3. Object-store credentials — use `.aws(...)`, `.gcp(...)`, or `.azure(...)` to
       match your bucket's cloud. (Omit when `manifest_source` is `"atlan"`.)
    4. Path in object storage where the dbt artifacts live.
    5. Pipe-separated folder-name patterns to include during Core extraction.

## Other metadata options

=== ":lang-python: Python"

    ```python linenums="1" title="Additional dbt configuration"
    (
        AtlanDbt(client)
        .source("api")
        .api(password="dbtc_...", host="https://abc123.us1.dbt.com")
        .connection(name="production-dbt", admin_roles=[...])
        .exclude_metadata({"24670": {"999999": {}}}) # (1)
        .import_tags(True) # (2)
        .advanced_options(True) # (3)
        .run(name="dbt-prod")
    )
    ```

    1. Exclude specific accounts/jobs — same nested shape as `include_metadata`.
       Exclude takes priority over include.
    2. Sync dbt tags to Atlan tags.
    3. Enable advanced processing options.
