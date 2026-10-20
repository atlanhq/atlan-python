# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        page_qualified_name: str,
        page_name: str,
        workbook_name: str,
        data_element_id: str,
    ) -> "SigmaDataElement":
        validate_required_fields(
            [
                "name",
                "page_qualified_name",
                "page_name",
                "workbook_name",
                "data_element_id",
            ],
            [name, page_qualified_name, page_name, workbook_name, data_element_id],
        )
        fields = page_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid page_qualified_name: {page_qualified_name}. "
                "Expected format: default/sigma/<epoch>/<workbook_id>/<page_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{page_qualified_name}/{data_element_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            sigma_workbook_qualified_name="/".join(fields[:4]),
            sigma_workbook_name=workbook_name,
            sigma_page_qualified_name=page_qualified_name,
            sigma_page_name=page_name,
            sigma_page=RelatedSigmaPage(
                unique_attributes={"qualifiedName": page_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "SigmaDataElement":
        return cls.creator(**kwargs)

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SigmaDataElement":
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SigmaDataElement":
        return cls.updater(**kwargs)

    def trim_to_required(self) -> "SigmaDataElement":
        return SigmaDataElement.updater(qualified_name=self.qualified_name, name=self.name)
