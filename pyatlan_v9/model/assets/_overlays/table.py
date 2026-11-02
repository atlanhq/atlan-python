# INTERNAL_IMPORT: from pyatlan.utils import init_guid, resolve_sql_parents, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str | None = None,
        schema_name: str | None = None,
        database_name: str | None = None,
        database_qualified_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "Table":
        """
        Create a new Table asset.

        Without ``connection_qualified_name``, ``schema_qualified_name`` must have the standard
        5 segments (default/connector/connection_id/database/schema) and the other parents are
        derived from it. With ``connection_qualified_name``, parents of any depth are accepted,
        and ``schema_qualified_name`` may be omitted for a table directly under the connection
        (qualifiedName ``{connection_qualified_name}/{name}``).

        Args:
            name: Name of the table
            schema_qualified_name: Unique name of the schema in which this table exists
            schema_name: Simple name of the schema (optional, will be derived if not provided)
            database_name: Simple name of the database (optional, will be derived if not provided)
            database_qualified_name: Unique name of the database (optional, will be derived if not provided)
            connection_qualified_name: Unique name of the connection (optional, will be derived if not provided)

        Returns:
            Table instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(["name"], [name])
        if schema_qualified_name is None and connection_qualified_name is None:
            raise ValueError("schema_qualified_name is required")
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
        table = cls(
            name=name,
            qualified_name=f"{sch_qualified_name or connection_qn}/{name}",
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
        )
        if db_qualified_name is not None:
            table.database_name = db_name
            table.database_qualified_name = db_qualified_name
        if sch_qualified_name is not None:
            table.schema_name = sch_name
            table.schema_qualified_name = sch_qualified_name
            table.atlan_schema = RelatedSchema(qualified_name=sch_qualified_name)
        return table

    @classmethod
    def create(cls, *, name: str, schema_qualified_name: str) -> "Table":
        """
        Create a new Table asset (deprecated - use creator instead).

        Args:
            name: Name of the table
            schema_qualified_name: Unique name of the schema in which this table exists

        Returns:
            Table instance ready to be created
        """
        return cls.creator(name=name, schema_qualified_name=schema_qualified_name)
