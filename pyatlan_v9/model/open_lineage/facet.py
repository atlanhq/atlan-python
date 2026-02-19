# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Dict, List, Optional, Union

import msgspec

from pyatlan_v9.model.open_lineage.base import OpenLineageBaseFacet


class OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields(
    msgspec.Struct, kw_only=True, omit_defaults=True
):
    namespace: Union[str, None] = None
    name: Union[str, None] = None
    field: Union[str, None] = None


class OpenLineageColumnLineageDatasetFacetFieldsAdditional(
    msgspec.Struct, kw_only=True, omit_defaults=True
):
    input_fields: Union[
        List[OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields], None
    ] = msgspec.field(default=None, name="inputFields")
    transformation_description: Union[str, None] = msgspec.field(
        default=None, name="transformationDescription"
    )
    transformation_type: Union[str, None] = msgspec.field(
        default=None, name="transformationType"
    )


class OpenLineageDatasetFacet(OpenLineageBaseFacet):
    """A Dataset Facet"""

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/DatasetFacet"


class OpenLineageJobFacet(OpenLineageBaseFacet):
    """A Job Facet"""

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/JobFacet"


class OpenLineageColumnLineageDatasetFacet(OpenLineageBaseFacet):
    """
    This facet contains column lineage of a dataset.
    """

    fields: Dict[str, OpenLineageColumnLineageDatasetFacetFieldsAdditional] = (
        msgspec.field(default_factory=dict)
    )

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/facets/1-1-0/ColumnLineageDatasetFacet.json#/$defs/ColumnLineageDatasetFacet"


class OpenLineageDatasetFacets(msgspec.Struct, kw_only=True, omit_defaults=True):
    """A Dataset Facets"""

    column_lineage: Union[OpenLineageColumnLineageDatasetFacet, None] = msgspec.field(
        default=None, name="columnLineage"
    )
