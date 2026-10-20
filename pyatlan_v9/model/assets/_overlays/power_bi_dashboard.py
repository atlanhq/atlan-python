# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        workspace_qualified_name: str,
        dashboard_id: str,
    ) -> "PowerBIDashboard":
        validate_required_fields(
            ["name", "workspace_qualified_name", "dashboard_id"],
            [name, workspace_qualified_name, dashboard_id],
        )
        fields = workspace_qualified_name.split("/")
        if len(fields) != 4 or not all(fields):
            raise ValueError("workspace_qualified_name is invalid")
        return cls(
            name=name,
            qualified_name=f"{workspace_qualified_name}/{dashboard_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            workspace_qualified_name=workspace_qualified_name,
            workspace=RelatedPowerBIWorkspace(
                unique_attributes={"qualifiedName": workspace_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "PowerBIDashboard":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "PowerBIDashboard":
        return cls.updater(**kwargs)
