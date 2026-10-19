# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        page_qualified_name: str,
        page_name: str,
    ) -> "FabricVisual":
        validate_required_fields(
            ["name", "page_qualified_name", "page_name"],
            [name, page_qualified_name, page_name],
        )
        fields = page_qualified_name.split("/")
        if len(fields) != 6:
            raise ValueError(
                f"Invalid page_qualified_name: {page_qualified_name}. "
                "Expected format: "
                "default/fabric/<epoch>/<workspace_id>/<report_id>/<page_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{page_qualified_name}/{name}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            asset_space_qualified_name="/".join(fields[:4]),
            fabric_page_qualified_name=page_qualified_name,
            fabric_page_name=page_name,
            fabric_page=RelatedFabricPage(qualified_name=page_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "FabricVisual":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "FabricVisual":
        return cls.updater(**kwargs)
