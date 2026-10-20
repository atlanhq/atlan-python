# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        workspace_qualified_name: str,
        report_id: str,
    ) -> "FabricReport":
        validate_required_fields(
            ["name", "workspace_qualified_name", "report_id"],
            [name, workspace_qualified_name, report_id],
        )
        fields = workspace_qualified_name.split("/")
        if len(fields) != 4:
            raise ValueError(
                f"Invalid workspace_qualified_name: {workspace_qualified_name}. "
                "Expected format: default/fabric/<epoch>/<workspace_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{workspace_qualified_name}/{report_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_space_qualified_name=workspace_qualified_name,
            fabric_workspace=RelatedFabricWorkspace(
                qualified_name=workspace_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "FabricReport":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "FabricReport":
        return cls.updater(**kwargs)
