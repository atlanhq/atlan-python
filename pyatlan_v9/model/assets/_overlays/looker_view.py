# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        project_qualified_name: str,
        file_path: str,
    ) -> "LookerView":
        """
        Create a new LookerView, keyed as atlan-looker-app keys it:
        ``{project_qualified_name}/view/{md5(file_path)}/{name}``.

        Args:
            name: Name of the LookML view
            project_qualified_name: Unique name of the project in which the view exists
            file_path: Path of the LookML file that declares the view. Anything up to and
                including ``cloned_repos/`` is ignored when hashing, as the app does.

        Returns:
            LookerView instance ready to be created
        """
        validate_required_fields(
            ["name", "project_qualified_name", "file_path"],
            [name, project_qualified_name, file_path],
        )
        view = looker_qn.looker_id(name, "name")
        parent = looker_qn.parse_project(project_qualified_name)
        file_hash = looker_qn.file_path_hash(file_path)
        return cls(
            name=name,
            qualified_name=f"{project_qualified_name}/view/{file_hash}/{view}",
            connection_qualified_name=parent.connection_qualified_name,
            connector_name=looker_qn.connector_name(parent.connection_qualified_name),
            project_name=parent.project_name,
            looker_view_file_path=file_path,
            project=RelatedLookerProject(qualified_name=project_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "LookerView":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerView":
        return cls.updater(**kwargs)
