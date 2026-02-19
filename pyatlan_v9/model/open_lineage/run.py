# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, Union
from uuid import UUID

import msgspec

from pyatlan_v9.model.open_lineage.job import OpenLineageJob
from pyatlan_v9.model.open_lineage.utils import generate_new_uuid


class OpenLineageRun(msgspec.Struct, kw_only=True, omit_defaults=True):
    """
    Atlan wrapper for abstracting OpenLineage runs.

    A run is an instance of a job execution.

    For more details
    https://openlineage.io/docs/spec/object-model#run
    """

    # job is excluded from serialization (it's a reference field)
    job: Union[OpenLineageJob, None] = None

    run_id: Union[str, None] = msgspec.field(default=None, name="runId")
    """Globally unique ID of the run associated with the job."""

    facets: Union[Dict[str, Any], None] = msgspec.field(default_factory=dict)
    """Run facets."""

    def __post_init__(self) -> None:
        if self.run_id is not None:
            # Validate it's a valid UUID
            UUID(self.run_id)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/Run"

    @classmethod
    def creator(cls, job: OpenLineageJob) -> OpenLineageRun:
        """
        Builds the minimal object necessary to create an OpenLineage run.

        :param job: OpenLineage job for which to create a new run
        :returns: the minimal request necessary to create the run
        """
        return OpenLineageRun(job=job, run_id=str(generate_new_uuid()), facets={})
