# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .custom import Custom


class CustomEntity(Custom):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> CustomEntity:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = CustomEntity.Attributes.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="CustomEntity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CustomEntity":
            raise ValueError("must be CustomEntity")
        return v

    def __setattr__(self, name, value):
        if name in CustomEntity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUSTOM_CHILDREN_SUBTYPE: ClassVar[KeywordField] = KeywordField(
        "customChildrenSubtype", "customChildrenSubtype"
    )
    """
    Label of the children column for this asset type.
    """

    CUSTOM_PARENT_ENTITY: ClassVar[RelationField] = RelationField("customParentEntity")
    """
    TBC
    """
    CUSTOM_CHILD_ENTITIES: ClassVar[RelationField] = RelationField(
        "customChildEntities"
    )
    """
    TBC
    """
    CUSTOM_RELATED_TO_ENTITIES: ClassVar[RelationField] = RelationField(
        "customRelatedToEntities"
    )
    """
    TBC
    """
    CUSTOM_RELATED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "customRelatedFromEntities"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "custom_children_subtype",
        "custom_parent_entity",
        "custom_child_entities",
        "custom_related_to_entities",
        "custom_related_from_entities",
    ]

    @property
    def custom_children_subtype(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.custom_children_subtype
        )

    @custom_children_subtype.setter
    def custom_children_subtype(self, custom_children_subtype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_children_subtype = custom_children_subtype

    @property
    def custom_parent_entity(self) -> Optional[CustomEntity]:
        return None if self.attributes is None else self.attributes.custom_parent_entity

    @custom_parent_entity.setter
    def custom_parent_entity(self, custom_parent_entity: Optional[CustomEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_parent_entity = custom_parent_entity

    @property
    def custom_child_entities(self) -> Optional[List[CustomEntity]]:
        return (
            None if self.attributes is None else self.attributes.custom_child_entities
        )

    @custom_child_entities.setter
    def custom_child_entities(
        self, custom_child_entities: Optional[List[CustomEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_child_entities = custom_child_entities

    @property
    def custom_related_to_entities(self) -> Optional[List[CustomEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.custom_related_to_entities
        )

    @custom_related_to_entities.setter
    def custom_related_to_entities(
        self, custom_related_to_entities: Optional[List[CustomEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_related_to_entities = custom_related_to_entities

    @property
    def custom_related_from_entities(self) -> Optional[List[CustomEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.custom_related_from_entities
        )

    @custom_related_from_entities.setter
    def custom_related_from_entities(
        self, custom_related_from_entities: Optional[List[CustomEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_related_from_entities = custom_related_from_entities

    class Attributes(Custom.Attributes):
        custom_children_subtype: Optional[str] = Field(default=None, description="")
        custom_parent_entity: Optional[CustomEntity] = Field(
            default=None, description=""
        )  # relationship
        custom_child_entities: Optional[List[CustomEntity]] = Field(
            default=None, description=""
        )  # relationship
        custom_related_to_entities: Optional[List[CustomEntity]] = Field(
            default=None, description=""
        )  # relationship
        custom_related_from_entities: Optional[List[CustomEntity]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls, *, name: str, connection_qualified_name: str
        ) -> CustomEntity.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return CustomEntity.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: CustomEntity.Attributes = Field(
        default_factory=lambda: CustomEntity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


CustomEntity.Attributes.update_forward_refs()
