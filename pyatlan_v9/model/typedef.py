# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

"""
Type definition models for pyatlan_v9, migrated from pyatlan/model/typedef.py.

This module provides:
- TypeDef: Base type definition
- EnumDef: Enumeration type definitions with ElementDef
- AttributeDef: Custom metadata attribute definitions with Options
- RelationshipAttributeDef: Relationship attribute definitions
- StructDef: Struct type definitions
- AtlanTagDef: Classification/tag type definitions
- EntityDef: Entity type definitions
- RelationshipDef: Relationship type definitions
- CustomMetadataDef: Custom metadata (business metadata) type definitions
- TypeDefResponse: Response containing all type definitions
"""

from __future__ import annotations

import importlib
import json
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan.model.constants import (
    AIAssetTypes,
    AssetTypes,
    DomainTypes,
    EntityTypes,
    GlossaryTypes,
    OtherAssetTypes,
)
from pyatlan.model.enums import (
    AtlanCustomAttributePrimitiveType,
    AtlanIcon,
    AtlanTagColor,
    AtlanTypeCategory,
    Cardinality,
    IndexType,
    TagIconType,
)
from pyatlan_v9.model.atlan_image import AtlanImage

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================

_complete_type_list: AssetTypes = {
    "ADLSAccount",
    "ADLSContainer",
    "ADLSObject",
    "AnaplanPage",
    "AnaplanList",
    "AnaplanLineItem",
    "AnaplanWorkspace",
    "AnaplanModule",
    "AnaplanModel",
    "AnaplanApp",
    "AnaplanDimension",
    "AnaplanView",
    "APIObject",
    "APIQuery",
    "APIField",
    "APIPath",
    "APISpec",
    "Application",
    "ApplicationField",
    "Collection",
    "Query",
    "BIProcess",
    "Badge",
    "Column",
    "ColumnProcess",
    "Connection",
    "CustomEntity",
    "DataStudioAsset",
    "DataverseAttribute",
    "DataverseEntity",
    "Database",
    "DbtColumnProcess",
    "DbtMetric",
    "DbtModel",
    "DbtModelColumn",
    "DbtProcess",
    "DbtSource",
    "Folder",
    "GCSBucket",
    "GCSObject",
    "Insight",
    "KafkaConsumerGroup",
    "KafkaTopic",
    "Process",
    "Link",
    "LookerDashboard",
    "LookerExplore",
    "LookerField",
    "LookerFolder",
    "LookerLook",
    "LookerModel",
    "LookerProject",
    "LookerQuery",
    "LookerTile",
    "LookerView",
    "MCIncident",
    "MCMonitor",
    "MaterialisedView",
    "MetabaseCollection",
    "MetabaseDashboard",
    "MetabaseQuestion",
    "ModeChart",
    "ModeCollection",
    "ModeQuery",
    "ModeReport",
    "ModeWorkspace",
    "PowerBIColumn",
    "PowerBIDashboard",
    "PowerBIDataflow",
    "PowerBIDataset",
    "PowerBIDatasource",
    "PowerBIMeasure",
    "PowerBIPage",
    "PowerBIReport",
    "PowerBITable",
    "PowerBITile",
    "PowerBIWorkspace",
    "PresetChart",
    "PresetDashboard",
    "PresetDataset",
    "PresetWorkspace",
    "Procedure",
    "QlikApp",
    "QlikChart",
    "QlikDataset",
    "QlikSheet",
    "QlikSpace",
    "QlikStream",
    "QuickSightAnalysis",
    "QuickSightAnalysisVisual",
    "QuickSightDashboard",
    "QuickSightDashboardVisual",
    "QuickSightDataset",
    "QuickSightDatasetField",
    "QuickSightFolder",
    "Readme",
    "ReadmeTemplate",
    "RedashDashboard",
    "RedashQuery",
    "RedashVisualization",
    "S3Bucket",
    "S3Object",
    "SalesforceDashboard",
    "SalesforceField",
    "SalesforceObject",
    "SalesforceOrganization",
    "SalesforceReport",
    "Schema",
    "SigmaDataElement",
    "SigmaDataElementField",
    "SigmaDataset",
    "SigmaDatasetColumn",
    "SigmaPage",
    "SigmaWorkbook",
    "SnowflakePipe",
    "SnowflakeStream",
    "SnowflakeTag",
    "SupersetChart",
    "SupersetDashboard",
    "SupersetDataset",
    "Table",
    "TablePartition",
    "TableauCalculatedField",
    "TableauDashboard",
    "TableauDatasource",
    "TableauDatasourceField",
    "TableauFlow",
    "TableauMetric",
    "TableauProject",
    "TableauSite",
    "TableauWorkbook",
    "TableauWorksheet",
    "ThoughtspotAnswer",
    "ThoughtspotDashlet",
    "ThoughtspotLiveboard",
    "View",
}

_all_glossary_types: GlossaryTypes = {
    "AtlasGlossary",
    "AtlasGlossaryCategory",
    "AtlasGlossaryTerm",
}

_all_domains: Set[str] = {"*/super"}

_all_domain_types: DomainTypes = {
    "DataDomain",
    "DataProduct",
}

_all_ai_asset_types: AIAssetTypes = {"AIApplication", "AIModel"}
_all_other_types: OtherAssetTypes = {"File"}


def _get_all_qualified_names(client: AtlanClient, asset_type: str) -> Set[str]:
    """Retrieve all qualified names for assets of the given type."""
    from pyatlan.model.assets import Asset
    from pyatlan.model.fluent_search import FluentSearch

    request = (
        FluentSearch.select()
        .where(Asset.TYPE_NAME.eq(asset_type))
        .include_on_results(Asset.QUALIFIED_NAME)
        .to_request()
    )
    results = client.asset.search(request)
    names = [result.qualified_name or "" for result in results]
    return set(names)


# =============================================================================
# TYPE DEFINITION BASE
# =============================================================================


class TypeDef(msgspec.Struct, kw_only=True, rename="camel"):
    """Base type definition."""

    category: AtlanTypeCategory
    """Type of the type definition."""

    create_time: Union[int, None] = None
    """Time (epoch) at which this object was created, in milliseconds."""

    created_by: Union[str, None] = None
    """Username of the user who created the object."""

    description: Union[str, None] = None
    """Description of the type definition."""

    guid: Union[str, None] = None
    """Unique identifier that represents the type definition."""

    name: Union[str, None] = None
    """Unique name of this type definition."""

    type_version: Union[str, None] = None
    """Internal use only."""

    update_time: Union[int, None] = None
    """Time (epoch) at which this object was last updated, in milliseconds."""

    updated_by: Union[str, None] = None
    """Username of the user who last updated the object."""

    version: Union[int, None] = None
    """Version of this type definition."""


# =============================================================================
# ENUM DEFINITION
# =============================================================================


class EnumDef(TypeDef, kw_only=True):
    """Enumeration type definition."""

    class ElementDef(msgspec.Struct, kw_only=True, rename="camel"):
        """One element (valid value) within an enumeration."""

        value: str
        """One unique value within the enumeration."""

        description: Union[str, None] = None
        """Unused."""

        ordinal: Union[int, None] = None
        """Unique numeric identifier for the value."""

        @staticmethod
        def of(ordinal: int, value: str) -> EnumDef.ElementDef:
            """Create an element definition with the given ordinal and value."""
            from pyatlan_v9.utils import validate_required_fields

            validate_required_fields(
                ["ordinal", "value"],
                [ordinal, value],
            )
            return EnumDef.ElementDef(ordinal=ordinal, value=value)

        @staticmethod
        def list_from(values: List[str]) -> List[EnumDef.ElementDef]:
            """Create a list of element definitions from a list of strings."""
            from pyatlan_v9.utils import validate_required_fields

            validate_required_fields(
                ["values"],
                [values],
            )
            return [
                EnumDef.ElementDef.of(ordinal=i, value=values[i])
                for i in range(len(values))
            ]

        @staticmethod
        def extend_elements(current: List[str], new: List[str]) -> List[str]:
            """
            Extends the element definitions without duplications
            and also retains the order of the current enum values.

            :param current: current list of element definitions.
            :param new: list of new element definitions to be added.
            :return: list of unique element definitions without duplications.
            """
            unique_elements = set(current)
            extended_list = current[:]
            for element in new:
                if element not in unique_elements:
                    extended_list.append(element)
                    unique_elements.add(element)
            return extended_list

    category: AtlanTypeCategory = AtlanTypeCategory.ENUM
    """Type category for enumeration definitions."""

    element_defs: List[EnumDef.ElementDef] = msgspec.field(default_factory=list)
    """Valid values for the enumeration."""

    options: Union[Dict[str, Any], None] = None
    """Optional properties of the type definition."""

    service_type: Union[str, None] = None
    """Internal use only."""

    @staticmethod
    def create(name: str, values: List[str]) -> EnumDef:
        """
        Builds the minimal object necessary to create an enumeration definition.

        :param name: display name the human-readable name for the enumeration
        :param values: the list of additional valid values
        (as strings) to add to the existing enumeration
        :returns: the minimal object necessary to create the enumeration typedef
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["name", "values"],
            [name, values],
        )
        return EnumDef(
            category=AtlanTypeCategory.ENUM,
            name=name,
            element_defs=EnumDef.ElementDef.list_from(values),
        )

    @staticmethod
    def update(
        client: AtlanClient, name: str, values: List[str], replace_existing: bool
    ) -> EnumDef:
        """
        Builds the minimal object necessary to update an enumeration definition.

        :param client: connectivity to an Atlan tenant
        :param name: display name the human-readable name for the enumeration
        :param values: the list of additional valid values
        (as strings) to add to the existing enumeration
        :param replace_existing: if True, will replace all
        existing values in the enumeration with the new ones;
        or if False the new ones will be appended to the existing set
        :returns: the minimal object necessary to update the enumeration typedef
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["name", "values", "replace_existing"],
            [name, values, replace_existing],
        )
        update_values = (
            values
            if replace_existing
            else EnumDef.ElementDef.extend_elements(
                new=values,
                current=client.enum_cache.get_by_name(str(name)).get_valid_values(),
            )
        )
        return EnumDef(
            name=name,
            category=AtlanTypeCategory.ENUM,
            element_defs=EnumDef.ElementDef.list_from(update_values),
        )

    @staticmethod
    async def update_async(
        client, name: str, values: List[str], replace_existing: bool
    ) -> EnumDef:
        """
        Builds the minimal object necessary to update an enumeration definition (async).

        :param client: connectivity to an Atlan tenant
        :param name: display name the human-readable name for the enumeration
        :param values: the list of additional valid values
        (as strings) to add to the existing enumeration
        :param replace_existing: if True, will replace all
        existing values in the enumeration with the new ones;
        or if False the new ones will be appended to the existing set
        :returns: the minimal object necessary to update the enumeration typedef
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["name", "values", "replace_existing"],
            [name, values, replace_existing],
        )
        update_values = (
            values
            if replace_existing
            else EnumDef.ElementDef.extend_elements(
                new=values,
                current=(
                    await client.enum_cache.get_by_name(str(name))
                ).get_valid_values(),
            )
        )
        return EnumDef(
            name=name,
            category=AtlanTypeCategory.ENUM,
            element_defs=EnumDef.ElementDef.list_from(update_values),
        )

    def get_valid_values(self) -> List[str]:
        """Translate the element definitions into a simple list of strings."""
        return [one.value for one in self.element_defs] if self.element_defs else []


# =============================================================================
# ATTRIBUTE DEFINITION
# =============================================================================


class AttributeDef(msgspec.Struct, kw_only=True, rename="camel"):
    """Custom metadata attribute definition."""

    class Options(msgspec.Struct, kw_only=True, rename="camel"):
        """Extensible options for a custom metadata attribute."""

        custom_metadata_version: str = "v2"
        """Indicates the version of the custom metadata structure."""

        description: Union[str, None] = None
        """Optional description of the attribute."""

        applicable_entity_types: Union[str, None] = None
        """Set of entities on which this attribute can be applied (JSON-encoded)."""

        custom_applicable_entity_types: Union[str, None] = None
        """Deprecated: see applicable_asset_types, applicable_glossary_types."""

        allow_search: Union[bool, None] = None
        """Whether the attribute should be searchable (true) or not (false)."""

        max_str_length: Union[str, None] = None
        """Maximum length allowed for a string value."""

        allow_filtering: Union[bool, None] = None
        """Whether this attribute should appear in the filterable facets."""

        multi_value_select: Union[bool, None] = None
        """Whether this attribute can have multiple values."""

        show_in_overview: Union[bool, None] = None
        """Whether users will see this attribute in the overview tab."""

        is_deprecated: Union[str, None] = None
        """Whether the attribute is deprecated ('true') or not."""

        is_enum: Union[bool, None] = None
        """Whether the attribute is an enumeration."""

        enum_type: Union[str, None] = None
        """Name of the enumeration (options), when the attribute is an enumeration."""

        custom_type: Union[str, None] = None
        """Used for Atlan-specific types like users, groups, url, and SQL."""

        has_time_precision: Union[bool, None] = None
        """If true for a date attribute, time-level precision is also available."""

        is_archived: Union[bool, None] = None
        """Whether the attribute has been deleted."""

        archived_at: Union[int, None] = None
        """When the attribute was deleted."""

        archived_by: Union[str, None] = None
        """User who deleted the attribute."""

        is_soft_reference: Union[str, None] = None
        """TBC"""

        is_append_on_partial_update: Union[str, None] = None
        """TBC"""

        primitive_type: Union[str, None] = None
        """Type of the attribute."""

        applicable_connections: Union[str, None] = None
        """Qualified names of connections to restrict the attribute (JSON-encoded)."""

        applicable_glossaries: Union[str, None] = None
        """Qualified names of glossaries to restrict the attribute (JSON-encoded)."""

        applicable_domains: Union[str, None] = None
        """Qualified names of domains to restrict the attribute (JSON-encoded)."""

        applicable_asset_types: Union[str, None] = msgspec.field(
            default=None, name="assetTypesList"
        )
        """Asset type names to restrict the attribute (JSON-encoded)."""

        applicable_glossary_types: Union[str, None] = msgspec.field(
            default=None, name="glossaryTypeList"
        )
        """Glossary type names to restrict the attribute (JSON-encoded)."""

        applicable_domain_types: Union[str, None] = msgspec.field(
            default=None, name="domainTypesList"
        )
        """Data product type names to restrict the attribute (JSON-encoded)."""

        applicable_ai_asset_types: Union[str, None] = msgspec.field(
            default=None, name="aiAssetsTypeList"
        )
        """AI asset type names to restrict the attribute (JSON-encoded)."""

        applicable_other_asset_types: Union[str, None] = msgspec.field(
            default=None, name="otherAssetTypeList"
        )
        """Other asset type names to restrict the attribute (JSON-encoded)."""

        is_rich_text: Union[bool, None] = False
        """Whether this attribute supports rich text formatting."""

        _attr_def: object = msgspec.field(default=None, name="_attrDef")
        """Internal back-reference to the parent AttributeDef (not serialized)."""

        def __setattr__(self, name: str, value: object) -> None:
            super().__setattr__(name, value)
            if name == "multi_value_select" and value is True and self._attr_def:
                self._attr_def.cardinality = Cardinality.SET
                if self._attr_def.type_name and "array<" not in str(
                    self._attr_def.type_name
                ):
                    self._attr_def.type_name = f"array<{self._attr_def.type_name}>"

        @staticmethod
        def create(
            attribute_type: AtlanCustomAttributePrimitiveType,
            options_name: Optional[str] = None,
        ) -> AttributeDef.Options:
            """Create options for a custom metadata attribute."""
            from pyatlan_v9.utils import validate_required_fields

            validate_required_fields(
                ["type"],
                [type],
            )
            options = AttributeDef.Options(
                custom_metadata_version="v2",
                primitive_type=attribute_type.value,
                applicable_entity_types='["Asset"]',
                allow_search=False,
                max_str_length="100000000",
                allow_filtering=True,
                multi_value_select=False,
                show_in_overview=False,
                is_enum=False,
                is_rich_text=False,
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
            elif attribute_type == AtlanCustomAttributePrimitiveType.RICH_TEXT:
                options.is_rich_text = True
                options.multi_value_select = False
            return options

    is_new: Union[bool, None] = None
    """Whether the attribute is being newly created."""

    cardinality: Union[Cardinality, None] = None
    """Whether the attribute allows a single or multiple values."""

    constraints: Union[List[Dict[str, Any]], None] = None
    """Internal use only."""

    enum_values: Union[List[str], None] = None
    """List of values for an enumeration."""

    description: Union[str, None] = None
    """Description of the attribute definition."""

    default_value: Union[str, None] = None
    """Default value for this attribute (if any)."""

    display_name: Union[str, None] = None
    """Name to use within all user interactions through the UI."""

    name: Union[str, None] = None
    """Unique name of this attribute definition."""

    include_in_notification: Union[bool, None] = None
    """TBC"""

    index_type: Union[IndexType, None] = None
    """Index type for the attribute."""

    is_indexable: Union[bool, None] = None
    """When true, values for this attribute will be indexed for searching."""

    is_optional: Union[bool, None] = None
    """When true, a value will not be required for this attribute."""

    is_unique: Union[bool, None] = None
    """When true, this attribute must be unique across all assets."""

    options: Union[AttributeDef.Options, None] = msgspec.field(default_factory=Options)
    """Extensible options for the attribute."""

    search_weight: Union[float, None] = None
    """TBC"""

    skip_scrubbing: Union[bool, None] = None
    """When true, scrubbing of data will be skipped."""

    type_name: Union[str, None] = None
    """Type of this attribute."""

    values_min_count: Union[float, None] = None
    """Minimum number of values for this attribute."""

    values_max_count: Union[float, None] = None
    """Maximum number of values for this attribute."""

    index_type_es_config: Union[Dict[str, str], None] = msgspec.field(
        default=None, name="indexTypeESConfig"
    )
    """Internal use only."""

    index_type_es_fields: Union[Dict[str, Dict[str, str]], None] = msgspec.field(
        default=None, name="indexTypeESFields"
    )
    """Internal use only."""

    is_default_value_null: Union[bool, None] = None
    """TBC"""

    def __post_init__(self):
        """Set back-reference from Options to this AttributeDef."""
        if self.options is not None:
            self.options._attr_def = self

    # --- Convenience property accessors ---
    # These properties read/write from self.options and handle JSON encoding.
    # In the legacy code, these were implemented via __setattr__ + _convenience_properties.
    # In msgspec, we use @property descriptors that delegate to get_*/set_* methods.

    def _get_option_set(self, attr: str) -> Set[str]:
        """Helper to parse a JSON-encoded set from options."""
        val = getattr(self.options, attr, None) if self.options else None
        if val:
            return set(json.loads(val))
        return set()

    def _set_option_json(self, attr: str, value: Set[str]) -> None:
        """Helper to set a JSON-encoded set on options."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        setattr(self.options, attr, json.dumps(list(value)))

    def get_applicable_entity_types(self) -> EntityTypes:
        """Set of entities on which this attribute can be applied."""
        return self._get_option_set("applicable_entity_types")

    def set_applicable_entity_types(self, entity_types: EntityTypes) -> None:
        """Set the entities on which this attribute can be applied."""
        if not isinstance(entity_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_entity_types", EntityTypes
            )
        self._set_option_json("applicable_entity_types", entity_types)

    def get_applicable_asset_types(self) -> Union[Set[str], AssetTypes]:
        """Asset type names to which to restrict the attribute."""
        return self._get_option_set("applicable_asset_types")

    def set_applicable_asset_types(
        self, asset_types: Union[Set[str], AssetTypes]
    ) -> None:
        """Set asset types to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(asset_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_asset_types", AssetTypes
            )
        # Validate asset type names against SDK asset classes
        invalid_types = {
            asset_type
            for asset_type in asset_types
            if not getattr(
                importlib.import_module("pyatlan.model.assets"), asset_type, None
            )
        }
        if invalid_types:
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                invalid_types, "applicable_asset_types", "SDK asset types"
            )
        self.options.applicable_asset_types = json.dumps(list(asset_types))

    def get_applicable_glossary_types(self) -> GlossaryTypes:
        """Glossary type names to which to restrict the attribute."""
        return self._get_option_set("applicable_glossary_types")

    def set_applicable_glossary_types(self, glossary_types: GlossaryTypes) -> None:
        """Set glossary types to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(glossary_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_glossary_types", GlossaryTypes
            )
        if not glossary_types.issubset(_all_glossary_types):
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                glossary_types, "applicable_glossary_types", _all_glossary_types
            )
        self.options.applicable_glossary_types = json.dumps(list(glossary_types))

    def get_applicable_domain_types(self) -> DomainTypes:
        """Data product type names to which to restrict the attribute."""
        return self._get_option_set("applicable_domain_types")

    def set_applicable_domain_types(self, domain_types: DomainTypes) -> None:
        """Set domain types to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(domain_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_domain_types", DomainTypes
            )
        if not domain_types.issubset(_all_domain_types):
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                domain_types, "applicable_domain_types", _all_domain_types
            )
        self.options.applicable_domain_types = json.dumps(list(domain_types))

    def get_applicable_ai_asset_types(self) -> AIAssetTypes:
        """AI asset type names to which this attribute is restricted."""
        return self._get_option_set("applicable_ai_asset_types")

    def set_applicable_ai_asset_types(self, ai_asset_types: AIAssetTypes) -> None:
        """Set AI asset types to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(ai_asset_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_ai_asset_types", AIAssetTypes
            )
        if not ai_asset_types.issubset(_all_ai_asset_types):
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                ai_asset_types, "applicable_ai_asset_types", _all_ai_asset_types
            )
        self.options.applicable_ai_asset_types = json.dumps(list(ai_asset_types))

    def get_applicable_other_asset_types(self) -> OtherAssetTypes:
        """Other asset type names to which to restrict the attribute."""
        return self._get_option_set("applicable_other_asset_types")

    def set_applicable_other_asset_types(
        self, other_asset_types: OtherAssetTypes
    ) -> None:
        """Set other asset types to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(other_asset_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_other_asset_types", OtherAssetTypes
            )
        if not other_asset_types.issubset(_all_other_types):
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                other_asset_types,
                "applicable_other_asset_types",
                OtherAssetTypes,
            )
        self.options.applicable_other_asset_types = json.dumps(list(other_asset_types))

    def get_applicable_connections(self) -> Set[str]:
        """Qualified names of connections to which to restrict the attribute."""
        return self._get_option_set("applicable_connections")

    def set_applicable_connections(self, connections: Set[str]) -> None:
        """Set connections to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(connections, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_connections", "Set[str]"
            )
        self.options.applicable_connections = json.dumps(list(connections))

    def get_applicable_glossaries(self) -> Set[str]:
        """Qualified names of glossaries to which to restrict the attribute."""
        return self._get_option_set("applicable_glossaries")

    def set_applicable_glossaries(self, glossaries: Set[str]) -> None:
        """Set glossaries to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(glossaries, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_glossaries", "Set[str]"
            )
        self.options.applicable_glossaries = json.dumps(list(glossaries))

    def get_applicable_domains(self) -> Set[str]:
        """Qualified names of domains to which to restrict the attribute."""
        return self._get_option_set("applicable_domains")

    def set_applicable_domains(self, domains: Set[str]) -> None:
        """Set domains to which to restrict the attribute."""
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(domains, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_domains", "Set[str]"
            )
        self.options.applicable_domains = json.dumps(list(domains))

    # --- Property descriptors for parity with legacy AttributeDef ---

    @property
    def applicable_entity_types(self) -> EntityTypes:
        """Set of entities on which this attribute can be applied."""
        return self.get_applicable_entity_types()

    @applicable_entity_types.setter
    def applicable_entity_types(self, entity_types: EntityTypes) -> None:
        self.set_applicable_entity_types(entity_types)

    @property
    def applicable_asset_types(self) -> Union[Set[str], AssetTypes]:
        """Asset type names to which to restrict the attribute."""
        return self.get_applicable_asset_types()

    @applicable_asset_types.setter
    def applicable_asset_types(self, asset_types: Union[Set[str], AssetTypes]) -> None:
        self.set_applicable_asset_types(asset_types)

    @property
    def applicable_glossary_types(self) -> GlossaryTypes:
        """Glossary type names to which to restrict the attribute."""
        return self.get_applicable_glossary_types()

    @applicable_glossary_types.setter
    def applicable_glossary_types(self, glossary_types: GlossaryTypes) -> None:
        self.set_applicable_glossary_types(glossary_types)

    @property
    def applicable_domain_types(self) -> DomainTypes:
        """Data product type names to which to restrict the attribute."""
        return self.get_applicable_domain_types()

    @applicable_domain_types.setter
    def applicable_domain_types(self, domain_types: DomainTypes) -> None:
        self.set_applicable_domain_types(domain_types)

    @property
    def applicable_ai_asset_types(self) -> AIAssetTypes:
        """AI asset type names to which this attribute is restricted."""
        return self.get_applicable_ai_asset_types()

    @applicable_ai_asset_types.setter
    def applicable_ai_asset_types(self, ai_asset_types: AIAssetTypes) -> None:
        self.set_applicable_ai_asset_types(ai_asset_types)

    @property
    def applicable_other_asset_types(self) -> OtherAssetTypes:
        """Other asset type names to which to restrict the attribute."""
        return self.get_applicable_other_asset_types()

    @applicable_other_asset_types.setter
    def applicable_other_asset_types(self, other_asset_types: OtherAssetTypes) -> None:
        self.set_applicable_other_asset_types(other_asset_types)

    @property
    def applicable_connections(self) -> Set[str]:
        """Qualified names of connections to which to restrict the attribute."""
        return self.get_applicable_connections()

    @applicable_connections.setter
    def applicable_connections(self, connections: Set[str]) -> None:
        self.set_applicable_connections(connections)

    @property
    def applicable_glossaries(self) -> Set[str]:
        """Qualified names of glossaries to which to restrict the attribute."""
        return self.get_applicable_glossaries()

    @applicable_glossaries.setter
    def applicable_glossaries(self, glossaries: Set[str]) -> None:
        self.set_applicable_glossaries(glossaries)

    @property
    def applicable_domains(self) -> Set[str]:
        """Qualified names of domains to which to restrict the attribute."""
        return self.get_applicable_domains()

    @applicable_domains.setter
    def applicable_domains(self, domains: Set[str]) -> None:
        self.set_applicable_domains(domains)

    @staticmethod
    def create(
        client: AtlanClient,
        display_name: str,
        attribute_type: AtlanCustomAttributePrimitiveType,
        multi_valued: bool = False,
        options_name: Optional[str] = None,
        applicable_connections: Optional[Set[str]] = None,
        applicable_asset_types: Optional[Union[Set[str], AssetTypes]] = None,
        applicable_glossaries: Optional[Set[str]] = None,
        applicable_glossary_types: Optional[GlossaryTypes] = None,
        applicable_other_asset_types: Optional[OtherAssetTypes] = None,
        applicable_domains: Optional[Set[str]] = None,
        applicable_domain_types: Optional[DomainTypes] = None,
        applicable_ai_asset_types: Optional[AIAssetTypes] = None,
        description: Optional[str] = None,
    ) -> AttributeDef:
        """
        Builds the minimal object necessary to create a custom metadata attribute.

        :param client: connectivity to an Atlan tenant
        :param display_name: human-readable name for the attribute
        :param attribute_type: type of the attribute
        :param multi_valued: whether the attribute can have multiple values
        :param options_name: name of the enumeration (if type is OPTIONS)
        :param applicable_connections: connections where this attribute applies
        :param applicable_asset_types: asset types where this attribute applies
        :param applicable_glossaries: glossaries where this attribute applies
        :param applicable_glossary_types: glossary types where this attribute applies
        :param applicable_other_asset_types: other asset types where this attribute applies
        :param applicable_domains: domains where this attribute applies
        :param applicable_domain_types: domain types where this attribute applies
        :param applicable_ai_asset_types: AI asset types where this attribute applies
        :param description: description of the attribute
        :returns: AttributeDef configured for the specified parameters
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["display_name", "attribute_type"],
            [display_name, attribute_type],
        )
        # RichText attributes cannot be multi-valued
        if (
            attribute_type == AtlanCustomAttributePrimitiveType.RICH_TEXT
            and multi_valued
        ):
            raise ErrorCode.INVALID_RICH_TEXT_CREATION.exception_with_parameters(
                display_name
            )
        attr_def = AttributeDef(
            display_name=display_name,
            options=AttributeDef.Options.create(
                attribute_type=attribute_type, options_name=options_name
            ),
            is_new=True,
            cardinality=Cardinality.SINGLE,
            description=description,
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
            attr_def.options.multi_value_select = True  # type: ignore[union-attr]
            attr_def.cardinality = Cardinality.SET
        else:
            attr_def.type_name = base_type
        if add_enum_values:
            if enum_def := client.enum_cache.get_by_name(str(options_name)):
                attr_def.enum_values = enum_def.get_valid_values()
            else:
                attr_def.enum_values = []

        attr_def.set_applicable_asset_types(
            applicable_asset_types or _complete_type_list
        )
        attr_def.set_applicable_glossary_types(
            applicable_glossary_types or _all_glossary_types
        )
        attr_def.set_applicable_domain_types(
            applicable_domain_types or _all_domain_types
        )
        attr_def.set_applicable_other_asset_types(
            applicable_other_asset_types or _all_other_types
        )
        attr_def.set_applicable_connections(
            applicable_connections or _get_all_qualified_names(client, "Connection")
        )
        attr_def.set_applicable_glossaries(
            applicable_glossaries or _get_all_qualified_names(client, "AtlasGlossary")
        )
        attr_def.set_applicable_domains(applicable_domains or _all_domains)
        attr_def.set_applicable_ai_asset_types(applicable_ai_asset_types or set())
        return attr_def

    @staticmethod
    async def create_async(
        client,  # AsyncAtlanClient
        display_name: str,
        attribute_type: AtlanCustomAttributePrimitiveType,
        multi_valued: bool = False,
        options_name: Optional[str] = None,
        applicable_connections: Optional[Set[str]] = None,
        applicable_asset_types: Optional[Union[Set[str], AssetTypes]] = None,
        applicable_glossaries: Optional[Set[str]] = None,
        applicable_glossary_types: Optional[GlossaryTypes] = None,
        applicable_other_asset_types: Optional[OtherAssetTypes] = None,
        applicable_domains: Optional[Set[str]] = None,
        applicable_domain_types: Optional[DomainTypes] = None,
        applicable_ai_asset_types: Optional[AIAssetTypes] = None,
        description: Optional[str] = None,
    ) -> AttributeDef:
        """
        Create an AttributeDef with async client support.

        :param client: AsyncAtlanClient instance
        :param display_name: human-readable name for the attribute
        :param attribute_type: type of the attribute
        :param multi_valued: whether the attribute can have multiple values
        :param options_name: name of the enumeration (if type is OPTIONS)
        :param applicable_connections: connections where this attribute applies
        :param applicable_asset_types: asset types where this attribute applies
        :param applicable_glossaries: glossaries where this attribute applies
        :param applicable_glossary_types: glossary types where this attribute applies
        :param applicable_other_asset_types: other asset types where this attribute applies
        :param applicable_domains: domains where this attribute applies
        :param applicable_domain_types: domain types where this attribute applies
        :param applicable_ai_asset_types: AI asset types where this attribute applies
        :param description: description of the attribute
        :returns: AttributeDef configured for the specified parameters
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["display_name", "attribute_type"],
            [display_name, attribute_type],
        )
        if (
            attribute_type == AtlanCustomAttributePrimitiveType.RICH_TEXT
            and multi_valued
        ):
            raise ErrorCode.INVALID_RICH_TEXT_CREATION.exception_with_parameters(
                display_name
            )

        async def _get_all_qualified_names_async(asset_type: str):
            from pyatlan.model.assets import Asset
            from pyatlan.model.fluent_search import FluentSearch

            request = (
                FluentSearch.select()
                .where(Asset.TYPE_NAME.eq(asset_type))
                .include_on_results(Asset.QUALIFIED_NAME)
                .to_request()
            )
            results = await client.asset.search(request)
            names = []
            async for result in results:
                names.append(result.qualified_name or "")
            return set(names)

        attr_def = AttributeDef(
            display_name=display_name,
            options=AttributeDef.Options.create(
                attribute_type=attribute_type, options_name=options_name
            ),
            is_new=True,
            cardinality=Cardinality.SINGLE,
            description=description,
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
            attr_def.options.multi_value_select = True  # type: ignore[union-attr]
            attr_def.cardinality = Cardinality.SET
        else:
            attr_def.type_name = base_type
        if add_enum_values:
            if enum_def := await client.enum_cache.get_by_name(str(options_name)):
                attr_def.enum_values = enum_def.get_valid_values()
            else:
                attr_def.enum_values = []

        attr_def.set_applicable_asset_types(
            applicable_asset_types or _complete_type_list
        )
        attr_def.set_applicable_glossary_types(
            applicable_glossary_types or _all_glossary_types
        )
        attr_def.set_applicable_domain_types(
            applicable_domain_types or _all_domain_types
        )
        attr_def.set_applicable_other_asset_types(
            applicable_other_asset_types or _all_other_types
        )
        attr_def.set_applicable_connections(
            applicable_connections or await _get_all_qualified_names_async("Connection")
        )
        attr_def.set_applicable_glossaries(
            applicable_glossaries
            or await _get_all_qualified_names_async("AtlasGlossary")
        )
        attr_def.set_applicable_domains(applicable_domains or _all_domains)
        attr_def.set_applicable_ai_asset_types(applicable_ai_asset_types or set())
        return attr_def

    def is_archived(self) -> bool:
        """Check if this attribute has been archived."""
        return bool(opt.is_archived) if (opt := self.options) else False

    def archive(self, by: str) -> AttributeDef:
        """Mark this attribute as archived."""
        if self.options:
            removal_epoch = int(time.time() * 1000)
            self.options.is_archived = True
            self.options.archived_by = by
            self.options.archived_at = removal_epoch
            self.display_name = f"{self.display_name}-archived-{removal_epoch}"
        return self


# =============================================================================
# RELATIONSHIP ATTRIBUTE DEFINITION
# =============================================================================


class RelationshipAttributeDef(AttributeDef, kw_only=True):
    """Relationship attribute definition."""

    is_legacy_attribute: Union[bool, None] = None
    """Unused."""

    relationship_type_name: Union[str, None] = None
    """Name of the relationship type."""


# =============================================================================
# STRUCT DEFINITION
# =============================================================================


class StructDef(TypeDef, kw_only=True):
    """Struct type definition."""

    category: AtlanTypeCategory = AtlanTypeCategory.STRUCT
    """Type category for struct definitions."""

    attribute_defs: Union[List[AttributeDef], None] = None
    """List of attributes that should be available in the type definition."""

    service_type: Union[str, None] = None
    """Internal use only."""


# =============================================================================
# ATLAN TAG DEFINITION (CLASSIFICATION)
# =============================================================================


class AtlanTagDef(TypeDef, kw_only=True):
    """Classification (Atlan tag) type definition."""

    attribute_defs: Union[List[AttributeDef], None] = None
    """Unused."""

    category: AtlanTypeCategory = AtlanTypeCategory.CLASSIFICATION
    """Type category for classification definitions."""

    display_name: Union[str, None] = None
    """Name used for display purposes (in user interfaces)."""

    entity_types: Union[List[str], None] = None
    """A list of entity types that this classification can be used against."""

    options: Union[Dict[str, Any], None] = None
    """Optional properties of the type definition."""

    sub_types: Union[List[str], None] = None
    """List of sub-types that extend from this type definition."""

    super_types: Union[List[str], None] = None
    """List of super-types that this type definition extends."""

    service_type: Union[str, None] = None
    """Name used for display purposes."""

    skip_display_name_uniqueness_check: Union[bool, None] = None
    """TBC"""

    @staticmethod
    def create(
        name: str,
        color: AtlanTagColor = AtlanTagColor.GRAY,
        icon: AtlanIcon = AtlanIcon.ATLAN_TAG,
        image: Optional[AtlanImage] = None,
        emoji: Optional[str] = None,
    ) -> AtlanTagDef:
        """
        Builds the minimal object necessary to create an Atlan tag definition.

        :param name: human-readable name for the Atlan tag
        :param color: color for the tag
        :param icon: icon for the tag
        :param image: optional image for the tag
        :param emoji: optional emoji for the tag
        :returns: the minimal object necessary to create the tag typedef
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["name", "color"],
            [name, color],
        )
        cls_options: Dict[str, str] = {
            "color": color.value,
            "iconName": icon.value,
        }
        if image:
            cls_options["imageID"] = str(image.id)
            cls_options["iconType"] = TagIconType.IMAGE.value
        elif emoji:
            cls_options["emoji"] = emoji
            cls_options["iconType"] = TagIconType.EMOJI.value
        else:
            cls_options["imageID"] = ""
            cls_options["iconType"] = TagIconType.ICON.value

        return AtlanTagDef(
            category=AtlanTypeCategory.CLASSIFICATION,
            name=name,
            display_name=name,
            options=cls_options,
            skip_display_name_uniqueness_check=False,
        )


# =============================================================================
# ENTITY DEFINITION
# =============================================================================

RESERVED_SERVICE_TYPES = {"atlas_core", "atlan", "aws", "azure", "gcp", "google"}


class EntityDef(TypeDef, kw_only=True):
    """Entity type definition."""

    attribute_defs: List[Dict[str, Any]] = msgspec.field(default_factory=list)
    """Unused."""

    business_attribute_defs: Union[Dict[str, List[Dict[str, Any]]], None] = (
        msgspec.field(default_factory=dict)
    )
    """Unused."""

    category: AtlanTypeCategory = AtlanTypeCategory.ENTITY
    """Type category for entity definitions."""

    relationship_attribute_defs: List[Dict[str, Any]] = msgspec.field(
        default_factory=list
    )
    """Unused."""

    service_type: Union[str, None] = None
    """Internal use only."""

    sub_types: List[str] = msgspec.field(default_factory=list)
    """List of sub-types that extend from this type definition."""

    super_types: List[str] = msgspec.field(default_factory=list)
    """List of super-types that this type definition extends."""

    @property
    def reserved_type(self) -> bool:
        """Whether this entity definition is a reserved (built-in) type."""
        return self.service_type in RESERVED_SERVICE_TYPES


# =============================================================================
# RELATIONSHIP DEFINITION
# =============================================================================


class RelationshipDef(TypeDef, kw_only=True):
    """Relationship type definition."""

    attribute_defs: List[Dict[str, Any]] = msgspec.field(default_factory=list)
    """Unused."""

    category: AtlanTypeCategory = AtlanTypeCategory.RELATIONSHIP
    """Type category for relationship definitions."""

    end_def1: Union[Dict[str, Any], None] = msgspec.field(default_factory=dict)
    """Unused."""

    end_def2: Union[Dict[str, Any], None] = msgspec.field(default_factory=dict)
    """Unused."""

    propagate_tags: str = "ONE_TO_TWO"
    """Unused."""

    relationship_category: str = "AGGREGATION"
    """Unused."""

    relationship_label: str = "__SalesforceOrganization.reports"
    """Unused."""

    service_type: Union[str, None] = None
    """Internal use only."""


# =============================================================================
# CUSTOM METADATA DEFINITION
# =============================================================================


class CustomMetadataDef(TypeDef, kw_only=True):
    """Custom metadata (business metadata) type definition."""

    class Options(msgspec.Struct, kw_only=True, rename="camel"):
        """Options for a custom metadata definition."""

        emoji: Union[str, None] = None
        """If the logoType is emoji, this holds the emoji character."""

        image_id: Union[str, None] = None
        """The id of the image used for the logo."""

        is_locked: Union[bool, None] = None
        """Whether the custom metadata can be managed in the UI (false) or not (true)."""

        logo_type: Union[str, None] = None
        """Type of logo used for the custom metadata."""

        logo_url: Union[str, None] = None
        """If the logoType is image, this holds a URL to the image."""

        icon_color: Union[AtlanTagColor, None] = None
        """Color to use for the icon."""

        icon_name: Union[AtlanIcon, None] = None
        """Icon to use to represent the custom metadata."""

        @staticmethod
        def with_logo_as_emoji(
            emoji: str, locked: bool = False
        ) -> CustomMetadataDef.Options:
            """Create options with an emoji logo."""
            from pyatlan_v9.utils import validate_required_fields

            validate_required_fields(
                ["emoji"],
                [emoji],
            )
            return CustomMetadataDef.Options(
                emoji=emoji, logo_type="emoji", is_locked=locked
            )

        @staticmethod
        def with_logo_from_url(
            url: str, locked: bool = False
        ) -> CustomMetadataDef.Options:
            """Create options with a URL-based image logo."""
            from pyatlan_v9.utils import validate_required_fields

            validate_required_fields(
                ["url"],
                [url],
            )
            return CustomMetadataDef.Options(
                logo_url=url, logo_type="image", is_locked=locked
            )

        @staticmethod
        def with_logo_from_icon(
            icon: AtlanIcon, color: AtlanTagColor, locked: bool = False
        ) -> CustomMetadataDef.Options:
            """Create options with a built-in icon."""
            from pyatlan_v9.utils import validate_required_fields

            validate_required_fields(
                ["icon", "color"],
                [icon, color],
            )
            return CustomMetadataDef.Options(
                logo_type="icon",
                icon_color=color,
                icon_name=icon,
                is_locked=locked,
            )

    attribute_defs: List[AttributeDef] = msgspec.field(default_factory=list)
    """List of custom attributes defined within the custom metadata."""

    category: AtlanTypeCategory = AtlanTypeCategory.CUSTOM_METADATA
    """Type category for custom metadata definitions."""

    display_name: Union[str, None] = None
    """Name used for display purposes (in user interfaces)."""

    options: Union[CustomMetadataDef.Options, None] = None
    """Optional properties of the type definition."""

    @staticmethod
    def create(
        display_name: str, description: Optional[str] = None
    ) -> CustomMetadataDef:
        """
        Builds the minimal object necessary to create a custom metadata definition.

        :param display_name: human-readable name for the custom metadata
        :param description: optional description
        :returns: the minimal object necessary to create the custom metadata typedef
        """
        from pyatlan_v9.utils import validate_required_fields

        validate_required_fields(
            ["display_name"],
            [display_name],
        )
        return CustomMetadataDef(
            category=AtlanTypeCategory.CUSTOM_METADATA,
            display_name=display_name,
            name=display_name,
            description=description,
        )


# =============================================================================
# TYPE DEFINITION RESPONSE
# =============================================================================


class TypeDefResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Response containing all type definitions."""

    enum_defs: List[EnumDef] = msgspec.field(default_factory=list)
    """List of enumeration type definitions."""

    struct_defs: List[StructDef] = msgspec.field(default_factory=list)
    """List of struct type definitions."""

    atlan_tag_defs: List[AtlanTagDef] = msgspec.field(
        default_factory=list, name="classificationDefs"
    )
    """List of classification type definitions."""

    entity_defs: List[EntityDef] = msgspec.field(default_factory=list)
    """List of entity type definitions."""

    relationship_defs: List[RelationshipDef] = msgspec.field(default_factory=list)
    """List of relationship type definitions."""

    custom_metadata_defs: List[CustomMetadataDef] = msgspec.field(
        default_factory=list, name="businessMetadataDefs"
    )
    """List of custom metadata type definitions."""

    # Internal computed lists (populated in __post_init__)
    _reserved_entity_defs: list = []  # noqa: RUF012
    _custom_entity_defs: list = []  # noqa: RUF012
    _custom_entity_def_names: set = set()  # noqa: RUF012

    def __post_init__(self):
        """Categorize entity defs into reserved and custom after initialization."""
        self._reserved_entity_defs = []
        self._custom_entity_defs = []
        self._custom_entity_def_names = set()
        for entity_def in self.entity_defs:
            if entity_def.reserved_type:
                self._reserved_entity_defs.append(entity_def)
            else:
                self._custom_entity_defs.append(entity_def)
                self._custom_entity_def_names.add(entity_def.name)

    @property
    def reserved_entity_defs(self) -> List[EntityDef]:
        """Entity definitions for reserved (built-in) types."""
        return self._reserved_entity_defs

    @property
    def custom_entity_defs(self) -> List[EntityDef]:
        """Entity definitions for custom types."""
        return self._custom_entity_defs

    @property
    def custom_entity_def_names(self) -> Set[str]:
        """Names of custom entity definitions."""
        return self._custom_entity_def_names

    def is_custom_entity_def_name(self, name: str) -> bool:
        """Check if the given name matches any custom entity definition."""
        for custom_name in self.custom_entity_def_names:
            if custom_name in name:
                return True
        return False
