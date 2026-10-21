# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
        database_name: str | None = None,
        connection_qualified_name: str | None = None,
    ) -> "MongoDBCollection":
        """Create a new MongoDBCollection asset."""
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )
        parts = database_qualified_name.split("/")
        if len(parts) < 4:
            raise ValueError("database_qualified_name is invalid")
        database_name = database_name or parts[-1]
        connection_qualified_name = connection_qualified_name or "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            database_name=database_name,
            database_qualified_name=database_qualified_name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{database_qualified_name}/{name}",
            connector_name=connector_name,
            mongo_db_database=RelatedMongoDBDatabase(
                unique_attributes={"qualifiedName": database_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "MongoDBCollection":
        """Create a MongoDBCollection instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "MongoDBCollection":
        """Return only fields required for update operations."""
        return MongoDBCollection.updater(
            qualified_name=self.qualified_name,
            name=self.name,
        )
