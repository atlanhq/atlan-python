from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryRelatedTerm(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryRelatedTerm",
        description="Links terms that may also be of interest. It is like a 'see also' link in a dictionary.",
    )
    attributes: AtlasGlossaryRelatedTerm.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryRelatedTerm.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        description: Optional[str] = Field(
            default=None,
            description="Explains why the linked term is of interest.",
        )
        expression: Optional[str] = Field(
            default=None,
            description="Expression used to set the related term.",
        )
        status: Optional[AtlasGlossaryTermRelationshipStatus] = Field(
            default=None,
            description="Status of the related term assignment, typically used by discovery engines.",
        )
        steward: Optional[str] = Field(
            default=None,
            description="User responsible for assessing the relationship and deciding if it should be approved or not.",
        )
        source: Optional[str] = Field(
            default=None,
            description="Source of the related term assignment.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class SeeAlso(Asset):
        type_name: str = Field(
            default="AtlasGlossaryRelatedTerm",
            description="Linked terms that may also be of interest.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryRelatedTerm",
            description="Fixed typeName for AtlasGlossaryRelatedTerm.",
        )
        relationship_attributes: AtlasGlossaryRelatedTerm = Field(
            default=None,
            description="Attributes of the AtlasGlossaryRelatedTerm.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def see_also(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryRelatedTerm.SeeAlso:
        """
        Build the AtlasGlossaryRelatedTerm relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryRelatedTerm.SeeAlso._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryRelatedTerm.SeeAlso._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryRelatedTerm.SeeAlso.update_forward_refs()
AtlasGlossaryRelatedTerm.update_forward_refs()
