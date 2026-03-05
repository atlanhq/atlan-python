# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
        database_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "Schema":
        """
        Create a new Schema asset with auto-derived fields.

        Args:
            name: Simple name of the schema
            database_qualified_name: Unique name of the database in which this schema exists
            database_name: Simple name of the database (auto-derived if not provided)
            connection_qualified_name: Unique name of the connection (auto-derived if not provided)

        Returns:
            New Schema instance with all fields populated

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )

        # Validate database_qualified_name format: default/connector/connection_id/database
        fields = database_qualified_name.split("/")
        if len(fields) != 4:
            raise ValueError(
                f"Invalid database_qualified_name: {database_qualified_name}. "
                "Expected format: default/connector/connection_id/database"
            )

        # Derive other fields from database_qualified_name
        connector_name = fields[1]
        connection_qn = (
            connection_qualified_name or f"{fields[0]}/{fields[1]}/{fields[2]}"
        )
        db_name = database_name or fields[3]
        qualified_name = f"{database_qualified_name}/{name}"

        return cls(
            name=name,
            qualified_name=qualified_name,
            database_name=db_name,
            database_qualified_name=database_qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            database=RelatedDatabase(qualified_name=database_qualified_name),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "Schema":
        """
        Create a Schema instance for updating an existing asset.

        Args:
            qualified_name: Unique name of the schema to update
            name: Simple name of the schema

        Returns:
            Schema instance configured for updates

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Schema":
        """
        Return a Schema with only required fields for reference.

        Returns:
            Schema instance with only qualified_name and name set
        """
        return Schema(qualified_name=self.qualified_name, name=self.name)

    @classmethod
    def create(cls, **kwargs) -> "Schema":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "Schema":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
