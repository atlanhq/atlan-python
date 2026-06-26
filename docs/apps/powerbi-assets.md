---
title: Power BI assets app
description: Learn how to crawl Power BI assets and publish them to Atlan for discovery.
---

# Power BI assets app

The Power BI assets app crawls Power BI workspaces, dashboards, reports, datasets,
and related assets and publishes them to Atlan. Build it with the `PowerbiCrawler`
builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Power BI supports two authentication methods: **basic** (delegated user) and
**service principal**.

## Service principal

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Power BI crawling with a service principal"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import PowerbiCrawler

    client = AtlanClient()

    response = (
        PowerbiCrawler(client)
        .service_principal( # (1)
            tenant_id="...", # (2)
            client_id="...", # (3)
            client_secret="••••••", # (4)
            admin_api=True, # (5)
        )
        .connection(
            name="production-powerbi",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_workspaces({"ws-id-1": {}, "ws-id-2": {}}) # (6)
        .run(name="powerbi-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Service-principal auth; the secret is vaulted.
    2. **Required.** Azure AD tenant id.
    3. **Required.** Application client id.
    4. **Required.** Application client secret.
    5. **Required.** Enable Scanner (admin) API access. `admin_api_summary`, `host`,
       and `port` are optional.
    6. **Step 3 — Metadata.** Workspaces to crawl (`{workspace_id: {}}`). Omit to
       crawl all workspaces.

## Basic authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Power BI crawling with basic auth"
    (
        PowerbiCrawler(client)
        .basic(
            username="atlan_user", # (1)
            password="••••••", # (2)
            tenant_id="...", # (3)
            client_id="...", # (4)
            client_secret="••••••", # (5)
        )
        .connection(name="production-powerbi", admin_roles=[...])
        .run(name="powerbi-prod")
    )
    ```

    1. **Required.** Username.
    2. **Required.** Password.
    3. **Required.** Azure AD tenant id.
    4. **Required.** Application client id.
    5. **Required.** Application client secret. `host` / `port` are optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Power BI metadata configuration"
    (
        PowerbiCrawler(client)
        .service_principal(tenant_id="...", client_id="...", client_secret="••••••", admin_api=True)
        .connection(name="production-powerbi", admin_roles=[...])
        .include_workspaces({"ws-id-1": {}}) # (1)
        .exclude_workspaces({"ws-id-2": {}}) # (2)
        .include_dashboard_and_reports_regex("^Finance.*") # (3)
        .exclude_dashboard_and_reports_regex(".*_draft$") # (4)
        .attach_endorsements_from_power_bi(True) # (5)
        .fetch_report_definition_extracts(True) # (6)
        .enable_incremental_extraction(False) # (7)
        .run(name="powerbi-prod")
    )
    ```

    1. Workspaces to include (`{workspace_id: {}}`).
    2. Workspaces to exclude.
    3. Include dashboards/reports matching this regex.
    4. Exclude dashboards/reports matching this regex.
    5. Auto-certify assets endorsed in Power BI.
    6. Fetch Power BI report definition extracts.
    7. Only extract assets changed since the last successful run.
