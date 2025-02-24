from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic.v1 import Field, root_validator

from pyatlan.model.open_lineage.dataset import OpenLineageDataset
from pyatlan.model.open_lineage.facet import (
    OpenLineageColumnLineageDatasetFacet,
    OpenLineageColumnLineageDatasetFacetFieldsAdditional,
    OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields,
    OpenLineageDatasetFacets,
)


class OpenLineageOutputDataset(OpenLineageDataset):
    """
    Model for handling OpenLineage datasets
    to be used as lineage targets (outputs).
    """

    output_facets: Optional[Dict[str, Any]] = Field(default_factory=dict)
    to_fields: Optional[
        List[
            Dict[
                str,
                List[OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields],
            ]
        ]
    ] = Field(default_factory=list, exclude=True)
    # NOTE: Added to follow a similar pattern used in the Atlan Java SDK
    # This field is excluded from serialization
    producer: Optional[str] = Field(default=None, exclude=True)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/OutputDataset"

    @classmethod
    def creator(
        cls, namespace: str, asset_name: str, producer: str
    ) -> OpenLineageOutputDataset:
        """
        Builds the minimal object necessary to create
        an OpenLineage dataset use-able as a lineage target.

        :param namespace: name of the source of the asset
        (see: https://github.com/OpenLineage/OpenLineage/blob/main/spec/Naming.md)
        :param asset_name: name of the asset, by OpenLineage standard (for eg: `DB.SCHEMA.TABLE`)
        :param producer: a pre-configured OpenLineage producer
        :returns: the minimal request necessary to create the output dataset
        """

        return OpenLineageOutputDataset(
            namespace=namespace, name=asset_name, producer=producer
        )

    @root_validator(pre=True)
    def transform_to_fields_into_facets(cls, values: dict) -> dict:
        """
        Custom logic to transform to_fields into facets.
        This validator will modify facets based on to_fields before validation.
        """
        column_lineage_data = {}
        producer = values.get("producer", "")
        values["facets"] = values.get("facets", {})
        to_fields = values.get("to_fields", [])

        for entry in to_fields:
            for key, value in entry.items():
                # Build the OpenLineageColumnLineageDatasetFacet with input_fields
                fields_additional = (
                    OpenLineageColumnLineageDatasetFacetFieldsAdditional(
                        input_fields=value
                    )
                )
                # Add to the column lineage dict
                column_lineage_data[key] = fields_additional

        #  TODO: Below code will clobber any pre-existing facets
        if column_lineage_data:
            values["facets"] = OpenLineageDatasetFacets(
                column_lineage=OpenLineageColumnLineageDatasetFacet(
                    fields=column_lineage_data,
                    producer=producer,  # type:ignore[call-arg]
                )
            ).dict(exclude_unset=True, by_alias=True)

        return values
