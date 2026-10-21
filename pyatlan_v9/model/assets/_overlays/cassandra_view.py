# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        keyspace_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "CassandraView":
        validate_required_fields(
            ["name", "keyspace_qualified_name"], [name, keyspace_qualified_name]
        )
        fields = keyspace_qualified_name.split("/")
        if len(fields) < 4:
            raise ValueError(
                "keyspace_qualified_name must be {connection_qualified_name}/{keyspace}"
            )
        connection_qualified_name = connection_qualified_name or "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{keyspace_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=fields[1],
            cassandra_keyspace_name=fields[-1],
            cassandra_keyspace=RelatedCassandraKeyspace(
                qualified_name=keyspace_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "CassandraView":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "CassandraView":
        return cls.updater(**kwargs)
