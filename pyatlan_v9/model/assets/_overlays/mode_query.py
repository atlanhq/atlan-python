# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        mode_token: str,
        mode_report_qualified_name: str,
        mode_report_name: str,
        mode_workspace_name: str,
        mode_workspace_qualified_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "ModeQuery":
        """Create a new ModeQuery asset."""
        validate_required_fields(
            [
                "name",
                "mode_token",
                "mode_report_qualified_name",
                "mode_report_name",
                "mode_workspace_name",
            ],
            [
                name,
                mode_token,
                mode_report_qualified_name,
                mode_report_name,
                mode_workspace_name,
            ],
        )
        # A report qualifiedName is {connection_qn}/workspaces/{ws}/reports/{report_token}.
        parts = mode_report_qualified_name.split("/")
        if len(parts) < 7 or parts[-2] != "reports" or parts[-4] != "workspaces":
            raise ValueError("mode_report_qualified_name is invalid")
        if not mode_workspace_qualified_name:
            mode_workspace_qualified_name = "/".join(parts[:-2])
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:-4])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            mode_token=mode_token,
            qualified_name=f"{mode_report_qualified_name}/queries/{mode_token}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            mode_workspace_qualified_name=mode_workspace_qualified_name,
            mode_workspace_name=mode_workspace_name,
            mode_report_qualified_name=mode_report_qualified_name,
            mode_report_name=mode_report_name,
            mode_report=RelatedModeReport(
                unique_attributes={"qualifiedName": mode_report_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ModeQuery":
        """Create a ModeQuery instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ModeQuery":
        """Return only fields required for update operations."""
        return ModeQuery.updater(qualified_name=self.qualified_name, name=self.name)
