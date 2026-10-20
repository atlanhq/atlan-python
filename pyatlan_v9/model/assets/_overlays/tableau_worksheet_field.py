# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        worksheet_qualified_name: str,
        field_id: str,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauWorksheetField":
        """
        field_id is the id of the datasource or calculated field this worksheet field uses.
        """
        validate_required_fields(
            ["name", "worksheet_qualified_name", "field_id"],
            [name, worksheet_qualified_name, field_id],
        )
        fields = worksheet_qualified_name.split("/")
        if len(fields) != 7:
            raise ValueError(
                f"Invalid worksheet_qualified_name: {worksheet_qualified_name}. "
                "Expected format: default/tableau/<epoch>/<site_id>/<project_id>/"
                "<workbook_id>/<worksheet_id>"
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
            qualified_name=f"{worksheet_qualified_name}/{field_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            tableau_site_qualified_name=site_qn,
            tableau_project_qualified_name=project_qn,
            tableau_top_level_project_qualified_name=(
                top_level_project_qualified_name or project_qn
            ),
            tableau_workbook_qualified_name="/".join(fields[:6]),
            tableau_worksheet_qualified_name=worksheet_qualified_name,
            tableau_worksheet=RelatedTableauWorksheet(
                qualified_name=worksheet_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "TableauWorksheetField":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauWorksheetField":
        return cls.updater(**kwargs)
