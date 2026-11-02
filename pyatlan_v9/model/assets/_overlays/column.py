# STDLIB_IMPORT: from warnings import warn
# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# IMPORT: from pyatlan.utils import validate_required_fields
# INTERNAL_IMPORT: from pyatlan.utils import validate_optional_fields
# INTERNAL_IMPORT: from pyatlan.utils import init_guid

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        parent_type: type,
        order: int,
        parent_name: str | None = None,
        database_name: str | None = None,
        database_qualified_name: str | None = None,
        schema_name: str | None = None,
        schema_qualified_name: str | None = None,
        table_name: str | None = None,
        table_qualified_name: str | None = None,
        connection_qualified_name: str | None = None,
        parent_column: "Column | None" = None,
    ) -> "Column":
        """
        Create a new Column asset.

        Without ``connection_qualified_name``, ``parent_qualified_name`` must have the standard
        depth (6 segments for a table-like parent, 5 for a collection) and the other parents are
        derived from it. With ``connection_qualified_name``, parents of any depth are accepted;
        database and schema are then only set when passed or derivable from a standard-depth parent.

        For a nested column, pass ``parent_type=Column`` and the parent column as
        ``parent_column``: the container, database and schema are copied from it, and
        ``parent_column``, ``column_depth_level`` and ``column_hierarchy`` are set.

        Args:
            name: Name of the column
            parent_qualified_name: Unique name of the parent (table/view/collection/column etc)
            parent_type: Type of parent (Table, View, MaterialisedView, TablePartition,
                SnowflakeDynamicTable, MongoDBCollection, DocumentDBCollection or Column)
            order: Order of the column in the parent
            parent_name: Simple name of the parent
            database_name: Simple name of the database
            database_qualified_name: Unique name of the database
            schema_name: Simple name of the schema
            schema_qualified_name: Unique name of the schema
            table_name: (deprecated) Simple name of the table
            table_qualified_name: (deprecated) Unique name of the table
            connection_qualified_name: Unique name of the connection
            parent_column: The parent column, required when parent_type is Column

        Returns:
            Column instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        if table_name:
            warn(
                ("`table_name` is deprecated, please use `parent_name` instead"),
                DeprecationWarning,
                stacklevel=2,
            )
        if table_qualified_name:
            warn(
                (
                    "`table_qualified_name` is deprecated, please use `parent_qualified_name` instead"
                ),
                DeprecationWarning,
                stacklevel=2,
            )

        validate_required_fields(
            ["name", "parent_qualified_name", "parent_type", "order"],
            [name, parent_qualified_name, parent_type, order],
        )
        validate_optional_fields(
            [
                "parent_name",
                "database_name",
                "database_qualified_name",
                "schema_name",
                "schema_qualified_name",
                "connection_qualified_name",
            ],
            [
                parent_name,
                database_name,
                database_qualified_name,
                schema_name,
                schema_qualified_name,
                connection_qualified_name,
            ],
        )
        if order < 0:
            raise ValueError("Order must be be a positive integer")

        # Get the type name from the parent_type class
        parent_type_name = getattr(parent_type, "__name__", None)

        table_like = [
            "Table",
            "View",
            "MaterialisedView",
            "TablePartition",
            "SnowflakeDynamicTable",
        ]
        collections = ["MongoDBCollection", "DocumentDBCollection"]
        if parent_type_name not in table_like + collections + ["Column"]:
            raise ValueError(
                "parent_type must be either Table, SnowflakeDynamicTable, View, MaterializeView, "
                "TablePartition, MongoDBCollection, DocumentDBCollection or Column"
            )

        qualified_name = f"{parent_qualified_name}/{name}"
        parent_name = parent_name or parent_qualified_name.rsplit("/", 1)[-1]

        if parent_type_name == "Column":
            return cls._nested_creator(
                name=name,
                qualified_name=qualified_name,
                order=order,
                parent_qualified_name=parent_qualified_name,
                parent_name=parent_name,
                parent_column=parent_column,
                connection_qualified_name=connection_qualified_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                schema_name=schema_name,
                schema_qualified_name=schema_qualified_name,
            )

        # Standard depth: {conn}/{db}/{schema}/{table} or {conn}/{db}/{collection}
        standard_depth = 6 if parent_type_name in table_like else 5
        fields = parent_qualified_name.split("/")
        if connection_qualified_name:
            # Use AtlanConnectorType.get_connector_name for validation (exact parity with pydantic)
            connector_name = str(
                AtlanConnectorType.get_connector_name(connection_qualified_name)
            )
            if not parent_qualified_name.startswith(f"{connection_qualified_name}/"):
                raise ValueError("parent_qualified_name is invalid")
            is_standard = len(fields) == standard_depth
        else:
            result = AtlanConnectorType.get_connector_name(
                parent_qualified_name, "parent_qualified_name", standard_depth
            )
            connection_qualified_name = str(result[0])
            connector_name = str(result[1])
            is_standard = True

        if is_standard and not database_qualified_name:
            database_name = database_name or fields[3]
        if database_name and not database_qualified_name:
            database_qualified_name = f"{connection_qualified_name}/{database_name}"
        if database_qualified_name and not database_name:
            database_name = database_qualified_name.rsplit("/", 1)[-1]
        if parent_type_name in table_like:
            if is_standard and not schema_qualified_name:
                schema_name = schema_name or fields[4]
            if schema_name and not schema_qualified_name and database_qualified_name:
                schema_qualified_name = f"{database_qualified_name}/{schema_name}"
            if schema_qualified_name and not schema_name:
                schema_name = schema_qualified_name.rsplit("/", 1)[-1]

        col = cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
            order=order,
        )
        if database_qualified_name:
            col.database_name = database_name
            col.database_qualified_name = database_qualified_name
        if schema_qualified_name:
            col.schema_name = schema_name
            col.schema_qualified_name = schema_qualified_name

        # Set parent-specific fields
        if parent_type_name == "Table":
            col.table_qualified_name = parent_qualified_name
            col.table = RelatedTable(
                qualified_name=parent_qualified_name, type_name="Table"
            )
            col.table_name = parent_name
        elif parent_type_name == "View":
            col.view_qualified_name = parent_qualified_name
            col.view = RelatedView(
                qualified_name=parent_qualified_name, type_name="View"
            )
            col.view_name = parent_name
        elif parent_type_name == "MaterialisedView":
            col.view_qualified_name = parent_qualified_name
            col.materialised_view = RelatedMaterialisedView(
                qualified_name=parent_qualified_name, type_name="MaterialisedView"
            )
            col.view_name = parent_name
        elif parent_type_name == "TablePartition":
            col.table_qualified_name = parent_qualified_name
            col.table_partition = RelatedTablePartition(
                qualified_name=parent_qualified_name, type_name="TablePartition"
            )
            col.table_name = parent_name
        elif parent_type_name == "SnowflakeDynamicTable":
            col.table_qualified_name = parent_qualified_name
            col.snowflake_dynamic_table = RelatedSnowflakeDynamicTable(
                qualified_name=parent_qualified_name,
                type_name="SnowflakeDynamicTable",
            )
            col.table_name = parent_name
        elif parent_type_name == "MongoDBCollection":
            col.nosql_collection_qualified_name = parent_qualified_name
            col.mongo_db_collection = RelatedMongoDBCollection(
                qualified_name=parent_qualified_name, type_name="MongoDBCollection"
            )
            col.nosql_collection_name = parent_name
        elif parent_type_name == "DocumentDBCollection":
            # DocumentDBCollection is a Table subtype, so it holds its columns as a table
            col.table_qualified_name = parent_qualified_name
            col.table = RelatedTable(
                qualified_name=parent_qualified_name, type_name="DocumentDBCollection"
            )
            col.table_name = parent_name
            col.nosql_collection_qualified_name = parent_qualified_name
            col.nosql_collection_name = parent_name

        return col

    @classmethod
    def _nested_creator(
        cls,
        *,
        name: str,
        qualified_name: str,
        order: int,
        parent_qualified_name: str,
        parent_name: str,
        parent_column: "Column | None",
        connection_qualified_name: str | None,
        database_name: str | None,
        database_qualified_name: str | None,
        schema_name: str | None,
        schema_qualified_name: str | None,
    ) -> "Column":
        if parent_column is None:
            raise ValueError("parent_column is required when parent_type is Column")
        if parent_column.qualified_name != parent_qualified_name:
            raise ValueError("parent_column does not match parent_qualified_name")
        connection_qualified_name = (
            connection_qualified_name or parent_column.connection_qualified_name
        )
        if not connection_qualified_name:
            raise ValueError("connection_qualified_name is required")
        if not parent_qualified_name.startswith(f"{connection_qualified_name}/"):
            raise ValueError("parent_qualified_name is invalid")

        col = cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=str(
                AtlanConnectorType.get_connector_name(connection_qualified_name)
            ),
            connection_qualified_name=connection_qualified_name,
            order=order,
        )
        # Inherit the container and its denormalised names from the parent column
        for attr in (
            "database_name",
            "database_qualified_name",
            "schema_name",
            "schema_qualified_name",
            "table_name",
            "table_qualified_name",
            "view_name",
            "view_qualified_name",
            "nosql_collection_name",
            "nosql_collection_qualified_name",
            "table",
            "view",
            "materialised_view",
            "table_partition",
            "snowflake_dynamic_table",
            "mongo_db_collection",
        ):
            value = getattr(parent_column, attr)
            if value is not UNSET and value is not None:
                setattr(col, attr, value)
        if database_qualified_name:
            col.database_qualified_name = database_qualified_name
            col.database_name = (
                database_name or database_qualified_name.rsplit("/", 1)[-1]
            )
        if schema_qualified_name:
            col.schema_qualified_name = schema_qualified_name
            col.schema_name = schema_name or schema_qualified_name.rsplit("/", 1)[-1]

        parent_depth = parent_column.column_depth_level
        if parent_depth is UNSET or parent_depth is None:
            parent_depth = 1
        hierarchy = parent_column.column_hierarchy
        if hierarchy is UNSET or hierarchy is None:
            hierarchy = []
        col.parent_column = RelatedColumn(qualified_name=parent_qualified_name)
        col.parent_column_qualified_name = parent_qualified_name
        col.parent_column_name = parent_name
        col.column_depth_level = parent_depth + 1
        col.column_hierarchy = [
            *hierarchy,
            {
                "depth": str(parent_depth),
                "name": parent_name,
                "qualifiedName": parent_qualified_name,
            },
        ]
        return col

    @classmethod
    def updater(cls, qualified_name: str = "", name: str = "") -> "Column":
        """
        Create a Column instance for modification.

        Args:
            qualified_name: Unique name of the column
            name: Name of the column

        Returns:
            Column instance for modification

        Raises:
            ValueError: If required parameters are missing
        """
        if not qualified_name:
            raise ValueError("qualified_name is required")
        if not name:
            raise ValueError("name is required")

        return cls(qualified_name=qualified_name, name=name)
