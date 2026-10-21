# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        domo_dataset_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "DomoDatasetColumn":
        """Create a new DomoDatasetColumn asset."""
        validate_required_fields(
            ["name", "domo_dataset_qualified_name"],
            [name, domo_dataset_qualified_name],
        )
        # A dataset qualifiedName is {connection_qn}/dataset/{domo_id}.
        parts = domo_dataset_qualified_name.split("/")
        if len(parts) < 5:
            raise ValueError("domo_dataset_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{domo_dataset_qualified_name}/column/{name}",
            domo_dataset_qualified_name=domo_dataset_qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            domo_dataset=RelatedDomoDataset(
                unique_attributes={"qualifiedName": domo_dataset_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DomoDatasetColumn":
        """Create a DomoDatasetColumn instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DomoDatasetColumn":
        """Return only fields required for update operations."""
        return DomoDatasetColumn.updater(
            qualified_name=self.qualified_name, name=self.name
        )
