from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossarySynonym(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossarySynonym",
        description="Terms that have the same (or a very similar) meaning, in the same language.",
    )
    attributes: AtlasGlossarySynonym.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossarySynonym.Attributes(),
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
            description="Status of the synonym assignment, typically used by discovery engines.",
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

    class Synonyms(Asset):
        type_name: str = Field(
            default="AtlasGlossarySynonym",
            description="Terms that have the same (or a very similar) meaning, in the same language.",
        )
        relationship_type: str = Field(
            default="AtlasGlossarySynonym",
            description="Fixed typeName for AtlasGlossarySynonym.",
        )
        relationship_attributes: AtlasGlossarySynonym = Field(
            default=None,
            description="Attributes of the AtlasGlossarySynonym.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def synonyms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossarySynonym.Synonyms:
        """
        Build the AtlasGlossarySynonym relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossarySynonym.Synonyms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossarySynonym.Synonyms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossarySynonym.Synonyms.update_forward_refs()
AtlasGlossarySynonym.update_forward_refs()
