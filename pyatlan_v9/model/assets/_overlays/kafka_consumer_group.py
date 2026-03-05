# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        kafka_topic_qualified_names: list[str],
    ) -> "KafkaConsumerGroup":
        validate_required_fields(
            ["name", "kafka_topic_qualified_names"],
            [name, kafka_topic_qualified_names],
        )
        # Extract connection from the first topic qualified name
        first_topic_qn = kafka_topic_qualified_names[0]
        fields = first_topic_qn.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qn = (
            f"{fields[0]}/{fields[1]}/{fields[2]}" if len(fields) >= 3 else None
        )
        qualified_name = f"{connection_qn}/consumer-group/{name}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            kafka_topic_qualified_names=set(kafka_topic_qualified_names),
        )

    @classmethod
    def create(cls, **kwargs) -> "KafkaConsumerGroup":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "KafkaConsumerGroup":
        return cls.updater(**kwargs)
