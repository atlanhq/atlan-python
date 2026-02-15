# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Related type classes for Superset module.

This module contains all Related{Type} classes for the Superset type hierarchy.
These classes are used for relationship attributes to reference related entities.
"""

from __future__ import annotations

from typing import Union

from msgspec import UNSET, UnsetType

from .catalog_related import RelatedBI
from .referenceable_related import RelatedReferenceable

__all__ = [
    "RelatedSuperset",
    "RelatedSupersetChart",
    "RelatedSupersetDashboard",
    "RelatedSupersetDataset",
]


class RelatedSuperset(RelatedBI):
    """
    Related entity reference for Superset assets.

    Extends RelatedBI with Superset-specific attributes.
    """

    # type_name inherited from parent with default=UNSET
    # __post_init__ sets it to "Superset" so it serializes correctly

    superset_dashboard_id: Union[int, None, UnsetType] = UNSET
    """Identifier of the dashboard in which this asset exists, in Superset."""

    superset_dashboard_qualified_name: Union[str, None, UnsetType] = UNSET
    """Unique name of the dashboard in which this asset exists."""

    def __post_init__(self) -> None:
        RelatedReferenceable.__post_init__(self)
        self.type_name = "Superset"


class RelatedSupersetChart(RelatedSuperset):
    """
    Related entity reference for SupersetChart assets.

    Extends RelatedSuperset with SupersetChart-specific attributes.
    """

    # type_name inherited from parent with default=UNSET
    # __post_init__ sets it to "SupersetChart" so it serializes correctly

    superset_chart_description_markdown: Union[str, None, UnsetType] = UNSET
    """Description markdown of the chart."""

    superset_chart_form_data: Union[dict[str, str], None, UnsetType] = UNSET
    """Data stored for the chart in key value pairs."""

    def __post_init__(self) -> None:
        RelatedReferenceable.__post_init__(self)
        self.type_name = "SupersetChart"


class RelatedSupersetDashboard(RelatedSuperset):
    """
    Related entity reference for SupersetDashboard assets.

    Extends RelatedSuperset with SupersetDashboard-specific attributes.
    """

    # type_name inherited from parent with default=UNSET
    # __post_init__ sets it to "SupersetDashboard" so it serializes correctly

    superset_dashboard_changed_by_name: Union[str, None, UnsetType] = UNSET
    """Name of the user who changed the dashboard."""

    superset_dashboard_changed_by_url: Union[str, None, UnsetType] = UNSET
    """URL of the user profile that changed the dashboard."""

    superset_dashboard_is_managed_externally: Union[bool, None, UnsetType] = UNSET
    """Whether the dashboard is managed externally (true) or not (false)."""

    superset_dashboard_is_published: Union[bool, None, UnsetType] = UNSET
    """Whether the dashboard is published (true) or not (false)."""

    superset_dashboard_thumbnail_url: Union[str, None, UnsetType] = UNSET
    """URL for the dashboard thumbnail image in superset."""

    superset_dashboard_chart_count: Union[int, None, UnsetType] = UNSET
    """Count of charts present in the dashboard."""

    def __post_init__(self) -> None:
        RelatedReferenceable.__post_init__(self)
        self.type_name = "SupersetDashboard"


class RelatedSupersetDataset(RelatedSuperset):
    """
    Related entity reference for SupersetDataset assets.

    Extends RelatedSuperset with SupersetDataset-specific attributes.
    """

    # type_name inherited from parent with default=UNSET
    # __post_init__ sets it to "SupersetDataset" so it serializes correctly

    superset_dataset_datasource_name: Union[str, None, UnsetType] = UNSET
    """Name of the datasource for the dataset."""

    superset_dataset_id: Union[int, None, UnsetType] = UNSET
    """Id of the dataset in superset."""

    superset_dataset_type: Union[str, None, UnsetType] = UNSET
    """Type of the dataset in superset."""

    def __post_init__(self) -> None:
        RelatedReferenceable.__post_init__(self)
        self.type_name = "SupersetDataset"
