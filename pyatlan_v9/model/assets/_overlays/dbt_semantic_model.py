# INTERNAL_IMPORT: from pyatlan.model.dbt_utils import dbt_env_qualified_name
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        account_id: str,
        project_id: str,
        environment_id: str,
        unique_id: str,
    ) -> "DbtSemanticModel":
        validate_required_fields(["name"], [name])
        qualified_name, connector_name = dbt_env_qualified_name(
            connection_qualified_name, account_id, project_id, environment_id, unique_id
        )
        return cls(
            name=name,
            qualified_name=qualified_name,
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            asset_dbt_unique_id=unique_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "DbtSemanticModel":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DbtSemanticModel":
        return cls.updater(**kwargs)
