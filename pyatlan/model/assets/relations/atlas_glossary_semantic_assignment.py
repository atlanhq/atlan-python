from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossarySemanticAssignment(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossarySemanticAssignment",
        description="Assigns meaning to an asset by linking the term that describes the meaning of the asset. The semantic assignment needs to be a controlled relationship when glossary definitions are used to provide classifications for the data assets and hence define how the data is to be governed.",
    )
    attributes: AtlasGlossarySemanticAssignment.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossarySemanticAssignment.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        description: Optional[str] = Field(
            default=None,
            description="Details about the semantic assignment.",
        )
        expression: Optional[str] = Field(
            default=None,
            description="Expression that was used to create the semantic assignment.",
        )
        status: Optional[AtlasGlossaryTermRelationshipStatus] = Field(
            default=None,
            description="Status of the semantic assignment, typically used by discovery engines.",
        )
        confidence: Optional[int] = Field(
            default=None,
            description="Level of confidence (0-100%) in the correctness of the semantic assignment, typically used by discovery engines.",
        )
        created_by: Optional[str] = Field(
            default=None,
            description="Username of the user who created the semantic assignment.",
        )
        steward: Optional[str] = Field(
            default=None,
            description="User responsible for assessing the semantic assignment and deciding if it should be approved or not.",
        )
        source: Optional[str] = Field(
            default=None,
            description="Source of the semantic assignment.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class AssignedEntities(Asset):
        type_name: str = Field(
            default="AtlasGlossarySemanticAssignment",
            description="Assets assigned this term.",
        )
        relationship_type: str = Field(
            default="AtlasGlossarySemanticAssignment",
            description="Fixed typeName for AtlasGlossarySemanticAssignment.",
        )
        relationship_attributes: AtlasGlossarySemanticAssignment = Field(
            default=None,
            description="Attributes of the AtlasGlossarySemanticAssignment.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class Meanings(Asset):
        type_name: str = Field(
            default="AtlasGlossarySemanticAssignment",
            description="Glossary terms that are linked to this asset.",
        )
        relationship_type: str = Field(
            default="AtlasGlossarySemanticAssignment",
            description="Fixed typeName for AtlasGlossarySemanticAssignment.",
        )
        relationship_attributes: AtlasGlossarySemanticAssignment = Field(
            default=None,
            description="Attributes of the AtlasGlossarySemanticAssignment.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def assigned_entities(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossarySemanticAssignment.AssignedEntities:
        """
        Build the AtlasGlossarySemanticAssignment relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossarySemanticAssignment.AssignedEntities._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossarySemanticAssignment.AssignedEntities._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def meanings(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossarySemanticAssignment.Meanings:
        """
        Build the AtlasGlossarySemanticAssignment relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossarySemanticAssignment.Meanings._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossarySemanticAssignment.Meanings._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossarySemanticAssignment.AssignedEntities.update_forward_refs()
AtlasGlossarySemanticAssignment.Meanings.update_forward_refs()
AtlasGlossarySemanticAssignment.update_forward_refs()
