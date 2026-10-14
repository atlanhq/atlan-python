# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        dashboard_qualified_name: str,
        field_id: str,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauDashboardField":
        """
        field_id is the id of the datasource field this dashboard field uses.
        """
        validate_required_fields(
            ["name", "dashboard_qualified_name", "field_id"],
            [name, dashboard_qualified_name, field_id],
        )
        fields = dashboard_qualified_name.split("/")
        if len(fields) != 7:
            raise ValueError(
                f"Invalid dashboard_qualified_name: {dashboard_qualified_name}. "
                "Expected format: default/tableau/<epoch>/<site_id>/<project_id>/"
                "<workbook_id>/<dashboard_id>"
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
            qualified_name=f"{dashboard_qualified_name}/{field_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            tableau_site_qualified_name=site_qn,
            tableau_project_qualified_name=project_qn,
            tableau_top_level_project_qualified_name=(
                top_level_project_qualified_name or project_qn
            ),
            tableau_dashboard_qualified_name=dashboard_qualified_name,
            tableau_dashboard=RelatedTableauDashboard(
                qualified_name=dashboard_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "TableauDashboardField":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauDashboardField":
        return cls.updater(**kwargs)
