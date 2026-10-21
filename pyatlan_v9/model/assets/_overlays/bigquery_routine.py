# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        definition: str,
        schema_qualified_name: str,
        schema_name: str | None = None,
        database_name: str | None = None,
        database_qualified_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "BigqueryRoutine":
        """
        Builds the minimal object necessary to create a BigqueryRoutine.

        The qualifiedName is ``{schema_qualified_name}/_routines_/{name}``, the shape
        BigqueryRoutine assets carry on tenants and that atlan-dataplex-app aspect-sync
        parses. Current atlan-bigquery-app crawls emit ``Function`` / ``Procedure``
        instead of BigqueryRoutine.
        """
        validate_required_fields(
            ["name", "definition", "schema_qualified_name"],
            [name, definition, schema_qualified_name],
        )

        fields = schema_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid schema_qualified_name: {schema_qualified_name}. "
                "Expected format: default/bigquery/connection_id/project/dataset"
            )

        connector_name = fields[1]
        connection_qn = (
            connection_qualified_name or f"{fields[0]}/{fields[1]}/{fields[2]}"
        )
        db_name = database_name or fields[3]
        sch_name = schema_name or fields[4]
        db_qualified_name = database_qualified_name or f"{connection_qn}/{db_name}"

        return cls(
            name=name,
            definition=definition,
            qualified_name=f"{schema_qualified_name}/_routines_/{name}",
            database_name=db_name,
            database_qualified_name=db_qualified_name,
            schema_name=sch_name,
            schema_qualified_name=schema_qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            atlan_schema=RelatedSchema(qualified_name=schema_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "BigqueryRoutine":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "BigqueryRoutine":
        return cls.updater(**kwargs)
