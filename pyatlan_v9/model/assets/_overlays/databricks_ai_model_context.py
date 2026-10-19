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
    ) -> "DatabricksAIModelContext":
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        fields = schema_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid schema_qualified_name: {schema_qualified_name}. "
                "Expected format: default/connector/connection_id/catalog/schema"
            )
        connection_qn = connection_qualified_name or "/".join(fields[:3])
        db_name = database_name or fields[3]
        return cls(
            name=name,
            qualified_name=f"{schema_qualified_name}/{name}",
            database_name=db_name,
            database_qualified_name=database_qualified_name
            or f"{connection_qn}/{db_name}",
            schema_name=schema_name or fields[4],
            schema_qualified_name=schema_qualified_name,
            connector_name=fields[1],
            connection_qualified_name=connection_qn,
            databricks_ai_model_schema=RelatedSchema(
                qualified_name=schema_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksAIModelContext":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksAIModelContext":
        return cls.updater(**kwargs)
