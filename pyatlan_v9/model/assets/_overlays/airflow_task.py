# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        airflow_dag_qualified_name: str,
        connection_qualified_name: str | None = None,
    ) -> "AirflowTask":
        validate_required_fields(
            ["name", "airflow_dag_qualified_name"],
            [name, airflow_dag_qualified_name],
        )
        fields = airflow_dag_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qn = connection_qualified_name or (
            f"{fields[0]}/{fields[1]}/{fields[2]}" if len(fields) >= 3 else None
        )
        qualified_name = f"{airflow_dag_qualified_name}/{name}"
        return cls(
            name=name,
            qualified_name=qualified_name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            airflow_dag_qualified_name=airflow_dag_qualified_name,
            airflow_dag=RelatedAirflowDag(qualified_name=airflow_dag_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "AirflowTask":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "AirflowTask":
        return cls.updater(**kwargs)
