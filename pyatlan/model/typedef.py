from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanTypeCategory, Cardinality, IndexType


class TypeDef(AtlanObject):
    category: AtlanTypeCategory = Field(
        None, description="Type of the type_ definition.\n"
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
        None, description="Description of the type_ definition."
    )
    guid: Optional[str] = Field(
        None,
        description="Unique identifier that represents the type_ definition.",
        example="917ffec9-fa84-4c59-8e6c-c7b114d04be3",
    )
    name: str = Field(..., description="Unique name of this type_ definition.\n")
    type_version: Optional[str] = Field(
        None, description="Internal use only.\n", example="1.0"
    )
    update_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was last assets_updated, in milliseconds.\n",
        example=1649172284333,
    )
    updated_by: Optional[str] = Field(
        None,
        description="Username of the user who last assets_updated the object.\n",
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
        None, description="Optional properties of the type_ definition."
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )


class AttributeDef(AtlanObject):
    class Options(AtlanObject):
        description: Optional[str] = Field(
            None,
            description="Optional description of the attribute.\n",
        )
        applicable_entity_types: Optional[str] = Field(
            '["Asset"]',
            description="Set of entities on which this attribute can be applied.\n",
        )
        custom_applicable_entity_types: Optional[str] = Field(
            '["AtlasGlossary","LookerFolder","AtlasGlossaryCategory","SnowflakePipe","Process","LookerDashboard",'
            '"View","PowerBIWorkspace","PowerBIDatasource","ModeChart","GCSBucket","LookerField","LookerQuery",'
            '"PowerBITile","PresetChart","PowerBIDashboard","SalesforceReport","SalesforceObject","TableauDatasource",'
            '"Folder","S3Object","MetabaseCollection","SalesforceOrganization","PowerBIDataset","TableauDashboard",'
            '"S3Bucket","PowerBIMeasure","TablePartition","TableauWorkbook","TableauSite","Table",'
            '"TableauCalculatedField","TableauFlow","ModeQuery","PresetDataset","SalesforceDashboard",'
            '"Collection","LookerModel","PresetWorkspace","DbtModelColumn","PowerBIDataflow","LookerView",'
            '"MetabaseDashboard","DbtModel","SalesforceField","Query","TableauWorksheet","DataStudioAsset",'
            '"PowerBITable","TableauProject","DbtProcess","TableauDatasourceField","APIPath","DbtMetric","LookerLook",'
            '"ColumnProcess","PowerBIReport","MaterialisedView","Schema","SnowflakeStream","Database","LookerProject",'
            '"DbtColumnProcess","Column","LookerTile","BIProcess","TableauMetric","PowerBIColumn","PresetDashboard",'
            '"LookerExplore","ModeReport","ModeCollection","GCSObject","MetabaseQuestion","APISpec","PowerBIPage",'
            '"AtlasGlossaryTerm","ModeWorkspace"]',
            description="Set of entities on which this attribute should appear.\n",
        )
        allow_search: bool = Field(
            False,
            description="Whether the attribute should be searchable (true) or not (false).\n",
        )
        max_str_length: str = Field(
            "100000000", description="Maximum length allowed for a string value.\n"
        )
        allow_filtering: bool = Field(
            True,
            description="Whether this attribute should appear in the filterable facets of discovery (true) or not "
            "(false).\n",
        )
        multi_value_select: bool = Field(
            False,
            description="Whether this attribute can have multiple values (true) or only a single value (false).\n",
        )
        show_in_overview: bool = Field(
            False,
            description="Whether users will see this attribute in the overview tab of the sidebar (true) or not "
            "(false).\n",
        )
        is_deprecated: Optional[str] = Field(
            None,
            description="Whether the attribute is deprecated ('true') or not (None or 'false').\n",
        )
        is_enum: Optional[bool] = Field(
            None,
            description="Whether the attribute is an enumeration (true) or not (None or false).\n",
        )
        enum_type: Optional[str] = Field(
            None,
            description="Name of the enumeration (options), when the attribute is an enumeration.\n",
        )
        custom_type: Optional[str] = Field(
            None,
            description="Used for Atlan-specific types like `users`, `groups`, `url`, and `SQL`.\n",
        )
        is_archived: bool = Field(
            False,
            description="Whether the attribute has been deleted (true) or is still active (false).\n",
        )
        archived_at: Optional[int] = Field(
            None, description="When the attribute was deleted.\n"
        )
        archived_by: Optional[str] = Field(
            None, description="User who deleted the attribute.\n"
        )
        is_soft_reference: Optional[str] = Field(None, description="TBC")
        is_append_on_partial_update: Optional[str] = Field(None, description="TBC")
        primitive_type: Optional[str] = Field(
            None, description="The type of the option"
        )

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
    display_name: str = Field(
        None,
        description="Name to use within all user interactions through the user interface. Note that this may not "
        "be the same name used to update or interact with the attribute through API operations, for "
        "that see the `name` property. (This property can be used instead of `name` for the creation "
        "of an attribute definition as well.)\n",
        example="Custom Field 1",
    )
    name: str = Field(
        None,
        description="Unique name of this attribute definition. When provided during creation, this should be the "
        "human-readable name for the attribute. When returned (or provided for an update) this will be "
        "the static-hashed name that Atlan uses internally. (This is to allow the name to be changed "
        "by the user without impacting existing instances of the attribute.)\n",
    )
    include_in_notification: Optional[bool] = Field(
        False, description="", example=False
    )
    index_type: Optional[IndexType] = Field(None, description="", example="DEFAULT")
    is_indexable: Optional[bool] = Field(
        True,
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
    options: AttributeDef.Options = Field(
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
    index_type_es_config: Optional[Dict[str, str]] = Field(
        None, description="", alias="indexTypeESConfig"
    )
    index_type_es_fields: Optional[Dict[str, dict[str, str]]] = Field(
        None, description="", alias="indexTypeESFields"
    )
    is_default_value_null: Optional[bool] = Field(None, description="TBC")


class StructDef(TypeDef):
    category: AtlanTypeCategory = AtlanTypeCategory.STRUCT
    attribute_defs: Optional[List[AttributeDef]] = Field(
        None,
        description="List of attributes that should be available in the type_ definition.",
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )


class ClassificationDef(TypeDef):
    attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CLASSIFICATION
    display_name: str = Field(
        None, description="Name used for display purposes (in user interfaces).\n"
    )
    entity_types: Optional[List[str]] = Field(
        None,
        description="A list of the entity types that this classification can be used against."
        " (This should be `Asset` to allow classification of any asset in Atlan.)",
        example=["Asset"],
    )
    options: Optional[Dict[str, Any]] = Field(
        None, description="Optional properties of the type_ definition."
    )
    sub_types: Optional[List[str]] = Field(
        [],
        description="List of the sub-types that extend from this type_ definition. Generally this is not specified "
        "in any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
        example=[],
    )
    super_types: Optional[List[str]] = Field(
        [],
        description="List of the super-types that this type_ definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
        example=[],
    )
    service_type: Optional[str] = Field(
        None, description="Name used for display purposes (in user interfaces).\n"
    )
    skip_display_name_uniqueness_check: Optional[bool] = Field(None)


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
        description="List of the sub-types that extend from this type_ definition. Generally this is not specified in "
        "any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
        example=[],
    )
    super_types: Optional[List[str]] = Field(
        [],
        description="List of the super-types that this type_ definition should extend. (This is intended for internal "
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
        primitive_type: Optional[str] = Field(
            None, description="The type of the option", alias="primitiveType"
        )

    attribute_defs: List[AttributeDef] = Field(
        [],
        description="List of custom attributes defined within the custom metadata.\n",
        example=[],
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CUSTOM_METADATA
    display_name: str = Field(
        None, description="Name used for display purposes (in user interfaces).\n"
    )
    options: Optional[CustomMetadataDef.Options] = Field(
        None, description="Optional properties of the type_ definition."
    )


class TypeDefResponse(AtlanObject):
    enum_defs: List[EnumDef] = Field(
        None, description="List of enumeration type_ definitions."
    )
    struct_defs: List[StructDef] = Field(
        None, description="List of struct type_ definitions."
    )
    classification_defs: List[ClassificationDef] = Field(
        None, description="List of classification type_ definitions."
    )
    entity_defs: List[EntityDef] = Field(
        None, description="List of entity type_ definitions."
    )
    relationship_defs: List[RelationshipDef] = Field(
        None, description="List of relationship type_ definitions."
    )
    custom_metadata_defs: List[CustomMetadataDef] = Field(
        None,
        description="List of custom metadata type_ definitions.",
        alias="businessMetadataDefs",
    )
