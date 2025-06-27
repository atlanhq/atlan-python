from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryReplacementTerm(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryReplacementTerm",
        description="Indicates term(s) must be used instead of another. This is stronger version of the PreferredTerm.",
    )
    attributes: AtlasGlossaryReplacementTerm.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryReplacementTerm.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        description: Optional[str] = Field(
            default=None,
            description="Details about the relationship.",
        )
        expression: Optional[str] = Field(
            default=None,
            description="Expression used to set the relationship.",
        )
        status: Optional[AtlasGlossaryTermRelationshipStatus] = Field(
            default=None,
            description="Status of the relationship, typically used by discovery engines.",
        )
        steward: Optional[str] = Field(
            default=None,
            description="User responsible for assessing the relationship and deciding if it should be approved or not.",
        )
        source: Optional[str] = Field(
            default=None,
            description="Source of the relationship.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class ReplacedBy(Asset):
        type_name: str = Field(
            default="AtlasGlossaryReplacementTerm",
            description="Term(s) that must no longer be used.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryReplacementTerm",
            description="Fixed typeName for AtlasGlossaryReplacementTerm.",
        )
        relationship_attributes: AtlasGlossaryReplacementTerm = Field(
            default=None,
            description="Attributes of the AtlasGlossaryReplacementTerm.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class ReplacementTerms(Asset):
        type_name: str = Field(
            default="AtlasGlossaryReplacementTerm",
            description="Term(s) that must be used instead.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryReplacementTerm",
            description="Fixed typeName for AtlasGlossaryReplacementTerm.",
        )
        relationship_attributes: AtlasGlossaryReplacementTerm = Field(
            default=None,
            description="Attributes of the AtlasGlossaryReplacementTerm.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def replaced_by(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryReplacementTerm.ReplacedBy:
        """
        Build the AtlasGlossaryReplacementTerm relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryReplacementTerm.ReplacedBy._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryReplacementTerm.ReplacedBy._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def replacement_terms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryReplacementTerm.ReplacementTerms:
        """
        Build the AtlasGlossaryReplacementTerm relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryReplacementTerm.ReplacementTerms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryReplacementTerm.ReplacementTerms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryReplacementTerm.ReplacedBy.update_forward_refs()
AtlasGlossaryReplacementTerm.ReplacementTerms.update_forward_refs()
AtlasGlossaryReplacementTerm.update_forward_refs()
