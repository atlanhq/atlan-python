# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        micro_strategy_dossier_qualified_name: str,
        micro_strategy_dossier_name: str,
        chapter_key: str,
        page_key: str,
        visualization_key: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "MicroStrategyVisualization":
        validate_required_fields(
            [
                "name",
                "micro_strategy_dossier_qualified_name",
                "micro_strategy_dossier_name",
                "chapter_key",
                "page_key",
                "visualization_key",
            ],
            [
                name,
                micro_strategy_dossier_qualified_name,
                micro_strategy_dossier_name,
                chapter_key,
                page_key,
                visualization_key,
            ],
        )
        fields = micro_strategy_dossier_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qn = connection_qualified_name or "/".join(fields[:3])
        # atlan-microstrategy-app sets only the dossier context on visualizations
        # (no project relationship or project name), so neither does the creator.
        return cls(
            name=name,
            qualified_name=(
                f"{micro_strategy_dossier_qualified_name}/chapters/{chapter_key}"
                f"/pages/{page_key}/visualizations/{visualization_key}"
            ),
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            micro_strategy_dossier_qualified_name=micro_strategy_dossier_qualified_name,
            micro_strategy_dossier_name=micro_strategy_dossier_name,
            micro_strategy_dossier=RelatedMicroStrategyDossier(
                qualified_name=micro_strategy_dossier_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "MicroStrategyVisualization":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "MicroStrategyVisualization":
        return cls.updater(**kwargs)
