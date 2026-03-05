# IMPORT: from pyatlan.model.enums import EntityStatus
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        client: Any,
        name: str,
        cm_name: str,
        cm_attribute: str,
        badge_conditions: list[BadgeCondition],
    ) -> "Badge":
        """Create a new Badge asset."""
        validate_required_fields(
            ["client", "name", "cm_name", "cm_attribute", "badge_conditions"],
            [client, name, cm_name, cm_attribute, badge_conditions],
        )
        cm_id = client.custom_metadata_cache.get_id_for_name(cm_name)
        cm_attr_id = client.custom_metadata_cache.get_attr_id_for_name(
            set_name=cm_name, attr_name=cm_attribute
        )
        from pyatlan.model.enums import EntityStatus

        return cls(
            name=name,
            qualified_name=f"badges/global/{cm_id}.{cm_attr_id}",
            badge_metadata_attribute=f"{cm_id}.{cm_attr_id}",
            badge_conditions=badge_conditions,
            status=EntityStatus.ACTIVE,
        )

    @classmethod
    async def creator_async(
        cls,
        *,
        client: Any,
        name: str,
        cm_name: str,
        cm_attribute: str,
        badge_conditions: list[BadgeCondition],
    ) -> "Badge":
        """Create a new Badge asset (async version)."""
        validate_required_fields(
            ["client", "name", "cm_name", "cm_attribute", "badge_conditions"],
            [client, name, cm_name, cm_attribute, badge_conditions],
        )
        cm_id = await client.custom_metadata_cache.get_id_for_name(cm_name)
        cm_attr_id = await client.custom_metadata_cache.get_attr_id_for_name(
            set_name=cm_name, attr_name=cm_attribute
        )
        from pyatlan.model.enums import EntityStatus

        return cls(
            name=name,
            qualified_name=f"badges/global/{cm_id}.{cm_attr_id}",
            badge_metadata_attribute=f"{cm_id}.{cm_attr_id}",
            badge_conditions=badge_conditions,
            status=EntityStatus.ACTIVE,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "Badge":
        """Create a Badge instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "Badge":
        """Return only fields required for update operations."""
        return Badge.updater(qualified_name=self.qualified_name, name=self.name)
