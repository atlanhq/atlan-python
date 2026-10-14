# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        power_bi_dataflow_qualified_name: str,
        entity_name: str,
        column_name: str,
        name: Union[str, None] = None,
    ) -> "PowerBIDataflowEntityColumn":
        validate_required_fields(
            ["power_bi_dataflow_qualified_name", "entity_name", "column_name"],
            [power_bi_dataflow_qualified_name, entity_name, column_name],
        )
        fields = power_bi_dataflow_qualified_name.split("/")
        if len(fields) != 5 or not all(fields):
            raise ValueError("power_bi_dataflow_qualified_name is invalid")
        return cls(
            name=name if name is not None else f"{entity_name} -> {column_name}",
            qualified_name=(
                f"{power_bi_dataflow_qualified_name}/{entity_name}/{column_name}"
            ),
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            power_bi_workspace_qualified_name="/".join(fields[:4]),
            power_bi_dataflow_qualified_name=power_bi_dataflow_qualified_name,
            power_bi_dataflow_entity_name=entity_name,
            power_bi_dataflow=RelatedPowerBIDataflow(
                unique_attributes={"qualifiedName": power_bi_dataflow_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "PowerBIDataflowEntityColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "PowerBIDataflowEntityColumn":
        return cls.updater(**kwargs)
