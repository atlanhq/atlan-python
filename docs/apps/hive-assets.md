---
title: Hive assets app
description: Learn how to crawl Apache Hive assets and publish them to Atlan for discovery.
---

# Hive assets app

The Hive assets app crawls Apache Hive databases, tables, views, and columns and
publishes them to Atlan. Build it with the `HiveCrawler` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Hive supports two authentication methods: **basic** (username/password) and
**Kerberos**.

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Hive crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import HiveCrawler

    client = AtlanClient()

    response = (
        HiveCrawler(client)
        .basic( # (1)
            username="atlan_user", # (2)
            password="••••••", # (3)
            host="hive.example.com", # (4)
        )
        .connection(
            name="production-hive",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .include_metadata({"default": ["*"]}) # (5)
        .run(name="hive-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** Username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. *Optional.* Host. The port (`port=`), `default_schema`, and `database_name`
       are also optional.
    5. Databases/schemas to crawl, as `{database: [schema, ...]}`.

## Kerberos authentication

=== ":lang-python: Python"

    ```python linenums="1" title="Hive crawling with Kerberos"
    (
        HiveCrawler(client)
        .kerberos(
            principal="hive/_HOST@EXAMPLE.COM", # (1)
            service_name="hive", # (2)
            keytab_file=keytab_contents, # (3)
            krb5_conf_file=krb5_contents, # (4)
            kerberos_type="...", # (5)
            host="hive.example.com",
        )
        .connection(name="production-hive", admin_roles=[...])
        .run(name="hive-prod")
    )
    ```

    1. **Required.** The Kerberos principal.
    2. **Required.** The service name.
    3. **Required.** The keytab file contents.
    4. **Required.** The `krb5.conf` file contents.
    5. **Required.** The Kerberos connection type. TLS material
       (`ca_cert_file`/`client_cert_file`/`client_key_file`/`client_key_passphrase`)
       and `default_schema`/`database_name`/`host`/`port` are optional.

## Configuration options

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Hive metadata configuration"
    (
        HiveCrawler(client)
        .basic(username="atlan_user", password="••••••", host="...")
        .connection(name="production-hive", admin_roles=[...])
        .include_metadata({"default": ["*"]}) # (1)
        .exclude_metadata({"default": ["tmp"]}) # (2)
        .allow_partial_success(True) # (3)
        .advanced_config("...") # (4)
        .run(name="hive-prod")
    )
    ```

    1. Databases/schemas to include, as `{database: [schema, ...]}`.
    2. Databases/schemas to exclude.
    3. Ingest the assets Atlan can read even when some are blocked by permissions.
       Enable only if you understand the permission limitations.
    4. Advanced workflow configuration — leave unset unless you know you need it.
