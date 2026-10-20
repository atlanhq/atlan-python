# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        dataset_qualified_name: str,
    ) -> "PowerBITable":
        validate_required_fields(
            ["name", "dataset_qualified_name"],
            [name, dataset_qualified_name],
        )
        fields = dataset_qualified_name.split("/")
        if len(fields) != 5 or not all(fields):
            raise ValueError("dataset_qualified_name is invalid")
        return cls(
            name=name,
            qualified_name=f"{dataset_qualified_name}/{name}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            workspace_qualified_name="/".join(fields[:4]),
            dataset_qualified_name=dataset_qualified_name,
            dataset=RelatedPowerBIDataset(
                unique_attributes={"qualifiedName": dataset_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "PowerBITable":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "PowerBITable":
        return cls.updater(**kwargs)
