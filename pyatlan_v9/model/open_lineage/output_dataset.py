# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, List, Union

import msgspec

from pyatlan_v9.model.open_lineage.dataset import OpenLineageDataset
from pyatlan_v9.model.open_lineage.facet import (
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

    output_facets: Union[Dict[str, Any], None] = msgspec.field(
        default_factory=dict, name="outputFacets"
    )

    # NOTE: to_fields is excluded from serialization; it's used
    # to build column lineage facets before serialization.
    to_fields: Union[
        List[
            Dict[
                str,
                List[
                    OpenLineageColumnLineageDatasetFacetFieldsAdditionalInputFields
                ],
            ]
        ],
        None,
    ] = msgspec.field(default_factory=list)

    # NOTE: producer is excluded from serialization
    producer: Union[str, None] = None

    @staticmethod
    def _get_schema() -> str:
        return (
            "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/OutputDataset"
        )

    @classmethod
    def creator(
        cls, namespace: str, asset_name: str, producer: str
    ) -> OpenLineageOutputDataset:
        """
        Builds the minimal object necessary to create
        an OpenLineage dataset use-able as a lineage target.

        :param namespace: name of the source of the asset
        :param asset_name: name of the asset, by OpenLineage standard
        :param producer: a pre-configured OpenLineage producer
        :returns: the minimal request necessary to create the output dataset
        """
        return OpenLineageOutputDataset(
            namespace=namespace, name=asset_name, producer=producer
        )

    def _build_facets(self) -> Dict[str, Any]:
        """
        Transform to_fields into facets dict for serialization.
        Returns a facets dict with column lineage if to_fields is populated.
        """
        column_lineage_data: Dict[
            str, OpenLineageColumnLineageDatasetFacetFieldsAdditional
        ] = {}
        producer = self.producer or ""

        if self.to_fields:
            for entry in self.to_fields:
                for key, value in entry.items():
                    fields_additional = (
                        OpenLineageColumnLineageDatasetFacetFieldsAdditional(
                            input_fields=value
                        )
                    )
                    column_lineage_data[key] = fields_additional

        if column_lineage_data:
            dataset_facets = OpenLineageDatasetFacets(
                column_lineage=OpenLineageColumnLineageDatasetFacet(
                    fields=column_lineage_data,
                    producer=producer,
                )
            )
            return msgspec.to_builtins(dataset_facets)
        return self.facets or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this output dataset to a dictionary, applying
        the to_fields → facets transformation.
        """
        facets = self._build_facets()
        result: Dict[str, Any] = {}
        if self.namespace is not None:
            result["namespace"] = self.namespace
        if self.name is not None:
            result["name"] = self.name
        # Always include facets (even when empty) — matches legacy behaviour
        if facets is not None:
            result["facets"] = facets
        if self.output_facets:
            result["outputFacets"] = self.output_facets
        return result
