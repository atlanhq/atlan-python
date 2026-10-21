# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        kafka_topic_qualified_name: str,
        parent_field_path: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "KafkaField":
        """Create a new KafkaField asset.

        ``name`` is the full dotted field path (for example ``address.city``),
        as the Kafka app emits it, not the leaf name. Pass ``parent_field_path``
        for nested fields; it must be a dotted prefix of ``name``.
        """
        validate_required_fields(
            ["name", "kafka_topic_qualified_name"],
            [name, kafka_topic_qualified_name],
        )
        # A topic qualifiedName is {connection_qn}/topic/{topic_name}.
        parts = kafka_topic_qualified_name.split("/")
        if len(parts) < 5 or parts[-2] != "topic":
            raise ValueError("kafka_topic_qualified_name is invalid")
        if parent_field_path is not None and not name.startswith(
            f"{parent_field_path}."
        ):
            raise ValueError("parent_field_path is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:-2])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{kafka_topic_qualified_name}/field/{name}",
            kafka_topic_qualified_name=kafka_topic_qualified_name,
            kafka_parent_field_qualified_name=f"{kafka_topic_qualified_name}/field/{parent_field_path}"
            if parent_field_path is not None
            else UNSET,
            kafka_parent_field_name=parent_field_path
            if parent_field_path is not None
            else UNSET,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            kafka_topic=RelatedKafkaTopic(
                unique_attributes={"qualifiedName": kafka_topic_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "KafkaField":
        """Create a KafkaField instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "KafkaField":
        """Return only fields required for update operations."""
        return KafkaField.updater(qualified_name=self.qualified_name, name=self.name)
