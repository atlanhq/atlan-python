from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryIsARelationship(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryIsARelationship",
        description="Relationship between a more abstract and more concrete concept. For example, this relationship would be use to say that 'Cat' ISA 'Animal'.",
    )
    attributes: AtlasGlossaryIsARelationship.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryIsARelationship.Attributes(),
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

    class Classifies(Asset):
        type_name: str = Field(
            default="AtlasGlossaryIsARelationship",
            description="More general term that defines a group of terms, for example: 'animal'.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryIsARelationship",
            description="Fixed typeName for AtlasGlossaryIsARelationship.",
        )
        relationship_attributes: AtlasGlossaryIsARelationship = Field(
            default=None,
            description="Attributes of the AtlasGlossaryIsARelationship.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class IsA(Asset):
        type_name: str = Field(
            default="AtlasGlossaryIsARelationship",
            description="More specific term that is a sub-class of another term, for example: 'cat'.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryIsARelationship",
            description="Fixed typeName for AtlasGlossaryIsARelationship.",
        )
        relationship_attributes: AtlasGlossaryIsARelationship = Field(
            default=None,
            description="Attributes of the AtlasGlossaryIsARelationship.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def classifies(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryIsARelationship.Classifies:
        """
        Build the AtlasGlossaryIsARelationship relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryIsARelationship.Classifies._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryIsARelationship.Classifies._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def is_a(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryIsARelationship.IsA:
        """
        Build the AtlasGlossaryIsARelationship relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryIsARelationship.IsA._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryIsARelationship.IsA._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryIsARelationship.Classifies.update_forward_refs()
AtlasGlossaryIsARelationship.IsA.update_forward_refs()
AtlasGlossaryIsARelationship.update_forward_refs()
