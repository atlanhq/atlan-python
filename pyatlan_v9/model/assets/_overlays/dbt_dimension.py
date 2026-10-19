# INTERNAL_IMPORT: from pyatlan.model.dbt_utils import parse_dbt_env_qualified_name
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        semantic_model_qualified_name: str,
    ) -> "DbtDimension":
        validate_required_fields(["name"], [name])
        connection_qn, connector_name, semantic_model_unique_id = (
            parse_dbt_env_qualified_name(
                semantic_model_qualified_name, "semantic_model_qualified_name"
            )
        )
        return cls(
            name=name,
            qualified_name=f"{semantic_model_qualified_name}/dimension/{name}",
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            asset_dbt_unique_id=f"{semantic_model_unique_id}/dimension/{name}",
            dbt_semantic_model_qualified_name=semantic_model_qualified_name,
            semantic_model=RelatedSemanticModel(
                type_name="DbtSemanticModel",
                qualified_name=semantic_model_qualified_name,
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "DbtDimension":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DbtDimension":
        return cls.updater(**kwargs)
