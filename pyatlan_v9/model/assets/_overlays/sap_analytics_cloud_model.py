# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        resource_id: Union[str, None] = None,
        model_id: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
        parent_folder_qualified_name: Union[str, None] = None,
        parent_folder_name: Union[str, None] = None,
    ) -> "SapAnalyticsCloudModel":
        """
        Create a new SapAnalyticsCloudModel asset.

        An Import model is a file-repository resource, named by its
        resource_id under the folder that directly contains it (pass
        parent_folder_qualified_name) or under the connection when it has no
        folder. A Live model is not a file-repository resource: it has no
        folder and is named by its model_id under the connection.
        """
        validate_required_fields(["name"], [name])
        if not resource_id and not model_id:
            raise ValueError("One of resource_id or model_id is required")
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
            sap_analytics_cloud_resource_id=resource_id or UNSET,
            sap_analytics_cloud_model_id=model_id or UNSET,
            qualified_name=f"{parent_qualified_name}/{resource_id or model_id}",
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
    def updater(cls, *, qualified_name: str, name: str) -> "SapAnalyticsCloudModel":
        """Create a SapAnalyticsCloudModel instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SapAnalyticsCloudModel":
        """Return only fields required for update operations."""
        return SapAnalyticsCloudModel.updater(
            qualified_name=self.qualified_name, name=self.name
        )
