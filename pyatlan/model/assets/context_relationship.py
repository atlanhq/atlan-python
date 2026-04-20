# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import ContextCardinality, ContextJoinType
from pyatlan.model.fields.atlan_fields import KeywordField

from .context_studio import ContextStudio


class ContextRelationship(ContextStudio):
    """Description"""

    type_name: str = Field(default="ContextRelationship", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextRelationship":
            raise ValueError("must be ContextRelationship")
        return v

    def __setattr__(self, name, value):
        if name in ContextRelationship._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_RELATIONSHIP_LEFT_PARTICIPANT: ClassVar[KeywordField] = KeywordField(
        "contextRelationshipLeftParticipant", "contextRelationshipLeftParticipant"
    )
    """
    Qualified name of the left-side table or entity in this join relationship.
    """
    CONTEXT_RELATIONSHIP_RIGHT_PARTICIPANT: ClassVar[KeywordField] = KeywordField(
        "contextRelationshipRightParticipant", "contextRelationshipRightParticipant"
    )
    """
    Qualified name of the right-side table or entity in this join relationship.
    """
    CONTEXT_RELATIONSHIP_JOIN_TYPE: ClassVar[KeywordField] = KeywordField(
        "contextRelationshipJoinType", "contextRelationshipJoinType"
    )
    """
    Type of SQL join for this relationship.
    """
    CONTEXT_RELATIONSHIP_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "contextRelationshipCardinality", "contextRelationshipCardinality"
    )
    """
    Cardinality of this join relationship, describing the row-level mapping between left and right participants.
    """
    CONTEXT_RELATIONSHIP_JOIN_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "contextRelationshipJoinQualifiedNames", "contextRelationshipJoinQualifiedNames"
    )
    """
    Qualified names of the physical columns involved in the join condition, enabling lineage from the semantic join to the underlying foreign key or join path.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "context_relationship_left_participant",
        "context_relationship_right_participant",
        "context_relationship_join_type",
        "context_relationship_cardinality",
        "context_relationship_join_qualified_names",
    ]

    @property
    def context_relationship_left_participant(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_relationship_left_participant
        )

    @context_relationship_left_participant.setter
    def context_relationship_left_participant(
        self, context_relationship_left_participant: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_relationship_left_participant = (
            context_relationship_left_participant
        )

    @property
    def context_relationship_right_participant(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_relationship_right_participant
        )

    @context_relationship_right_participant.setter
    def context_relationship_right_participant(
        self, context_relationship_right_participant: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_relationship_right_participant = (
            context_relationship_right_participant
        )

    @property
    def context_relationship_join_type(self) -> Optional[ContextJoinType]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_relationship_join_type
        )

    @context_relationship_join_type.setter
    def context_relationship_join_type(
        self, context_relationship_join_type: Optional[ContextJoinType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_relationship_join_type = context_relationship_join_type

    @property
    def context_relationship_cardinality(self) -> Optional[ContextCardinality]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_relationship_cardinality
        )

    @context_relationship_cardinality.setter
    def context_relationship_cardinality(
        self, context_relationship_cardinality: Optional[ContextCardinality]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_relationship_cardinality = (
            context_relationship_cardinality
        )

    @property
    def context_relationship_join_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_relationship_join_qualified_names
        )

    @context_relationship_join_qualified_names.setter
    def context_relationship_join_qualified_names(
        self, context_relationship_join_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_relationship_join_qualified_names = (
            context_relationship_join_qualified_names
        )

    class Attributes(ContextStudio.Attributes):
        context_relationship_left_participant: Optional[str] = Field(
            default=None, description=""
        )
        context_relationship_right_participant: Optional[str] = Field(
            default=None, description=""
        )
        context_relationship_join_type: Optional[ContextJoinType] = Field(
            default=None, description=""
        )
        context_relationship_cardinality: Optional[ContextCardinality] = Field(
            default=None, description=""
        )
        context_relationship_join_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )

    attributes: ContextRelationship.Attributes = Field(
        default_factory=lambda: ContextRelationship.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


ContextRelationship.Attributes.update_forward_refs()
