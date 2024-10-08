from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.open_lineage.dataset import OpenLineageDataset
from pyatlan.model.open_lineage.facet import (
    OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields,
)


class OpenLineageInputDataset(OpenLineageDataset):
    """
    Model for handling OpenLineage datasets
    to be used as lineage sources (inputs).
    """

    facets: Optional[Dict[str, Any]] = Field(default_factory=dict)
    input_facets: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/InputDataset"

    @classmethod
    def creator(cls, namespace: str, asset_name: str) -> OpenLineageInputDataset:
        """
        Builds the minimal object necessary to create an OpenLineage dataset use-able as a lineage source.

        :param namespace: name of the source of the asset
        (see: https://github.com/OpenLineage/OpenLineage/blob/main/spec/Naming.md)
        :param asset_name: name of the asset, by OpenLineage standard (for eg: `DB.SCHEMA.TABLE`)
        :returns: the minimal request necessary to create the job
        """
        return OpenLineageInputDataset(namespace=namespace, name=asset_name, facets={})

    def from_field(
        self, field_name: str
    ) -> OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields:
        """
        Create a new reference to a field within this input dataset.

        :param field_name: name of the field within the input dataset to reference
        :returns: a reference to the field within this input dataset
        """
        return OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields(
            namespace=self.namespace, name=self.name, field=field_name
        )
