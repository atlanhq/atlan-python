# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        quick_sight_id: str,
        quick_sight_import_mode: Union[str, None] = None,
        quick_sight_dataset_folders: Union[list[str], None] = None,
    ) -> "QuickSightDataset":
        """Create a new QuickSightDataset asset."""
        validate_required_fields(
            ["name", "connection_qualified_name", "quick_sight_id"],
            [name, connection_qualified_name, quick_sight_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        folder_refs = (
            [
                RelatedQuickSightFolder(unique_attributes={"qualifiedName": folder_qn})
                for folder_qn in quick_sight_dataset_folders
            ]
            if quick_sight_dataset_folders
            else UNSET
        )
        return cls(
            name=name,
            quick_sight_id=quick_sight_id,
            qualified_name=f"{connection_qualified_name}/{quick_sight_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            quick_sight_import_mode=quick_sight_import_mode
            if quick_sight_import_mode is not None
            else UNSET,
            quick_sight_dataset_folders=folder_refs,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "QuickSightDataset":
        """Create a QuickSightDataset instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "QuickSightDataset":
        """Return only fields required for update operations."""
        return QuickSightDataset.updater(
            qualified_name=self.qualified_name, name=self.name
        )
