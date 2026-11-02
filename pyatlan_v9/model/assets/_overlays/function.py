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
        function_definition: str | None = None,
        function_language: str | None = None,
    ) -> "Function":
        """
        Create a new Function asset.

        Args:
            name: Name of the function
            schema_qualified_name: Unique name of the schema in which this function exists
            schema_name: Simple name of the schema (optional, will be derived if not provided)
            database_name: Simple name of the database (optional, will be derived if not provided)
            database_qualified_name: Unique name of the database (optional, will be derived if not provided)
            connection_qualified_name: Unique name of the connection (optional, will be derived
                if not provided; required when the schema is not at the standard
                default/connector/connection_id/database/schema depth)
            function_definition: Code or set of statements that determine the output of the function
            function_language: Programming language in which the function is written

        Returns:
            Function instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        connection_qn, connector_name, db_name, db_qualified_name, sch_name, _ = (
            resolve_sql_parents(
                schema_qualified_name=schema_qualified_name,
                schema_name=schema_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                connection_qualified_name=connection_qualified_name,
            )
        )

        function = cls(
            name=name,
            qualified_name=f"{schema_qualified_name}/{name}",
            schema_name=sch_name,
            schema_qualified_name=schema_qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            function_schema=RelatedSchema(qualified_name=schema_qualified_name),
            function_definition=(
                function_definition if function_definition is not None else UNSET
            ),
            function_language=(
                function_language if function_language is not None else UNSET
            ),
        )
        if db_qualified_name is not None:
            function.database_name = db_name
            function.database_qualified_name = db_qualified_name
        return function

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "Function":
        """Create a Function instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Function":
        """Return only fields required for update operations."""
        return Function.updater(qualified_name=self.qualified_name, name=self.name)
