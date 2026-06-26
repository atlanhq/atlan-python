---
title: Sigma assets app
description: Learn how to crawl Sigma assets and publish them to Atlan for discovery.
---

# Sigma assets app

The Sigma assets app crawls Sigma workbooks (and their elements) and publishes them
to Atlan. Build it with the `AtlanSigma` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## API token

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Sigma crawling with an API token"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanSigma

    client = AtlanClient()

    response = (
        AtlanSigma(client)
        .api_token( # (1)
            username="client-id", # (2)
            password="••••••", # (3)
            host="aws-api.sigmacomputing.com", # (4)
        )
        .connection(
            name="production-sigma",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_workbooks({"c13051d8-...": {}}) # (5)
        .run(name="sigma-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** API client-id + token auth; the token is vaulted.
    2. **Required.** The Sigma client id.
    3. **Required.** The Sigma API token.
    4. *Optional.* The Sigma API host. The port (`port=`) is optional.
    5. **Step 3 — Metadata.** Workbooks to crawl (`{workbook_id: {}}`). Omit to crawl
       all workbooks.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Sigma metadata configuration"
    (
        AtlanSigma(client)
        .api_token(username="client-id", password="••••••", host="aws-api.sigmacomputing.com")
        .connection(name="production-sigma", admin_roles=[...])
        .include_workbooks({"c13051d8-...": {}}) # (1)
        .exclude_workbooks({"99999999-...": {}}) # (2)
        .run(name="sigma-prod")
    )
    ```

    1. Workbooks to include (`{workbook_id: {}}`).
    2. Workbooks to exclude.
