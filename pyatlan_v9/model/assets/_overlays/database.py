# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> "Database":
        """
        Create a new Database asset.

        Args:
            name: Name of the database
            connection_qualified_name: Unique name of the connection in which this database exists

        Returns:
            Database instance ready to be created

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

        connector_name = fields[1]
        qualified_name = f"{connection_qualified_name}/{name}"

        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def create(cls, *, name: str, connection_qualified_name: str) -> "Database":
        """
        Create a new Database asset (deprecated - use creator instead).

        Args:
            name: Name of the database
            connection_qualified_name: Unique name of the connection in which this database exists

        Returns:
            Database instance ready to be created
        """
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )
