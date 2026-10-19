# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        semantic_model_table_qualified_name: str,
    ) -> "FabricSemanticModelMeasure":
        validate_required_fields(
            ["name", "semantic_model_table_qualified_name"],
            [name, semantic_model_table_qualified_name],
        )
        fields = semantic_model_table_qualified_name.split("/")
        if len(fields) < 6:
            raise ValueError(
                f"Invalid semantic_model_table_qualified_name: "
                f"{semantic_model_table_qualified_name}. "
                "Expected format: "
                "default/fabric/<epoch>/<workspace_id>/<semantic_model_id>/<table_name>"
            )
        return cls(
            name=name,
            qualified_name=f"{semantic_model_table_qualified_name}/{name}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_space_qualified_name="/".join(fields[:4]),
            fabric_semantic_model_qualified_name="/".join(fields[:5]),
            fabric_semantic_model_table_name="/".join(fields[5:]),
            fabric_semantic_model_table_qualified_name=semantic_model_table_qualified_name,
            fabric_semantic_model_table=RelatedFabricSemanticModelTable(
                qualified_name=semantic_model_table_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "FabricSemanticModelMeasure":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "FabricSemanticModelMeasure":
        return cls.updater(**kwargs)
