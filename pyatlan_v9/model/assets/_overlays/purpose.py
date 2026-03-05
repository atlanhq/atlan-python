# IMPORT: from pyatlan.model.enums import AuthPolicyCategory, AuthPolicyResourceCategory, AuthPolicyType, DataAction, PurposeMetadataAction
# INTERNAL_IMPORT: from pyatlan.model.core import AtlanTagName
# INTERNAL_IMPORT: from pyatlan.model.structs import SourceTagAttachment
# INTERNAL_IMPORT: from pyatlan.utils import init_guid, validate_required_fields

    @property
    def purpose_atlan_tags(self) -> Union[list[AtlanTagName], None]:
        """Expose purpose classifications as AtlanTagName objects for parity."""
        if self.purpose_classifications in (UNSET, None):
            return None
        return [
            tag if isinstance(tag, AtlanTagName) else AtlanTagName(str(tag))
            for tag in self.purpose_classifications
        ]

    @purpose_atlan_tags.setter
    def purpose_atlan_tags(self, value: Union[list[AtlanTagName], None]) -> None:
        if value is None:
            self.purpose_classifications = None
        else:
            self.purpose_classifications = [str(tag) for tag in value]

    @classmethod
    @init_guid
    def creator(cls, *, name: str, atlan_tags: list[AtlanTagName]) -> "Purpose":
        """Create a new Purpose asset."""
        validate_required_fields(["name", "atlan_tags"], [name, atlan_tags])
        return cls(
            name=name,
            qualified_name=name,
            display_name=name,
            description="",
            is_access_control_enabled=True,
            purpose_classifications=[str(tag) for tag in atlan_tags],
        )

    @classmethod
    def updater(
        cls, *, qualified_name: str, name: str, is_enabled: bool = True
    ) -> "Purpose":
        """Create a Purpose asset for update operations."""
        validate_required_fields(
            ["qualified_name", "name", "is_enabled"],
            [qualified_name, name, is_enabled],
        )
        return cls(
            qualified_name=qualified_name,
            name=name,
            is_access_control_enabled=is_enabled,
        )

    @classmethod
    def create_for_modification(
        cls,
        qualified_name: str = "",
        name: str = "",
        is_enabled: bool = True,
    ) -> "Purpose":
        warn(
            (
                "This method is deprecated, please use 'updater' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.updater(
            qualified_name=qualified_name, name=name, is_enabled=is_enabled
        )

    @classmethod
    def create_metadata_policy(
        cls,
        *,
        client: "AtlanClient",
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PurposeMetadataAction],
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["client", "name", "purpose_id", "policy_type", "actions"],
            [client, name, purpose_id, policy_type, actions],
        )
        target_found = False
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PURPOSE.value
        policy.policy_type = policy_type
        policy.policy_resource_category = AuthPolicyResourceCategory.TAG.value
        policy.policy_service_name = "atlas_tag"
        policy.policy_sub_category = "metadata"
        purpose = Purpose()
        purpose.guid = purpose_id
        policy.access_control = purpose
        if all_users:
            target_found = True
            policy.policy_groups = {"public"}
        else:
            if policy_groups:
                for group_name in policy_groups:
                    if not client.group_cache.get_id_for_name(group_name):
                        raise ValueError(
                            f"Provided group name {group_name} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                for username in policy_users:
                    if not client.user_cache.get_id_for_name(username):
                        raise ValueError(
                            f"Provided username {username} was not found in Atlan."
                        )
                target_found = True
                policy.policy_users = policy_users
            else:
                policy.policy_users = None
        if target_found:
            return policy
        else:
            raise ValueError("No user or group specified for the policy.")

    @classmethod
    def create_data_policy(
        cls,
        *,
        client: "AtlanClient",
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["client", "name", "purpose_id", "policy_type"],
            [client, name, purpose_id, policy_type],
        )
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {DataAction.SELECT.value}
        policy.policy_category = AuthPolicyCategory.PURPOSE.value
        policy.policy_type = policy_type
        policy.policy_resource_category = AuthPolicyResourceCategory.TAG.value
        policy.policy_service_name = "atlas_tag"
        policy.policy_sub_category = "data"
        purpose = Purpose()
        purpose.guid = purpose_id
        policy.access_control = purpose
        if all_users:
            target_found = True
            policy.policy_groups = {"public"}
        else:
            if policy_groups:
                for group_name in policy_groups:
                    if not client.group_cache.get_id_for_name(group_name):
                        raise ValueError(
                            f"Provided group name {group_name} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                for username in policy_users:
                    if not client.user_cache.get_id_for_name(username):
                        raise ValueError(
                            f"Provided username {username} was not found in Atlan."
                        )
                target_found = True
                policy.policy_users = policy_users
            else:
                policy.policy_users = None
        if target_found:
            return policy
        else:
            raise ValueError("No user or group specified for the policy.")

    def trim_to_required(self) -> "Purpose":
        """Return only required fields for updates."""
        return Purpose.updater(qualified_name=self.qualified_name, name=self.name)
