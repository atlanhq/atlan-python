from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import SaveSemantic


class CustomRelatedFromEntitiesCustomRelatedToEntities(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="custom_related_from_entities_custom_related_to_entities",
        description="Inter-relationship between two custom assets.",
    )
    attributes: CustomRelatedFromEntitiesCustomRelatedToEntities.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: CustomRelatedFromEntitiesCustomRelatedToEntities.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        custom_entity_to_label: Optional[str] = Field(
            default=None,
            description="Name for the relationship when referring from endDef1 entity to endDef2 entity.",
        )
        custom_entity_from_label: Optional[str] = Field(
            default=None,
            description="Name for the relationship when referring from endDef2 entity to endDef1 entity.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class CustomRelatedToEntities(Asset):
        type_name: str = Field(
            default="custom_related_from_entities_custom_related_to_entities",
            description="Target custom entity indicating where the relationship is directed.",
        )
        relationship_type: str = Field(
            default="custom_related_from_entities_custom_related_to_entities",
            description="Fixed typeName for custom_related_from_entities_custom_related_to_entities.",
        )
        relationship_attributes: CustomRelatedFromEntitiesCustomRelatedToEntities = Field(
            default=None,
            description="Attributes of the custom_related_from_entities_custom_related_to_entities.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class CustomRelatedFromEntities(Asset):
        type_name: str = Field(
            default="custom_related_from_entities_custom_related_to_entities",
            description="Source custom entity indicating where the relationship originates.",
        )
        relationship_type: str = Field(
            default="custom_related_from_entities_custom_related_to_entities",
            description="Fixed typeName for custom_related_from_entities_custom_related_to_entities.",
        )
        relationship_attributes: CustomRelatedFromEntitiesCustomRelatedToEntities = Field(
            default=None,
            description="Attributes of the custom_related_from_entities_custom_related_to_entities.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def custom_related_to_entities(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedToEntities:
        """
        Build the CustomRelatedFromEntitiesCustomRelatedToEntities relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedToEntities._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedToEntities._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def custom_related_from_entities(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedFromEntities:
        """
        Build the CustomRelatedFromEntitiesCustomRelatedToEntities relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedFromEntities._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedFromEntities._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedToEntities.update_forward_refs()
CustomRelatedFromEntitiesCustomRelatedToEntities.CustomRelatedFromEntities.update_forward_refs()
CustomRelatedFromEntitiesCustomRelatedToEntities.update_forward_refs()
