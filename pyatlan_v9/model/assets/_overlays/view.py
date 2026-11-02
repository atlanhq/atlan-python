# INTERNAL_IMPORT: from pyatlan.utils import init_guid, resolve_sql_parents, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
        schema_name: str | None = None,
        database_name: str | None = None,
        database_qualified_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "View":
        """
        Create a new View asset with auto-derived fields.

        Args:
            name: Simple name of the view
            schema_qualified_name: Unique name of the schema in which this view exists
            schema_name: Simple name of the schema (auto-derived if not provided)
            database_name: Simple name of the database (auto-derived if not provided)
            database_qualified_name: Unique name of the database (auto-derived if not provided)
            connection_qualified_name: Unique name of the connection (auto-derived if not provided)

        Returns:
            New View instance with all fields populated

        Without ``connection_qualified_name``, ``schema_qualified_name`` must have the standard
        5 segments (default/connector/connection_id/database/schema) and the other parents are
        derived from it. With ``connection_qualified_name``, parents of any depth are accepted.

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        (
            connection_qn,
            connector_name,
            db_name,
            db_qualified_name,
            sch_name,
            sch_qualified_name,
        ) = resolve_sql_parents(
            schema_qualified_name=schema_qualified_name,
            schema_name=schema_name,
            database_name=database_name,
            database_qualified_name=database_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        view = cls(
            name=name,
            qualified_name=f"{sch_qualified_name}/{name}",
            schema_name=sch_name,
            schema_qualified_name=sch_qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            atlan_schema=RelatedSchema(qualified_name=sch_qualified_name),
        )
        if db_qualified_name is not None:
            view.database_name = db_name
            view.database_qualified_name = db_qualified_name
        return view

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "View":
        """
        Create a View instance for updating an existing asset.

        Args:
            qualified_name: Unique name of the view to update
            name: Simple name of the view

        Returns:
            View instance configured for updates

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "View":
        """
        Return a View with only required fields for reference.

        Returns:
            View instance with only qualified_name and name set
        """
        return View(qualified_name=self.qualified_name, name=self.name)

    @classmethod
    def create(cls, **kwargs) -> "View":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "View":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
