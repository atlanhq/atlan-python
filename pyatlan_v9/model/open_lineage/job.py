# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, Union

import msgspec

from pyatlan_v9.model.open_lineage.facet import OpenLineageJobFacet
from pyatlan_v9.model.open_lineage.input_dataset import OpenLineageInputDataset
from pyatlan_v9.model.open_lineage.output_dataset import OpenLineageOutputDataset


class OpenLineageJob(msgspec.Struct, kw_only=True, omit_defaults=True):
    """
    Atlan wrapper for abstracting OpenLineage jobs.

    A job is a process that consumes or produces datasets.
    This is abstract, and can map to different things in different operational contexts.
    For example, a job could be a task in a workflow orchestration system.
    It could also be a model, a query, or a checkpoint. Depending on the
    system under observation, a Job can represent a small or large amount of work.

    For more details
    https://openlineage.io/docs/spec/object-model#job
    """

    name: Union[str, None] = None
    """Unique name for that job within that namespace."""

    namespace: Union[str, None] = None
    """Namespace containing that job."""

    facets: Union[Dict[str, OpenLineageJobFacet], None] = msgspec.field(
        default_factory=dict
    )
    """Job facets."""

    # NOTE: Added to follow a similar pattern used in the Atlan Java SDK
    # This field is excluded from serialization
    producer: Union[str, None] = None

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/Job"

    @classmethod
    def creator(
        cls, connection_name: str, job_name: str, producer: str
    ) -> OpenLineageJob:
        """
        Builds the minimal object necessary to create an OpenLineage job.

        :param connection_name: name of the Spark connection
        :param job_name: unique name of the job
        :param producer: URI indicating the code or software that implements this job
        :returns: the minimal request necessary to create the job
        """
        return OpenLineageJob(
            namespace=connection_name, name=job_name, producer=producer, facets={}
        )

    def create_input(self, namespace: str, asset_name: str) -> OpenLineageInputDataset:
        """
        Builds the minimal object necessary to create an OpenLineage dataset,
        wired to use as an input (source) for lineage.

        :param namespace: name of the source of the asset
        :param asset_name: name of the asset, by OpenLineage standard
        :returns: the minimal request necessary to create the input dataset
        """
        return OpenLineageInputDataset.creator(
            namespace=namespace,
            asset_name=asset_name,
        )

    def create_output(
        self,
        namespace: str,
        asset_name: str,
    ) -> OpenLineageOutputDataset:
        """
        Builds the minimal object necessary to create an OpenLineage dataset,
        wired to use as an output (target) for lineage.

        :param namespace: name of the source of the asset
        :param asset_name: name of the asset, by OpenLineage standard
        :returns: the minimal request necessary to create the output dataset
        """
        return OpenLineageOutputDataset.creator(
            namespace=namespace,
            asset_name=asset_name,
            producer=self.producer or "",
        )
