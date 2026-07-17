# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        metabase_id: str,
    ) -> "MetabaseDashboard":
        validate_required_fields(
            ["name", "connection_qualified_name", "metabase_id"],
            [name, connection_qualified_name, metabase_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/dashboards/{metabase_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def create(cls, **kwargs) -> "MetabaseDashboard":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "MetabaseDashboard":
        return cls.updater(**kwargs)
