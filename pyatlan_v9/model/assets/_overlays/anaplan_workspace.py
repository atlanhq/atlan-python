# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, connection_qualified_name: str
    ) -> "AnaplanWorkspace":
        """Create a new AnaplanWorkspace asset."""
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AnaplanWorkspace":
        """Create an AnaplanWorkspace instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AnaplanWorkspace":
        """Return only fields required for update operations."""
        return AnaplanWorkspace.updater(
            qualified_name=self.qualified_name, name=self.name
        )
