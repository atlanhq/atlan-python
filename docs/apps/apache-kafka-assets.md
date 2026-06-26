---
title: Apache Kafka assets app
description: Learn how to crawl Apache Kafka topics and publish them to Atlan for discovery.
---

# Apache Kafka assets app

The Apache Kafka assets app crawls Kafka topics (and, optionally, schema-registry
subjects) from a self-managed Apache Kafka cluster and publishes them to Atlan.
Build it with the `KafkaApache` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a **new** connection and new assets. To re-crawl, re-run the
    **existing** workflow (see
    [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

Apache Kafka supports four authentication methods: **SASL basic**, **SCRAM**,
**mTLS**, and **no auth**. All accept schema-registry settings.

## SASL basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Apache Kafka crawling with SASL basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import KafkaApache

    client = AtlanClient()

    response = (
        KafkaApache(client)
        .basic( # (1)
            username="kafka_user", # (2)
            password="••••••", # (3)
            security_protocol="SASL_SSL", # (4)
            include_schema_registry="false", # (5)
            host="broker1.example.com:9092", # (6)
        )
        .connection(
            name="production-kafka",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .skip_internal_topics(True) # (7)
        .run(name="apache-kafka-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** SASL username/password auth; the secret is vaulted.
    2. **Required.** Username.
    3. **Required.** Password.
    4. **Required.** Security protocol (e.g. `SASL_SSL`).
    5. **Required.** Whether to include the schema registry. When `"true"`, also pass
       `schema_registry_host=`, `schema_registry_username=`, and
       `schema_registry_password=`.
    6. **Required.** The bootstrap server (`host:port`).
    7. **Step 3 — Metadata.** Skip Kafka's internal topics (takes priority over the
       include/exclude filters).

## SCRAM, mTLS, and no-auth

=== ":lang-python: Python"

    ```python linenums="1" title="Other Apache Kafka auth methods"
    # SCRAM
    KafkaApache(client).scram(
        username="kafka_user", password="••••••",
        security_protocol="SASL_SSL", sasl_mechanism="SCRAM-SHA-256", # (1)
        include_schema_registry="false", host="broker1.example.com:9092",
    )

    # mTLS (client certificates)
    KafkaApache(client).mtls(
        mtls_cert=cert_bundle, # (2)
        key_password="••••••", # (3)
        include_schema_registry="false", host="broker1.example.com:9092",
    )

    # No auth
    KafkaApache(client).noauth(
        security_protocol="PLAINTEXT", # (4)
        include_schema_registry="false", host="broker1.example.com:9092",
    )
    ```

    1. **Required (SCRAM).** The SASL mechanism (e.g. `SCRAM-SHA-256`).
    2. **Required (mTLS).** The client certificate bundle.
    3. *Optional (mTLS).* The private-key password.
    4. **Required (no-auth).** The security protocol (e.g. `PLAINTEXT`).

## Topic filters

All metadata options are **optional**:

=== ":lang-python: Python"

    ```python linenums="1" title="Apache Kafka topic filters"
    (
        KafkaApache(client)
        .basic(username="kafka_user", password="••••••", security_protocol="SASL_SSL",
               include_schema_registry="false", host="broker1.example.com:9092")
        .connection(name="production-kafka", admin_roles=[...])
        .skip_internal_topics(True) # (1)
        .include_topic_regex("^prod\\..*") # (2)
        .exclude_topic_regex(".*\\.internal$") # (3)
        .run(name="apache-kafka-prod")
    )
    ```

    1. Skip Kafka's internal topics — takes priority over the filters below.
    2. Regex of topics to include (default: everything).
    3. Regex of topics to exclude — takes priority over include.
