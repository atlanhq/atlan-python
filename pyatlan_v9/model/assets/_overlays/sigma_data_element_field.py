# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        data_element_qualified_name: str,
        data_element_name: str,
        page_name: str,
        workbook_name: str,
        field_id: str,
    ) -> "SigmaDataElementField":
        validate_required_fields(
            [
                "name",
                "data_element_qualified_name",
                "data_element_name",
                "page_name",
                "workbook_name",
                "field_id",
            ],
            [
                name,
                data_element_qualified_name,
                data_element_name,
                page_name,
                workbook_name,
                field_id,
            ],
        )
        fields = data_element_qualified_name.split("/")
        if len(fields) != 6:
            raise ValueError(
                f"Invalid data_element_qualified_name: {data_element_qualified_name}. "
                "Expected format: "
                "default/sigma/<epoch>/<workbook_id>/<page_id>/<data_element_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{data_element_qualified_name}/{field_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            sigma_workbook_qualified_name="/".join(fields[:4]),
            sigma_workbook_name=workbook_name,
            sigma_page_qualified_name="/".join(fields[:5]),
            sigma_page_name=page_name,
            sigma_data_element_qualified_name=data_element_qualified_name,
            sigma_data_element_name=data_element_name,
            sigma_data_element=RelatedSigmaDataElement(
                unique_attributes={"qualifiedName": data_element_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "SigmaDataElementField":
        return cls.creator(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SigmaDataElementField":
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SigmaDataElementField":
        return cls.updater(**kwargs)

    def trim_to_required(self) -> "SigmaDataElementField":
        return SigmaDataElementField.updater(qualified_name=self.qualified_name, name=self.name)
