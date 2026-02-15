# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""SupersetChart asset model with flattened inheritance."""

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
from .superset_related import RelatedSupersetDashboard


@register_asset
class SupersetChart(Superset):
    """Instance of a Superset chart in Atlan."""

    type_name: Union[str, UnsetType] = "SupersetChart"

    superset_chart_description_markdown: Union[str, None, UnsetType] = UNSET
    superset_chart_form_data: Union[dict[str, str], None, UnsetType] = UNSET

    superset_dashboard: Union[RelatedSupersetDashboard, None, UnsetType] = UNSET

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: Union[str, None] = None,
    ) -> "SupersetChart":
        """Create a new SupersetChart asset."""
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
    def updater(cls, *, qualified_name: str, name: str) -> "SupersetChart":
        """Create a SupersetChart instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "SupersetChart":
        """Return only fields required for update operations."""
        return SupersetChart.updater(qualified_name=self.qualified_name, name=self.name)

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Convert to JSON string."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _superset_chart_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "SupersetChart":
        """Create from JSON string or bytes."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _superset_chart_from_nested_bytes(json_data, serde)


class SupersetChartAttributes(BIAttributes):
    """SupersetChart-specific attributes for nested API format."""

    superset_dashboard_id: Union[int, None, UnsetType] = UNSET
    superset_dashboard_qualified_name: Union[str, None, UnsetType] = UNSET

    superset_chart_description_markdown: Union[str, None, UnsetType] = UNSET
    superset_chart_form_data: Union[dict[str, str], None, UnsetType] = UNSET


class SupersetChartRelationshipAttributes(BIRelationshipAttributes):
    """SupersetChart-specific relationship attributes for nested API format."""

    superset_dashboard: Union[RelatedSupersetDashboard, None, UnsetType] = UNSET


class SupersetChartNested(BINested):
    """SupersetChart in nested API format for high-performance serialization."""

    attributes: Union[SupersetChartAttributes, UnsetType] = UNSET
    relationship_attributes: Union[SupersetChartRelationshipAttributes, UnsetType] = (
        UNSET
    )
    append_relationship_attributes: Union[
        SupersetChartRelationshipAttributes, UnsetType
    ] = UNSET
    remove_relationship_attributes: Union[
        SupersetChartRelationshipAttributes, UnsetType
    ] = UNSET


def _superset_chart_to_nested(superset_chart: SupersetChart) -> SupersetChartNested:
    """Convert flat SupersetChart to nested format."""
    attrs_kwargs = build_attributes_kwargs(superset_chart, SupersetChartAttributes)
    attrs = SupersetChartAttributes(**attrs_kwargs)
    rel_fields: list[str] = ["superset_dashboard"]
    replace_rels, append_rels, remove_rels = categorize_relationships(
        superset_chart, rel_fields, SupersetChartRelationshipAttributes
    )
    return SupersetChartNested(
        guid=superset_chart.guid,
        type_name=superset_chart.type_name,
        status=superset_chart.status,
        version=superset_chart.version,
        create_time=superset_chart.create_time,
        update_time=superset_chart.update_time,
        created_by=superset_chart.created_by,
        updated_by=superset_chart.updated_by,
        classifications=superset_chart.classifications,
        classification_names=superset_chart.classification_names,
        meanings=superset_chart.meanings,
        labels=superset_chart.labels,
        business_attributes=superset_chart.business_attributes,
        custom_attributes=superset_chart.custom_attributes,
        pending_tasks=superset_chart.pending_tasks,
        proxy=superset_chart.proxy,
        is_incomplete=superset_chart.is_incomplete,
        provenance_type=superset_chart.provenance_type,
        home_id=superset_chart.home_id,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _superset_chart_from_nested(nested: SupersetChartNested) -> SupersetChart:
    """Convert nested format to flat SupersetChart."""
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else SupersetChartAttributes()
    )
    rel_fields: list[str] = ["superset_dashboard"]
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        rel_fields,
        SupersetChartRelationshipAttributes,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, BINested, SupersetChartAttributes
    )
    return SupersetChart(**kwargs)


def _superset_chart_to_nested_bytes(
    superset_chart: SupersetChart, serde: Serde
) -> bytes:
    """Convert flat SupersetChart to nested JSON bytes."""
    return serde.encode(_superset_chart_to_nested(superset_chart))


def _superset_chart_from_nested_bytes(data: bytes, serde: Serde) -> SupersetChart:
    """Convert nested JSON bytes to flat SupersetChart."""
    nested = serde.decode(data, SupersetChartNested)
    return _superset_chart_from_nested(nested)
