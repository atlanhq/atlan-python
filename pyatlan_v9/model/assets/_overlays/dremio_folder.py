# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        dremio_source_qualified_name: Union[str, None] = None,
        dremio_space_qualified_name: Union[str, None] = None,
    ) -> "DremioFolder":
        """
        Create a new DremioFolder asset.

        qualifiedName is {parent_qualified_name}/{name}, the folder's Dremio path
        under the connection, exactly as atlan-dremio-app builds it. The parent is
        the root Source or Space, or another folder inside it. Pass exactly one of
        dremio_source_qualified_name or dremio_space_qualified_name to name that
        root: the folder links to it, and the connection, parent folder and folder
        hierarchy are derived from it and parent_qualified_name.
        """
        validate_required_fields(
            ["name", "parent_qualified_name"], [name, parent_qualified_name]
        )
        if bool(dremio_source_qualified_name) == bool(dremio_space_qualified_name):
            raise ValueError(
                "exactly one of dremio_source_qualified_name or "
                "dremio_space_qualified_name is required"
            )
        root_qualified_name = (
            dremio_source_qualified_name or dremio_space_qualified_name or ""
        )
        if "/" not in root_qualified_name:
            raise ValueError(
                "dremio_source_qualified_name is invalid"
                if dremio_source_qualified_name
                else "dremio_space_qualified_name is invalid"
            )
        if parent_qualified_name != root_qualified_name and not (
            parent_qualified_name.startswith(f"{root_qualified_name}/")
        ):
            raise ValueError("parent_qualified_name is invalid")
        connection_qualified_name, root_name = root_qualified_name.rsplit("/", 1)
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        folder = cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )
        if dremio_source_qualified_name:
            folder.dremio_parent_asset_type = "SOURCE"
            folder.dremio_source_qualified_name = root_qualified_name
            folder.dremio_source_name = root_name
            folder.dremio_source = RelatedDremioSource(
                unique_attributes={"qualifiedName": root_qualified_name}
            )
        else:
            folder.dremio_parent_asset_type = "SPACE"
            folder.dremio_space_qualified_name = root_qualified_name
            folder.dremio_space_name = root_name
            folder.dremio_space = RelatedDremioSpace(
                unique_attributes={"qualifiedName": root_qualified_name}
            )
        if parent_qualified_name != root_qualified_name:
            # Ancestor folders between the root and this folder, immediate parent first.
            names = parent_qualified_name[len(root_qualified_name) + 1 :].split("/")
            folder.dremio_folder_hierarchy = [
                {
                    "qualifiedName": "/".join([root_qualified_name, *names[: i + 1]]),
                    "name": names[i],
                }
                for i in range(len(names) - 1, -1, -1)
            ]
            folder.dremio_parent_folder_qualified_name = parent_qualified_name
            folder.dremio_parent_folder = RelatedDremioFolder(
                unique_attributes={"qualifiedName": parent_qualified_name}
            )
        return folder

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DremioFolder":
        """Create a DremioFolder instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DremioFolder":
        """Return only fields required for update operations."""
        return DremioFolder.updater(qualified_name=self.qualified_name, name=self.name)
