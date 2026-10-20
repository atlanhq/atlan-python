# INTERNAL_IMPORT: from pyatlan.model import looker_qn
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> "LookerProject":
        """
        Create a new LookerProject, keyed as atlan-looker-app keys it.

        Args:
            name: Name (id) of the LookML project
            connection_qualified_name: Unique name of the Looker connection

        Returns:
            LookerProject instance ready to be created
        """
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        project = looker_qn.looker_id(name, "name")
        connection_qn = looker_qn.connection(connection_qualified_name)
        return cls(
            name=name,
            qualified_name=f"{connection_qn}/project/{project}",
            connection_qualified_name=connection_qn,
            connector_name=looker_qn.connector_name(connection_qn),
        )

    @classmethod
    def create(cls, **kwargs) -> "LookerProject":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "LookerProject":
        return cls.updater(**kwargs)
