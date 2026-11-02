# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        resource_id: str,
        connection_qualified_name: Union[str, None] = None,
        parent_folder_qualified_name: Union[str, None] = None,
        parent_folder_name: Union[str, None] = None,
    ) -> "SapAnalyticsCloudStory":
        """
        Create a new SapAnalyticsCloudStory asset.

        A story outside any folder hangs directly off the connection (pass
        connection_qualified_name); otherwise it hangs off the folder that
        directly contains it (pass parent_folder_qualified_name), at any depth.
        """
        validate_required_fields(["name", "resource_id"], [name, resource_id])
        if parent_folder_qualified_name:
            # A folder qualifiedName is {connection_qn}/{resource_id}[/{resource_id}...].
            parts = parent_folder_qualified_name.split("/")
            if len(parts) < 4:
                raise ValueError("parent_folder_qualified_name is invalid")
            if not connection_qualified_name:
                connection_qualified_name = "/".join(parts[:3])
        validate_required_fields(
            ["connection_qualified_name"], [connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        parent_qualified_name = parent_folder_qualified_name or connection_qualified_name
        return cls(
            name=name,
            sap_analytics_cloud_resource_id=resource_id,
            qualified_name=f"{parent_qualified_name}/{resource_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            sap_analytics_cloud_parent_folder_qualified_name=parent_folder_qualified_name
            or UNSET,
            sap_analytics_cloud_parent_folder_name=parent_folder_name
            if parent_folder_name is not None
            else UNSET,
            sap_analytics_cloud_folder=RelatedSapAnalyticsCloudFolder(
                unique_attributes={"qualifiedName": parent_folder_qualified_name}
            )
            if parent_folder_qualified_name
            else UNSET,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SapAnalyticsCloudStory":
        """Create a SapAnalyticsCloudStory instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SapAnalyticsCloudStory":
        """Return only fields required for update operations."""
        return SapAnalyticsCloudStory.updater(
            qualified_name=self.qualified_name, name=self.name
        )
