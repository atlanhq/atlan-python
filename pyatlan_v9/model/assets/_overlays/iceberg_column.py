# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields
# IMPORT: from .iceberg_related import RelatedIcebergTable

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        table_qualified_name: str,
        order: int,
        parent_column_qualified_name: str | None = None,
    ) -> "IcebergColumn":
        """
        Create a new IcebergColumn asset.

        A top-level column is named under its table. A nested (struct / list /
        map) column is named under its parent column, so ``address.city`` in
        table ``t`` has qualifiedName ``{t}/address/city``. The table is always
        passed explicitly, because namespaces nest to any depth and the table
        cannot be told apart from a parent column by the name alone.

        Args:
            name: Name of the column (the last segment of its path)
            table_qualified_name: Unique name of the table in which this column exists
            order: Order (position) of the column within its table or parent column
            parent_column_qualified_name: Unique name of the parent column, for a nested column

        Returns:
            IcebergColumn instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "table_qualified_name", "order"],
            [name, table_qualified_name, order],
        )
        if order < 0:
            raise ValueError("Order must be a non-negative integer")
        fields = table_qualified_name.split("/")
        if len(fields) < 6:
            raise ValueError(
                f"Invalid table_qualified_name: {table_qualified_name}. "
                "Expected format: default/connector/connection_id/catalog/namespace[/namespace...]/table"
            )
        parent_path: list[str] = []
        if parent_column_qualified_name is not None:
            validate_required_fields(
                ["parent_column_qualified_name"], [parent_column_qualified_name]
            )
            prefix = f"{table_qualified_name}/"
            if not parent_column_qualified_name.startswith(prefix) or len(
                parent_column_qualified_name
            ) == len(prefix):
                raise ValueError(
                    f"Invalid parent_column_qualified_name: {parent_column_qualified_name}. "
                    f"Expected a column of table {table_qualified_name}"
                )
            parent_path = parent_column_qualified_name[len(prefix) :].split("/")
        parent_qualified_name = parent_column_qualified_name or table_qualified_name
        connection_qualified_name = "/".join(fields[:3])
        catalog_name = fields[3]
        catalog_qualified_name = f"{connection_qualified_name}/{catalog_name}"
        namespace_path = fields[4:-1]
        namespace_qualified_name = "/".join(fields[:-1])
        column = cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/{name}",
            order=order,
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            database_name=catalog_name,
            database_qualified_name=catalog_qualified_name,
            schema_name=namespace_path[-1],
            schema_qualified_name=namespace_qualified_name,
            table_name=fields[-1],
            table_qualified_name=table_qualified_name,
            table=RelatedIcebergTable(
                unique_attributes={"qualifiedName": table_qualified_name}
            ),
            column_depth_level=len(parent_path) + 1,
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
        if parent_path:
            column.parent_column_name = parent_path[-1]
            column.parent_column_qualified_name = parent_column_qualified_name
            column.column_hierarchy = [
                {
                    "name": parent_path[i - 1],
                    "depth": str(i),
                    "qualifiedName": "/".join([table_qualified_name, *parent_path[:i]]),
                }
                for i in range(1, len(parent_path) + 1)
            ]
        return column

    @classmethod
    def create(cls, **kwargs) -> "IcebergColumn":
        return cls.creator(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "IcebergColumn":
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "IcebergColumn":
        return cls.updater(**kwargs)

    def trim_to_required(self) -> "IcebergColumn":
        return IcebergColumn.updater(qualified_name=self.qualified_name, name=self.name)
