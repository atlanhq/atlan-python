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
    Base class for handling OpenLineage events,
    passing through to the OpenLineage Python SDK
    but wrapping events such that they are handled
    appropriately in the Atlan Python SDK.
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
        return OpenLineageEvent(
            run=run,
            job=run.job,
            producer=run.job.producer or "",
            event_type=event_type,
            event_time=datetime.now(tz=utc).isoformat(),  # type:ignore[call-arg]
        )

    def emit(self, client: Optional[AtlanClient] = None) -> str:
        from pyatlan.client.atlan import AtlanClient

        client = client or AtlanClient.get_default_client()
        return client.open_lineage.send(
            request=self, connector_type=AtlanConnectorType.SPARK
        )
