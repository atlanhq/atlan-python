from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryTermCategorization(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryTermCategorization",
        description="Organizes terms into categories. A term may be linked with many categories and a category may have many terms linked to it. This relationship may connect terms and categories both in the same glossary or in different glossaries.",
    )
    attributes: AtlasGlossaryTermCategorization.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryTermCategorization.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        description: Optional[str] = Field(
            default=None,
            description="Details about the term categorization.",
        )
        status: Optional[AtlasGlossaryTermRelationshipStatus] = Field(
            default=None,
            description="Status of the term categorization, typically used by discovery engines.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class Terms(Asset):
        type_name: str = Field(
            default="AtlasGlossaryTermCategorization",
            description="Terms organized within this category.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryTermCategorization",
            description="Fixed typeName for AtlasGlossaryTermCategorization.",
        )
        relationship_attributes: AtlasGlossaryTermCategorization = Field(
            default=None,
            description="Attributes of the AtlasGlossaryTermCategorization.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class Categories(Asset):
        type_name: str = Field(
            default="AtlasGlossaryTermCategorization",
            description="Categories within which this term is organized.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryTermCategorization",
            description="Fixed typeName for AtlasGlossaryTermCategorization.",
        )
        relationship_attributes: AtlasGlossaryTermCategorization = Field(
            default=None,
            description="Attributes of the AtlasGlossaryTermCategorization.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def terms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryTermCategorization.Terms:
        """
        Build the AtlasGlossaryTermCategorization relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryTermCategorization.Terms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryTermCategorization.Terms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def categories(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryTermCategorization.Categories:
        """
        Build the AtlasGlossaryTermCategorization relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryTermCategorization.Categories._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryTermCategorization.Categories._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryTermCategorization.Terms.update_forward_refs()
AtlasGlossaryTermCategorization.Categories.update_forward_refs()
AtlasGlossaryTermCategorization.update_forward_refs()
