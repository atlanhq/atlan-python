# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        context_repository_qualified_name: str,
    ) -> "Skill":
        validate_required_fields(
            ["name", "context_repository_qualified_name"],
            [name, context_repository_qualified_name],
        )
        fields = context_repository_qualified_name.split("/")
        if len(fields) != 5 or fields[3] != "skills":
            raise ValueError(
                "Invalid context_repository_qualified_name: "
                f"{context_repository_qualified_name}. "
                "Expected format: default/connector/connection_id/skills/scope_owner"
            )
        connection_qn = "/".join(fields[:3])
        return cls(
            name=name,
            qualified_name=f"{connection_qn}/skill/{fields[4]}/{name}",
            connection_qualified_name=connection_qn,
            connector_name=fields[1],
            context_source_repository=RelatedContextRepository(
                qualified_name=context_repository_qualified_name
            ),
        )

    @classmethod
    def create(cls, **kwargs) -> "Skill":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "Skill":
        return cls.updater(**kwargs)
