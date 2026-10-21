# INTERNAL_IMPORT: from pyatlan.utils import init_guid, resolve_database_parent, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str | None = None,
        database_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "Schema":
        """
        Create a new Schema asset with auto-derived fields.

        Without ``connection_qualified_name``, ``database_qualified_name`` must have the standard
        4 segments (default/connector/connection_id/database) and the other parents are derived
        from it. With ``connection_qualified_name``, a database of any depth is accepted, and
        ``database_qualified_name`` may be omitted for a schema directly under the connection
        (qualifiedName ``{connection_qualified_name}/{name}``).

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
        validate_required_fields(["name"], [name])
        if database_qualified_name is None and connection_qualified_name is None:
            raise ValueError("database_qualified_name is required")
        connection_qn, connector_name, db_name, db_qualified_name = (
            resolve_database_parent(
                database_qualified_name=database_qualified_name,
                database_name=database_name,
                connection_qualified_name=connection_qualified_name,
            )
        )
        sch = cls(
            name=name,
            qualified_name=f"{db_qualified_name or connection_qn}/{name}",
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
        )
        if db_qualified_name is not None:
            sch.database_name = db_name
            sch.database_qualified_name = db_qualified_name
            sch.database = RelatedDatabase(qualified_name=db_qualified_name)
        return sch

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
