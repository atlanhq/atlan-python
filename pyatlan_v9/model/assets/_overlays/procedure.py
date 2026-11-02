# INTERNAL_IMPORT: from pyatlan.utils import init_guid, resolve_sql_parents, validate_required_fields

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
    ) -> "Procedure":
        validate_required_fields(
            ["name", "definition", "schema_qualified_name"],
            [name, definition, schema_qualified_name],
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
        procedure = cls(
            name=name,
            definition=definition,
            qualified_name=f"{sch_qualified_name}/_procedures_/{name}",
            schema_name=sch_name,
            schema_qualified_name=sch_qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            atlan_schema=RelatedSchema(qualified_name=sch_qualified_name),
        )
        if db_qualified_name is not None:
            procedure.database_name = db_name
            procedure.database_qualified_name = db_qualified_name
        return procedure

    @classmethod
    def updater(
        cls,
        *,
        qualified_name: str,
        name: str,
        definition: str = "",
    ) -> "Procedure":
        validate_required_fields(
            ["qualified_name", "name"],
            [qualified_name, name],
        )
        proc = cls(qualified_name=qualified_name, name=name)
        if definition:
            proc.definition = definition
        return proc

    def trim_to_required(self) -> "Procedure":
        return Procedure.updater(
            qualified_name=self.qualified_name or "",
            name=self.name or "",
            definition=self.definition or "",
        )

    @classmethod
    def create(cls, **kwargs) -> "Procedure":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "Procedure":
        return cls.updater(**kwargs)
