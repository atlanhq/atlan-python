---
title: BigQuery assets app
description: Learn how to crawl Google BigQuery assets and publish them to Atlan for discovery.
---

# BigQuery assets app

The BigQuery assets app crawls Google BigQuery assets and publishes them to Atlan
for discovery. Build it with the `BigqueryCrawler` builder, which mirrors the
"new app" wizard: **Credential → Connection → Metadata**.

!!! warning "Creating an app creates a new connection"
    Each time you create the app it mints a **new** connection and new assets within
    it — running it repeatedly with the same settings can produce duplicate assets.
    To re-crawl, re-run the **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Service account

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To crawl BigQuery using service-account authentication (the UI default):

=== ":lang-python: Python"

    ```python linenums="1" title="BigQuery crawling with service-account auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import BigqueryCrawler

    client = AtlanClient()

    response = (
        BigqueryCrawler(client) # (1)
        .service_account( # (2)
            email="svc@my-project.iam.gserviceaccount.com", # (3)
            service_account_json=sa_json, # (4)
            project_id="my-project", # (5)
            connectivity="public", # (6)
        )
        .connection( # (7)
            name="production-bigquery",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
            admin_groups=None,
            admin_users=None,
        )
        .include({"my-project": ["analytics", "sales"]}) # (8)
        .exclude({"my-project": ["staging"]}) # (9)
        .exclude_regex(".*_TMP") # (10)
        .import_nested_columns(True) # (11)
        .combine_sharded_tables(True) # (12)
        .run(name="bigquery-prod") # (13)
    )
    print(response.slug, response.run_id) # (14)
    ```

    1. Base configuration for a new BigQuery crawler. You must provide a `client`.
    2. **Step 1 — Credential.** Service-account auth; the JSON key is vaulted and
       never persisted in the workflow.
    3. The service-account email.
    4. The service-account JSON key, as a string. Paste the key file's contents
       unmodified (newlines stay escaped as `\n`).
    5. Your GCP project id.
    6. `public` uses Google's public endpoint; `private` uses Private Service
       Connect — for `private`, also pass `host="https://your-psc-host"`.
    7. **Step 2 — Connection.** Provide a display name and at least one admin (role,
       group, or user). The builder mints the connection qualified name.
    8. **Step 3 — Metadata.** Datasets to crawl, as `{project: [dataset, ...]}`
       (anchored as regex automatically). Omit to crawl everything.
    9. Datasets to skip — exclude takes priority over include.
    10. Regex for tables/views to exclude from extraction.
    11. Parse nested (`STRUCT`/`ARRAY`) columns into child columns.
    12. Combine sharded tables of the same prefix into a single asset.
    13. `.run(name=...)` creates **and** submits a run. Use `.create(name=...)` to
        create without running.
    14. Persist `response.slug` for later operations (see [Manage apps](manage-apps.md)).

## Workload Identity Federation

To crawl BigQuery using Workload Identity Federation (keyless) auth:

=== ":lang-python: Python"

    ```python linenums="1" title="BigQuery crawling with Workload Identity Federation"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import BigqueryCrawler

    client = AtlanClient()

    response = (
        BigqueryCrawler(client)
        .workload_identity_federation( # (1)
            project_id="my-project",
            connectivity="public",
        )
        .connection(
            name="production-bigquery",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include({"my-project": ["analytics"]})
        .run(name="bigquery-prod")
    )
    ```

    1. Workload Identity Federation auth — no service-account key is stored. Provide
       any provider-specific values as additional keyword arguments.

## Other metadata options

Beyond the options shown above, the builder exposes the rest of the wizard's
metadata toggles:

=== ":lang-python: Python"

    ```python linenums="1" title="Additional metadata configuration"
    (
        BigqueryCrawler(client)
        .service_account(email=..., service_account_json=..., project_id=...)
        .connection(name="production-bigquery", admin_roles=[...])
        .import_tags(True) # (1)
        .hidden_assets(True) # (2)
        .custom_config('{"ignore-all-case": true}') # (3)
        .run(name="bigquery-prod")
    )
    ```

    1. Import tags from BigQuery into Atlan.
    2. Crawl hidden datasets.
    3. Switch advanced config to `custom` and supply a feature-flag JSON string.

## Preview the payload

Call `.preview()` instead of `.create()` / `.run()` to assemble and inspect the
`inputs` payload offline (no network call, secret redacted):

=== ":lang-python: Python"

    ```python linenums="1" title="Inspect the assembled payload"
    builder = (
        BigqueryCrawler(client)
        .service_account(email=..., service_account_json=..., project_id=...)
        .connection(name="production-bigquery", admin_roles=[...])
        .include({"my-project": ["analytics"]})
    )
    print(builder.preview()) # (1)
    ```

    1. Returns the full `inputs` dict the app would submit, with the credential
       redacted — handy for review and testing.

## Re-run with an existing credential

To create another workflow that reuses an already-vaulted credential (instead of
vaulting a new one), pass its guid:

=== ":lang-python: Python"

    ```python linenums="1" title="Reuse an existing vaulted credential"
    (
        BigqueryCrawler(client)
        .credential_guid("e49783c7-...") # (1)
        .connection(name="production-bigquery", admin_roles=[...])
        .include({"my-project": ["analytics"]})
        .run(name="bigquery-prod-2")
    )
    ```

    1. Reuses the vaulted credential by guid — no new secret is stored.
