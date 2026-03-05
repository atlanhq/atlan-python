# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        workspace_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "AnaplanModel":
        """Create a new AnaplanModel asset."""
        validate_required_fields(
            ["name", "workspace_qualified_name"], [name, workspace_qualified_name]
        )
        connection_qn: Union[str, None, UnsetType] = UNSET
        if connection_qualified_name is not None:
            connector_name = str(
                AtlanConnectorType.get_connector_name(connection_qualified_name)
            )
        else:
            connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                workspace_qualified_name, "workspace_qualified_name", 4
            )
        return cls(
            name=name,
            qualified_name=f"{workspace_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name or connection_qn,
            connector_name=connector_name,
            anaplan_workspace_qualified_name=workspace_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AnaplanModel":
        """Create an AnaplanModel instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AnaplanModel":
        """Return only fields required for update operations."""
        return AnaplanModel.updater(qualified_name=self.qualified_name, name=self.name)
