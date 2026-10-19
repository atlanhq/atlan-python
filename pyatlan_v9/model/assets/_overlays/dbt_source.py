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
        unique_id: str,
    ) -> "DbtSource":
        validate_required_fields(["name", "unique_id"], [name, unique_id])
        if "/" in unique_id:
            raise ValueError(f"unique_id cannot contain '/': {unique_id}")
        base, connector_name = dbt_project_qualified_name(
            connection_qualified_name, account_id, project_id
        )
        # Sources carry no env segment, unlike every other dbt type.
        return cls(
            name=name,
            qualified_name=f"{base}/{unique_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            asset_dbt_unique_id=unique_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "DbtSource":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "DbtSource":
        return cls.updater(**kwargs)
