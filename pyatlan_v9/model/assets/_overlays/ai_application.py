# IMPORT: from pyatlan.model.enums import AtlanConnectorType
# IMPORT: from pyatlan.utils import to_camel_case
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        ai_application_version: str,
        ai_application_development_stage: str,
        owner_groups: Union[set[str], None] = None,
        owner_users: Union[set[str], None] = None,
    ) -> "AIApplication":
        """Create a new AIApplication asset."""
        validate_required_fields(
            ["name", "ai_application_version", "ai_application_development_stage"],
            [name, ai_application_version, ai_application_development_stage],
        )
        name_camel_case = to_camel_case(name)
        return cls(
            name=name,
            qualified_name=f"default/ai/aiapplication/{name_camel_case}",
            connector_name=AtlanConnectorType.AI.value,
            ai_application_version=ai_application_version,
            ai_application_development_stage=ai_application_development_stage,
            owner_groups=owner_groups if owner_groups is not None else UNSET,
            owner_users=owner_users if owner_users is not None else UNSET,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AIApplication":
        """Create an AIApplication instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AIApplication":
        """Return only fields required for update operations."""
        return AIApplication.updater(qualified_name=self.qualified_name, name=self.name)
