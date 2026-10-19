# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        allowed_values: list[str] | None = None,
    ) -> "DatabricksUnityCatalogTag":
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        tag = cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/tag/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )
        if allowed_values is not None:
            tag.tag_allowed_values = allowed_values
        return tag

    @classmethod
    def create(cls, **kwargs) -> "DatabricksUnityCatalogTag":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksUnityCatalogTag":
        return cls.updater(**kwargs)
