from __future__ import annotations

import time
from typing import Any, Callable, Optional, cast

from pydantic import Field

from pyatlan.model.atlan_image import AtlanImage
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import (
    AtlanCustomAttributePrimitiveType,
    AtlanIcon,
    AtlanTagColor,
    AtlanTypeCategory,
    Cardinality,
    IndexType,
    TagIconType,
)

_complete_type_list = (
    '["ADLSAccount",'
    '"ADLSAccount",'
    '"ADLSContainer",'
    '"ADLSObject",'
    '"APIPath",'
    '"APISpec",'
    '"Collection",'
    '"Query",'
    '"BIProcess",'
    '"Badge",'
    '"Column",'
    '"ColumnProcess",'
    '"Connection",'
    '"DataStudioAsset",'
    '"Database",'
    '"DbtColumnProcess",'
    '"DbtMetric",'
    '"DbtModel",'
    '"DbtModelColumn",'
    '"DbtProcess",'
    '"DbtSource",'
    '"Folder",'
    '"GCSBucket",'
    '"GCSObject",'
    '"AtlasGlossary",'
    '"AtlasGlossaryCategory",'
    '"AtlasGlossaryTerm",'
    '"Insight",'
    '"KafkaConsumerGroup",'
    '"KafkaTopic",'
    '"Process",'
    '"Link",'
    '"LookerDashboard",'
    '"LookerExplore",'
    '"LookerField",'
    '"LookerFolder",'
    '"LookerLook",'
    '"LookerModel",'
    '"LookerProject",'
    '"LookerQuery",'
    '"LookerTile",'
    '"LookerView",'
    '"MCIncident",'
    '"MCMonitor",'
    '"MaterialisedView",'
    '"MetabaseCollection",'
    '"MetabaseDashboard",'
    '"MetabaseQuestion",'
    '"ModeChart",'
    '"ModeCollection",'
    '"ModeQuery",'
    '"ModeReport",'
    '"ModeWorkspace",'
    '"PowerBIColumn",'
    '"PowerBIDashboard",'
    '"PowerBIDataflow",'
    '"PowerBIDataset",'
    '"PowerBIDatasource",'
    '"PowerBIMeasure",'
    '"PowerBIPage",'
    '"PowerBIReport",'
    '"PowerBITable",'
    '"PowerBITile",'
    '"PowerBIWorkspace",'
    '"PresetChart",'
    '"PresetDashboard",'
    '"PresetDataset",'
    '"PresetWorkspace",'
    '"Procedure",'
    '"QlikApp",'
    '"QlikChart",'
    '"QlikDataset",'
    '"QlikSheet",'
    '"QlikSpace",'
    '"QlikStream",'
    '"QuickSightAnalysis",'
    '"QuickSightAnalysisVisual",'
    '"QuickSightDashboard",'
    '"QuickSightDashboardVisual",'
    '"QuickSightDataset",'
    '"QuickSightDatasetField",'
    '"QuickSightFolder",'
    '"Readme",'
    '"ReadmeTemplate",'
    '"RedashDashboard",'
    '"RedashQuery",'
    '"RedashVisualization",'
    '"S3Bucket",'
    '"S3Object",'
    '"SalesforceDashboard",'
    '"SalesforceField",'
    '"SalesforceObject",'
    '"SalesforceOrganization",'
    '"SalesforceReport",'
    '"Schema",'
    '"SigmaDataElement",'
    '"SigmaDataElementField",'
    '"SigmaDataset",'
    '"SigmaDatasetColumn",'
    '"SigmaPage",'
    '"SigmaWorkbook",'
    '"SnowflakePipe",'
    '"SnowflakeStream",'
    '"SnowflakeTag",'
    '"Table",'
    '"TablePartition",'
    '"TableauCalculatedField",'
    '"TableauDashboard",'
    '"TableauDatasource",'
    '"TableauDatasourceField",'
    '"TableauFlow",'
    '"TableauMetric",'
    '"TableauProject",'
    '"TableauSite",'
    '"TableauWorkbook",'
    '"TableauWorksheet",'
    '"ThoughtspotAnswer",'
    '"ThoughtspotDashlet",'
    '"ThoughtspotLiveboard",'
    '"View"]'
)


class TypeDef(AtlanObject):
    category: AtlanTypeCategory = Field(description="Type of the type definition.")
    create_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which this object was created, in milliseconds.",
    )
    created_by: Optional[str] = Field(
        description="Username of the user who created the object."
    )
    description: Optional[str] = Field(
        description="Description of the type definition."
    )
    guid: Optional[str] = Field(
        description="Unique identifier that represents the type definition."
    )
    name: str = Field(description="Unique name of this type definition.")
    type_version: Optional[str] = Field(description="Internal use only.")
    update_time: Optional[int] = Field(
        description="Time (epoch) at which this object was last assets_updated, in milliseconds."
    )
    updated_by: Optional[str] = Field(
        description="Username of the user who last assets_updated the object."
    )
    version: Optional[int] = Field(description="Version of this type definition.")


class EnumDef(TypeDef):
    class ElementDef(AtlanObject):
        value: str = Field(description="One unique value within the enumeration.")
        description: Optional[str] = Field(description="Unused.")
        ordinal: Optional[int] = Field(
            description="Unique numeric identifier for the value."
        )

        @staticmethod
        def of(ordinal: int, value: str) -> EnumDef.ElementDef:
            from pyatlan.utils import validate_required_fields

            validate_required_fields(
                ["ordinal", "value"],
                [ordinal, value],
            )
            return EnumDef.ElementDef(ordinal=ordinal, value=value)

        @staticmethod
        def list_from(values: list[str]) -> list[EnumDef.ElementDef]:
            from pyatlan.utils import validate_required_fields

            validate_required_fields(
                ["values"],
                [values],
            )
            elements: list[EnumDef.ElementDef] = []
            elements.extend(
                EnumDef.ElementDef.of(ordinal=i, value=values[i])
                for i in range(len(values))
            )
            return elements

    category: AtlanTypeCategory = AtlanTypeCategory.ENUM
    element_defs: list["EnumDef.ElementDef"] = Field(
        description="Valid values for the enumeration."
    )
    options: Optional[dict[str, Any]] = Field(
        description="Optional properties of the type definition."
    )
    service_type: Optional[str] = Field(description="Internal use only.")

    @staticmethod
    def create(name: str, values: list[str]) -> EnumDef:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["name", "values"],
            [name, values],
        )
        # Explicitly set all defaults to ensure inclusion during pydantic serialization
        return EnumDef(
            category=AtlanTypeCategory.ENUM,
            name=name,
            element_defs=EnumDef.ElementDef.list_from(values),
        )

    def get_valid_values(self) -> Optional[list[str]]:
        """
        Translate the element definitions in this enumeration into simple list of strings.
        """
        return [one.value for one in self.element_defs] if self.element_defs else []


class AttributeDef(AtlanObject):
    class Options(AtlanObject):
        description: Optional[str] = Field(
            description="Optional description of the attribute."
        )
        applicable_entity_types: Optional[str] = Field(
            description="Set of entities on which this attribute can be applied.",
        )
        custom_applicable_entity_types: Optional[str] = Field(
            description="Set of entities on which this attribute should appear.",
        )
        allow_search: bool = Field(
            description="Whether the attribute should be searchable (true) or not (false).",
        )
        max_str_length: str = Field(
            description="Maximum length allowed for a string value.",
        )
        allow_filtering: bool = Field(
            description="Whether this attribute should appear in the filterable facets of discovery (true) or not "
            "(false).",
        )
        multi_value_select: bool = Field(
            description="Whether this attribute can have multiple values (true) or only a single value (false).",
        )
        show_in_overview: Optional[bool] = Field(
            description="Whether users will see this attribute in the overview tab of the sidebar (true) or not "
            "(false).",
        )
        is_deprecated: Optional[str] = Field(
            description="Whether the attribute is deprecated ('true') or not (None or 'false')."
        )
        is_enum: Optional[bool] = Field(
            description="Whether the attribute is an enumeration (true) or not (None or false).",
        )
        enum_type: Optional[str] = Field(
            description="Name of the enumeration (options), when the attribute is an enumeration."
        )
        custom_type: Optional[str] = Field(
            description="Used for Atlan-specific types like `users`, `groups`, `url`, and `SQL`."
        )
        is_archived: Optional[bool] = Field(
            description="Whether the attribute has been deleted (true) or is still active (false)."
        )
        archived_at: Optional[int] = Field(
            description="When the attribute was deleted."
        )
        archived_by: Optional[str] = Field(
            description="User who deleted the attribute."
        )
        is_soft_reference: Optional[str] = Field(description="TBC")
        is_append_on_partial_update: Optional[str] = Field(description="TBC")
        primitive_type: Optional[str] = Field(description="Type of the attribute.")

        @staticmethod
        def create(
            attribute_type: AtlanCustomAttributePrimitiveType,
            options_name: Optional[str] = None,
        ) -> AttributeDef.Options:
            from pyatlan.utils import validate_required_fields

            validate_required_fields(
                ["type"],
                [type],
            )
            # Explicitly set all defaults to ensure inclusion during pydantic serialization
            options = AttributeDef.Options(
                primitive_type=attribute_type.value,
                applicable_entity_types='["Asset"]',
                custom_applicable_entity_types=_complete_type_list,
                allow_search=False,
                max_str_length="100000000",
                allow_filtering=True,
                multi_value_select=False,
                show_in_overview=False,
                is_enum=False,
            )
            if attribute_type in (
                AtlanCustomAttributePrimitiveType.USERS,
                AtlanCustomAttributePrimitiveType.GROUPS,
                AtlanCustomAttributePrimitiveType.URL,
                AtlanCustomAttributePrimitiveType.SQL,
            ):
                options.custom_type = attribute_type.value
            elif attribute_type == AtlanCustomAttributePrimitiveType.OPTIONS:
                options.is_enum = True
                options.enum_type = options_name
            return options

    is_new: Optional[bool] = Field(
        description="Whether the attribute is being newly created (true) or not (false).",
    )
    cardinality: Optional[Cardinality] = Field(
        description="Whether the attribute allows a single or multiple values. In the case of multiple values, "
        "`LIST` indicates they are ordered and duplicates are allowed, while `SET` indicates "
        "they are unique and unordered.",
    )
    constraints: Optional[list[dict[str, Any]]] = Field(
        description="Internal use only."
    )
    enum_values: Optional[list[str]] = Field(
        description="list of values for an enumeration."
    )
    description: Optional[str] = Field(
        description="Description of the attribute definition."
    )
    default_value: Optional[str] = Field(
        description="Default value for this attribute (if any)."
    )
    display_name: Optional[str] = Field(
        description="Name to use within all user interactions through the user interface. Note that this may not "
        "be the same name used to update or interact with the attribute through API operations, for "
        "that see the `name` property. (This property can be used instead of `name` for the creation "
        "of an attribute definition as well.)"
    )
    name: Optional[str] = Field(
        description="Unique name of this attribute definition. When provided during creation, this should be the "
        "human-readable name for the attribute. When returned (or provided for an update) this will be "
        "the static-hashed name that Atlan uses internally. (This is to allow the name to be changed "
        "by the user without impacting existing instances of the attribute.)",
    )
    include_in_notification: Optional[bool] = Field(description="TBC")
    index_type: Optional[IndexType] = Field(description="", example="DEFAULT")
    is_indexable: Optional[bool] = Field(
        description="When true, values for this attribute will be indexed for searching.",
    )
    is_optional: Optional[bool] = Field(
        description="When true, a value will not be required for this attribute.",
    )
    is_unique: Optional[bool] = Field(
        description="When true, this attribute must be unique across all assets.",
    )
    options: Optional[AttributeDef.Options] = Field(
        description="Extensible options for the attribute."
    )
    search_weight: Optional[float] = Field(description="TBC")
    skip_scrubbing: Optional[bool] = Field(
        description="When true, scrubbing of data will be skipped."
    )
    type_name: Optional[str] = Field(description="Type of this attribute.")
    values_min_count: Optional[float] = Field(
        description="Minimum number of values for this attribute. If greater than 0, this attribute "
        "becomes required.",
    )
    values_max_count: Optional[float] = Field(
        description="Maximum number of values for this attribute. If greater than 1, this attribute allows "
        "multiple values.",
    )
    index_type_es_config: Optional[dict[str, str]] = Field(
        description="Internal use only.", alias="indexTypeESConfig"
    )
    index_type_es_fields: Optional[dict[str, dict[str, str]]] = Field(
        description="Internal use only.", alias="indexTypeESFields"
    )
    is_default_value_null: Optional[bool] = Field(description="TBC")

    @staticmethod
    def create(
        display_name: str,
        attribute_type: AtlanCustomAttributePrimitiveType,
        multi_valued: bool = False,
        options_name: Optional[str] = None,
    ) -> AttributeDef:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["display_name", "attribute_type"],
            [display_name, attribute_type],
        )
        # Explicitly set all defaults to ensure inclusion during pydantic serialization
        attr_def = AttributeDef(
            display_name=display_name,
            options=AttributeDef.Options.create(
                attribute_type=attribute_type, options_name=options_name
            ),
            is_new=True,
            cardinality=Cardinality.SINGLE,
            description="",
            name="",
            include_in_notification=False,
            is_indexable=True,
            is_optional=True,
            is_unique=False,
            values_min_count=0,
            values_max_count=1,
        )
        add_enum_values = attribute_type == AtlanCustomAttributePrimitiveType.OPTIONS
        if attribute_type == AtlanCustomAttributePrimitiveType.OPTIONS:
            base_type = options_name
        elif attribute_type in (
            AtlanCustomAttributePrimitiveType.USERS,
            AtlanCustomAttributePrimitiveType.GROUPS,
            AtlanCustomAttributePrimitiveType.URL,
            AtlanCustomAttributePrimitiveType.SQL,
        ):
            base_type = AtlanCustomAttributePrimitiveType.STRING.value
        else:
            base_type = attribute_type.value
        if multi_valued:
            attr_def.type_name = f"array<{str(base_type)}>"
            attr_def.options.multi_value_select = True  # type: ignore
        else:
            attr_def.type_name = base_type
        if add_enum_values:
            from pyatlan.cache.enum_cache import EnumCache

            if enum_def := EnumCache.get_by_name(str(options_name)):
                attr_def.enum_values = enum_def.get_valid_values()
            else:
                attr_def.enum_values = []
        return attr_def

    def is_archived(self) -> bool:
        return bool(opt.is_archived) if (opt := self.options) else False

    def archive(self, by: str) -> AttributeDef:
        if self.options:
            removal_epoch = int(time.time() * 1000)
            self.options.is_archived = True
            self.options.archived_by = by
            self.options.archived_at = removal_epoch
            self.display_name = f"{self.display_name}-archived-{str(removal_epoch)}"
        return self


class RelationshipAttributeDef(AttributeDef):
    is_legacy_attribute: Optional[bool] = Field(description="Unused.")
    relationship_type_name: Optional[str] = Field(
        description="Name of the relationship type."
    )


class StructDef(TypeDef):
    category: AtlanTypeCategory = AtlanTypeCategory.STRUCT
    attribute_defs: Optional[list[AttributeDef]] = Field(
        None,
        description="list of attributes that should be available in the type_ definition.",
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )


class AtlanTagDef(TypeDef):
    attribute_defs: Optional[list[dict[str, Any]]] = Field(description="Unused.")
    category: AtlanTypeCategory = AtlanTypeCategory.CLASSIFICATION
    display_name: str = Field(
        description="Name used for display purposes (in user interfaces)."
    )
    entity_types: Optional[list[str]] = Field(
        description="A list of the entity types that this classification can be used against."
        " (This should be `Asset` to allow classification of any asset in Atlan.)"
    )
    options: Optional[dict[str, Any]] = Field(
        description="Optional properties of the type_ definition."
    )
    sub_types: Optional[list[str]] = Field(
        description="list of the sub-types that extend from this type_ definition. Generally this is not specified "
        "in any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
    )
    super_types: Optional[list[str]] = Field(
        description="list of the super-types that this type_ definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
    )
    service_type: Optional[str] = Field(
        description="Name used for display purposes (in user interfaces)."
    )
    skip_display_name_uniqueness_check: Optional[bool] = Field(description="TBC")

    @staticmethod
    def create(
        name: str,
        color: AtlanTagColor,
        icon: AtlanIcon = AtlanIcon.ATLAN_TAG,
        image: Optional[AtlanImage] = None,
    ) -> AtlanTagDef:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["name", "color"],
            [name, color],
        )
        cls_options = {
            "color": color.value,
            "iconName": icon.value,
        }
        if image:
            cls_options["imageID"] = str(image.id)
            cls_options["iconType"] = TagIconType.IMAGE.value
        else:
            cls_options["imageID"] = ""
            cls_options["iconType"] = TagIconType.ICON.value

        # Explicitly set all defaults to ensure inclusion during pydantic serialization
        return AtlanTagDef(
            category=AtlanTypeCategory.CLASSIFICATION,
            name=name,
            display_name=name,
            options=cls_options,
            skip_display_name_uniqueness_check=False,
        )


class EntityDef(TypeDef):
    attribute_defs: Optional[list[dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    business_attribute_defs: Optional[dict[str, list[dict[str, Any]]]] = Field(
        default_factory=cast(Callable[[], dict[str, list[dict[str, Any]]]], dict),
        description="Unused.",
        example=[],
    )
    category: AtlanTypeCategory = AtlanTypeCategory.ENTITY
    relationship_attribute_defs: Optional[list[dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    service_type: Optional[str] = Field(
        None, description="Internal use only.", example="atlan"
    )
    sub_types: Optional[list[str]] = Field(
        [],
        description="list of the sub-types that extend from this type_ definition. Generally this is not specified in "
        "any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
        example=[],
    )
    super_types: Optional[list[str]] = Field(
        [],
        description="list of the super-types that this type_ definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
        example=[],
    )


class RelationshipDef(TypeDef):
    attribute_defs: Optional[list[dict[str, Any]]] = Field(
        [], description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.RELATIONSHIP
    end_def1: Optional[dict[str, Any]] = Field({}, description="Unused.", example={})
    end_def2: Optional[dict[str, Any]] = Field({}, description="Unused.", example={})
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
            description="If the logoType is emoji, this should hold the emoji character."
        )
        image_id: Optional[str] = Field(
            description="The id of the image used for the logo."
        )
        is_locked: Optional[str] = Field(
            description="Indicates whether the custom metadata can be managed in the UI (false) or not (true)."
        )
        logo_type: Optional[str] = Field(
            description="Type of logo used for the custom metadata."
        )
        logo_url: Optional[str] = Field(
            description="If the logoType is image, this should hold a URL to the image."
        )

        @staticmethod
        def with_logo_as_emoji(
            emoji: str, locked: bool = False
        ) -> CustomMetadataDef.Options:
            from pyatlan.utils import validate_required_fields

            validate_required_fields(
                ["emoji"],
                [emoji],
            )
            return CustomMetadataDef.Options(
                emoji=emoji, logo_type="emoji", is_locked=str(locked).lower()
            )

        @staticmethod
        def with_logo_from_url(
            url: str, locked: bool = False
        ) -> CustomMetadataDef.Options:
            from pyatlan.utils import validate_required_fields

            validate_required_fields(
                ["url"],
                [url],
            )
            return CustomMetadataDef.Options(
                logo_url=url, logo_type="image", is_locked=locked
            )

    attribute_defs: list[AttributeDef] = Field(
        default=[],
        description="list of custom attributes defined within the custom metadata.",
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CUSTOM_METADATA
    display_name: str = Field(
        description="Name used for display purposes (in user interfaces)."
    )
    options: Optional[CustomMetadataDef.Options] = Field(
        description="Optional properties of the type definition."
    )

    @staticmethod
    def create(display_name: str) -> CustomMetadataDef:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["display_name"],
            [display_name],
        )
        # Explicitly set all defaults to ensure inclusion during pydantic serialization
        return CustomMetadataDef(
            category=AtlanTypeCategory.CUSTOM_METADATA,
            display_name=display_name,
            name=display_name,
        )


class TypeDefResponse(AtlanObject):
    enum_defs: list[EnumDef] = Field(
        [], description="list of enumeration type definitions."
    )
    struct_defs: list[StructDef] = Field(
        [], description="list of struct type definitions."
    )
    atlan_tag_defs: list[AtlanTagDef] = Field(
        [],
        description="list of classification type definitions.",
        alias="classificationDefs",
    )
    entity_defs: list[EntityDef] = Field(
        [], description="list of entity type_ definitions."
    )
    relationship_defs: list[RelationshipDef] = Field(
        [], description="list of relationship type_ definitions."
    )
    custom_metadata_defs: list[CustomMetadataDef] = Field(
        [],
        description="list of custom metadata type_ definitions.",
        alias="businessMetadataDefs",
    )
