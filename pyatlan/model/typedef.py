from __future__ import annotations

import json
import time
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, cast

from pydantic.v1 import Field, PrivateAttr

from pyatlan.errors import ErrorCode
from pyatlan.model.atlan_image import AtlanImage
from pyatlan.model.constants import (
    AssetTypes,
    DomainTypes,
    EntityTypes,
    GlossaryTypes,
    OtherAssetTypes,
)
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

_complete_type_list: AssetTypes = {
    "ADLSAccount",
    "ADLSContainer",
    "ADLSObject",
    "APIPath",
    "APISpec",
    "Collection",
    "Query",
    "BIProcess",
    "Badge",
    "Column",
    "ColumnProcess",
    "Connection",
    "DataStudioAsset",
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

_all_other_types: OtherAssetTypes = {"File"}


def _get_all_qualified_names(asset_type: str) -> Set[str]:
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.assets import Asset
    from pyatlan.model.fluent_search import FluentSearch

    client = AtlanClient.get_default_client()
    request = (
        FluentSearch.select()
        .where(Asset.TYPE_NAME.eq(asset_type))
        .include_on_results(Asset.QUALIFIED_NAME)
        .to_request()
    )
    results = client.asset.search(request)
    names = [result.qualified_name or "" for result in results]
    return set(names)


class TypeDef(AtlanObject):
    category: AtlanTypeCategory = Field(description="Type of the type definition.")
    create_time: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which this object was created, in milliseconds.",
    )
    created_by: Optional[str] = Field(
        default=None, description="Username of the user who created the object."
    )
    description: Optional[str] = Field(
        default=None, description="Description of the type definition."
    )
    guid: Optional[str] = Field(
        default=None,
        description="Unique identifier that represents the type definition.",
    )
    name: str = Field(default=None, description="Unique name of this type definition.")
    type_version: Optional[str] = Field(default=None, description="Internal use only.")
    update_time: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which this object was last assets_updated, in milliseconds.",
    )
    updated_by: Optional[str] = Field(
        default=None,
        description="Username of the user who last assets_updated the object.",
    )
    version: Optional[int] = Field(
        default=None, description="Version of this type definition."
    )


class EnumDef(TypeDef):
    class ElementDef(AtlanObject):
        value: str = Field(description="One unique value within the enumeration.")
        description: Optional[str] = Field(default=None, description="Unused.")
        ordinal: Optional[int] = Field(
            default=None, description="Unique numeric identifier for the value."
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
        def list_from(values: List[str]) -> List[EnumDef.ElementDef]:
            from pyatlan.utils import validate_required_fields

            validate_required_fields(
                ["values"],
                [values],
            )
            elements: List[EnumDef.ElementDef] = []
            elements.extend(
                EnumDef.ElementDef.of(ordinal=i, value=values[i])
                for i in range(len(values))
            )
            return elements

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
            # Make a copy of current values list
            extended_list = current[:]
            for element in new:
                if element not in unique_elements:
                    extended_list.append(element)
                    unique_elements.add(element)
            return extended_list

    category: AtlanTypeCategory = AtlanTypeCategory.ENUM
    element_defs: List[EnumDef.ElementDef] = Field(
        description="Valid values for the enumeration."
    )
    options: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional properties of the type definition."
    )
    service_type: Optional[str] = Field(default=None, description="Internal use only.")

    @staticmethod
    def create(name: str, values: List[str]) -> EnumDef:
        """
        Builds the minimal object necessary to create an enumeration definition.

        :param name: display name the human-readable name for the enumeration
        :param values: the list of additional valid values
        (as strings) to add to the existing enumeration
        :returns: the minimal object necessary to create the enumeration typedef
        """
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["name", "values"],
            [name, values],
        )
        # Explicitly set all defaults to ensure
        # inclusion during pydantic serialization
        return EnumDef(
            category=AtlanTypeCategory.ENUM,
            name=name,
            element_defs=EnumDef.ElementDef.list_from(values),
        )

    @staticmethod
    def update(name: str, values: List[str], replace_existing: bool) -> EnumDef:
        """
        Builds the minimal object necessary to update an enumeration definition.

        :param name: display name the human-readable name for the enumeration
        :param values: the list of additional valid values
        (as strings) to add to the existing enumeration
        :param replace_existing: if `True`, will replace all
        existing values in the enumeration with the new ones;
        or if `False` the new ones will be appended to the existing set
        :returns: the minimal object necessary to update the enumeration typedef
        """
        from pyatlan.cache.enum_cache import EnumCache
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["name", "values", "replace_existing"],
            [name, values, replace_existing],
        )
        update_values = (
            values
            if replace_existing
            else EnumDef.ElementDef.extend_elements(
                new=values, current=EnumCache.get_by_name(str(name)).get_valid_values()
            )
        )
        return EnumDef(
            name=name,
            category=AtlanTypeCategory.ENUM,
            element_defs=EnumDef.ElementDef.list_from(update_values),
        )

    def get_valid_values(self) -> List[str]:
        """
        Translate the element definitions in this enumeration into simple list of strings.
        """
        return [one.value for one in self.element_defs] if self.element_defs else []


class AttributeDef(AtlanObject):
    class Options(AtlanObject):
        custom_metadata_version: str = Field(
            description="Indicates the version of the custom metadata structure. This determines which other options "
            "are available and used.",
            default="v2",
        )
        description: Optional[str] = Field(
            default=None, description="Optional description of the attribute."
        )
        applicable_entity_types: Optional[str] = Field(
            default=None,
            description="Set of entities on which this attribute can be applied. "
            "Note: generally this should be left as-is. Any overrides should instead be applied through "
            "one or more of applicable_asset_types}, applicable_glossary_types}, or "
            "applicable_other_asset_types}.",
        )
        custom_applicable_entity_types: Optional[str] = Field(
            default=None,
            description="Set of entities on which this attribute should appear."
            "Deprecated: see applicable_asset_types, applicable_glossary_types and "
            "applicable_other_asset_types",
        )
        allow_search: Optional[bool] = Field(
            default=None,
            description="Whether the attribute should be searchable (true) or not (false).",
        )
        max_str_length: Optional[str] = Field(
            default=None,
            description="Maximum length allowed for a string value.",
        )
        allow_filtering: Optional[bool] = Field(
            default=None,
            description="Whether this attribute should appear in the filterable facets of discovery (true) or not "
            "(false).",
        )
        multi_value_select: Optional[bool] = Field(
            default=None,
            description="Whether this attribute can have multiple values (true) or only a single value (false).",
        )
        show_in_overview: Optional[bool] = Field(
            default=None,
            description="Whether users will see this attribute in the overview tab of the sidebar (true) or not "
            "(false).",
        )
        is_deprecated: Optional[str] = Field(
            default=None,
            description="Whether the attribute is deprecated ('true') or not (None or 'false').",
        )
        is_enum: Optional[bool] = Field(
            default=None,
            description="Whether the attribute is an enumeration (true) or not (None or false).",
        )
        enum_type: Optional[str] = Field(
            default=None,
            description="Name of the enumeration (options), when the attribute is an enumeration.",
        )
        custom_type: Optional[str] = Field(
            default=None,
            description="Used for Atlan-specific types like `users`, `groups`, `url`, and `SQL`.",
        )
        has_time_precision: Optional[bool] = Field(
            default=None,
            description="If true for a date attribute, then time-level precision is also available in the UI "
            "(otherwise only date-level)",
        )
        is_archived: Optional[bool] = Field(
            default=None,
            description="Whether the attribute has been deleted (true) or is still active (false).",
        )
        archived_at: Optional[int] = Field(
            default=None, description="When the attribute was deleted."
        )
        archived_by: Optional[str] = Field(
            default=None, description="User who deleted the attribute."
        )
        is_soft_reference: Optional[str] = Field(default=None, description="TBC")
        is_append_on_partial_update: Optional[str] = Field(
            default=None, description="TBC"
        )
        primitive_type: Optional[str] = Field(
            default=None, description="Type of the attribute."
        )
        applicable_connections: Optional[str] = Field(
            default=None,
            description="Qualified names of connections to which to restrict the attribute. "
            "Only assets within one of these connections will have this attribute available. "
            "To further restrict the types of assets within the connections, see applicable_asset_types.",
        )
        applicable_glossaries: Optional[str] = Field(
            default=None,
            description="Qualified names of glossaries to which to restrict the attribute. "
            "Only glossary assets within one of these glossaries will have this attribute available. "
            "To further restrict the types of assets within the glossaries, see applicable_glossary_types.",
        )
        applicable_domains: Optional[str] = Field(
            default=None,
            description="Qualified names of domains to which to restrict the attribute. "
            "Only domains and data products within one of these domains will have this attribute available. "
            "To further restrict the types of assets within the domains, see applicable_domain_types.",
        )
        applicable_asset_types: Optional[str] = Field(
            default=None,
            alias="assetTypesList",
            description="Asset type names to which to restrict the attribute. "
            "Only assets of one of these types will have this attribute available. "
            "To further restrict the assets for this custom metadata by "
            "connection, see applicable_connections. ",
        )
        applicable_glossary_types: Optional[str] = Field(
            default=None,
            alias="glossaryTypeList",
            description="Glossary type names to which to restrict the attribute. "
            "Only glossary assets of one of these types will have this attribute available. "
            "To further restrict the glossary content for this "
            "custom metadata by glossary, see applicable_glossaries.",
        )
        applicable_domain_types: Optional[str] = Field(
            default=None,
            alias="domainTypesList",
            description="Data product type names to which to restrict the attribute. "
            "These cover asset types in data products and data domains. "
            "Only assets of one of these types will have this attribute available.",
        )
        applicable_other_asset_types: Optional[str] = Field(
            default=None,
            alias="otherAssetTypeList",
            description="Any other asset type names to which to restrict the attribute. "
            "These cover any asset type that is not managed within a connection or a glossary. "
            "Only assets of one of these types will have this attribute available.",
        )

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
                custom_metadata_version="v2",
                primitive_type=attribute_type.value,
                applicable_entity_types='["Asset"]',
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
        default=None,
        description="Whether the attribute is being newly created (true) or not (false).",
    )
    cardinality: Optional[Cardinality] = Field(
        default=None,
        description="Whether the attribute allows a single or multiple values. In the case of multiple values, "
        "`LIST` indicates they are ordered and duplicates are allowed, while `SET` indicates "
        "they are unique and unordered.",
    )
    constraints: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Internal use only."
    )
    enum_values: Optional[List[str]] = Field(
        default=None, description="list of values for an enumeration."
    )
    description: Optional[str] = Field(
        default=None, description="Description of the attribute definition."
    )
    default_value: Optional[str] = Field(
        default=None, description="Default value for this attribute (if any)."
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Name to use within all user interactions through the user interface. Note that this may not "
        "be the same name used to update or interact with the attribute through API operations, for "
        "that see the `name` property. (This property can be used instead of `name` for the creation "
        "of an attribute definition as well.)",
    )
    name: Optional[str] = Field(
        default=None,
        description="Unique name of this attribute definition. When provided during creation, this should be the "
        "human-readable name for the attribute. When returned (or provided for an update) this will be "
        "the static-hashed name that Atlan uses internally. (This is to allow the name to be changed "
        "by the user without impacting existing instances of the attribute.)",
    )
    include_in_notification: Optional[bool] = Field(default=None, description="TBC")
    index_type: Optional[IndexType] = Field(
        default=None, description="", example="DEFAULT"
    )
    is_indexable: Optional[bool] = Field(
        default=None,
        description="When true, values for this attribute will be indexed for searching.",
    )
    is_optional: Optional[bool] = Field(
        default=None,
        description="When true, a value will not be required for this attribute.",
    )
    is_unique: Optional[bool] = Field(
        default=None,
        description="When true, this attribute must be unique across all assets.",
    )
    options: Optional[AttributeDef.Options] = Field(
        default=None, description="Extensible options for the attribute."
    )
    search_weight: Optional[float] = Field(default=None, description="TBC")
    skip_scrubbing: Optional[bool] = Field(
        default=None, description="When true, scrubbing of data will be skipped."
    )
    type_name: Optional[str] = Field(
        default=None, description="Type of this attribute."
    )
    values_min_count: Optional[float] = Field(
        default=None,
        description="Minimum number of values for this attribute. If greater than 0, this attribute "
        "becomes required.",
    )
    values_max_count: Optional[float] = Field(
        default=None,
        description="Maximum number of values for this attribute. If greater than 1, this attribute allows "
        "multiple values.",
    )
    index_type_es_config: Optional[Dict[str, str]] = Field(
        default=None, description="Internal use only.", alias="indexTypeESConfig"
    )
    index_type_es_fields: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None, description="Internal use only.", alias="indexTypeESFields"
    )
    is_default_value_null: Optional[bool] = Field(default=None, description="TBC")

    def __setattr__(self, name, value):
        if name in AttributeDef._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = [
        "applicable_asset_types",
        "applicable_glossary_types",
        "applicable_domain_types",
        "applicable_other_asset_types",
        "applicable_entity_types",
        "applicable_connections",
        "applicable_glossaries",
        "applicable_domains",
    ]

    @property
    def applicable_entity_types(self) -> EntityTypes:
        """
        Set of entities on which this attribute can be applied.
        Note: generally this should be left as-is. Any overrides should instead be applied through
        one or more of applicable_asset_types, applicable_glossary_types, or applicable_other_asset_types.
        """
        if self.options and self.options.applicable_entity_types:
            return set(json.loads(self.options.applicable_entity_types))
        return set()

    @applicable_entity_types.setter
    def applicable_entity_types(self, entity_types: EntityTypes):
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(entity_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_entity_types", EntityTypes
            )
        self.options.applicable_entity_types = json.dumps(list(entity_types))

    @property
    def applicable_asset_types(self) -> AssetTypes:
        """
        Asset type names to which to restrict the attribute.
        Only assets of one of these types will have this attribute available.
        To further restrict the assets for this custom metadata by connection, see applicable_connections.
        """
        if self.options and self.options.applicable_asset_types:
            return set(json.loads(self.options.applicable_asset_types))
        return set()

    @applicable_asset_types.setter
    def applicable_asset_types(self, asset_types: AssetTypes):
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(asset_types, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_asset_types", AssetTypes
            )
        if not asset_types.issubset(_complete_type_list):
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                asset_types, "applicable_asset_types", _complete_type_list
            )
        self.options.applicable_asset_types = json.dumps(list(asset_types))

    @property
    def applicable_glossary_types(self) -> GlossaryTypes:
        """
        Glossary type names to which to restrict the attribute.
        Only glossary assets of one of these types will have this attribute available.
        To further restrict the glossary content for this custom metadata by glossary, see applicable_glossaries.
        """
        if self.options and self.options.applicable_glossary_types:
            return set(json.loads(self.options.applicable_glossary_types))
        return set()

    @applicable_glossary_types.setter
    def applicable_glossary_types(self, glossary_types: GlossaryTypes):
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

    @property
    def applicable_domain_types(self) -> DomainTypes:
        """
        Data product type names to which to restrict the attribute.
        These cover asset types in data products and data domains.
        Only assets of one of these types will have this attribute available.
        """
        if self.options and self.options.applicable_domain_types:
            return set(json.loads(self.options.applicable_domain_types))
        return set()

    @applicable_domain_types.setter
    def applicable_domain_types(self, domain_types: DomainTypes):
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

    @property
    def applicable_other_asset_types(self) -> OtherAssetTypes:
        """
        Any other asset type names to which to restrict the attribute.
        These cover any asset type that is not managed within a connection or a glossary.
        Only assets of one of these types will have this attribute available.
        """
        if self.options and self.options.applicable_other_asset_types:
            return set(json.loads(self.options.applicable_other_asset_types))
        return set()

    @applicable_other_asset_types.setter
    def applicable_other_asset_types(self, other_asset_types: OtherAssetTypes):
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

    @property
    def applicable_connections(self) -> Set[str]:
        """
        Qualified names of connections to which to restrict the attribute.
        Only assets within one of these connections will have this attribute available.
        To further restrict the types of assets within the glossaries, see applicable_asset_types}.
        """
        if self.options and self.options.applicable_connections:
            return set(json.loads(self.options.applicable_connections))
        return set()

    @applicable_connections.setter
    def applicable_connections(self, connections: Set[str]):
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(connections, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_connections", "Set[str]"
            )
        self.options.applicable_connections = json.dumps(list(connections))

    @property
    def applicable_glossaries(self) -> Set[str]:
        """
        Qualified names of glossaries to which to restrict the attribute.
        Only glossary assets within one of these glossaries will have this attribute available.
        To further restrict the types of assets within the glossaries, see applicable_glossary_types.
        """
        if self.options and self.options.applicable_glossaries:
            return set(json.loads(self.options.applicable_glossaries))
        return set()

    @applicable_glossaries.setter
    def applicable_glossaries(self, glossaries: Set[str]):
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(glossaries, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_glossaries", "Set[str]"
            )
        self.options.applicable_glossaries = json.dumps(list(glossaries))

    @property
    def applicable_domains(self) -> Set[str]:
        """
        Qualified names of domains to which to restrict the attribute.
        Only domains and data products within one of these domains will have this attribute available.
        To further restrict the types of assets within the domains, see applicable_domain_types.
        """
        if self.options and self.options.applicable_domains:
            return set(json.loads(self.options.applicable_domains))
        return set()

    @applicable_domains.setter
    def applicable_domains(self, domains: Set[str]):
        if self.options is None:
            raise ErrorCode.MISSING_OPTIONS.exception_with_parameters()
        if not isinstance(domains, set):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "applicable_domains", "Set[str]"
            )
        self.options.applicable_domains = json.dumps(list(domains))

    @staticmethod
    def create(
        display_name: str,
        attribute_type: AtlanCustomAttributePrimitiveType,
        multi_valued: bool = False,
        options_name: Optional[str] = None,
        applicable_connections: Optional[Set[str]] = None,
        applicable_asset_types: Optional[AssetTypes] = None,
        applicable_glossaries: Optional[Set[str]] = None,
        applicable_glossary_types: Optional[GlossaryTypes] = None,
        applicable_other_asset_types: Optional[OtherAssetTypes] = None,
        applicable_domains: Optional[Set[str]] = None,
        applicable_domain_types: Optional[DomainTypes] = None,
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

        attr_def.applicable_asset_types = applicable_asset_types or _complete_type_list
        attr_def.applicable_glossary_types = (
            applicable_glossary_types or _all_glossary_types
        )
        attr_def.applicable_domain_types = applicable_domain_types or _all_domain_types
        attr_def.applicable_other_asset_types = (
            applicable_other_asset_types or _all_other_types
        )
        attr_def.applicable_connections = (
            applicable_connections or _get_all_qualified_names("Connection")
        )
        attr_def.applicable_glossaries = (
            applicable_glossaries or _get_all_qualified_names("AtlasGlossary")
        )
        attr_def.applicable_domains = applicable_domains or _all_domains
        return attr_def

    def is_archived(self) -> bool:
        return bool(opt.is_archived) if (opt := self.options) else False

    def archive(self, by: str) -> AttributeDef:
        if self.options:
            removal_epoch = int(time.time() * 1000)
            self.options.is_archived = True
            self.options.archived_by = by
            self.options.archived_at = removal_epoch
            self.display_name = f"{self.display_name}-archived-{removal_epoch}"
        return self


class RelationshipAttributeDef(AttributeDef):
    is_legacy_attribute: Optional[bool] = Field(default=None, description="Unused.")
    relationship_type_name: Optional[str] = Field(
        default=None, description="Name of the relationship type."
    )


class StructDef(TypeDef):
    category: AtlanTypeCategory = AtlanTypeCategory.STRUCT
    attribute_defs: Optional[List[AttributeDef]] = Field(
        default=None,
        description="list of attributes that should be available in the type_ definition.",
    )
    service_type: Optional[str] = Field(
        default=None, description="Internal use only.", example="atlan"
    )


class AtlanTagDef(TypeDef):
    attribute_defs: Optional[List[AttributeDef]] = Field(
        default=None, description="Unused."
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CLASSIFICATION
    display_name: str = Field(
        default=None, description="Name used for display purposes (in user interfaces)."
    )
    entity_types: Optional[List[str]] = Field(
        default=None,
        description="A list of the entity types that this classification can be used against."
        " (This should be `Asset` to allow classification of any asset in Atlan.)",
    )
    options: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional properties of the type_ definition."
    )
    sub_types: Optional[List[str]] = Field(
        default=None,
        description="list of the sub-types that extend from this type_ definition. Generally this is not specified "
        "in any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
    )
    super_types: Optional[List[str]] = Field(
        default=None,
        description="list of the super-types that this type_ definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
    )
    service_type: Optional[str] = Field(
        default=None, description="Name used for display purposes (in user interfaces)."
    )
    skip_display_name_uniqueness_check: Optional[bool] = Field(
        default=None, description="TBC"
    )

    @staticmethod
    def create(
        name: str,
        color: AtlanTagColor = AtlanTagColor.GRAY,
        icon: AtlanIcon = AtlanIcon.ATLAN_TAG,
        image: Optional[AtlanImage] = None,
        emoji: Optional[str] = None,
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
        elif emoji:
            cls_options["emoji"] = emoji
            cls_options["iconType"] = TagIconType.EMOJI.value
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


RESERVED_SERVICE_TYPES = {"atlas_core", "atlan", "aws", "azure", "gcp", "google"}


class EntityDef(TypeDef):
    attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Unused.", example=[]
    )
    business_attribute_defs: Optional[Dict[str, List[Dict[str, Any]]]] = Field(
        default_factory=cast(Callable[[], Dict[str, List[Dict[str, Any]]]], dict),
        description="Unused.",
        example=[],
    )
    category: AtlanTypeCategory = AtlanTypeCategory.ENTITY
    relationship_attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Unused.", example=[]
    )
    service_type: Optional[str] = Field(
        default=None, description="Internal use only.", example="atlan"
    )
    sub_types: Optional[List[str]] = Field(
        default_factory=list,
        description="list of the sub-types that extend from this type_ definition. Generally this is not specified in "
        "any request, but is only supplied in responses. (This is intended for internal use only, and "
        "should not be used without specific guidance.)",
        example=[],
    )
    super_types: Optional[List[str]] = Field(
        default_factory=list,
        description="list of the super-types that this type_ definition should extend. (This is intended for internal "
        "use only, and should not be used without specific guidance.)",
        example=[],
    )

    @property
    def reserved_type(self) -> bool:
        return self.service_type in RESERVED_SERVICE_TYPES


class RelationshipDef(TypeDef):
    attribute_defs: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Unused.", example=[]
    )
    category: AtlanTypeCategory = AtlanTypeCategory.RELATIONSHIP
    end_def1: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Unused.", example={}
    )
    end_def2: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Unused.", example={}
    )
    propagate_tags: str = Field(
        default="ONE_TO_TWO", description="Unused", example="ONE_TO_TWO"
    )
    relationship_category: str = Field(
        default="AGGREGATION", description="Unused", example="AGGREGATION"
    )
    relationship_label: str = Field(
        default="__SalesforceOrganization.reports",
        description="Unused",
        example="__SalesforceOrganization.reports",
    )
    service_type: Optional[str] = Field(
        default=None, description="Internal use only.", example="atlan"
    )


class CustomMetadataDef(TypeDef):
    class Options(AtlanObject):
        emoji: Optional[str] = Field(
            default=None,
            description="If the logoType is emoji, this should hold the emoji character.",
        )
        image_id: Optional[str] = Field(
            default=None, description="The id of the image used for the logo."
        )
        is_locked: Optional[bool] = Field(
            description="Indicates whether the custom metadata can be managed in the UI (false) or not (true)."
        )
        logo_type: Optional[str] = Field(
            default=None, description="Type of logo used for the custom metadata."
        )
        logo_url: Optional[str] = Field(
            default=None,
            description="If the logoType is image, this should hold a URL to the image.",
        )
        icon_color: Optional[AtlanTagColor] = Field(
            default=None, description="Color to use for the icon."
        )
        icon_name: Optional[AtlanIcon] = Field(
            default=None, description="Icon to use to represent the custom metadata."
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
                emoji=emoji, logo_type="emoji", is_locked=locked
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

        @staticmethod
        def with_logo_from_icon(
            icon: AtlanIcon, color: AtlanTagColor, locked: bool = False
        ) -> CustomMetadataDef.Options:
            from pyatlan.utils import validate_required_fields

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

    attribute_defs: List[AttributeDef] = Field(
        default_factory=list,
        description="list of custom attributes defined within the custom metadata.",
    )
    category: AtlanTypeCategory = AtlanTypeCategory.CUSTOM_METADATA
    display_name: str = Field(
        default=None, description="Name used for display purposes (in user interfaces)."
    )
    options: Optional[CustomMetadataDef.Options] = Field(
        default=None, description="Optional properties of the type definition."
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
    enum_defs: List[EnumDef] = Field(
        default_factory=list, description="list of enumeration type definitions."
    )
    struct_defs: List[StructDef] = Field(
        default_factory=list, description="list of struct type definitions."
    )
    atlan_tag_defs: List[AtlanTagDef] = Field(
        default_factory=list,
        description="list of classification type definitions.",
        alias="classificationDefs",
    )
    entity_defs: List[EntityDef] = Field(
        default_factory=list, description="list of entity type_ definitions."
    )
    relationship_defs: List[RelationshipDef] = Field(
        default_factory=list, description="list of relationship type_ definitions."
    )
    custom_metadata_defs: List[CustomMetadataDef] = Field(
        default_factory=list,
        description="list of custom metadata type_ definitions.",
        alias="businessMetadataDefs",
    )

    _reserved_entity_defs: List[EntityDef] = PrivateAttr(default_factory=list)

    _custom_entity_defs: List[EntityDef] = PrivateAttr(default_factory=list)

    _custom_entity_def_names: Set[str] = PrivateAttr(default_factory=set)

    def __init__(self, **data):
        super().__init__(**data)
        for entity_def in self.entity_defs:
            if entity_def.reserved_type:
                self._reserved_entity_defs.append(entity_def)
            else:
                self._custom_entity_defs.append(entity_def)
                self._custom_entity_def_names.add(entity_def.name)

    @property
    def reserved_entity_defs(self) -> List[EntityDef]:
        return self._reserved_entity_defs

    @property
    def custom_entity_defs(self) -> List[EntityDef]:
        return self._custom_entity_defs

    @property
    def custom_entity_def_names(self) -> Set[str]:
        return self._custom_entity_def_names

    def is_custom_entity_def_name(self, name: str) -> bool:
        for custom_name in self.custom_entity_def_names:
            if custom_name in name:
                return True
        return False
