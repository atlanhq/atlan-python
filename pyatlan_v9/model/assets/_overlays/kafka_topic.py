# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> "KafkaTopic":
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        qualified_name = f"{connection_qualified_name}/topic/{name}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
        )

    @classmethod
    def create(cls, **kwargs) -> "KafkaTopic":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "KafkaTopic":
        return cls.updater(**kwargs)
