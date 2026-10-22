# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> "DremioSource":
        """
        Create a new DremioSource asset.

        qualifiedName is {connection_qualified_name}/{name}, the Dremio path of
        the source under the connection, exactly as atlan-dremio-app builds it.
        """
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        qualified_name = f"{connection_qualified_name}/{name}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            dremio_source_qualified_name=qualified_name,
            dremio_source_name=name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DremioSource":
        """Create a DremioSource instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DremioSource":
        """Return only fields required for update operations."""
        return DremioSource.updater(qualified_name=self.qualified_name, name=self.name)
