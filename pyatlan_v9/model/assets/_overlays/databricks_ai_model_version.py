# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        model_qualified_name: str,
        version: int | str,
        name: str | None = None,
    ) -> "DatabricksAIModelVersion":
        validate_required_fields(
            ["model_qualified_name", "version"], [model_qualified_name, version]
        )
        fields = model_qualified_name.split("/")
        if len(fields) != 6:
            raise ValueError(
                f"Invalid model_qualified_name: {model_qualified_name}. "
                "Expected format: default/connector/connection_id/catalog/schema/model"
            )
        connection_qn = "/".join(fields[:3])
        return cls(
            name=name or f"{fields[5]}_v{version}",
            qualified_name=f"{model_qualified_name}/version/{version}",
            database_name=fields[3],
            database_qualified_name=f"{connection_qn}/{fields[3]}",
            schema_name=fields[4],
            schema_qualified_name="/".join(fields[:5]),
            connector_name=fields[1],
            connection_qualified_name=connection_qn,
            ai_model_qualified_name=model_qualified_name,
            databricks_ai_model_version_id=int(version),
            databricks_ai_model_context=RelatedDatabricksAIModelContext(
                qualified_name=model_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksAIModelVersion":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksAIModelVersion":
        return cls.updater(**kwargs)
