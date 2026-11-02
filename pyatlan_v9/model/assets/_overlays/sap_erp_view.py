# STDLIB_IMPORT: import re
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> "SapErpView":
        """
        Build a SAP ERP view under a connection.

        name is the raw SAP view name. As atlan-saperp-app does, the qualifiedName
        uses it cleaned (every non-word character replaced by "_"):
        {connection_qualified_name}/view/{cleaned name}.
        """
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        cleaned_name = re.sub(r"\W", "_", name.strip(), flags=re.ASCII)
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/view/{cleaned_name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SapErpView":
        """Create a SapErpView instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SapErpView":
        """Return only fields required for update operations."""
        return SapErpView.updater(qualified_name=self.qualified_name, name=self.name)
