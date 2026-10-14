# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        data_model_qualified_name: str,
        data_model_name: str,
        element_id: str,
        column_id: str,
    ) -> "SigmaDataModelColumn":
        validate_required_fields(
            [
                "name",
                "data_model_qualified_name",
                "data_model_name",
                "element_id",
                "column_id",
            ],
            [name, data_model_qualified_name, data_model_name, element_id, column_id],
        )
        fields = data_model_qualified_name.split("/")
        if len(fields) != 5 or fields[3] != "dataModels":
            raise ValueError(
                f"Invalid data_model_qualified_name: {data_model_qualified_name}. "
                "Expected format: default/sigma/<epoch>/dataModels/<data_model_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{data_model_qualified_name}/{element_id}/{column_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_source_id=column_id,
            sigma_data_model_qualified_name=data_model_qualified_name,
            sigma_data_model_name=data_model_name,
            sigma_data_model=RelatedSigmaDataModel(
                qualified_name=data_model_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "SigmaDataModelColumn":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SigmaDataModelColumn":
        return cls.updater(**kwargs)
