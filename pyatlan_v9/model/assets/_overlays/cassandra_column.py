# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        parent_type: type,
        connection_qualified_name: str | None = None,
    ) -> "CassandraColumn":
        """
        Create a new CassandraColumn in a CassandraTable or CassandraView.

        Args:
            name: Name of the column
            parent_qualified_name: Unique name of the table or view
            parent_type: CassandraTable or CassandraView
            connection_qualified_name: Unique name of the connection
                (derived from parent_qualified_name when omitted)

        Returns:
            CassandraColumn instance ready to be created

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        validate_required_fields(
            ["name", "parent_qualified_name", "parent_type"],
            [name, parent_qualified_name, parent_type],
        )
        parent_type_name = getattr(parent_type, "__name__", None)
        if parent_type_name not in ("CassandraTable", "CassandraView"):
            raise ValueError("parent_type must be either CassandraTable or CassandraView")
        fields = parent_qualified_name.split("/")
        if len(fields) < 5:
            raise ValueError(
                "parent_qualified_name must be "
                "{connection_qualified_name}/{keyspace}/{table_or_view}"
            )
        connection_qualified_name = connection_qualified_name or "/".join(fields[:3])
        column = cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            cassandra_keyspace_name=fields[-2],
        )
        if parent_type_name == "CassandraTable":
            column.cassandra_table_name = fields[-1]
            column.cassandra_table_qualified_name = parent_qualified_name
            column.cassandra_table = RelatedCassandraTable(
                qualified_name=parent_qualified_name
            )
        else:
            column.cassandra_view_name = fields[-1]
            column.cassandra_view_qualified_name = parent_qualified_name
            column.cassandra_view = RelatedCassandraView(
                qualified_name=parent_qualified_name
            )
        return column

    @classmethod
    def create(cls, **kwargs) -> "CassandraColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "CassandraColumn":
        return cls.updater(**kwargs)
