# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

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
    ) -> "MaterialisedView":
        """
        Create a new MaterialisedView asset with auto-derived fields.

        Args:
            name: Simple name of the materialized view
            schema_qualified_name: Unique name of the schema in which this materialized view exists
            schema_name: Simple name of the schema (auto-derived if not provided)
            database_name: Simple name of the database (auto-derived if not provided)
            database_qualified_name: Unique name of the database (auto-derived if not provided)
            connection_qualified_name: Unique name of the connection (auto-derived if not provided)

        Returns:
            New MaterialisedView instance with all fields populated

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )

        fields = schema_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid schema_qualified_name: {schema_qualified_name}. "
                "Expected format: default/connector/connection_id/database/schema"
            )

        connector_name = fields[1]
        connection_qn = (
            connection_qualified_name or f"{fields[0]}/{fields[1]}/{fields[2]}"
        )
        db_name = database_name or fields[3]
        sch_name = schema_name or fields[4]
        db_qualified_name = database_qualified_name or f"{connection_qn}/{db_name}"
        qualified_name = f"{schema_qualified_name}/{name}"

        return cls(
            name=name,
            qualified_name=qualified_name,
            database_name=db_name,
            database_qualified_name=db_qualified_name,
            schema_name=sch_name,
            schema_qualified_name=schema_qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            atlan_schema=RelatedSchema(qualified_name=schema_qualified_name),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "MaterialisedView":
        """
        Create a MaterialisedView instance for updating an existing asset.

        Args:
            qualified_name: Unique name of the materialized view to update
            name: Simple name of the materialized view

        Returns:
            MaterialisedView instance configured for updates

        Raises:
            ValueError: If required parameters are missing
        """
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "MaterialisedView":
        """
        Return a MaterialisedView with only required fields for reference.

        Returns:
            MaterialisedView instance with only qualified_name and name set
        """
        return MaterialisedView(qualified_name=self.qualified_name, name=self.name)

    @classmethod
    def create(cls, **kwargs) -> "MaterialisedView":
        """Backward compatibility alias for creator()."""
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "MaterialisedView":
        """Backward compatibility alias for updater()."""
        return cls.updater(**kwargs)
