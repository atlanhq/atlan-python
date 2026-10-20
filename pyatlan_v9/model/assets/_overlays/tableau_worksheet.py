# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        workbook_qualified_name: str,
        worksheet_id: str,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauWorksheet":
        validate_required_fields(
            ["name", "workbook_qualified_name", "worksheet_id"],
            [name, workbook_qualified_name, worksheet_id],
        )
        fields = workbook_qualified_name.split("/")
        if len(fields) != 6:
            raise ValueError(
                f"Invalid workbook_qualified_name: {workbook_qualified_name}. "
                "Expected format: "
                "default/tableau/<epoch>/<site_id>/<project_id>/<workbook_id>"
            )
        site_qn = "/".join(fields[:4])
        project_qn = "/".join(fields[:5])
        if top_level_project_qualified_name is not None and (
            len(top_level_project_qualified_name.split("/")) != 5
            or not top_level_project_qualified_name.startswith(f"{site_qn}/")
        ):
            raise ValueError(
                f"Invalid top_level_project_qualified_name: "
                f"{top_level_project_qualified_name}. "
                f"Expected format: {site_qn}/<project_id>"
            )
        return cls(
            name=name,
            qualified_name=f"{workbook_qualified_name}/{worksheet_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            site_qualified_name=site_qn,
            project_qualified_name=project_qn,
            top_level_project_qualified_name=(
                top_level_project_qualified_name or project_qn
            ),
            workbook_qualified_name=workbook_qualified_name,
            workbook=RelatedTableauWorkbook(qualified_name=workbook_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "TableauWorksheet":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauWorksheet":
        return cls.updater(**kwargs)
