from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic.v1 import Field, validator

from pyatlan.model.core import AtlanObject
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.utils import generate_new_uuid


class OpenLineageRun(AtlanObject):
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

    job: OpenLineageJob = Field(default=None, exclude=True)
    run_id: Optional[str] = Field(
        default=None,
        description="Globally unique ID of the run associated with the job.",
    )
    facets: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Run facets."
    )

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/Run"

    @validator("run_id")
    def validate_run_id(cls, value: str) -> str:
        UUID(value)
        return value

    @classmethod
    def creator(cls, job: OpenLineageJob) -> OpenLineageRun:
        """
        Builds the minimal object necessary to create an OpenLineage run.

        :param job: OpenLineage job for which to create a new run
        :returns: the minimal request necessary to create the run
        """
        return OpenLineageRun(job=job, run_id=str(generate_new_uuid()), facets={})
