# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        dataflow_qualified_name: str,
        dataflow_name: str,
        entity_name: str,
    ) -> "FabricDataflowEntityColumn":
        validate_required_fields(
            ["name", "dataflow_qualified_name", "dataflow_name", "entity_name"],
            [name, dataflow_qualified_name, dataflow_name, entity_name],
        )
        fields = dataflow_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid dataflow_qualified_name: {dataflow_qualified_name}. "
                "Expected format: default/fabric/<epoch>/<workspace_id>/<dataflow_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{dataflow_qualified_name}/{entity_name}/{name}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_space_qualified_name="/".join(fields[:4]),
            fabric_dataflow_qualified_name=dataflow_qualified_name,
            fabric_dataflow_name=dataflow_name,
            fabric_dataflow=RelatedFabricDataflow(
                qualified_name=dataflow_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "FabricDataflowEntityColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "FabricDataflowEntityColumn":
        return cls.updater(**kwargs)
