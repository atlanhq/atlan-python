---
title: Anaplan assets app
description: Learn how to crawl Anaplan assets and publish them to Atlan for discovery.
---

# Anaplan assets app

The Anaplan assets app crawls Anaplan workspaces, models, modules, and line items
and publishes them to Atlan. Build it with the `Anaplan` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Anaplan supports two authentication methods: **basic** (username/password) and
**CA certificate**.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Anaplan crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import Anaplan

    client = AtlanClient()

    response = (
        Anaplan(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
        )
        .connection(
            name="production-anaplan",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"my_workspace": {}}) # (4)
        .run(name="anaplan-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password. A custom `host` is optional.
    4. **Step 3 — Metadata.** Workspaces/models to crawl.

## CA certificate authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Anaplan crawling with a CA certificate"
    (
        Anaplan(client)
        .ca_cert(
            username=encoded_data, # (1)
            password=encoded_signed_data, # (2)
            ca_certificate=ca_cert_contents, # (3)
        )
        .connection(name="production-anaplan", admin_roles=[...])
        .run(name="anaplan-prod")
    )
    ```

    1. **Required.** The encoded data.
    2. **Required.** The encoded signed data.
    3. **Required.** The CA certificate file contents. A custom `host` is optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Anaplan metadata configuration"
    (
        Anaplan(client)
        .basic(username="atlan_user", password="••••••")
        .connection(name="production-anaplan", admin_roles=[...])
        .include_metadata({"my_workspace": {}}) # (1)
        .exclude_metadata({"sandbox_workspace": {}}) # (2)
        .exclude_empty_modules(True) # (3)
        .ingest_system_dimensions("proxy") # (4)
        .run(name="anaplan-prod")
    )
    ```

    1. Workspaces/models to include.
    2. Workspaces/models to exclude.
    3. Exclude modules that have no line items.
    4. How to ingest system dimensions (Time and Versions) — as a proxy,
       individually, or not at all.
