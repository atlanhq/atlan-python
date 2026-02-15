# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""SupersetDashboard asset model with flattened inheritance."""

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
from pyatlan_v9.utils import init_guid, validate_required_fields

from .bi import BIAttributes, BINested, BIRelationshipAttributes
from .superset import Superset
from .superset_related import RelatedSupersetChart, RelatedSupersetDataset


@register_asset
class SupersetDashboard(Superset):
    """Instance of a Superset dashboard in Atlan."""

    type_name: Union[str, UnsetType] = "SupersetDashboard"

    superset_dashboard_changed_by_name: Union[str, None, UnsetType] = UNSET
    superset_dashboard_changed_by_url: Union[str, None, UnsetType] = UNSET
    superset_dashboard_is_managed_externally: Union[bool, None, UnsetType] = UNSET
    superset_dashboard_is_published: Union[bool, None, UnsetType] = UNSET
    superset_dashboard_thumbnail_url: Union[str, None, UnsetType] = UNSET
    superset_dashboard_chart_count: Union[int, None, UnsetType] = UNSET

    superset_datasets: Union[list[RelatedSupersetDataset], None, UnsetType] = UNSET
    superset_charts: Union[list[RelatedSupersetChart], None, UnsetType] = UNSET

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, connection_qualified_name: str
    ) -> "SupersetDashboard":
        """Create a new SupersetDashboard asset."""
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "SupersetDashboard":
        """Create a SupersetDashboard instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SupersetDashboard":
        """Return only fields required for update operations."""
        return SupersetDashboard.updater(
            qualified_name=self.qualified_name, name=self.name
        )

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Convert to JSON string."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _superset_dashboard_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "SupersetDashboard":
        """Create from JSON string or bytes."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _superset_dashboard_from_nested_bytes(json_data, serde)


class SupersetDashboardAttributes(BIAttributes):
    """SupersetDashboard-specific attributes for nested API format."""

    superset_dashboard_id: Union[int, None, UnsetType] = UNSET
    superset_dashboard_qualified_name: Union[str, None, UnsetType] = UNSET

    superset_dashboard_changed_by_name: Union[str, None, UnsetType] = UNSET
    superset_dashboard_changed_by_url: Union[str, None, UnsetType] = UNSET
    superset_dashboard_is_managed_externally: Union[bool, None, UnsetType] = UNSET
    superset_dashboard_is_published: Union[bool, None, UnsetType] = UNSET
    superset_dashboard_thumbnail_url: Union[str, None, UnsetType] = UNSET
    superset_dashboard_chart_count: Union[int, None, UnsetType] = UNSET


class SupersetDashboardRelationshipAttributes(BIRelationshipAttributes):
    """SupersetDashboard-specific relationship attributes for nested API format."""

    superset_datasets: Union[list[RelatedSupersetDataset], None, UnsetType] = UNSET
    superset_charts: Union[list[RelatedSupersetChart], None, UnsetType] = UNSET


class SupersetDashboardNested(BINested):
    """SupersetDashboard in nested API format for high-performance serialization."""

    attributes: Union[SupersetDashboardAttributes, UnsetType] = UNSET
    relationship_attributes: Union[
        SupersetDashboardRelationshipAttributes, UnsetType
    ] = UNSET
    append_relationship_attributes: Union[
        SupersetDashboardRelationshipAttributes, UnsetType
    ] = UNSET
    remove_relationship_attributes: Union[
        SupersetDashboardRelationshipAttributes, UnsetType
    ] = UNSET


def _superset_dashboard_to_nested(
    superset_dashboard: SupersetDashboard,
) -> SupersetDashboardNested:
    """Convert flat SupersetDashboard to nested format."""
    attrs_kwargs = build_attributes_kwargs(
        superset_dashboard, SupersetDashboardAttributes
    )
    attrs = SupersetDashboardAttributes(**attrs_kwargs)
    rel_fields: list[str] = ["superset_datasets", "superset_charts"]
    replace_rels, append_rels, remove_rels = categorize_relationships(
        superset_dashboard, rel_fields, SupersetDashboardRelationshipAttributes
    )
    return SupersetDashboardNested(
        guid=superset_dashboard.guid,
        type_name=superset_dashboard.type_name,
        status=superset_dashboard.status,
        version=superset_dashboard.version,
        create_time=superset_dashboard.create_time,
        update_time=superset_dashboard.update_time,
        created_by=superset_dashboard.created_by,
        updated_by=superset_dashboard.updated_by,
        classifications=superset_dashboard.classifications,
        classification_names=superset_dashboard.classification_names,
        meanings=superset_dashboard.meanings,
        labels=superset_dashboard.labels,
        business_attributes=superset_dashboard.business_attributes,
        custom_attributes=superset_dashboard.custom_attributes,
        pending_tasks=superset_dashboard.pending_tasks,
        proxy=superset_dashboard.proxy,
        is_incomplete=superset_dashboard.is_incomplete,
        provenance_type=superset_dashboard.provenance_type,
        home_id=superset_dashboard.home_id,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _superset_dashboard_from_nested(
    nested: SupersetDashboardNested,
) -> SupersetDashboard:
    """Convert nested format to flat SupersetDashboard."""
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else SupersetDashboardAttributes()
    )
    rel_fields: list[str] = ["superset_datasets", "superset_charts"]
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        rel_fields,
        SupersetDashboardRelationshipAttributes,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, BINested, SupersetDashboardAttributes
    )
    return SupersetDashboard(**kwargs)


def _superset_dashboard_to_nested_bytes(
    superset_dashboard: SupersetDashboard, serde: Serde
) -> bytes:
    """Convert flat SupersetDashboard to nested JSON bytes."""
    return serde.encode(_superset_dashboard_to_nested(superset_dashboard))


def _superset_dashboard_from_nested_bytes(
    data: bytes, serde: Serde
) -> SupersetDashboard:
    """Convert nested JSON bytes to flat SupersetDashboard."""
    nested = serde.decode(data, SupersetDashboardNested)
    return _superset_dashboard_from_nested(nested)
