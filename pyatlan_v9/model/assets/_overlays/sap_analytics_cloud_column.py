# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        sap_analytics_cloud_model_qualified_name: str,
        sap_analytics_cloud_model_name: str,
        order: int,
        parent_column_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SapAnalyticsCloudColumn":
        """
        Create a new SapAnalyticsCloudColumn asset.

        A measure or dimension is named under its model. A dimension's
        attribute or hierarchy level is named under the model and its parent
        dimension (pass parent_column_name), so attribute ``ID`` of dimension
        ``Account`` in model ``m`` has qualifiedName ``{m}/Account/ID``. Every
        column, at every depth, is contained by its model.
        """
        validate_required_fields(
            [
                "name",
                "sap_analytics_cloud_model_qualified_name",
                "sap_analytics_cloud_model_name",
                "order",
            ],
            [
                name,
                sap_analytics_cloud_model_qualified_name,
                sap_analytics_cloud_model_name,
                order,
            ],
        )
        # A model qualifiedName is {connection_qn}[/{folder_id}...]/{model_id}.
        parts = sap_analytics_cloud_model_qualified_name.split("/")
        if len(parts) < 4:
            raise ValueError("sap_analytics_cloud_model_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        parent_column_qualified_name = (
            f"{sap_analytics_cloud_model_qualified_name}/{parent_column_name}"
            if parent_column_name
            else None
        )
        parent_qualified_name = (
            parent_column_qualified_name or sap_analytics_cloud_model_qualified_name
        )
        return cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/{name}",
            order=order,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            sap_analytics_cloud_model_qualified_name=sap_analytics_cloud_model_qualified_name,
            sap_analytics_cloud_model_name=sap_analytics_cloud_model_name,
            sap_analytics_cloud_model=RelatedSapAnalyticsCloudModel(
                unique_attributes={
                    "qualifiedName": sap_analytics_cloud_model_qualified_name
                }
            ),
            column_depth_level=2 if parent_column_qualified_name else 1,
            parent_column_name=parent_column_name or UNSET,
            parent_column_qualified_name=parent_column_qualified_name or UNSET,
            parent_column=RelatedColumn(
                type_name="SapAnalyticsCloudColumn",
                unique_attributes={"qualifiedName": parent_column_qualified_name},
            )
            if parent_column_qualified_name
            else UNSET,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SapAnalyticsCloudColumn":
        """Create a SapAnalyticsCloudColumn instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SapAnalyticsCloudColumn":
        """Return only fields required for update operations."""
        return SapAnalyticsCloudColumn.updater(
            qualified_name=self.qualified_name, name=self.name
        )
