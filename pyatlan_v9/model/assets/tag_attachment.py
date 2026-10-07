# Passthrough type in atlanhq/models: generated once with passthrough off, maintained here (see _init_manual.py).
# ruff: noqa: ARG002
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
TagAttachment asset model with flattened inheritance.

This module provides:
- TagAttachment: Flat asset class (easy to use)
- TagAttachmentAttributes: Nested attributes struct (extends AssetAttributes)
- TagAttachmentNested: Nested API format struct
"""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.model.conversion_utils import (
    categorize_relationships,
    merge_relationships,
)
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.transform import register_asset

from .airflow_related import RelatedAirflowTask
from .anomalo_related import RelatedAnomaloCheck
from .app_related import RelatedApplication, RelatedApplicationField
from .asset import (
    _ASSET_REL_FIELDS,
    Asset,
    AssetAttributes,
    AssetNested,
    AssetRelationshipAttributes,
    _extract_asset_attrs,
    _populate_asset_attrs,
)
from .context_related import RelatedContextRepository
from .data_contract_related import RelatedDataContract
from .data_mesh_related import RelatedDataProduct
from .data_quality_related import RelatedDataQualityRule, RelatedMetric
from .gcp_dataplex_related import RelatedGCPDataplexAspectType
from .gtc_related import RelatedAtlasGlossaryTerm
from .knowledge_related import RelatedKnowledgeFile
from .model_related import RelatedModelAttribute, RelatedModelEntity
from .monte_carlo_related import RelatedMCIncident, RelatedMCMonitor
from .partial_related import RelatedPartialField, RelatedPartialObject
from .process_related import RelatedProcess
from .referenceable_related import RelatedReferenceable
from .resource_related import RelatedFile, RelatedLink, RelatedReadme
from .schema_registry_related import RelatedSchemaRegistrySubject
from .soda_related import RelatedSodaCheck
from .spark_related import RelatedSparkJob
from .tag_related import RelatedTagAttachment

# =============================================================================
# FLAT ASSET CLASS
# =============================================================================


@register_asset
class TagAttachment(Asset):
    """
    Represents Source tag association asset.
    """

    TAG_QUALIFIED_NAME: ClassVar[Any] = None
    OBJECT_QUALIFIED_NAME: ClassVar[Any] = None
    OBJECT_TYPE_NAME: ClassVar[Any] = None
    SOURCE_TAG_QUALIFIED_NAME: ClassVar[Any] = None
    SOURCE_TAG_DISPLAY_NAME: ClassVar[Any] = None
    SOURCE_TAG_TYPE_NAME: ClassVar[Any] = None
    VALUE_TYPE: ClassVar[Any] = None
    VALUE: ClassVar[Any] = None
    PROPAGATE: ClassVar[Any] = None
    TAG_ATTACHMENT_STRING_VALUE: ClassVar[Any] = None
    TAG_ID: ClassVar[Any] = None
    TAG_ATTRIBUTES: ClassVar[Any] = None
    TAG_ALLOWED_VALUES: ClassVar[Any] = None
    MAPPED_CLASSIFICATION_NAME: ClassVar[Any] = None
    CATALOG_DATASET_GUID: ClassVar[Any] = None
    INPUT_TO_AIRFLOW_TASKS: ClassVar[Any] = None
    OUTPUT_FROM_AIRFLOW_TASKS: ClassVar[Any] = None
    ANOMALO_CHECKS: ClassVar[Any] = None
    APPLICATION: ClassVar[Any] = None
    APPLICATION_FIELD: ClassVar[Any] = None
    CONTEXT_REPOSITORIES: ClassVar[Any] = None
    DATA_CONTRACT_LATEST: ClassVar[Any] = None
    DATA_CONTRACT_LATEST_CERTIFIED: ClassVar[Any] = None
    OUTPUT_PORT_DATA_PRODUCTS: ClassVar[Any] = None
    INPUT_PORT_DATA_PRODUCTS: ClassVar[Any] = None
    MODEL_IMPLEMENTED_ENTITIES: ClassVar[Any] = None
    MODEL_IMPLEMENTED_ATTRIBUTES: ClassVar[Any] = None
    METRICS: ClassVar[Any] = None
    DQ_BASE_DATASET_RULES: ClassVar[Any] = None
    DQ_REFERENCE_DATASET_RULES: ClassVar[Any] = None
    GCP_DATAPLEX_ASPECT_TYPE_METADATA_ENTITIES: ClassVar[Any] = None
    MEANINGS: ClassVar[Any] = None
    KNOWLEDGE_LINKED_FILES: ClassVar[Any] = None
    MC_MONITORS: ClassVar[Any] = None
    MC_INCIDENTS: ClassVar[Any] = None
    PARTIAL_CHILD_FIELDS: ClassVar[Any] = None
    PARTIAL_CHILD_OBJECTS: ClassVar[Any] = None
    INPUT_TO_PROCESSES: ClassVar[Any] = None
    OUTPUT_FROM_PROCESSES: ClassVar[Any] = None
    USER_DEF_RELATIONSHIP_TO: ClassVar[Any] = None
    USER_DEF_RELATIONSHIP_FROM: ClassVar[Any] = None
    FILES: ClassVar[Any] = None
    LINKS: ClassVar[Any] = None
    README: ClassVar[Any] = None
    SCHEMA_REGISTRY_SUBJECTS: ClassVar[Any] = None
    SODA_CHECKS: ClassVar[Any] = None
    INPUT_TO_SPARK_JOBS: ClassVar[Any] = None
    OUTPUT_FROM_SPARK_JOBS: ClassVar[Any] = None

    tag_qualified_name: Union[str, None, UnsetType] = UNSET
    """Represents associated source tag's qualified name."""

    object_qualified_name: Union[str, None, UnsetType] = UNSET
    """Qualified name of the asset the source tag is attached to. Read by publish-app; not an Atlas typedef attribute."""

    object_type_name: Union[str, None, UnsetType] = UNSET
    """Type name of the asset the source tag is attached to. Read by publish-app; not an Atlas typedef attribute."""

    source_tag_qualified_name: Union[str, None, UnsetType] = UNSET
    """Qualified name of the source tag. Read by publish-app; not an Atlas typedef attribute."""

    source_tag_display_name: Union[str, None, UnsetType] = UNSET
    """Name of the source tag, used as the Atlan tag name. Read by publish-app; not an Atlas typedef attribute."""

    source_tag_type_name: Union[str, None, UnsetType] = UNSET
    """Type name of the source tag, for example GlueTag. Read by publish-app; not an Atlas typedef attribute."""

    value_type: Union[str, None, UnsetType] = UNSET
    """Type of the tag value, for example STRING. Read by publish-app; not an Atlas typedef attribute."""

    value: Union[str, None, UnsetType] = UNSET
    """Value of the source tag on the asset. Read by publish-app; not an Atlas typedef attribute."""

    propagate: Union[bool, None, UnsetType] = UNSET
    """Whether the Atlan tag propagates from the asset. Read by publish-app; not an Atlas typedef attribute."""

    tag_attachment_string_value: Union[str, None, UnsetType] = UNSET
    """Represents associated tag value."""

    tag_id: Union[str, None, UnsetType] = UNSET
    """Unique identifier of the tag in the source system."""

    tag_attributes: Union[List[Dict[str, Any]], None, UnsetType] = UNSET
    """Attributes associated with the tag in the source system."""

    tag_allowed_values: Union[List[str], None, UnsetType] = UNSET
    """Allowed values for the tag in the source system. These are denormalized from tagAttributes for ease of querying."""

    mapped_classification_name: Union[str, None, UnsetType] = UNSET
    """Name of the classification in Atlan that is mapped to this tag."""

    catalog_dataset_guid: Union[str, None, UnsetType] = UNSET
    """Unique identifier of the dataset this asset belongs to."""

    input_to_airflow_tasks: Union[List[RelatedAirflowTask], None, UnsetType] = UNSET
    """Tasks to which this asset provides input."""

    output_from_airflow_tasks: Union[List[RelatedAirflowTask], None, UnsetType] = UNSET
    """Tasks from which this asset is output."""

    anomalo_checks: Union[List[RelatedAnomaloCheck], None, UnsetType] = UNSET
    """Checks that run on this asset."""

    application: Union[RelatedApplication, None, UnsetType] = UNSET
    """Application owning the Asset."""

    application_field: Union[RelatedApplicationField, None, UnsetType] = UNSET
    """ApplicationField owning the Asset."""

    context_repositories: Union[List[RelatedContextRepository], None, UnsetType] = UNSET
    """Context repositories that use this asset as input."""

    data_contract_latest: Union[RelatedDataContract, None, UnsetType] = UNSET
    """Latest version of the data contract (in any status) for this asset."""

    data_contract_latest_certified: Union[RelatedDataContract, None, UnsetType] = UNSET
    """Latest certified version of the data contract for this asset."""

    output_port_data_products: Union[List[RelatedDataProduct], None, UnsetType] = UNSET
    """Data products for which this asset is an output port."""

    input_port_data_products: Union[List[RelatedDataProduct], None, UnsetType] = UNSET
    """Data products for which this asset is an input port."""

    model_implemented_entities: Union[List[RelatedModelEntity], None, UnsetType] = UNSET
    """Entities implemented by this asset."""

    model_implemented_attributes: Union[
        List[RelatedModelAttribute], None, UnsetType
    ] = UNSET
    """Attributes implemented by this asset."""

    metrics: Union[List[RelatedMetric], None, UnsetType] = UNSET
    """"""

    dq_base_dataset_rules: Union[List[RelatedDataQualityRule], None, UnsetType] = UNSET
    """Rules that are applied on this dataset."""

    dq_reference_dataset_rules: Union[List[RelatedDataQualityRule], None, UnsetType] = (
        UNSET
    )
    """Rules where this dataset is referenced."""

    gcp_dataplex_aspect_type_metadata_entities: Union[
        List[RelatedGCPDataplexAspectType], None, UnsetType
    ] = UNSET
    """Dataplex entries (assets) that have aspects of this Aspect Type attached."""

    meanings: Union[List[RelatedAtlasGlossaryTerm], None, UnsetType] = UNSET
    """Glossary terms that are linked to this asset."""

    knowledge_linked_files: Union[List[RelatedKnowledgeFile], None, UnsetType] = UNSET
    """Knowledge files linked to this asset."""

    mc_monitors: Union[List[RelatedMCMonitor], None, UnsetType] = UNSET
    """Monitors that observe this asset."""

    mc_incidents: Union[List[RelatedMCIncident], None, UnsetType] = UNSET
    """"""

    partial_child_fields: Union[List[RelatedPartialField], None, UnsetType] = UNSET
    """Partial fields contained in the asset."""

    partial_child_objects: Union[List[RelatedPartialObject], None, UnsetType] = UNSET
    """Partial objects contained in the asset."""

    input_to_processes: Union[List[RelatedProcess], None, UnsetType] = UNSET
    """Processes to which this asset provides input."""

    output_from_processes: Union[List[RelatedProcess], None, UnsetType] = UNSET
    """Processes from which this asset is produced as output."""

    user_def_relationship_to: Union[List[RelatedReferenceable], None, UnsetType] = UNSET
    """"""

    user_def_relationship_from: Union[List[RelatedReferenceable], None, UnsetType] = (
        UNSET
    )
    """"""

    files: Union[List[RelatedFile], None, UnsetType] = UNSET
    """"""

    links: Union[List[RelatedLink], None, UnsetType] = UNSET
    """Links that are attached to this asset."""

    readme: Union[RelatedReadme, None, UnsetType] = UNSET
    """README that is linked to this asset."""

    schema_registry_subjects: Union[
        List[RelatedSchemaRegistrySubject], None, UnsetType
    ] = UNSET
    """Schema registry subjects associated with this asset."""

    soda_checks: Union[List[RelatedSodaCheck], None, UnsetType] = UNSET
    """"""

    input_to_spark_jobs: Union[List[RelatedSparkJob], None, UnsetType] = UNSET
    """"""

    output_from_spark_jobs: Union[List[RelatedSparkJob], None, UnsetType] = UNSET
    """"""

    def __post_init__(self) -> None:
        self.type_name = "TagAttachment"

    # =========================================================================
    # SDK Methods
    # =========================================================================

    def validate(self, for_creation: bool = False) -> None:
        """
        Dry-run validation of this TagAttachment instance.

        Checks that required fields (type_name, name, qualified_name) are set.
        When ``for_creation=True``, also checks hierarchy-specific fields
        (parent references, denormalized attributes) needed to create this asset.

        This is purely opt-in and is NOT called by any serde path — only by
        explicit user invocation (e.g., validating JSONL before sending to Atlan).

        Args:
            for_creation: If True, also validate fields required for asset creation.

        Raises:
            ValueError: If any required fields are missing or invalid.
        """
        errors: list[str] = []
        if self.type_name is UNSET:
            errors.append("type_name is required")
        if self.name is UNSET:
            errors.append("name is required")
        if self.qualified_name is UNSET or self.qualified_name is None:
            errors.append("qualified_name is required")
        if for_creation:
            if self.tag_id is UNSET:
                errors.append("tag_id is required for creation")
            if self.tag_allowed_values is UNSET:
                errors.append("tag_allowed_values is required for creation")
            if self.mapped_classification_name is UNSET:
                errors.append("mapped_classification_name is required for creation")
        if errors:
            raise ValueError(f"TagAttachment validation failed: {errors}")

    def minimize(self) -> "TagAttachment":
        """
        Return a minimal copy of this TagAttachment with only updater-required fields.

        Calls :meth:`validate` first to ensure the instance is valid, then
        returns a new TagAttachment with only the fields needed for an update
        (qualified_name, name, and any type-specific additional fields).

        Returns:
            A new TagAttachment instance with only the minimum required fields.
        """
        self.validate()
        return TagAttachment(qualified_name=self.qualified_name, name=self.name)

    def relate(self) -> "RelatedTagAttachment":
        """
        Create a :class:`RelatedTagAttachment` reference from this instance.

        Returns a lightweight reference suitable for use in relationship
        attributes. Prefers ``guid`` if set, otherwise falls back to
        ``qualified_name``.

        Returns:
            A RelatedTagAttachment reference to this asset.
        """
        if self.guid is not UNSET:
            return RelatedTagAttachment(guid=self.guid)
        return RelatedTagAttachment(qualified_name=self.qualified_name)

    # =========================================================================
    # Optimized Serialization Methods (override Asset base class)
    # =========================================================================

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """
        Convert to JSON string using optimized nested struct serialization.

        Args:
            nested: If True (default), use nested API format. If False, use flat format.
            serde: Optional Serde instance for encoder reuse. Uses shared singleton if None.

        Returns:
            JSON string representation
        """
        if serde is None:
            serde = get_serde()
        if nested:
            return self.to_nested_bytes(serde).decode("utf-8")
        else:
            return serde.encode(self).decode("utf-8")

    def to_nested_bytes(self, serde: Serde | None = None) -> bytes:
        """Serialize to Atlas nested-format JSON bytes (pure msgspec, no dict intermediate)."""
        if serde is None:
            serde = get_serde()
        return _tag_attachment_to_nested_bytes(self, serde)

    @staticmethod
    def from_json(json_data: str | bytes, serde: Serde | None = None) -> TagAttachment:
        """
        Create from JSON string or bytes using optimized nested struct deserialization.

        Args:
            json_data: JSON string or bytes to deserialize
            serde: Optional Serde instance for decoder reuse. Uses shared singleton if None.

        Returns:
            TagAttachment instance
        """
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _tag_attachment_from_nested_bytes(json_data, serde)


# =============================================================================
# NESTED FORMAT CLASSES
# =============================================================================


class TagAttachmentAttributes(AssetAttributes):
    """TagAttachment-specific attributes for nested API format."""

    tag_qualified_name: Union[str, None, UnsetType] = UNSET
    """Represents associated source tag's qualified name."""

    object_qualified_name: Union[str, None, UnsetType] = UNSET
    """Qualified name of the asset the source tag is attached to. Read by publish-app; not an Atlas typedef attribute."""

    object_type_name: Union[str, None, UnsetType] = UNSET
    """Type name of the asset the source tag is attached to. Read by publish-app; not an Atlas typedef attribute."""

    source_tag_qualified_name: Union[str, None, UnsetType] = UNSET
    """Qualified name of the source tag. Read by publish-app; not an Atlas typedef attribute."""

    source_tag_display_name: Union[str, None, UnsetType] = UNSET
    """Name of the source tag, used as the Atlan tag name. Read by publish-app; not an Atlas typedef attribute."""

    source_tag_type_name: Union[str, None, UnsetType] = UNSET
    """Type name of the source tag, for example GlueTag. Read by publish-app; not an Atlas typedef attribute."""

    value_type: Union[str, None, UnsetType] = UNSET
    """Type of the tag value, for example STRING. Read by publish-app; not an Atlas typedef attribute."""

    value: Union[str, None, UnsetType] = UNSET
    """Value of the source tag on the asset. Read by publish-app; not an Atlas typedef attribute."""

    propagate: Union[bool, None, UnsetType] = UNSET
    """Whether the Atlan tag propagates from the asset. Read by publish-app; not an Atlas typedef attribute."""

    tag_attachment_string_value: Union[str, None, UnsetType] = UNSET
    """Represents associated tag value."""

    tag_id: Union[str, None, UnsetType] = UNSET
    """Unique identifier of the tag in the source system."""

    tag_attributes: Union[List[Dict[str, Any]], None, UnsetType] = UNSET
    """Attributes associated with the tag in the source system."""

    tag_allowed_values: Union[List[str], None, UnsetType] = UNSET
    """Allowed values for the tag in the source system. These are denormalized from tagAttributes for ease of querying."""

    mapped_classification_name: Union[str, None, UnsetType] = UNSET
    """Name of the classification in Atlan that is mapped to this tag."""

    catalog_dataset_guid: Union[str, None, UnsetType] = UNSET
    """Unique identifier of the dataset this asset belongs to."""


class TagAttachmentRelationshipAttributes(AssetRelationshipAttributes):
    """TagAttachment-specific relationship attributes for nested API format."""

    input_to_airflow_tasks: Union[List[RelatedAirflowTask], None, UnsetType] = UNSET
    """Tasks to which this asset provides input."""

    output_from_airflow_tasks: Union[List[RelatedAirflowTask], None, UnsetType] = UNSET
    """Tasks from which this asset is output."""

    anomalo_checks: Union[List[RelatedAnomaloCheck], None, UnsetType] = UNSET
    """Checks that run on this asset."""

    application: Union[RelatedApplication, None, UnsetType] = UNSET
    """Application owning the Asset."""

    application_field: Union[RelatedApplicationField, None, UnsetType] = UNSET
    """ApplicationField owning the Asset."""

    context_repositories: Union[List[RelatedContextRepository], None, UnsetType] = UNSET
    """Context repositories that use this asset as input."""

    data_contract_latest: Union[RelatedDataContract, None, UnsetType] = UNSET
    """Latest version of the data contract (in any status) for this asset."""

    data_contract_latest_certified: Union[RelatedDataContract, None, UnsetType] = UNSET
    """Latest certified version of the data contract for this asset."""

    output_port_data_products: Union[List[RelatedDataProduct], None, UnsetType] = UNSET
    """Data products for which this asset is an output port."""

    input_port_data_products: Union[List[RelatedDataProduct], None, UnsetType] = UNSET
    """Data products for which this asset is an input port."""

    model_implemented_entities: Union[List[RelatedModelEntity], None, UnsetType] = UNSET
    """Entities implemented by this asset."""

    model_implemented_attributes: Union[
        List[RelatedModelAttribute], None, UnsetType
    ] = UNSET
    """Attributes implemented by this asset."""

    metrics: Union[List[RelatedMetric], None, UnsetType] = UNSET
    """"""

    dq_base_dataset_rules: Union[List[RelatedDataQualityRule], None, UnsetType] = UNSET
    """Rules that are applied on this dataset."""

    dq_reference_dataset_rules: Union[List[RelatedDataQualityRule], None, UnsetType] = (
        UNSET
    )
    """Rules where this dataset is referenced."""

    gcp_dataplex_aspect_type_metadata_entities: Union[
        List[RelatedGCPDataplexAspectType], None, UnsetType
    ] = UNSET
    """Dataplex entries (assets) that have aspects of this Aspect Type attached."""

    meanings: Union[List[RelatedAtlasGlossaryTerm], None, UnsetType] = UNSET
    """Glossary terms that are linked to this asset."""

    knowledge_linked_files: Union[List[RelatedKnowledgeFile], None, UnsetType] = UNSET
    """Knowledge files linked to this asset."""

    mc_monitors: Union[List[RelatedMCMonitor], None, UnsetType] = UNSET
    """Monitors that observe this asset."""

    mc_incidents: Union[List[RelatedMCIncident], None, UnsetType] = UNSET
    """"""

    partial_child_fields: Union[List[RelatedPartialField], None, UnsetType] = UNSET
    """Partial fields contained in the asset."""

    partial_child_objects: Union[List[RelatedPartialObject], None, UnsetType] = UNSET
    """Partial objects contained in the asset."""

    input_to_processes: Union[List[RelatedProcess], None, UnsetType] = UNSET
    """Processes to which this asset provides input."""

    output_from_processes: Union[List[RelatedProcess], None, UnsetType] = UNSET
    """Processes from which this asset is produced as output."""

    user_def_relationship_to: Union[List[RelatedReferenceable], None, UnsetType] = UNSET
    """"""

    user_def_relationship_from: Union[List[RelatedReferenceable], None, UnsetType] = (
        UNSET
    )
    """"""

    files: Union[List[RelatedFile], None, UnsetType] = UNSET
    """"""

    links: Union[List[RelatedLink], None, UnsetType] = UNSET
    """Links that are attached to this asset."""

    readme: Union[RelatedReadme, None, UnsetType] = UNSET
    """README that is linked to this asset."""

    schema_registry_subjects: Union[
        List[RelatedSchemaRegistrySubject], None, UnsetType
    ] = UNSET
    """Schema registry subjects associated with this asset."""

    soda_checks: Union[List[RelatedSodaCheck], None, UnsetType] = UNSET
    """"""

    input_to_spark_jobs: Union[List[RelatedSparkJob], None, UnsetType] = UNSET
    """"""

    output_from_spark_jobs: Union[List[RelatedSparkJob], None, UnsetType] = UNSET
    """"""


class TagAttachmentNested(AssetNested):
    """TagAttachment in nested API format for high-performance serialization."""

    attributes: Union[TagAttachmentAttributes, UnsetType] = UNSET
    relationship_attributes: Union[TagAttachmentRelationshipAttributes, UnsetType] = (
        UNSET
    )
    append_relationship_attributes: Union[
        TagAttachmentRelationshipAttributes, UnsetType
    ] = UNSET
    remove_relationship_attributes: Union[
        TagAttachmentRelationshipAttributes, UnsetType
    ] = UNSET


# =============================================================================
# CONVERSION HELPERS & CONSTANTS
# =============================================================================

_TAG_ATTACHMENT_REL_FIELDS: List[str] = [
    *_ASSET_REL_FIELDS,
    "input_to_airflow_tasks",
    "output_from_airflow_tasks",
    "anomalo_checks",
    "application",
    "application_field",
    "context_repositories",
    "data_contract_latest",
    "data_contract_latest_certified",
    "output_port_data_products",
    "input_port_data_products",
    "model_implemented_entities",
    "model_implemented_attributes",
    "metrics",
    "dq_base_dataset_rules",
    "dq_reference_dataset_rules",
    "gcp_dataplex_aspect_type_metadata_entities",
    "meanings",
    "knowledge_linked_files",
    "mc_monitors",
    "mc_incidents",
    "partial_child_fields",
    "partial_child_objects",
    "input_to_processes",
    "output_from_processes",
    "user_def_relationship_to",
    "user_def_relationship_from",
    "files",
    "links",
    "readme",
    "schema_registry_subjects",
    "soda_checks",
    "input_to_spark_jobs",
    "output_from_spark_jobs",
]


def _populate_tag_attachment_attrs(
    attrs: TagAttachmentAttributes, obj: TagAttachment
) -> None:
    """Populate TagAttachment-specific attributes on the attrs struct."""
    _populate_asset_attrs(attrs, obj)
    attrs.tag_qualified_name = obj.tag_qualified_name
    attrs.object_qualified_name = obj.object_qualified_name
    attrs.object_type_name = obj.object_type_name
    attrs.source_tag_qualified_name = obj.source_tag_qualified_name
    attrs.source_tag_display_name = obj.source_tag_display_name
    attrs.source_tag_type_name = obj.source_tag_type_name
    attrs.value_type = obj.value_type
    attrs.value = obj.value
    attrs.propagate = obj.propagate
    attrs.tag_attachment_string_value = obj.tag_attachment_string_value
    attrs.tag_id = obj.tag_id
    attrs.tag_attributes = obj.tag_attributes
    attrs.tag_allowed_values = obj.tag_allowed_values
    attrs.mapped_classification_name = obj.mapped_classification_name
    attrs.catalog_dataset_guid = obj.catalog_dataset_guid


def _extract_tag_attachment_attrs(attrs: TagAttachmentAttributes) -> dict:
    """Extract all TagAttachment attributes from the attrs struct into a flat dict."""
    result = _extract_asset_attrs(attrs)
    result["tag_qualified_name"] = attrs.tag_qualified_name
    result["object_qualified_name"] = attrs.object_qualified_name
    result["object_type_name"] = attrs.object_type_name
    result["source_tag_qualified_name"] = attrs.source_tag_qualified_name
    result["source_tag_display_name"] = attrs.source_tag_display_name
    result["source_tag_type_name"] = attrs.source_tag_type_name
    result["value_type"] = attrs.value_type
    result["value"] = attrs.value
    result["propagate"] = attrs.propagate
    result["tag_attachment_string_value"] = attrs.tag_attachment_string_value
    result["tag_id"] = attrs.tag_id
    result["tag_attributes"] = attrs.tag_attributes
    result["tag_allowed_values"] = attrs.tag_allowed_values
    result["mapped_classification_name"] = attrs.mapped_classification_name
    result["catalog_dataset_guid"] = attrs.catalog_dataset_guid
    return result


# =============================================================================
# CONVERSION FUNCTIONS
# =============================================================================


def _tag_attachment_to_nested(tag_attachment: TagAttachment) -> TagAttachmentNested:
    """Convert flat TagAttachment to nested format."""
    attrs = TagAttachmentAttributes()
    _populate_tag_attachment_attrs(attrs, tag_attachment)
    # Categorize relationships by save semantic (REPLACE, APPEND, REMOVE)
    replace_rels, append_rels, remove_rels = categorize_relationships(
        tag_attachment, _TAG_ATTACHMENT_REL_FIELDS, TagAttachmentRelationshipAttributes
    )
    return TagAttachmentNested(
        guid=tag_attachment.guid,
        type_name=tag_attachment.type_name,
        status=tag_attachment.status,
        version=tag_attachment.version,
        create_time=tag_attachment.create_time,
        update_time=tag_attachment.update_time,
        created_by=tag_attachment.created_by,
        updated_by=tag_attachment.updated_by,
        classifications=tag_attachment.classifications,
        classification_names=tag_attachment.classification_names,
        meanings=tag_attachment.meanings,
        labels=tag_attachment.labels,
        business_attributes=tag_attachment.business_attributes,
        custom_attributes=tag_attachment.custom_attributes,
        pending_tasks=tag_attachment.pending_tasks,
        proxy=tag_attachment.proxy,
        is_incomplete=tag_attachment.is_incomplete,
        provenance_type=tag_attachment.provenance_type,
        home_id=tag_attachment.home_id,
        depth=tag_attachment.depth,
        immediate_upstream=tag_attachment.immediate_upstream,
        immediate_downstream=tag_attachment.immediate_downstream,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _tag_attachment_from_nested(nested: TagAttachmentNested) -> TagAttachment:
    """Convert nested format to flat TagAttachment."""
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else TagAttachmentAttributes()
    )
    # Merge relationships from all three buckets
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        _TAG_ATTACHMENT_REL_FIELDS,
        TagAttachmentRelationshipAttributes,
    )
    # Build kwargs so a field carried by both the top level and the merged
    # relationships (e.g. `meanings`) is passed once, with the relationship
    # value winning — otherwise the constructor gets a duplicate keyword.
    kwargs = {
        "guid": nested.guid,
        "type_name": nested.type_name,
        "status": nested.status,
        "version": nested.version,
        "create_time": nested.create_time,
        "update_time": nested.update_time,
        "created_by": nested.created_by,
        "updated_by": nested.updated_by,
        "classifications": nested.classifications,
        "classification_names": nested.classification_names,
        "meanings": nested.meanings,
        "labels": nested.labels,
        "business_attributes": nested.business_attributes,
        "custom_attributes": nested.custom_attributes,
        "pending_tasks": nested.pending_tasks,
        "proxy": nested.proxy,
        "is_incomplete": nested.is_incomplete,
        "provenance_type": nested.provenance_type,
        "home_id": nested.home_id,
        "depth": nested.depth,
        "immediate_upstream": nested.immediate_upstream,
        "immediate_downstream": nested.immediate_downstream,
    }
    kwargs.update(_extract_tag_attachment_attrs(attrs))
    kwargs.update(merged_rels)
    return TagAttachment(**kwargs)


def _tag_attachment_to_nested_bytes(
    tag_attachment: TagAttachment, serde: Serde
) -> bytes:
    """Convert flat TagAttachment to nested JSON bytes."""
    return serde.encode(_tag_attachment_to_nested(tag_attachment))


def _tag_attachment_from_nested_bytes(data: bytes, serde: Serde) -> TagAttachment:
    """Convert nested JSON bytes to flat TagAttachment."""
    nested = serde.decode(data, TagAttachmentNested)
    return _tag_attachment_from_nested(nested)


# ---------------------------------------------------------------------------
# Deferred field descriptor initialization
# ---------------------------------------------------------------------------
from pyatlan.model.fields.atlan_fields import (  # noqa: E402
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
)

TagAttachment.TAG_QUALIFIED_NAME = KeywordTextField(
    "tagQualifiedName", "tagQualifiedName", "tagQualifiedName.text"
)
TagAttachment.OBJECT_QUALIFIED_NAME = KeywordField(
    "objectQualifiedName", "objectQualifiedName"
)
TagAttachment.OBJECT_TYPE_NAME = KeywordField("objectTypeName", "objectTypeName")
TagAttachment.SOURCE_TAG_QUALIFIED_NAME = KeywordField(
    "sourceTagQualifiedName", "sourceTagQualifiedName"
)
TagAttachment.SOURCE_TAG_DISPLAY_NAME = KeywordField(
    "sourceTagDisplayName", "sourceTagDisplayName"
)
TagAttachment.SOURCE_TAG_TYPE_NAME = KeywordField(
    "sourceTagTypeName", "sourceTagTypeName"
)
TagAttachment.VALUE_TYPE = KeywordField("valueType", "valueType")
TagAttachment.VALUE = KeywordField("value", "value")
TagAttachment.PROPAGATE = BooleanField("propagate", "propagate")
TagAttachment.TAG_ATTACHMENT_STRING_VALUE = KeywordTextField(
    "tagAttachmentStringValue",
    "tagAttachmentStringValue",
    "tagAttachmentStringValue.text",
)
TagAttachment.TAG_ID = KeywordField("tagId", "tagId")
TagAttachment.TAG_ATTRIBUTES = KeywordField("tagAttributes", "tagAttributes")
TagAttachment.TAG_ALLOWED_VALUES = KeywordTextField(
    "tagAllowedValues", "tagAllowedValues", "tagAllowedValues.text"
)
TagAttachment.MAPPED_CLASSIFICATION_NAME = KeywordField(
    "mappedClassificationName", "mappedClassificationName"
)
TagAttachment.CATALOG_DATASET_GUID = KeywordField(
    "catalogDatasetGuid", "catalogDatasetGuid"
)
TagAttachment.INPUT_TO_AIRFLOW_TASKS = RelationField("inputToAirflowTasks")
TagAttachment.OUTPUT_FROM_AIRFLOW_TASKS = RelationField("outputFromAirflowTasks")
TagAttachment.ANOMALO_CHECKS = RelationField("anomaloChecks")
TagAttachment.APPLICATION = RelationField("application")
TagAttachment.APPLICATION_FIELD = RelationField("applicationField")
TagAttachment.CONTEXT_REPOSITORIES = RelationField("contextRepositories")
TagAttachment.DATA_CONTRACT_LATEST = RelationField("dataContractLatest")
TagAttachment.DATA_CONTRACT_LATEST_CERTIFIED = RelationField(
    "dataContractLatestCertified"
)
TagAttachment.OUTPUT_PORT_DATA_PRODUCTS = RelationField("outputPortDataProducts")
TagAttachment.INPUT_PORT_DATA_PRODUCTS = RelationField("inputPortDataProducts")
TagAttachment.MODEL_IMPLEMENTED_ENTITIES = RelationField("modelImplementedEntities")
TagAttachment.MODEL_IMPLEMENTED_ATTRIBUTES = RelationField("modelImplementedAttributes")
TagAttachment.METRICS = RelationField("metrics")
TagAttachment.DQ_BASE_DATASET_RULES = RelationField("dqBaseDatasetRules")
TagAttachment.DQ_REFERENCE_DATASET_RULES = RelationField("dqReferenceDatasetRules")
TagAttachment.GCP_DATAPLEX_ASPECT_TYPE_METADATA_ENTITIES = RelationField(
    "gcpDataplexAspectTypeMetadataEntities"
)
TagAttachment.MEANINGS = RelationField("meanings")
TagAttachment.KNOWLEDGE_LINKED_FILES = RelationField("knowledgeLinkedFiles")
TagAttachment.MC_MONITORS = RelationField("mcMonitors")
TagAttachment.MC_INCIDENTS = RelationField("mcIncidents")
TagAttachment.PARTIAL_CHILD_FIELDS = RelationField("partialChildFields")
TagAttachment.PARTIAL_CHILD_OBJECTS = RelationField("partialChildObjects")
TagAttachment.INPUT_TO_PROCESSES = RelationField("inputToProcesses")
TagAttachment.OUTPUT_FROM_PROCESSES = RelationField("outputFromProcesses")
TagAttachment.USER_DEF_RELATIONSHIP_TO = RelationField("userDefRelationshipTo")
TagAttachment.USER_DEF_RELATIONSHIP_FROM = RelationField("userDefRelationshipFrom")
TagAttachment.FILES = RelationField("files")
TagAttachment.LINKS = RelationField("links")
TagAttachment.README = RelationField("readme")
TagAttachment.SCHEMA_REGISTRY_SUBJECTS = RelationField("schemaRegistrySubjects")
TagAttachment.SODA_CHECKS = RelationField("sodaChecks")
TagAttachment.INPUT_TO_SPARK_JOBS = RelationField("inputToSparkJobs")
TagAttachment.OUTPUT_FROM_SPARK_JOBS = RelationField("outputFromSparkJobs")
