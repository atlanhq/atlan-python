# STDLIB_IMPORT: from warnings import warn
# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# IMPORT: from pyatlan.utils import validate_required_fields
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
    ) -> "Column":
        """
        Create a new Column asset.

        Args:
            name: Name of the column
            parent_qualified_name: Unique name of the parent (table/view/etc)
            parent_type: Type of parent (Table, View, MaterialisedView, etc)
            order: Order of the column in the parent
            parent_name: Simple name of the parent
            database_name: Simple name of the database
            database_qualified_name: Unique name of the database
            schema_name: Simple name of the schema
            schema_qualified_name: Unique name of the schema
            table_name: (deprecated) Simple name of the table
            table_qualified_name: (deprecated) Unique name of the table
            connection_qualified_name: Unique name of the connection

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

        # Use AtlanConnectorType.get_connector_name for validation (exact parity with pydantic)
        connection_qn: str | None = None
        if connection_qualified_name:
            connector_name = str(
                AtlanConnectorType.get_connector_name(connection_qualified_name)
            )
        else:
            result = AtlanConnectorType.get_connector_name(
                parent_qualified_name, "parent_qualified_name", 6
            )
            connection_qn = str(result[0])
            connector_name = str(result[1])
        if order < 0:
            raise ValueError("Order must be be a positive integer")

        # Get the type name from the parent_type class
        parent_type_name = getattr(parent_type, "__name__", None)

        # Validate parent type
        valid_types = [
            "Table",
            "View",
            "MaterialisedView",
            "TablePartition",
            "SnowflakeDynamicTable",
            "Column",
        ]
        if parent_type_name not in valid_types:
            raise ValueError(
                "parent_type must be either Table, SnowflakeDynamicTable, View, MaterializeView or TablePartition"
            )

        if parent_type_name == "Column":
            raise ValueError(
                "parent_type must be either Table, SnowflakeDynamicTable, View, MaterializeView or TablePartition"
            )

        # Parse parent_qualified_name to derive fields
        fields = parent_qualified_name.split("/")

        connection_qualified_name = connection_qualified_name or connection_qn
        database_name = database_name or fields[3]
        schema_name = schema_name or fields[4]
        parent_name = parent_name or fields[5]
        database_qualified_name = (
            database_qualified_name or f"{connection_qualified_name}/{database_name}"
        )
        schema_qualified_name = (
            schema_qualified_name or f"{database_qualified_name}/{schema_name}"
        )

        database_qualified_name = (
            database_qualified_name
            or f"{fields[0]}/{fields[1]}/{fields[2]}/{database_name}"
        )
        schema_qualified_name = (
            schema_qualified_name or f"{database_qualified_name}/{schema_name}"
        )

        connection_qualified_name = (
            connection_qualified_name or f"{fields[0]}/{fields[1]}/{fields[2]}"
        )

        qualified_name = f"{parent_qualified_name}/{name}"

        # Build the column
        col = cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
            schema_name=schema_name,
            schema_qualified_name=schema_qualified_name,
            database_name=database_name,
            database_qualified_name=database_qualified_name,
            order=order,
        )

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
