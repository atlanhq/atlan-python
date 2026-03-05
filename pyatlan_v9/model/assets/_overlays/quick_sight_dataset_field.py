# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        quick_sight_dataset_qualified_name: str,
        quick_sight_id: str,
        quick_sight_dataset_field_type: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "QuickSightDatasetField":
        """Create a new QuickSightDatasetField asset."""
        validate_required_fields(
            ["name", "quick_sight_dataset_qualified_name", "quick_sight_id"],
            [name, quick_sight_dataset_qualified_name, quick_sight_id],
        )
        if connection_qualified_name:
            connector_name = (
                connection_qualified_name.split("/")[1]
                if len(connection_qualified_name.split("/")) > 1
                else ""
            )
        else:
            fields = quick_sight_dataset_qualified_name.split("/")
            if len(fields) < 3:
                raise ValueError("quick_sight_dataset_qualified_name is invalid")
            connection_qualified_name = "/".join(fields[:3])
            connector_name = fields[1]
        return cls(
            name=name,
            quick_sight_id=quick_sight_id,
            quick_sight_dataset_qualified_name=quick_sight_dataset_qualified_name,
            qualified_name=f"{quick_sight_dataset_qualified_name}/{quick_sight_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            quick_sight_dataset_field_type=quick_sight_dataset_field_type
            if quick_sight_dataset_field_type is not None
            else UNSET,
            quick_sight_dataset=RelatedQuickSightDataset(
                unique_attributes={"qualifiedName": quick_sight_dataset_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "QuickSightDatasetField":
        """Create a QuickSightDatasetField instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "QuickSightDatasetField":
        """Return only fields required for update operations."""
        return QuickSightDatasetField.updater(
            qualified_name=self.qualified_name, name=self.name
        )
