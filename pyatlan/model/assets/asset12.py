# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional, Set

from pydantic import Field, validator

from pyatlan.model.enums import (
    AuthPolicyCategory,
    AuthPolicyResourceCategory,
    AuthPolicyType,
    DataAction,
    PersonaGlossaryAction,
    PersonaMetadataAction,
)
from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.utils import validate_required_fields

from .asset00 import SelfAsset
from .asset05 import AccessControl, AuthPolicy


class Persona(AccessControl):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(cls, *, name: str) -> Persona:
        validate_required_fields(["name"], [name])
        attributes = Persona.Attributes.create(name=name)
        return cls(attributes=attributes)

    @classmethod
    # @validate_arguments()
    def create_metadata_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PersonaMetadataAction],
        connection_qualified_name: str,
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "actions", "resources"],
            [name, persona_id, policy_type, actions, resources],
        )
        policy = AuthPolicy._AuthPolicy__create(name=name)  # type: ignore
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.connection_qualified_name = connection_qualified_name
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "metadata"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    # @validate_arguments()
    def create_data_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        connection_qualified_name: str,
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "resources"],
            [name, persona_id, policy_type, resources],
        )
        policy = AuthPolicy._AuthPolicy__create(name=name)  # type: ignore
        policy.policy_actions = {DataAction.SELECT.value}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.connection_qualified_name = connection_qualified_name
        policy.policy_resources = resources
        policy.policy_resources.add("entity-type:*")
        policy.policy_resource_category = AuthPolicyResourceCategory.ENTITY.value
        policy.policy_service_name = "heka"
        policy.policy_sub_category = "data"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    # @validate_arguments()
    def create_glossary_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PersonaGlossaryAction],
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "actions", "resources"],
            [name, persona_id, policy_type, actions, resources],
        )
        policy = AuthPolicy._AuthPolicy__create(name=name)  # type: ignore
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "glossary"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        is_enabled: bool = True,
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "is_enabled"],
            [name, qualified_name, is_enabled],
        )
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
                is_access_control_enabled=is_enabled,
            )
        )

    type_name: str = Field("Persona", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Persona":
            raise ValueError("must be Persona")
        return v

    def __setattr__(self, name, value):
        if name in Persona._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PERSONA_GROUPS: ClassVar[KeywordField] = KeywordField(
        "personaGroups", "personaGroups"
    )
    """
    TBC
    """
    PERSONA_USERS: ClassVar[KeywordField] = KeywordField("personaUsers", "personaUsers")
    """
    TBC
    """
    ROLE_ID: ClassVar[KeywordField] = KeywordField("roleId", "roleId")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "persona_groups",
        "persona_users",
        "role_id",
    ]

    @property
    def persona_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.persona_groups

    @persona_groups.setter
    def persona_groups(self, persona_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.persona_groups = persona_groups

    @property
    def persona_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.persona_users

    @persona_users.setter
    def persona_users(self, persona_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.persona_users = persona_users

    @property
    def role_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.role_id

    @role_id.setter
    def role_id(self, role_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.role_id = role_id

    class Attributes(AccessControl.Attributes):
        persona_groups: Optional[set[str]] = Field(
            None, description="", alias="personaGroups"
        )
        persona_users: Optional[set[str]] = Field(
            None, description="", alias="personaUsers"
        )
        role_id: Optional[str] = Field(None, description="", alias="roleId")

        @classmethod
        # @validate_arguments()
        def create(cls, name: str) -> Persona.Attributes:
            if not name:
                raise ValueError("name cannot be blank")
            validate_required_fields(["name"], [name])
            return Persona.Attributes(
                qualified_name=name,
                name=name,
                display_name=name,
                is_access_control_enabled=True,
                description="",
            )

    attributes: "Persona.Attributes" = Field(
        default_factory=lambda: Persona.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Persona.Attributes.update_forward_refs()
