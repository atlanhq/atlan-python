# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> "IcebergCatalog":
        """
        Create a new IcebergCatalog asset.

        Args:
            name: Name of the catalog
            connection_qualified_name: Unique name of the connection in which this catalog exists

        Returns:
            IcebergCatalog instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        if len(fields) != 3:
            raise ValueError(
                f"Invalid connection_qualified_name: {connection_qualified_name}. "
                "Expected format: default/connector/connection_id"
            )
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
        )

    @classmethod
    def create(cls, **kwargs) -> "IcebergCatalog":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "IcebergCatalog":
        return cls.updater(**kwargs)
