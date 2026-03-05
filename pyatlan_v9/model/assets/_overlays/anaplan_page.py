# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        app_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "AnaplanPage":
        """Create a new AnaplanPage asset."""
        validate_required_fields(
            ["name", "app_qualified_name"], [name, app_qualified_name]
        )
        connection_qn: Union[str, None, UnsetType] = UNSET
        if connection_qualified_name is not None:
            connector_name = str(
                AtlanConnectorType.get_connector_name(connection_qualified_name)
            )
        else:
            connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                app_qualified_name, "app_qualified_name", 4
            )
        return cls(
            name=name,
            qualified_name=f"{app_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name or connection_qn,
            connector_name=connector_name,
            anaplan_app_qualified_name=app_qualified_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AnaplanPage":
        """Create an AnaplanPage instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AnaplanPage":
        """Return only fields required for update operations."""
        return AnaplanPage.updater(qualified_name=self.qualified_name, name=self.name)
