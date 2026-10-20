# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        project_qualified_name: str,
    ) -> "LookerModel":
        """
        Create a new LookerModel, keyed as atlan-looker-app keys it.

        Args:
            name: Name of the LookML model
            project_qualified_name: Unique name of the project in which the model exists

        Returns:
            LookerModel instance ready to be created
        """
        validate_required_fields(
            ["name", "project_qualified_name"], [name, project_qualified_name]
        )
        model = looker_qn.looker_id(name, "name")
        parent = looker_qn.parse_project(project_qualified_name)
        return cls(
            name=name,
            qualified_name=f"{project_qualified_name}/model/{model}",
            connection_qualified_name=parent.connection_qualified_name,
            connector_name=looker_qn.connector_name(parent.connection_qualified_name),
            project_name=parent.project_name,
            project=RelatedLookerProject(qualified_name=project_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "LookerModel":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerModel":
        return cls.updater(**kwargs)
