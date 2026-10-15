# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        model_qualified_name: str,
    ) -> "LookerExplore":
        """
        Create a new LookerExplore, keyed as atlan-looker-app keys it:
        ``{model_qualified_name}/{model}::{name}``.

        Args:
            name: Name of the explore (its LookML name, not its title)
            model_qualified_name: Unique name of the model in which the explore exists

        Returns:
            LookerExplore instance ready to be created
        """
        validate_required_fields(
            ["name", "model_qualified_name"], [name, model_qualified_name]
        )
        explore = looker_qn.looker_id(name, "name")
        parent = looker_qn.parse_model(model_qualified_name)
        project_qn = f"{parent.connection_qualified_name}/project/{parent.project_name}"
        return cls(
            name=name,
            qualified_name=f"{model_qualified_name}/{parent.model_name}::{explore}",
            connection_qualified_name=parent.connection_qualified_name,
            connector_name=looker_qn.connector_name(parent.connection_qualified_name),
            project_name=parent.project_name,
            model_name=parent.model_name,
            project=RelatedLookerProject(qualified_name=project_qn),
            model=RelatedLookerModel(qualified_name=model_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "LookerExplore":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerExplore":
        return cls.updater(**kwargs)
