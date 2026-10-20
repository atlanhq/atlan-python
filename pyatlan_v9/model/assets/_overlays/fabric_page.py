# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        report_qualified_name: str,
        page_id: str,
    ) -> "FabricPage":
        validate_required_fields(
            ["name", "report_qualified_name", "page_id"],
            [name, report_qualified_name, page_id],
        )
        fields = report_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid report_qualified_name: {report_qualified_name}. "
                "Expected format: default/fabric/<epoch>/<workspace_id>/<report_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{report_qualified_name}/{page_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_space_qualified_name="/".join(fields[:4]),
            fabric_report_qualified_name=report_qualified_name,
            fabric_report=RelatedFabricReport(qualified_name=report_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "FabricPage":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "FabricPage":
        return cls.updater(**kwargs)
