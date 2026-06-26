---
title: Sigma assets app
description: Learn how to crawl Sigma and publish to Atlan for discovery.
---

# Sigma assets app

The Sigma assets app crawls Sigma assets and publishes to Atlan. Build it with the `AtlanSigma` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Api Token authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Sigma assets crawling with api_token auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import AtlanSigma

    client = AtlanClient()

    response = (
        AtlanSigma(client)
        .api_token(
            username="...",  # (1)
            password="...",  # (2)
            host="...",  # (3)
            port=0,  # (4)
        )
        .connection(  # (5)
            name="production-sigma",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="sigma-prod")  # (6)
    )
    print(response.slug, response.run_id)
    ```

    1. Client ID.
    2. API Token.
    3. Host.
    4. Port.
    5. Display name + at least one admin (role, group, or user).
    6. `.run()` creates and submits a run; use `.create()` to create without running.

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        AtlanSigma(client)
        .api_token(...)
        .connection(name="production-sigma", admin_roles=[...])
        .exclude_workbooks({...})  # (1)
        .include_workbooks({...})  # (2)
        .run(name="sigma-prod")
    )
    ```

    1. Exclude Workbooks — Selected workbooks will be excluded from extraction.
    2. Include Workbooks — Selected workbooks will be extracted.
