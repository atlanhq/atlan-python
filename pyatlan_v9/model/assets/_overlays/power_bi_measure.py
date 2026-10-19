# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        power_bi_table_qualified_name: str,
    ) -> "PowerBIMeasure":
        validate_required_fields(
            ["name", "power_bi_table_qualified_name"],
            [name, power_bi_table_qualified_name],
        )
        # Table names may contain "/", so only the leading segments are fixed.
        fields = power_bi_table_qualified_name.split("/")
        if len(fields) < 6 or not all(fields[:5]):
            raise ValueError("power_bi_table_qualified_name is invalid")
        return cls(
            name=name,
            qualified_name=f"{power_bi_table_qualified_name}/{name}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            workspace_qualified_name="/".join(fields[:4]),
            dataset_qualified_name="/".join(fields[:5]),
            power_bi_table_qualified_name=power_bi_table_qualified_name,
            table=RelatedPowerBITable(
                unique_attributes={"qualifiedName": power_bi_table_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "PowerBIMeasure":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "PowerBIMeasure":
        return cls.updater(**kwargs)
