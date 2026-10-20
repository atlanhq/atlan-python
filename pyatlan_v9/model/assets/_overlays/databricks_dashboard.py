# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        workspace_id: str,
        dashboard_id: str,
    ) -> "DatabricksDashboard":
        validate_required_fields(
            ["name", "connection_qualified_name", "workspace_id", "dashboard_id"],
            [name, connection_qualified_name, workspace_id, dashboard_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=(
                f"{connection_qualified_name}/{workspace_id}/dashboards/{dashboard_id}"
            ),
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            asset_source_id=dashboard_id,
            databricks_dashboard_workspace_id=workspace_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksDashboard":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksDashboard":
        return cls.updater(**kwargs)
