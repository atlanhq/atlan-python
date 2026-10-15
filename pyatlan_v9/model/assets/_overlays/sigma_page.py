# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        workbook_qualified_name: str,
        workbook_name: str,
        page_id: str,
    ) -> "SigmaPage":
        validate_required_fields(
            ["name", "workbook_qualified_name", "workbook_name", "page_id"],
            [name, workbook_qualified_name, workbook_name, page_id],
        )
        fields = workbook_qualified_name.split("/")
        if len(fields) != 4:
            raise ValueError(
                f"Invalid workbook_qualified_name: {workbook_qualified_name}. "
                "Expected format: default/sigma/<epoch>/<workbook_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{workbook_qualified_name}/{page_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            sigma_workbook_qualified_name=workbook_qualified_name,
            sigma_workbook_name=workbook_name,
            sigma_workbook=RelatedSigmaWorkbook(qualified_name=workbook_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "SigmaPage":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SigmaPage":
        return cls.updater(**kwargs)
