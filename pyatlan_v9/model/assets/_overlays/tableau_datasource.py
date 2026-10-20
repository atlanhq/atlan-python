# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        project_qualified_name: str,
        datasource_id: str,
        workbook_qualified_name: Optional[str] = None,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauDatasource":
        """
        Builds a published datasource, or an embedded one when
        workbook_qualified_name is given (its qualifiedName then sits under the workbook).
        """
        validate_required_fields(
            ["name", "project_qualified_name", "datasource_id"],
            [name, project_qualified_name, datasource_id],
        )
        fields = project_qualified_name.split("/")
        if len(fields) != 5:
            raise ValueError(
                f"Invalid project_qualified_name: {project_qualified_name}. "
                "Expected format: default/tableau/<epoch>/<site_id>/<project_id>"
            )
        if workbook_qualified_name is not None and (
            len(workbook_qualified_name.split("/")) != 6
            or not workbook_qualified_name.startswith(f"{project_qualified_name}/")
        ):
            raise ValueError(
                f"Invalid workbook_qualified_name: {workbook_qualified_name}. "
                f"Expected format: {project_qualified_name}/<workbook_id>"
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
        datasource = cls(
            name=name,
            qualified_name=f"{workbook_qualified_name or project_qualified_name}/{datasource_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            site_qualified_name=site_qn,
            project_qualified_name=project_qualified_name,
            top_level_project_qualified_name=(
                top_level_project_qualified_name or project_qualified_name
            ),
            is_published=workbook_qualified_name is None,
            project=RelatedTableauProject(qualified_name=project_qualified_name),
        )
        if workbook_qualified_name:
            datasource.workbook_qualified_name = workbook_qualified_name
            datasource.workbook = RelatedTableauWorkbook(
                qualified_name=workbook_qualified_name
            )
        return datasource

    @classmethod
    def create(cls, **kwargs) -> "TableauDatasource":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauDatasource":
        return cls.updater(**kwargs)
