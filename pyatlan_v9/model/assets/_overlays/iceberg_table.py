# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields
# IMPORT: from .iceberg_related import RelatedIcebergNamespace

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        namespace_qualified_name: str,
    ) -> "IcebergTable":
        """
        Create a new IcebergTable asset.

        Args:
            name: Name of the table
            namespace_qualified_name: Unique name of the (possibly nested) namespace in which this table exists

        Returns:
            IcebergTable instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "namespace_qualified_name"], [name, namespace_qualified_name]
        )
        fields = namespace_qualified_name.split("/")
        if len(fields) < 5:
            raise ValueError(
                f"Invalid namespace_qualified_name: {namespace_qualified_name}. "
                "Expected format: default/connector/connection_id/catalog/namespace[/namespace...]"
            )
        connection_qualified_name = "/".join(fields[:3])
        catalog_name = fields[3]
        catalog_qualified_name = f"{connection_qualified_name}/{catalog_name}"
        namespace_path = fields[4:]
        return cls(
            name=name,
            qualified_name=f"{namespace_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            database_name=catalog_name,
            database_qualified_name=catalog_qualified_name,
            schema_name=namespace_path[-1],
            schema_qualified_name=namespace_qualified_name,
            atlan_schema=RelatedIcebergNamespace(
                unique_attributes={"qualifiedName": namespace_qualified_name}
            ),
            iceberg_parent_namespace_qualified_name=(
                namespace_qualified_name if len(namespace_path) > 1 else None
            ),
            iceberg_namespace_hierarchy=[
                {
                    "qualifiedName": "/".join(
                        [catalog_qualified_name, *namespace_path[:i]]
                    ),
                    "name": namespace_path[i - 1],
                }
                for i in range(1, len(namespace_path) + 1)
            ],
        )

    @classmethod
    def create(cls, **kwargs) -> "IcebergTable":
        return cls.creator(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "IcebergTable":
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "IcebergTable":
        return cls.updater(**kwargs)

    def trim_to_required(self) -> "IcebergTable":
        return IcebergTable.updater(qualified_name=self.qualified_name, name=self.name)
