from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryTranslation(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryTranslation",
        description="Related terms that represent the same meaning, but each written in a different language. Hence one is a translation of the other. The language of each term is defined in the Glossary object that anchors the term.",
    )
    attributes: AtlasGlossaryTranslation.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryTranslation.Attributes(),
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

    class TranslatedTerms(Asset):
        type_name: str = Field(
            default="AtlasGlossaryTranslation",
            description="Term(s) that are a translation of this term.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryTranslation",
            description="Fixed typeName for AtlasGlossaryTranslation.",
        )
        relationship_attributes: AtlasGlossaryTranslation = Field(
            default=None,
            description="Attributes of the AtlasGlossaryTranslation.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class TranslationTerms(Asset):
        type_name: str = Field(
            default="AtlasGlossaryTranslation",
            description="Term(s) for which this term is a translation.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryTranslation",
            description="Fixed typeName for AtlasGlossaryTranslation.",
        )
        relationship_attributes: AtlasGlossaryTranslation = Field(
            default=None,
            description="Attributes of the AtlasGlossaryTranslation.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def translated_terms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryTranslation.TranslatedTerms:
        """
        Build the AtlasGlossaryTranslation relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryTranslation.TranslatedTerms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryTranslation.TranslatedTerms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def translation_terms(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryTranslation.TranslationTerms:
        """
        Build the AtlasGlossaryTranslation relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryTranslation.TranslationTerms._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryTranslation.TranslationTerms._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryTranslation.TranslatedTerms.update_forward_refs()
AtlasGlossaryTranslation.TranslationTerms.update_forward_refs()
AtlasGlossaryTranslation.update_forward_refs()
