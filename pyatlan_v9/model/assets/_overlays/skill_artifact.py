# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        skill_qualified_name: str,
        relative_path: str,
        file_type: str,
        name: str | None = None,
    ) -> "SkillArtifact":
        validate_required_fields(
            ["skill_qualified_name", "relative_path", "file_type"],
            [skill_qualified_name, relative_path, file_type],
        )
        fields = skill_qualified_name.split("/")
        if len(fields) < 6 or fields[3] != "skill":
            raise ValueError(
                f"Invalid skill_qualified_name: {skill_qualified_name}. "
                "Expected format: default/connector/connection_id/skill/scope_owner/name"
            )
        return cls(
            name=name or relative_path.split("/")[-1],
            qualified_name=f"{skill_qualified_name}/artifact/{relative_path}",
            connection_qualified_name="/".join(fields[:3]),
            connector_name=fields[1],
            file_type=file_type,
            skill_source=RelatedSkill(qualified_name=skill_qualified_name),
        )

    @classmethod
    def create(cls, **kwargs) -> "SkillArtifact":
        return cls.creator(**kwargs)

    @classmethod
    def create_for_modification(cls, **kwargs) -> "SkillArtifact":
        return cls.updater(**kwargs)
