from __future__ import annotations

from typing import Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.open_lineage.facet import OpenLineageDatasetFacet


class OpenLineageDataset(AtlanObject):
    """
    Model for handling OpenLineage datasets.
    """

    name: Optional[str] = Field(
        default=None, description="Unique name for that dataset within that namespace."
    )
    namespace: Optional[str] = Field(
        default=None,
        description="Namespace containing that dataset.",
    )
    facets: Optional[Dict[str, OpenLineageDatasetFacet]] = Field(
        default_factory=dict,
        description="Facets for this dataset",
    )

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/Job"
