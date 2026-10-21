# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        table_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "CassandraIndex":
        validate_required_fields(
            ["name", "table_qualified_name"], [name, table_qualified_name]
        )
        fields = table_qualified_name.split("/")
        if len(fields) < 5:
            raise ValueError(
                "table_qualified_name must be "
                "{connection_qualified_name}/{keyspace}/{table}"
            )
        connection_qualified_name = connection_qualified_name or "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{table_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            cassandra_keyspace_name=fields[-2],
            cassandra_table_name=fields[-1],
            cassandra_table_qualified_name=table_qualified_name,
            cassandra_table=RelatedCassandraTable(qualified_name=table_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "CassandraIndex":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "CassandraIndex":
        return cls.updater(**kwargs)
