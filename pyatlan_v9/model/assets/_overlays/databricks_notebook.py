# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        connection_qualified_name: str,
        workspace_id: str,
        notebook_path: str,
        name: str | None = None,
    ) -> "DatabricksNotebook":
        validate_required_fields(
            ["connection_qualified_name", "workspace_id", "notebook_path"],
            [connection_qualified_name, workspace_id, notebook_path],
        )
        name = name or notebook_path.split("/")[-1]
        validate_required_fields(["name"], [name])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            # The path is kept verbatim, so "/Users/..." yields "{workspace_id}//Users/...",
            # matching the qualifiedName atlan-databricks-app emits.
            qualified_name=f"{connection_qualified_name}/{workspace_id}/{notebook_path}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            databricks_notebook_path=notebook_path,
            databricks_notebook_workspace_id=workspace_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "DatabricksNotebook":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DatabricksNotebook":
        return cls.updater(**kwargs)
