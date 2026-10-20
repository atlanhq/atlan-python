# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        data_pipeline_qualified_name: str,
    ) -> "FabricActivity":
        validate_required_fields(
            ["name", "data_pipeline_qualified_name"],
            [name, data_pipeline_qualified_name],
        )
        fields = data_pipeline_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid data_pipeline_qualified_name: "
                f"{data_pipeline_qualified_name}. "
                "Expected format: "
                "default/fabric/<epoch>/<workspace_id>/<data_pipeline_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{data_pipeline_qualified_name}/{name}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_space_qualified_name="/".join(fields[:4]),
            fabric_data_pipeline=RelatedFabricDataPipeline(
                qualified_name=data_pipeline_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "FabricActivity":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "FabricActivity":
        return cls.updater(**kwargs)
