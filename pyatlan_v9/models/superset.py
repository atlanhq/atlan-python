# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Superset asset model with flattened inheritance."""

from __future__ import annotations

from typing import Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    categorize_relationships,
    merge_relationships,
)
from pyatlan_v9.serde import Serde, get_serde
from pyatlan_v9.transform import register_asset

from .bi import BI, BIAttributes, BINested, BIRelationshipAttributes


@register_asset
class Superset(BI):
    """Base class for Superset assets."""

    type_name: Union[str, UnsetType] = "Superset"

    superset_dashboard_id: Union[int, None, UnsetType] = UNSET
    """Identifier of the dashboard in Superset."""

    superset_dashboard_qualified_name: Union[str, None, UnsetType] = UNSET
    """Unique name of the dashboard in which this asset exists."""

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Convert to JSON string."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _superset_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "Superset":
        """Create from JSON string or bytes."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _superset_from_nested_bytes(json_data, serde)


class SupersetAttributes(BIAttributes):
    """Superset-specific attributes for nested API format."""

    superset_dashboard_id: Union[int, None, UnsetType] = UNSET
    superset_dashboard_qualified_name: Union[str, None, UnsetType] = UNSET


class SupersetRelationshipAttributes(BIRelationshipAttributes):
    """Superset-specific relationship attributes for nested API format."""

    pass


class SupersetNested(BINested):
    """Superset in nested API format for high-performance serialization."""

    attributes: Union[SupersetAttributes, UnsetType] = UNSET
    relationship_attributes: Union[SupersetRelationshipAttributes, UnsetType] = UNSET
    append_relationship_attributes: Union[SupersetRelationshipAttributes, UnsetType] = (
        UNSET
    )
    remove_relationship_attributes: Union[SupersetRelationshipAttributes, UnsetType] = (
        UNSET
    )


def _superset_to_nested(superset: Superset) -> SupersetNested:
    """Convert flat Superset to nested format."""
    attrs_kwargs = build_attributes_kwargs(superset, SupersetAttributes)
    attrs = SupersetAttributes(**attrs_kwargs)
    rel_fields: list[str] = []
    replace_rels, append_rels, remove_rels = categorize_relationships(
        superset, rel_fields, SupersetRelationshipAttributes
    )
    return SupersetNested(
        guid=superset.guid,
        type_name=superset.type_name,
        status=superset.status,
        version=superset.version,
        create_time=superset.create_time,
        update_time=superset.update_time,
        created_by=superset.created_by,
        updated_by=superset.updated_by,
        classifications=superset.classifications,
        classification_names=superset.classification_names,
        meanings=superset.meanings,
        labels=superset.labels,
        business_attributes=superset.business_attributes,
        custom_attributes=superset.custom_attributes,
        pending_tasks=superset.pending_tasks,
        proxy=superset.proxy,
        is_incomplete=superset.is_incomplete,
        provenance_type=superset.provenance_type,
        home_id=superset.home_id,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _superset_from_nested(nested: SupersetNested) -> Superset:
    """Convert nested format to flat Superset."""
    attrs = (
        nested.attributes if nested.attributes is not UNSET else SupersetAttributes()
    )
    rel_fields: list[str] = []
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        rel_fields,
        SupersetRelationshipAttributes,
    )
    kwargs = build_flat_kwargs(nested, attrs, merged_rels, BINested, SupersetAttributes)
    return Superset(**kwargs)


def _superset_to_nested_bytes(superset: Superset, serde: Serde) -> bytes:
    """Convert flat Superset to nested JSON bytes."""
    return serde.encode(_superset_to_nested(superset))


def _superset_from_nested_bytes(data: bytes, serde: Serde) -> Superset:
    """Convert nested JSON bytes to flat Superset."""
    nested = serde.decode(data, SupersetNested)
    return _superset_from_nested(nested)
