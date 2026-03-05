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
    ) -> "Table":
        """
        Create a new Table asset.

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
