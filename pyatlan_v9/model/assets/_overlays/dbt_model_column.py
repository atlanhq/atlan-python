# INTERNAL_IMPORT: from pyatlan.model.dbt_utils import parse_dbt_env_qualified_name
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        model_qualified_name: str | None = None,
        seed_qualified_name: str | None = None,
    ) -> "DbtModelColumn":
        """Create a column of a dbt model or seed: pass exactly one parent."""
        validate_required_fields(["name"], [name])
        if (model_qualified_name is None) == (seed_qualified_name is None):
            raise ValueError(
                "Exactly one of model_qualified_name or seed_qualified_name is required"
            )
        parent_qualified_name = model_qualified_name or seed_qualified_name
        parent_arg = "model_qualified_name"
        if model_qualified_name is None:
            parent_arg = "seed_qualified_name"
        parsed = parse_dbt_env_qualified_name(parent_qualified_name, parent_arg)
        connection_qn, connector_name, parent_unique_id = parsed
        # atlan-dbt-app sets dbtModelQualifiedName to the parent for seeds too.
        column = cls(
            name=name,
            qualified_name=f"{parent_qualified_name}/{name}",
            connection_qualified_name=connection_qn,
            connector_name=connector_name,
            asset_dbt_unique_id=f"{parent_unique_id}/{name}",
            dbt_model_qualified_name=parent_qualified_name,
        )
        if model_qualified_name is not None:
            column.dbt_model = RelatedDbtModel(qualified_name=model_qualified_name)
        else:
            column.dbt_seed = RelatedDbtSeed(qualified_name=seed_qualified_name)
        return column

    @classmethod
    def create(cls, **kwargs) -> "DbtModelColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DbtModelColumn":
        return cls.updater(**kwargs)
