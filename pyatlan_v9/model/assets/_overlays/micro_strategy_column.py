# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        micro_strategy_id: str,
        micro_strategy_project_name: Union[str, None] = None,
        connection_qualified_name: Union[str, None] = None,
    ) -> "MicroStrategyColumn":
        """
        Build a MicroStrategyColumn under any of its seven parent types.

        The parent type is read from the parent's qualifiedName segment
        (``{project}/attributes/{id}``, ``{project}/facts/{id}``, ...), and the
        column is keyed on the project, not the parent:
        ``{project}/columns/{micro_strategy_id}``.
        """
        validate_required_fields(
            ["name", "parent_qualified_name", "micro_strategy_id"],
            [name, parent_qualified_name, micro_strategy_id],
        )
        # qualifiedName segment -> (relationship, typed parent qualifiedName, ref type)
        parents = {
            "attributes": (
                "micro_strategy_attribute",
                "micro_strategy_column_attribute_qualified_name",
                RelatedMicroStrategyAttribute,
            ),
            "facts": (
                "micro_strategy_fact",
                "micro_strategy_column_fact_qualified_name",
                RelatedMicroStrategyFact,
            ),
            "metrics": (
                "micro_strategy_metric",
                "micro_strategy_column_metric_qualified_name",
                RelatedMicroStrategyMetric,
            ),
            "cubes": (
                "micro_strategy_cube",
                "micro_strategy_column_cube_qualified_name",
                RelatedMicroStrategyCube,
            ),
            "reports": (
                "micro_strategy_report",
                "micro_strategy_column_report_qualified_name",
                RelatedMicroStrategyReport,
            ),
            "documents": (
                "micro_strategy_document",
                "micro_strategy_column_document_qualified_name",
                RelatedMicroStrategyDocument,
            ),
            "dossiers": (
                "micro_strategy_dossier",
                "micro_strategy_column_dossier_qualified_name",
                RelatedMicroStrategyDossier,
            ),
        }
        fields = parent_qualified_name.split("/")
        if len(fields) < 4 or fields[-4] != "projects" or fields[-2] not in parents:
            raise ValueError(
                "parent_qualified_name must be the qualified name of a MicroStrategy "
                "attribute, fact, metric, cube, report, document or dossier: "
                "{project}/{attributes|facts|metrics|cubes|reports|documents|dossiers}/{id}"
            )
        parent_field, parent_qn_field, related_cls = parents[fields[-2]]
        project_qn = "/".join(fields[:-2])
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qn = connection_qualified_name or "/".join(fields[:3])
        # atlan-microstrategy-app sets the project qualifiedName (not the project
        # relationship or name) plus the typed parent qualifiedName on columns.
        optional = (
            {"micro_strategy_project_name": micro_strategy_project_name}
            if micro_strategy_project_name
            else {}
        )
        return cls(
            name=name,
            qualified_name=f"{project_qn}/columns/{micro_strategy_id}",
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            micro_strategy_project_qualified_name=project_qn,
            **{
                parent_field: related_cls(qualified_name=parent_qualified_name),
                parent_qn_field: parent_qualified_name,
            },
            **optional,
        )

    @classmethod
    def create(cls, **kwargs) -> "MicroStrategyColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "MicroStrategyColumn":
        return cls.updater(**kwargs)
