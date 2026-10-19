# STDLIB_IMPORT: from typing import Optional
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        site_qualified_name: str,
        project_id: str,
        parent_project_qualified_name: Optional[str] = None,
        top_level_project_qualified_name: Optional[str] = None,
    ) -> "TableauProject":
        validate_required_fields(
            ["name", "site_qualified_name", "project_id"],
            [name, site_qualified_name, project_id],
        )
        fields = site_qualified_name.split("/")
        if len(fields) != 4:
            raise ValueError(
                f"Invalid site_qualified_name: {site_qualified_name}. "
                "Expected format: default/tableau/<epoch>/<site_id>"
            )
        # Tableau project qualifiedNames are flat under the site, even when nested:
        # the nesting is carried only by parentProject and the project hierarchy.
        for label, project_qn in (
            ("parent_project_qualified_name", parent_project_qualified_name),
            ("top_level_project_qualified_name", top_level_project_qualified_name),
        ):
            if project_qn is not None and (
                len(project_qn.split("/")) != 5
                or not project_qn.startswith(f"{site_qualified_name}/")
            ):
                raise ValueError(
                    f"Invalid {label}: {project_qn}. "
                    f"Expected format: {site_qualified_name}/<project_id>"
                )
        if top_level_project_qualified_name and not parent_project_qualified_name:
            raise ValueError(
                "top_level_project_qualified_name requires parent_project_qualified_name"
            )
        project = cls(
            name=name,
            qualified_name=f"{site_qualified_name}/{project_id}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            site_qualified_name=site_qualified_name,
            is_top_level_project=parent_project_qualified_name is None,
            site=RelatedTableauSite(qualified_name=site_qualified_name),
        )
        if parent_project_qualified_name:
            project.top_level_project_qualified_name = (
                top_level_project_qualified_name or parent_project_qualified_name
            )
            project.parent_project = RelatedTableauProject(
                qualified_name=parent_project_qualified_name
            )
        return project

    @classmethod
    def create(cls, **kwargs) -> "TableauProject":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "TableauProject":
        return cls.updater(**kwargs)
