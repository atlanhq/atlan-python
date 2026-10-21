# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        mode_token: str,
        mode_workspace_qualified_name: str,
        mode_workspace_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "ModeCollection":
        """Create a new ModeCollection asset."""
        validate_required_fields(
            [
                "name",
                "mode_token",
                "mode_workspace_qualified_name",
                "mode_workspace_name",
            ],
            [name, mode_token, mode_workspace_qualified_name, mode_workspace_name],
        )
        # A workspace qualifiedName is {connection_qn}/workspaces/{workspace_token}.
        parts = mode_workspace_qualified_name.split("/")
        if len(parts) < 5 or parts[-2] != "workspaces":
            raise ValueError("mode_workspace_qualified_name is invalid")
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:-2])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            mode_token=mode_token,
            qualified_name=f"{mode_workspace_qualified_name}/collections/{mode_token}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            mode_workspace_qualified_name=mode_workspace_qualified_name,
            mode_workspace_name=mode_workspace_name,
            mode_workspace=RelatedModeWorkspace(
                unique_attributes={"qualifiedName": mode_workspace_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "ModeCollection":
        """Create a ModeCollection instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "ModeCollection":
        """Return only fields required for update operations."""
        return ModeCollection.updater(
            qualified_name=self.qualified_name, name=self.name
        )
