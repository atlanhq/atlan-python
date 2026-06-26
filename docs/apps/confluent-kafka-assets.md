---
title: Confluent Kafka assets app
description: Learn how to crawl Confluent Kafka topics and publish them to Atlan for discovery.
---

# Confluent Kafka assets app

The Confluent Kafka assets app crawls Kafka topics (and, optionally, schema-registry
subjects) from Confluent Cloud and publishes them to Atlan. Build it with the
`KafkaConfluent` builder.

## API key / secret

<!-- md:python 9.8.0 -->
<!-- md:flag experimental -->

To crawl Confluent Kafka using an API key and secret:

=== ":lang-python: Python"

    ```python linenums="1" title="Confluent Kafka crawling with API key/secret"
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.apps import KafkaConfluent

    client = AtlanClient()

    response = (
        KafkaConfluent(client)
        .basic( # (1)
            host="pkc-abc12.us-east-2.aws.confluent.cloud:9092", # (2)
            username="ABCD1234EFGH5678", # (3)
            password="cflt...", # (4)
            security_protocol="SASL_SSL", # (5)
            include_cloud_metrics="false", # (6)
            include_schema_registry="false", # (7)
        )
        .connection(
            name="production-kafka",
            admin_roles=[client.role_cache.get_id_for_name("$admin")],
        )
        .skip_internal_topics(True) # (8)
        .run(name="kafka-prod")
    )
    print(response.slug, response.run_id)
    ```

    1. **Step 1 — Credential.** API key/secret auth; the secret is vaulted.
    2. The bootstrap server (`host:port`).
    3. The cluster API key.
    4. The cluster API secret.
    5. The security protocol (e.g. `SASL_SSL`).
    6. Whether to include Confluent Cloud metrics. When `"true"`, also provide
       `cloud_api_key=`, `cloud_api_secret=`, and `cluster_id=`.
    7. Whether to include the schema registry. When `"true"`, also provide
       `schema_registry_host=`, `schema_registry_username=`, and
       `schema_registry_password=`.
    8. **Step 3 — Metadata.** Skip Kafka's internal topics (e.g. `__consumer_offsets`).
       This takes priority over the include/exclude filters.

## With Cloud metrics and Schema Registry

=== ":lang-python: Python"

    ```python linenums="1" title="Include Cloud metrics + schema registry"
    (
        KafkaConfluent(client)
        .basic(
            host="pkc-abc12.us-east-2.aws.confluent.cloud:9092",
            username="ABCD1234EFGH5678",
            password="cflt...",
            security_protocol="SASL_SSL",
            include_cloud_metrics="true", # (1)
            cloud_api_key="...",
            cloud_api_secret="...",
            cluster_id="lkc-12345",
            include_schema_registry="true", # (2)
            schema_registry_host="https://psrc-abc12.us-east-2.aws.confluent.cloud",
            schema_registry_username="SR-KEY",
            schema_registry_password="SR-SECRET",
        )
        .connection(name="production-kafka", admin_roles=[...])
        .run(name="kafka-prod")
    )
    ```

    1. Enable Cloud metrics — requires the `cloud_api_key` / `cloud_api_secret` /
       `cluster_id` fields.
    2. Enable schema registry — requires the `schema_registry_*` fields.

## Topic filters

=== ":lang-python: Python"

    ```python linenums="1" title="Include / exclude topics by regex"
    (
        KafkaConfluent(client)
        .basic(host="...", username="...", password="...",
               security_protocol="SASL_SSL", include_cloud_metrics="false",
               include_schema_registry="false")
        .connection(name="production-kafka", admin_roles=[...])
        .include_topic_regex("^prod\\..*") # (1)
        .exclude_topic_regex(".*\\.internal$") # (2)
        .run(name="kafka-prod")
    )
    ```

    1. Regex of topics to include (default: everything).
    2. Regex of topics to exclude — takes priority over include.
