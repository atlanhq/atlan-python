from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.open_lineage.dataset import OpenLineageDataset
from pyatlan.model.open_lineage.facet import (
    OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields,
)


class OpenLineageInputDataset(OpenLineageDataset):

    facets: Optional[Dict[str, Any]] = Field(default_factory=dict)
    input_facets: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/InputDataset"

    @classmethod
    def creator(cls, namespace: str, asset_name: str) -> OpenLineageInputDataset:
        return OpenLineageInputDataset(namespace=namespace, name=asset_name, facets={})

    def from_field(
        self, field_name: str
    ) -> OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields:
        return OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields(
            namespace=self.namespace, name=self.name, field=field_name
        )
