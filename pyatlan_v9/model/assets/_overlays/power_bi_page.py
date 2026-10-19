# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        report_qualified_name: str,
        page_id: str,
    ) -> "PowerBIPage":
        validate_required_fields(
            ["name", "report_qualified_name", "page_id"],
            [name, report_qualified_name, page_id],
        )
        fields = report_qualified_name.split("/")
        if len(fields) != 5 or not all(fields):
            raise ValueError("report_qualified_name is invalid")
        return cls(
            name=name,
            qualified_name=f"{report_qualified_name}/{page_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            workspace_qualified_name="/".join(fields[:4]),
            report_qualified_name=report_qualified_name,
            report=RelatedPowerBIReport(
                unique_attributes={"qualifiedName": report_qualified_name}
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "PowerBIPage":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "PowerBIPage":
        return cls.updater(**kwargs)
