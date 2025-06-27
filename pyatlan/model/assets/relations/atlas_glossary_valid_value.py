from __future__ import annotations

from typing import Any, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.assets import Asset
from pyatlan.model.assets.relations import RelationshipAttributes
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlasGlossaryTermRelationshipStatus, SaveSemantic


class AtlasGlossaryValidValue(RelationshipAttributes):
    type_name: str = Field(
        allow_mutation=False,
        default="AtlasGlossaryValidValue",
        description="Terms that represent valid values for another, for example: 'red', 'blue', 'green' could all be valid values for a term 'color'.",
    )
    attributes: AtlasGlossaryValidValue.Attributes = Field(  # type: ignore[name-defined]
        default_factory=lambda: AtlasGlossaryValidValue.Attributes(),
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

    class ValidValuesFor(Asset):
        type_name: str = Field(
            default="AtlasGlossaryValidValue",
            description="Term for which this is a valid value.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryValidValue",
            description="Fixed typeName for AtlasGlossaryValidValue.",
        )
        relationship_attributes: AtlasGlossaryValidValue = Field(
            default=None,
            description="Attributes of the AtlasGlossaryValidValue.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    class ValidValues(Asset):
        type_name: str = Field(
            default="AtlasGlossaryValidValue",
            description="Valid values for this term.",
        )
        relationship_type: str = Field(
            default="AtlasGlossaryValidValue",
            description="Fixed typeName for AtlasGlossaryValidValue.",
        )
        relationship_attributes: AtlasGlossaryValidValue = Field(
            default=None,
            description="Attributes of the AtlasGlossaryValidValue.",
        )

        @validator("type_name")
        def validate_type_name(cls, v):
            return v

        def __init__(__pydantic_self__, **data: Any) -> None:
            super().__init__(**data)
            __pydantic_self__.__fields_set__.update(["type_name", "relationship_type"])

    def valid_values_for(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryValidValue.ValidValuesFor:
        """
        Build the AtlasGlossaryValidValue relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryValidValue.ValidValuesFor._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryValidValue.ValidValuesFor._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )

    def valid_values(
        self, related: Asset, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> AtlasGlossaryValidValue.ValidValues:
        """
        Build the AtlasGlossaryValidValue relationship (with attributes) into a related object.

        :param: related asset to which to build the detailed relationship
        :param: semantic to use for saving the relationship
        :returns: a detailed Atlan relationship that conforms
        to the necessary interface for a related asset
        """
        if related.guid:
            return AtlasGlossaryValidValue.ValidValues._create_ref(
                type_name=related.type_name,
                guid=related.guid,
                semantic=semantic,
                relationship_attributes=self,
            )

        # If the related asset does not have a GUID, we use qualifiedName
        return AtlasGlossaryValidValue.ValidValues._create_ref(
            type_name=related.type_name,
            unique_attributes={"qualifiedName": related.qualified_name},
            semantic=semantic,
            relationship_attributes=self,
        )


AtlasGlossaryValidValue.ValidValuesFor.update_forward_refs()
AtlasGlossaryValidValue.ValidValues.update_forward_refs()
AtlasGlossaryValidValue.update_forward_refs()
