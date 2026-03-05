# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        data_studio_asset_type: str,
    ) -> "DataStudioAsset":
        """Create a new DataStudioAsset asset."""
        validate_required_fields(
            ["name", "connection_qualified_name", "data_studio_asset_type"],
            [name, connection_qualified_name, data_studio_asset_type],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connector_name=connector_name,
            data_studio_asset_type=data_studio_asset_type,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DataStudioAsset":
        """Create a DataStudioAsset instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DataStudioAsset":
        """Return only fields required for update operations."""
        return DataStudioAsset.updater(
            qualified_name=self.qualified_name,
            name=self.name,
        )
