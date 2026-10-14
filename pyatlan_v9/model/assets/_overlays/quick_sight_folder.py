# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        quick_sight_id: str,
        quick_sight_folder_type: Union[str, None] = None,
    ) -> "QuickSightFolder":
        validate_required_fields(
            ["name", "connection_qualified_name", "quick_sight_id"],
            [name, connection_qualified_name, quick_sight_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        qualified_name = f"{connection_qualified_name}/{quick_sight_id}"
        return cls(
            name=name,
            quick_sight_id=quick_sight_id,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            quick_sight_folder_type=quick_sight_folder_type
            if quick_sight_folder_type is not None
            else UNSET,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "QuickSightFolder":
        """Create a QuickSightFolder instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "QuickSightFolder":
        """Return only fields required for update operations."""
        return QuickSightFolder.updater(
            qualified_name=self.qualified_name, name=self.name
        )
