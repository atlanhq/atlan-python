from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryPreferredTerm(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryPreferredTerm",
        description="Indicates term(s) should be used in place of another. This relationship can be used to encourage adoption of newer vocabularies. This is a weaker version of ReplacementTerm.",
    )
    attributes: AtlasGlossaryPreferredTerm.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryPreferredTerm.Attributes(),
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
            description="Status of the relationship.",
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

    class PreferredTerms(Asset):
        type_name: str = Field(
            default="AtlasGlossaryPreferredTerm",
            description="Preferred term(s) to use instead of this term.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryPreferredTerm",
            description="Fixed typeName for AtlasGlossaryPreferredTerm.",
        )
        relationship_attributes: AtlasGlossaryPreferredTerm = Field(
            default=None,
            description="Attributes of the AtlasGlossaryPreferredTerm.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class PreferredToTerms(Asset):
        type_name: str = Field(
            default="AtlasGlossaryPreferredTerm",
            description="Other term(s) that are less common or less preferred than this term.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryPreferredTerm",
            description="Fixed typeName for AtlasGlossaryPreferredTerm.",
        )
        relationship_attributes: AtlasGlossaryPreferredTerm = Field(
            default=None,
            description="Attributes of the AtlasGlossaryPreferredTerm.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def preferred_terms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryPreferredTerm.PreferredTerms:
        """
        Build the AtlasGlossaryPreferredTerm relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryPreferredTerm.PreferredTerms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryPreferredTerm.PreferredTerms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def preferred_to_terms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryPreferredTerm.PreferredToTerms:
        """
        Build the AtlasGlossaryPreferredTerm relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryPreferredTerm.PreferredToTerms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryPreferredTerm.PreferredToTerms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryPreferredTerm.PreferredTerms.update_forward_refs()
AtlasGlossaryPreferredTerm.PreferredToTerms.update_forward_refs()
AtlasGlossaryPreferredTerm.update_forward_refs()
