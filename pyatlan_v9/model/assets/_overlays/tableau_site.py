# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        site_id: str,
    ) -> "TableauSite":
        validate_required_fields(
            ["name", "connection_qualified_name", "site_id"],
            [name, connection_qualified_name, site_id],
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError(
                f"Invalid connection_qualified_name: {connection_qualified_name}. "
                "Expected format: default/tableau/<epoch>"
            )
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{site_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
        )

    @classmethod
    def create(cls, **kwargs) -> "TableauSite":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauSite":
        return cls.updater(**kwargs)
