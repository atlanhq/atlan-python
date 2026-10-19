# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        datasource_qualified_name: str,
        field_id: str,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauCalculatedField":
        """
        Builds a field in a published datasource
        (default/tableau/<epoch>/<site_id>/<project_id>/<datasource_id>) or in an
        embedded one (.../<project_id>/<workbook_id>/<datasource_id>).
        """
        validate_required_fields(
            ["name", "datasource_qualified_name", "field_id"],
            [name, datasource_qualified_name, field_id],
        )
        fields = datasource_qualified_name.split("/")
        if len(fields) not in (6, 7):
            raise ValueError(
                f"Invalid datasource_qualified_name: {datasource_qualified_name}. "
                "Expected format: "
                "default/tableau/<epoch>/<site_id>/<project_id>/<datasource_id> "
                "(published) or "
                "default/tableau/<epoch>/<site_id>/<project_id>/<workbook_id>/<datasource_id> "
                "(embedded)"
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
        field = cls(
            name=name,
            qualified_name=f"{datasource_qualified_name}/{field_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            site_qualified_name=site_qn,
            project_qualified_name=project_qn,
            top_level_project_qualified_name=(
                top_level_project_qualified_name or project_qn
            ),
            datasource_qualified_name=datasource_qualified_name,
            datasource=RelatedTableauDatasource(
                qualified_name=datasource_qualified_name
            ),
        )
        if len(fields) == 7:
            field.workbook_qualified_name = "/".join(fields[:6])
        return field

    @classmethod
    def create(cls, **kwargs) -> "TableauCalculatedField":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauCalculatedField":
        return cls.updater(**kwargs)
