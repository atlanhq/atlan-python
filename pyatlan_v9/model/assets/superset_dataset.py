# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""SupersetDataset asset model with flattened inheritance."""

from __future__ import annotations

from typing import Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.model.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    categorize_relationships,
    merge_relationships,
)
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .bi import BIAttributes, BINested, BIRelationshipAttributes
from .superset import Superset
from .superset_related import RelatedSupersetDashboard


@register_asset
class SupersetDataset(Superset):
    """Instance of a Superset dataset in Atlan."""

    type_name: Union[str, UnsetType] = "SupersetDataset"

    superset_dataset_datasource_name: Union[str, None, UnsetType] = UNSET
    superset_dataset_id: Union[int, None, UnsetType] = UNSET
    superset_dataset_type: Union[str, None, UnsetType] = UNSET

    superset_dashboard: Union[RelatedSupersetDashboard, None, UnsetType] = UNSET

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SupersetDataset":
        """Create a new SupersetDataset asset."""
        validate_required_fields(
            ["name", "superset_dashboard_qualified_name"],
            [name, superset_dashboard_qualified_name],
        )
        if connection_qualified_name:
            fields = connection_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
        else:
            fields = superset_dashboard_qualified_name.split("/")
            connector_name = fields[1] if len(fields) > 1 else None
            connection_qualified_name = (
                "/".join(fields[:3])
                if len(fields) >= 3
                else superset_dashboard_qualified_name
            )
        return cls(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
            qualified_name=f"{superset_dashboard_qualified_name}/{name}",
            connector_name=connector_name,
            superset_dashboard=RelatedSupersetDashboard(
                unique_attributes={"qualifiedName": superset_dashboard_qualified_name}
            ),
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SupersetDataset":
        """Create a SupersetDataset instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SupersetDataset":
        """Return only fields required for update operations."""
        return SupersetDataset.updater(
            qualified_name=self.qualified_name, name=self.name
        )

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Convert to JSON string."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _superset_dataset_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "SupersetDataset":
        """Create from JSON string or bytes."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _superset_dataset_from_nested_bytes(json_data, serde)


class SupersetDatasetAttributes(BIAttributes):
    """SupersetDataset-specific attributes for nested API format."""

    superset_dashboard_id: Union[int, None, UnsetType] = UNSET
    superset_dashboard_qualified_name: Union[str, None, UnsetType] = UNSET

    superset_dataset_datasource_name: Union[str, None, UnsetType] = UNSET
    superset_dataset_id: Union[int, None, UnsetType] = UNSET
    superset_dataset_type: Union[str, None, UnsetType] = UNSET


class SupersetDatasetRelationshipAttributes(BIRelationshipAttributes):
    """SupersetDataset-specific relationship attributes for nested API format."""

    superset_dashboard: Union[RelatedSupersetDashboard, None, UnsetType] = UNSET


class SupersetDatasetNested(BINested):
    """SupersetDataset in nested API format for high-performance serialization."""

    attributes: Union[SupersetDatasetAttributes, UnsetType] = UNSET
    relationship_attributes: Union[SupersetDatasetRelationshipAttributes, UnsetType] = (
        UNSET
    )
    append_relationship_attributes: Union[
        SupersetDatasetRelationshipAttributes, UnsetType
    ] = UNSET
    remove_relationship_attributes: Union[
        SupersetDatasetRelationshipAttributes, UnsetType
    ] = UNSET


def _superset_dataset_to_nested(
    superset_dataset: SupersetDataset,
) -> SupersetDatasetNested:
    """Convert flat SupersetDataset to nested format."""
    attrs_kwargs = build_attributes_kwargs(superset_dataset, SupersetDatasetAttributes)
    attrs = SupersetDatasetAttributes(**attrs_kwargs)
    rel_fields: list[str] = ["superset_dashboard"]
    replace_rels, append_rels, remove_rels = categorize_relationships(
        superset_dataset, rel_fields, SupersetDatasetRelationshipAttributes
    )
    return SupersetDatasetNested(
        guid=superset_dataset.guid,
        type_name=superset_dataset.type_name,
        status=superset_dataset.status,
        version=superset_dataset.version,
        create_time=superset_dataset.create_time,
        update_time=superset_dataset.update_time,
        created_by=superset_dataset.created_by,
        updated_by=superset_dataset.updated_by,
        classifications=superset_dataset.classifications,
        classification_names=superset_dataset.classification_names,
        meanings=superset_dataset.meanings,
        labels=superset_dataset.labels,
        business_attributes=superset_dataset.business_attributes,
        custom_attributes=superset_dataset.custom_attributes,
        pending_tasks=superset_dataset.pending_tasks,
        proxy=superset_dataset.proxy,
        is_incomplete=superset_dataset.is_incomplete,
        provenance_type=superset_dataset.provenance_type,
        home_id=superset_dataset.home_id,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _superset_dataset_from_nested(nested: SupersetDatasetNested) -> SupersetDataset:
    """Convert nested format to flat SupersetDataset."""
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else SupersetDatasetAttributes()
    )
    rel_fields: list[str] = ["superset_dashboard"]
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        rel_fields,
        SupersetDatasetRelationshipAttributes,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, BINested, SupersetDatasetAttributes
    )
    return SupersetDataset(**kwargs)


def _superset_dataset_to_nested_bytes(
    superset_dataset: SupersetDataset, serde: Serde
) -> bytes:
    """Convert flat SupersetDataset to nested JSON bytes."""
    return serde.encode(_superset_dataset_to_nested(superset_dataset))


def _superset_dataset_from_nested_bytes(data: bytes, serde: Serde) -> SupersetDataset:
    """Convert nested JSON bytes to flat SupersetDataset."""
    nested = serde.decode(data, SupersetDatasetNested)
    return _superset_dataset_from_nested(nested)
