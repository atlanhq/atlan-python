# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        preset_workspace_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "PresetDashboard":
        validate_required_fields(
            ["name", "preset_workspace_qualified_name"],
            [name, preset_workspace_qualified_name],
        )
        fields = preset_workspace_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qn = connection_qualified_name or (
            f"{fields[0]}/{fields[1]}/{fields[2]}" if len(fields) >= 3 else None
        )
        return cls(
            name=name,
            qualified_name=f"{preset_workspace_qualified_name}/{name}",
            preset_workspace_qualified_name=preset_workspace_qualified_name,
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            preset_workspace=RelatedPresetWorkspace(
                qualified_name=preset_workspace_qualified_name
            ),
        )
