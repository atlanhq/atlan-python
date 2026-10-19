# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        scope_owner: str,
        connection_qualified_name: str,
    ) -> "ContextRepository":
        validate_required_fields(
            ["scope_owner", "connection_qualified_name"],
            [scope_owner, connection_qualified_name],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=scope_owner,
            qualified_name=f"{connection_qualified_name}/skills/{scope_owner}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def create(cls, **kwargs) -> "ContextRepository":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "ContextRepository":
        return cls.updater(**kwargs)
