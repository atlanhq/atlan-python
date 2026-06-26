---
title: Apache Kafka assets app
description: Learn how to crawl Apache Kafka and publish to Atlan for discovery.
---

# Apache Kafka assets app

The Apache Kafka assets app crawls Apache Kafka assets and publishes to Atlan. Build it with the `KafkaApache` builder.

!!! warning "Creating an app creates a new connection"
    Each create mints a new connection and new assets. To re-crawl, re-run the
    existing workflow (see [Re-run an existing app](manage-apps.md#re-run-an-existing-app)).

## Basic authentication

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

=== ":lang-python: Python"

    ```python linenums="1" title="Apache Kafka assets crawling with basic auth"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import KafkaApache

    client = AtlanClient()

    response = (
        KafkaApache(client)
        .basic(
            username="...",  # (1)
            password="...",  # (2)
            security_protocol="...",  # (3)
            include_schema_registry="...",  # (4)
            schema_registry_host="...",  # (5)
            schema_registry_username="...",  # (6)
            schema_registry_password="...",  # (7)
            host="...",  # (8)
        )
        .connection(  # (9)
            name="production-apache-kafka",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .run(name="apache-kafka-prod")  # (10)
    )
    print(response.slug, response.run_id)
    ```

    1. Username.
    2. Password.
    3. Security protocol.
    4. Include Schema Registry.
    5. Schema registry host.
    6. API Key.
    7. API Secret.
    8. Host.
    9. Display name + at least one admin (role, group, or user).
    10. `.run()` creates and submits a run; use `.create()` to create without running.

## Other authentication methods

=== ":lang-python: Python"

    ```python linenums="1" title="Alternate auth methods"
    KafkaApache(client).mtls(mtls_cert="...", include_schema_registry="...", host="...")
    KafkaApache(client).noauth(security_protocol="...", include_schema_registry="...", host="...")
    KafkaApache(client).scram(username="...", password="...", security_protocol="...", sasl_mechanism="...", include_schema_registry="...", host="...")
    ```

## Configuration options

=== ":lang-python: Python"

    ```python linenums="1" title="Metadata configuration"
    (
        KafkaApache(client)
        .basic(...)
        .connection(name="production-apache-kafka", admin_roles=[...])
        .exclude_topic_regex("...")  # (1)
        .include_topic_regex("...")  # (2)
        .preflight_check("...")  # (3)
        .skip_internal_topics(True)  # (4)
        .run(name="apache-kafka-prod")
    )
    ```

    1. Exclude topic regex — Regex of kafka topics to ignore. By default, nothing will be excluded. This takes priority over include regex.
    2. Include topic regex — Regex of kafka topics to include.  By default, everything will be included.
    3. preflight_check
    4. Skip internal topics — Skip Kafka's internal topics (e.g. __consumer_offsets, _schemas etc). This takes priority over other filters.
