# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        qlik_id: str,
    ) -> "QlikStream":
        """Build a Qlik stream; qualifiedName is {connection}/stream/{qlik_id}."""
        validate_required_fields(
            ["name", "connection_qualified_name", "qlik_id"],
            [name, connection_qualified_name, qlik_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/stream/{qlik_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            qlik_id=qlik_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "QlikStream":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "QlikStream":
        return cls.updater(**kwargs)
