# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        parent_folder_qualified_name: Union[str, None] = None,
    ) -> "SSRSFolder":
        """Create a new SSRSFolder asset, at the root or under a parent folder."""
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        if parent_folder_qualified_name is not None and not (
            parent_folder_qualified_name.startswith(f"{connection_qualified_name}/")
        ):
            raise ValueError("parent_folder_qualified_name is invalid")
        parent_qualified_name = parent_folder_qualified_name or connection_qualified_name
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        # atlan-ssrs-app strips spaces from each qualifiedName segment.
        return cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/{name.replace(' ', '')}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            ssrs_parent_folder_qualified_name=parent_folder_qualified_name or UNSET,
            ssrs_parent_folder=RelatedSSRSFolder(
                unique_attributes={"qualifiedName": parent_folder_qualified_name}
            )
            if parent_folder_qualified_name
            else UNSET,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SSRSFolder":
        """Create an SSRSFolder instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SSRSFolder":
        """Return only fields required for update operations."""
        return SSRSFolder.updater(qualified_name=self.qualified_name, name=self.name)
