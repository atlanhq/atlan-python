# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        quick_sight_id: str,
        quick_sight_dashboard_folders: Union[list[str], None] = None,
    ) -> "QuickSightDashboard":
        """Create a new QuickSightDashboard asset."""
        validate_required_fields(
            ["name", "connection_qualified_name", "quick_sight_id"],
            [name, connection_qualified_name, quick_sight_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        folder_refs = (
            [
                RelatedQuickSightFolder(unique_attributes={"qualifiedName": folder_qn})
                for folder_qn in quick_sight_dashboard_folders
            ]
            if quick_sight_dashboard_folders
            else UNSET
        )
        return cls(
            name=name,
            quick_sight_id=quick_sight_id,
            qualified_name=f"{connection_qualified_name}/{quick_sight_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            quick_sight_dashboard_folders=folder_refs,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "QuickSightDashboard":
        """Create a QuickSightDashboard instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "QuickSightDashboard":
        """Return only fields required for update operations."""
        return QuickSightDashboard.updater(
            qualified_name=self.qualified_name, name=self.name
        )
