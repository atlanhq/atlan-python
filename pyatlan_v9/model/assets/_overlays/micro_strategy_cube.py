# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        micro_strategy_project_qualified_name: str,
        micro_strategy_project_name: str,
        micro_strategy_id: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "MicroStrategyCube":
        validate_required_fields(
            [
                "name",
                "micro_strategy_project_qualified_name",
                "micro_strategy_project_name",
                "micro_strategy_id",
            ],
            [
                name,
                micro_strategy_project_qualified_name,
                micro_strategy_project_name,
                micro_strategy_id,
            ],
        )
        fields = micro_strategy_project_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qn = connection_qualified_name or "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{micro_strategy_project_qualified_name}/cubes/{micro_strategy_id}",
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            micro_strategy_project_qualified_name=micro_strategy_project_qualified_name,
            micro_strategy_project_name=micro_strategy_project_name,
            micro_strategy_project=RelatedMicroStrategyProject(
                qualified_name=micro_strategy_project_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "MicroStrategyCube":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "MicroStrategyCube":
        return cls.updater(**kwargs)
