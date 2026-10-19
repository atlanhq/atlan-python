# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        micro_strategy_id: str,
    ) -> "MicroStrategyProject":
        validate_required_fields(
            ["name", "connection_qualified_name", "micro_strategy_id"],
            [name, connection_qualified_name, micro_strategy_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/projects/{micro_strategy_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def create(cls, **kwargs) -> "MicroStrategyProject":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "MicroStrategyProject":
        return cls.updater(**kwargs)
