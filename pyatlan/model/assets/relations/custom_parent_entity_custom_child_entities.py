from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import SaveSemantic


class CustomParentEntityCustomChildEntities(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="custom_parent_entity_custom_child_entities",
        description="Containment relationship between two custom entities.",
    )
    attributes: CustomParentEntityCustomChildEntities.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: CustomParentEntityCustomChildEntities.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        custom_entity_children_label: Optional[str] = Field(
            default=None,
            description="Name for the relationship when referring from the parent entity to its children entities.",
        )
        custom_entity_parent_label: Optional[str] = Field(
            default=None,
            description="Name for the relationship when referring from a child entity to its parent entity.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class CustomChildEntities(Asset):
        type_name: str = Field(
            default="custom_parent_entity_custom_child_entities",
            description="Custom entities contained within the parent entity.",
        )
        relationship_type: str = Field(
            default="custom_parent_entity_custom_child_entities",
            description="Fixed typeName for custom_parent_entity_custom_child_entities.",
        )
        relationship_attributes: CustomParentEntityCustomChildEntities = Field(
            default=None,
            description="Attributes of the custom_parent_entity_custom_child_entities.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class CustomParentEntity(Asset):
        type_name: str = Field(
            default="custom_parent_entity_custom_child_entities",
            description="Custom entity in which the child entities are contained.",
        )
        relationship_type: str = Field(
            default="custom_parent_entity_custom_child_entities",
            description="Fixed typeName for custom_parent_entity_custom_child_entities.",
        )
        relationship_attributes: CustomParentEntityCustomChildEntities = Field(
            default=None,
            description="Attributes of the custom_parent_entity_custom_child_entities.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def custom_child_entities(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> CustomParentEntityCustomChildEntities.CustomChildEntities:
        """
        Build the CustomParentEntityCustomChildEntities relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return (
                CustomParentEntityCustomChildEntities.CustomChildEntities._create_ref(
                    type_name=related.type_name,
                    guid=related.guid,
                    semantic=semantic,
                    relationship_attributes=self,
                )
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return CustomParentEntityCustomChildEntities.CustomChildEntities._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def custom_parent_entity(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> CustomParentEntityCustomChildEntities.CustomParentEntity:
        """
        Build the CustomParentEntityCustomChildEntities relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return CustomParentEntityCustomChildEntities.CustomParentEntity._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return CustomParentEntityCustomChildEntities.CustomParentEntity._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


CustomParentEntityCustomChildEntities.CustomChildEntities.update_forward_refs()
CustomParentEntityCustomChildEntities.CustomParentEntity.update_forward_refs()
CustomParentEntityCustomChildEntities.update_forward_refs()
