# STDLIB_IMPORT: import unicodedata
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        workspace_id: str,
        space_id: str,
    ) -> "DatabricksGenieAgent":
        validate_required_fields(
            ["name", "connection_qualified_name", "workspace_id", "space_id"],
            [name, connection_qualified_name, workspace_id, space_id],
        )
        # Strip and NFC-normalise, as atlan-databricks-app does before building the qn.
        name, workspace_id, space_id = (
            unicodedata.normalize("NFC", value.strip())
            for value in (name, workspace_id, space_id)
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=(
                f"{connection_qualified_name}/{workspace_id}/genie-spaces/{space_id}"
            ),
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            asset_source_id=space_id,
            databricks_genie_agent_workspace_id=workspace_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksGenieAgent":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksGenieAgent":
        return cls.updater(**kwargs)
