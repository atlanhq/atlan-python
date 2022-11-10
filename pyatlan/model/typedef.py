from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanTypeCategory, IndexType, Cardinality


class TypeDef(AtlanObject):
    category: Optional[AtlanTypeCategory] = Field(
        None, description="Type of the type definition.\n"
    )
    create_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was created, in milliseconds.\n",
        example=1648852296555,
    )
    created_by: Optional[str] = Field(
        None,
        description="Username of the user who created the object.\n",
        example="jsmith",
    )
    description: Optional[str] = Field(
        None, description="Description of the type definition."
    )
    guid: Optional[str] = Field(
        None,
        description="Unique identifier that represents the type definition.",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
    )
    name: Optional[str] = Field(
        None, description="Unique name of this type definition.\n"
    )
    type_version: Optional[str] = Field(
        None, description="Internal use only.\n", example="1.0"
    )
    update_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was last updated, in milliseconds.\n",
        example=1649172284333,
    )
    updated_by: Optional[str] = Field(
        None,
        description="Username of the user who last updated the object.\n",
        example="jsmith",
    )
    version: Optional[int] = Field(
        None, description="Version of this object.\n", example=2
    )


class EnumDef(TypeDef):
    class ElementDef(AtlanObject):
        value: str = Field(None, description="Unused.")
        description: Optional[str] = Field(None, description="Unused.")
        ordinal: Optional[int] = Field(None, description="Unused.")

    category: AtlanTypeCategory = AtlanTypeCategory.ENUM
    element_defs: List["EnumDef.ElementDef"] = Field(None, description="Unused.")
    options: Optional[Dict[str, Any]] = Field(
        None, description="Optional properties of the type definition."
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )


class StructDef(TypeDef):
    class AttributeDef(AtlanObject):
        cardinality: Optional[Cardinality] = Field(
            "SINGLE",
            description="Whether the attribute allows a single or multiple values. In the case of multiple values, "
            "`LIST` indicates they are ordered and duplicates are allowed, while `SET` indicates "
            "they are unique and unordered.\n",
            example="SINGLE",
        )
        constraints: Optional[List[Dict[str, Any]]] = Field(
            None, description="Internal use only."
        )
        description: Optional[str] = Field(
            None,
            description="Description of the attribute definition.\n",
            example="Our first custom metadata field.",
        )
        default_value: Optional[str] = Field(
            None,
            description="Default value for this attribute (if any).\n",
            example="abc123",
        )
        display_name: Optional[str] = Field(
            None,
            description="Name to use within all user interactions through the user interface. Note that this may not "
            "be the same name used to update or interact with the attribute through API operations, for "
            "that see the `name` property. (This property can be used instead of `name` for the creation "
            "of an attribute definition as well.)\n",
            example="Custom Field 1",
        )
        name: Optional[str] = Field(
            None,
            description="Unique name of this attribute definition. When provided during creation, this should be the "
            "human-readable name for the attribute. When returned (or provided for an update) this will be "
            "the static-hashed name that Atlan uses internally. (This is to allow the name to be changed "
            "by the user without impacting existing instances of the attribute.)\n",
        )
        include_in_notification: Optional[bool] = Field(
            None, description="", example=False
        )
        index_type: Optional[IndexType] = Field(None, description="", example="DEFAULT")
        is_indexable: Optional[bool] = Field(
            None,
            description="When true, values for this attribute will be indexed for searching.\n",
            example=True,
        )
        is_optional: Optional[bool] = Field(
            True,
            description="When true, a value will not be required for this attribute.\n",
            example=True,
        )
        is_unique: Optional[bool] = Field(
            False,
            description="When true, this attribute must be unique across all assets.\n",
            example=False,
        )
        options: Optional[Dict[str, Any]] = Field(
            None, description="Extensible options for the attribute."
        )
        search_weight: Optional[float] = Field(None, description="")
        skip_scrubbing: Optional[bool] = Field(
            False,
            description="When true, scrubbing of data will be skipped.\n",
            example=False,
        )
        type_name: Optional[str] = Field(
            "string", description="Type of this attribute.\n", example="string"
        )
        values_min_count: Optional[float] = Field(
            0,
            description="Minimum number of values for this attribute. If greater than 0, this attribute "
            "becomes required.\n",
            example=0,
        )
        values_max_count: Optional[float] = Field(
            1,
            description="Maximum number of values for this attribute. If greater than 1, this attribute allows "
            "multiple values.\n",
            example=1,
        )
        index_type_es_fields: Optional[Dict[str, dict[str, str]]] = Field(
            None, description="", alias="indexTypeESFields"
        )

    category: AtlanTypeCategory = AtlanTypeCategory.STRUCT
    attribute_defs: Optional[List[StructDef.AttributeDef]] = Field(
        None,
        description="List of attributes that should be available in the type definition.",
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )


class ClassificationDef(TypeDef):
    attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CLASSIFICATION
    display_name: Optional[str] = Field(
        None, description="Name used for display purposes (in user interfaces).\n"
    )
    entity_types: Optional[List[str]] = Field(
        None,
        description="A list of the entity types that this classification can be used against."
        " (This should be `Asset` to allow classification of any asset in Atlan.)",
        example=["Asset"],
    )
    options: Optional[Dict[str, Any]] = Field(
        None, description="Optional properties of the type definition."
    )
    sub_types: Optional[List[str]] = Field(
        [],
        description="List of the sub-types that extend from this type definition. Generally this is not specified "
        "in any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
        example=[],
    )
    super_types: Optional[List[str]] = Field(
        [],
        description="List of the super-types that this type definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
        example=[],
    )


class EntityDef(TypeDef):
    attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    business_attribute_defs: Optional[Dict[str, List[Dict[str, Any]]]] = Field(
        [], description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.ENTITY
    relationship_attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )
    sub_types: Optional[List[str]] = Field(
        [],
        description="List of the sub-types that extend from this type definition. Generally this is not specified in "
        "any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
        example=[],
    )
    super_types: Optional[List[str]] = Field(
        [],
        description="List of the super-types that this type definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
        example=[],
    )


class RelationshipDef(TypeDef):
    attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.RELATIONSHIP
    end_def1: Optional[Dict[str, Any]] = Field({}, description="Unused.", example={})
    end_def2: Optional[Dict[str, Any]] = Field({}, description="Unused.", example={})
    propagate_tags: str = Field(
        "ONE_TO_TWO", description="Unused", example="ONE_TO_TWO"
    )
    relationship_category: str = Field(
        "AGGREGATION", description="Unused", example="AGGREGATION"
    )
    relationship_label: str = Field(
        "__SalesforceOrganization.reports",
        description="Unused",
        example="__SalesforceOrganization.reports",
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )


class CustomMetadataDef(TypeDef):
    class AttributeDef(AtlanObject):
        cardinality: Optional[Cardinality] = Field(
            "SINGLE",
            description="Whether the attribute allows a single or multiple values. In the case of multiple values, "
            "`LIST` indicates they are ordered and duplicates are allowed, while `SET` indicates they are "
            "unique and unordered.\n",
            example="SINGLE",
        )
        constraints: Optional[List[Dict[str, Any]]] = Field(
            None, description="Internal use only."
        )
        description: Optional[str] = Field(
            None,
            description="Description of the attribute definition.\n",
            example="Our first custom metadata field.",
        )
        display_name: Optional[str] = Field(
            None,
            description="Name to use within all user interactions through the user interface. Note that this may not "
            "be the same name used to update or interact with the attribute through API operations, for "
            "that see the `name` property. (This property can be used instead of `name` for the creation "
            "of an attribute definition as well.)\n",
            example="Custom Field 1",
        )
        include_in_notification: Optional[bool] = Field(
            None, description="", example=False
        )
        index_type: Optional[IndexType] = Field(None, description="", example="DEFAULT")
        index_type_es_config: Optional[Dict[str, str]] = Field(
            None, description="", alias="indexTypeESConfig"
        )
        index_type_es_fields: Optional[Dict[str, Dict[str, str]]] = Field(
            None, description="", alias="indexTypeESFields"
        )
        is_indexable: Optional[bool] = Field(
            None,
            description="When true, values for this attribute will be indexed for searching.\n",
            example=True,
        )
        is_optional: Optional[bool] = Field(
            True,
            description="When true, a value will not be required for this attribute.\n",
            example=True,
        )
        is_unique: Optional[bool] = Field(
            False,
            description="When true, this attribute must be unique across all assets.\n",
            example=False,
        )
        name: Optional[str] = Field(
            None,
            description="Unique name of this attribute definition. When provided during creation, this should be the "
            "human-readable name for the attribute. When returned (or provided for an update) this will be "
            "the static-hashed name that Atlan uses internally. (This is to allow the name to be changed "
            "by the user without impacting existing instances of the attribute.)\n",
        )
        options: Optional[Dict[str, Any]] = Field(
            None, description="Extensible options for the attribute."
        )
        search_weight: Optional[float] = Field(None, description="")
        skip_scrubbing: Optional[bool] = Field(
            False,
            description="When true, scrubbing of data will be skipped.\n",
            example=False,
        )
        type_name: Optional[str] = Field(
            "string", description="Type of this attribute.\n", example="string"
        )
        values_min_count: Optional[float] = Field(
            0,
            description="Minimum number of values for this attribute. If greater than 0, this attribute becomes "
            "required.\n",
            example=0,
        )
        values_max_count: Optional[float] = Field(
            1,
            description="Maximum number of values for this attribute. If greater than 1, this attribute allows "
            "multiple values.\n",
            example=1,
        )

    class Options(AtlanObject):
        emoji: Optional[str] = Field(
            None,
            description="If the logoType is emoji, this should hold the emoji character.\n",
        )
        image_id: Optional[str] = Field(
            None, description="The id of the image used for the logo.\n"
        )
        is_locked: Optional[str] = Field(
            None,
            description="Indicates whether the custom metadata can be managed in the UI (false) or not (true).\n",
        )
        logo_type: Optional[str] = Field(
            None, description="Type of logo used for the custom metadata.\n"
        )
        logo_Url: Optional[str] = Field(
            None,
            description="If the logoType is image, this should hold a URL to the image.\n",
        )

    attribute_defs: Optional[List[CustomMetadataDef.AttributeDef]] = Field(
        [], description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CUSTOM_METADATA
    display_name: Optional[str] = Field(
        None, description="Name used for display purposes (in user interfaces).\n"
    )
    options: Optional[CustomMetadataDef.Options] = Field(
        None, description="Optional properties of the type definition."
    )


class TypeDefResponse(AtlanObject):
    enum_defs: Optional[List[EnumDef]] = Field(
        None, description="List of enumeration type definitions."
    )
    struct_defs: Optional[List[StructDef]] = Field(
        None, description="List of struct type definitions."
    )
    classification_defs: Optional[List[ClassificationDef]] = Field(
        None, description="List of classification type definitions."
    )
    entity_defs: Optional[List[EntityDef]] = Field(
        None, description="List of entity type definitions."
    )
    relationship_defs: Optional[List[RelationshipDef]] = Field(
        None, description="List of relationship type definitions."
    )
    custom_metadata_defs: Optional[List[CustomMetadataDef]] = Field(
        None,
        description="List of custom metadata type definitions.",
        alias="businessMetadataDefs",
    )
