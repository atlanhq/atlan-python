from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic.v1 import Field, root_validator
from pytz import utc  # type:ignore[import-untyped]

from pyatlan.model.enums import AtlanConnectorType, OpenLineageEventType
from pyatlan.model.open_lineage.base import OpenLineageBaseEvent
from pyatlan.model.open_lineage.input_dataset import OpenLineageInputDataset
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.output_dataset import OpenLineageOutputDataset
from pyatlan.model.open_lineage.run import OpenLineageRun

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class OpenLineageEvent(OpenLineageBaseEvent):
    """
    Atlan wrapper for abstracting OpenLineage events.

    An event represents a point-in-time state of a run.
    To process lineage in Atlan, you **must** have at least two states for any run:
    - `START`: Indicates that a run has started.
    - One of the following to mark that the run has finished:
        - `COMPLETE`: Run execution has successfully concluded.
        - `ABORT`: Run has been stopped abnormally.
        - `FAIL`: Run has failed.

    Additionally, for lineage to show inputs and outputs
    to a process in Atlan, at least one event must define `inputs` and `outputs`.
    These do not need to be included in every event, as they are merged across
    events for the same run (matching by `runId`).

    For more details, see the
    [OpenLineage documentation](https://openlineage.io/docs/spec/run-cycle).
    """

    run: Optional[OpenLineageRun] = Field(default=None)
    job: Optional[OpenLineageJob] = Field(default=None)
    event_type: Optional[OpenLineageEventType] = Field(default=None)
    inputs: Optional[List[OpenLineageInputDataset]] = Field(default_factory=list)
    outputs: Optional[List[OpenLineageOutputDataset]] = Field(default_factory=list)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"

    @root_validator(pre=True)
    def set_default_schema_url(cls, values):
        values["schema_url"] = cls._get_schema()
        return values

    @classmethod
    def creator(
        self, run: OpenLineageRun, event_type: OpenLineageEventType
    ) -> OpenLineageEvent:
        """
        Builds the minimal object necessary to create an OpenLineage event.

        :param run: OpenLineage run for which to create a new event
        :returns: the minimal request necessary to create the event
        """
        return OpenLineageEvent(
            run=run,
            job=run.job,
            producer=run.job and run.job.producer or "",
            event_type=event_type,
            event_time=datetime.now(tz=utc).isoformat(),  # type:ignore[call-arg]
        )

    def emit(self, client: Optional[AtlanClient] = None) -> None:
        """
        Send the OpenLineage event to Atlan to be processed.

        :raises AtlanError: on any API communication issues
        """
        from pyatlan.client.atlan import AtlanClient

        client = client or AtlanClient.get_default_client()
        return client.open_lineage.send(
            request=self, connector_type=AtlanConnectorType.SPARK
        )
