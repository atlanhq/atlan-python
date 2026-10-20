# INTERNAL_IMPORT: from pyatlan.model.dbt_utils import dbt_project_qualified_name
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
    ) -> "DbtTag":
        validate_required_fields(["name"], [name])
        base, connector_name = dbt_project_qualified_name(
            connection_qualified_name, account_id, project_id
        )
        return cls(
            name=name,
            qualified_name=f"{base}/tag/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def create(cls, **kwargs) -> "DbtTag":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DbtTag":
        return cls.updater(**kwargs)
