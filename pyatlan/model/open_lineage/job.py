from __future__ import annotations

from typing import Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.open_lineage.facet import OpenLineageJobFacet
from pyatlan.model.open_lineage.input_dataset import OpenLineageInputDataset
from pyatlan.model.open_lineage.output_dataset import OpenLineageOutputDataset


class OpenLineageJob(AtlanObject):
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

    name: Optional[str] = Field(
        default=None, description="Unique name for that job within that namespace."
    )
    namespace: Optional[str] = Field(
        default=None,
        description="Namespace containing that job.",
    )
    facets: Optional[Dict[str, OpenLineageJobFacet]] = Field(
        default_factory=dict,
        description="Job facets.",
    )
    # NOTE: Added to follow a similar pattern used in the Atlan Java SDK
    # This field is excluded from serialization
    producer: Optional[str] = Field(default=None, exclude=True)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/Job"

    @classmethod
    def creator(
        cls, connection_name: str, job_name: str, producer: str
    ) -> OpenLineageJob:
        """
        Builds the minimal object necessary to create an OpenLineage job.

        :param connection_name: name of the Spark connection in which the OpenLineage job should be created
        :param job_name: unique name of the job - if it already exists the existing job will be updated
        :param producer: URI indicating the code or software that implements this job
        :returns: the minimal request necessary to create the job
        """
        return OpenLineageJob(
            namespace=connection_name, name=job_name, producer=producer, facets={}
        )

    # TODO: provide some intuitive way to manage the facets of the job

    def create_input(self, namespace: str, asset_name: str) -> OpenLineageInputDataset:
        """
        Builds the minimal object necessary to create an OpenLineage dataset,
        wired to use as an input (source) for lineage.

        :param namespace: name of the source of the asset
        (see: https://github.com/OpenLineage/OpenLineage/blob/main/spec/Naming.md)
        :param asset_name: name of the asset, by OpenLineage standard (for eg: `DB.SCHEMA.TABLE`)
        :returns: the minimal request necessary to create the input dataset
        """
        return OpenLineageInputDataset.creator(
            namespace=namespace,
            asset_name=asset_name,
        )

    def create_output(
        self: OpenLineageJob,
        namespace: str,
        asset_name: str,
    ) -> OpenLineageOutputDataset:
        """
        Builds the minimal object necessary to create an OpenLineage dataset,
        wired to use as an output (target) for lineage.

        :param namespace: name of the source of the asset
        (see: https://github.com/OpenLineage/OpenLineage/blob/main/spec/Naming.md)
        :param asset_name: name of the asset, by OpenLineage standard (for eg: `DB.SCHEMA.TABLE`)
        :returns: the minimal request necessary to create the output dataset
        """
        return OpenLineageOutputDataset.creator(
            namespace=namespace,
            asset_name=asset_name,
            producer=self.producer or "",
        )
