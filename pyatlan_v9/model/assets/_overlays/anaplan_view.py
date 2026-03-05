# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        module_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "AnaplanView":
        """Create a new AnaplanView asset."""
        validate_required_fields(
            ["name", "module_qualified_name"], [name, module_qualified_name]
        )
        fields = module_qualified_name.split("/")
        connection_qn: Union[str, None, UnsetType] = UNSET
        if connection_qualified_name is not None:
            connector_name = str(
                AtlanConnectorType.get_connector_name(connection_qualified_name)
            )
        else:
            connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                module_qualified_name, "module_qualified_name", 6
            )
        workspace_qualified_name = "/".join(fields[:4]) if len(fields) >= 4 else UNSET
        workspace_name = fields[3] if len(fields) > 3 else UNSET
        model_qualified_name = "/".join(fields[:5]) if len(fields) >= 5 else UNSET
        model_name = fields[4] if len(fields) > 4 else UNSET
        module_name = fields[5] if len(fields) > 5 else UNSET
        return cls(
            name=name,
            qualified_name=f"{module_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name or connection_qn,
            connector_name=connector_name,
            anaplan_workspace_qualified_name=workspace_qualified_name,
            anaplan_workspace_name=workspace_name,
            anaplan_model_qualified_name=model_qualified_name,
            anaplan_model_name=model_name,
            anaplan_module_qualified_name=module_qualified_name,
            anaplan_module_name=module_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AnaplanView":
        """Create an AnaplanView instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AnaplanView":
        """Return only fields required for update operations."""
        return AnaplanView.updater(qualified_name=self.qualified_name, name=self.name)
