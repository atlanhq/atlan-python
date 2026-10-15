# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        data_model_id: str,
    ) -> "SigmaDataModel":
        validate_required_fields(
            ["name", "connection_qualified_name", "data_model_id"],
            [name, connection_qualified_name, data_model_id],
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/dataModels/{data_model_id}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
            asset_source_id=data_model_id,
        )

    @classmethod
    def create(cls, **kwargs) -> "SigmaDataModel":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SigmaDataModel":
        return cls.updater(**kwargs)
