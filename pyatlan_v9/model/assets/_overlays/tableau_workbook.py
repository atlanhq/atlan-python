# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        project_qualified_name: str,
        workbook_id: str,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauWorkbook":
        validate_required_fields(
            ["name", "project_qualified_name", "workbook_id"],
            [name, project_qualified_name, workbook_id],
        )
        fields = project_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid project_qualified_name: {project_qualified_name}. "
                "Expected format: default/tableau/<epoch>/<site_id>/<project_id>"
            )
        site_qn = "/".join(fields[:4])
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
            qualified_name=f"{project_qualified_name}/{workbook_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            site_qualified_name=site_qn,
            project_qualified_name=project_qualified_name,
            top_level_project_qualified_name=(
                top_level_project_qualified_name or project_qualified_name
            ),
            project=RelatedTableauProject(qualified_name=project_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "TableauWorkbook":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauWorkbook":
        return cls.updater(**kwargs)
