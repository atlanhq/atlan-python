# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        table_qualified_name: str,
        table_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "DynamoDBLocalSecondaryIndex":
        """Create a new DynamoDBLocalSecondaryIndex asset."""
        validate_required_fields(
            ["name", "table_qualified_name"], [name, table_qualified_name]
        )
        # A table qualifiedName is {connection_qn}/{table_name}.
        parts = table_qualified_name.split("/")
        if len(parts) < 4:
            raise ValueError("table_qualified_name is invalid")
        if not table_name:
            table_name = parts[-1]
        if not connection_qualified_name:
            connection_qualified_name = "/".join(parts[:3])
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{table_qualified_name}/_lsi_/{name}",
            table_name=table_name,
            table_qualified_name=table_qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            dynamo_db_table=RelatedDynamoDBTable(
                unique_attributes={"qualifiedName": table_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "DynamoDBLocalSecondaryIndex":
        """Create a DynamoDBLocalSecondaryIndex instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "DynamoDBLocalSecondaryIndex":
        """Return only fields required for update operations."""
        return DynamoDBLocalSecondaryIndex.updater(
            qualified_name=self.qualified_name, name=self.name
        )
