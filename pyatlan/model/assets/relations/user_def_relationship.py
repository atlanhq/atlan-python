from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import SaveSemantic


class UserDefRelationship(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="UserDefRelationship",
        description="A generic relationship to hold relationship between any type of asset",
    )
    attributes: UserDefRelationship.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: UserDefRelationship.Attributes(),
        description="Map of attributes in the instance and their values",
    )

    class Attributes(AtlanObject):
        to_type_label: Optional[str] = Field(
            default=None,
            description="Name for the relationship when referring from endDef1 asset to endDef2 asset.",
        )
        from_type_label: Optional[str] = Field(
            default=None,
            description="Name for the relationship when referring from endDef2 asset to endDef1 asset.",
        )

    def __init__(__pydantic_self__, **data: Any) -> None:
        if "attributes" not in data:
            data = {"attributes": data}
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["attributes", "type_name"])

    class UserDefRelationshipTo(Asset):
        type_name: str = Field(
            default="UserDefRelationship",
            description="Name of the relationship type that defines the relationship.",
        )
        relationship_type: str = Field(
            default="UserDefRelationship",
            description="Fixed typeName for UserDefRelationship.",
        )
        relationship_attributes: UserDefRelationship = Field(
            default=None,
            description="Attributes of the UserDefRelationship.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class UserDefRelationshipFrom(Asset):
        type_name: str = Field(
            default="UserDefRelationship",
            description="Name of the relationship type that defines the relationship.",
        )
        relationship_type: str = Field(
            default="UserDefRelationship",
            description="Fixed typeName for UserDefRelationship.",
        )
        relationship_attributes: UserDefRelationship = Field(
            default=None,
            description="Attributes of the UserDefRelationship.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def user_def_relationship_to(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> UserDefRelationship.UserDefRelationshipTo:
        """
        Build the UserDefRelationship relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return UserDefRelationship.UserDefRelationshipTo._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return UserDefRelationship.UserDefRelationshipTo._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def user_def_relationship_from(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> UserDefRelationship.UserDefRelationshipFrom:
        """
        Build the UserDefRelationship relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return UserDefRelationship.UserDefRelationshipFrom._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return UserDefRelationship.UserDefRelationshipFrom._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


UserDefRelationship.UserDefRelationshipTo.update_forward_refs()
UserDefRelationship.UserDefRelationshipFrom.update_forward_refs()
UserDefRelationship.update_forward_refs()
