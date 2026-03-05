# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "DocumentDBCollection":
        """Create a new DocumentDBCollection asset."""
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )
        if connection_qualified_name:
            fields = connection_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
        else:
            parts = database_qualified_name.split("/")
            if len(parts) < 3:
                raise ValueError("database_qualified_name is invalid")
            connection_qualified_name = "/".join(parts[:3])
            connector_name = parts[1]
        return cls(
            name=name,
            database_qualified_name=database_qualified_name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{database_qualified_name}/{name}",
            connector_name=connector_name,
            document_db_database=RelatedDocumentDBDatabase(
                unique_attributes={"qualifiedName": database_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DocumentDBCollection":
        """Create a DocumentDBCollection instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DocumentDBCollection":
        """Return only fields required for update operations."""
        return DocumentDBCollection.updater(
            qualified_name=self.qualified_name,
            name=self.name,
        )
