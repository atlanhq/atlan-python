from __future__ import annotations

from typing import Dict, List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.open_lineage.base import OpenLineageBaseFacet


class OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields(AtlanObject):
    namespace: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    field: Optional[str] = Field(default=None)


class OpenLineageColumnLineageDatasetFacetFieldsAdditional(AtlanObject):
    input_fields: Optional[
        List[OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields]
    ] = Field(default_factory=list)
    transformation_description: Optional[str] = Field(default=None)
    transformation_type: Optional[str] = Field(default=None)


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

    fields: Dict[str, OpenLineageColumnLineageDatasetFacetFieldsAdditional] = Field(
        default_factory=dict
    )

    @staticmethod
    def _get_schema() -> str:
        return (
            "https://openlineage.io/spec/facets/1-1-0/"
            "ColumnLineageDatasetFacet.json#/$defs/ColumnLineageDatasetFacet"
        )


class OpenLineageDatasetFacets(AtlanObject):
    """A Dataset Facets"""

    column_lineage: Optional[OpenLineageColumnLineageDatasetFacet] = Field(default=None)
