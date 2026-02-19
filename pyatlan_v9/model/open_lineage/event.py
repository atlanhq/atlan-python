# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Union

import msgspec
from pytz import utc  # type:ignore[import-untyped]

from pyatlan.model.enums import AtlanConnectorType, OpenLineageEventType
from pyatlan_v9.model.open_lineage.base import OpenLineageBaseEvent
from pyatlan_v9.model.open_lineage.input_dataset import OpenLineageInputDataset
from pyatlan_v9.model.open_lineage.job import OpenLineageJob
from pyatlan_v9.model.open_lineage.output_dataset import OpenLineageOutputDataset
from pyatlan_v9.model.open_lineage.run import OpenLineageRun

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class OpenLineageRawEvent:
    """
    Root model for handling raw OpenLineage events.

    This model accepts any arbitrary data structure (dict, list of dicts, string, etc.)
    and allows it to be sent as raw OpenLineage event data to Atlan's API.
    """

    def __init__(self, data: Any = None) -> None:
        self.data = data

    @classmethod
    def from_json(cls, json_str: str) -> OpenLineageRawEvent:
        """
        Create an OpenLineageRawEvent from a JSON string.

        :param json_str: JSON string containing raw OpenLineage event data
        :returns: New OpenLineageRawEvent instance
        """
        return cls(data=json.loads(json_str))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> OpenLineageRawEvent:
        """
        Create an OpenLineageRawEvent from a dictionary.

        :param data: Dictionary containing raw OpenLineage event data
        :returns: New OpenLineageRawEvent instance
        """
        return cls(data=data)

    @classmethod
    def parse_raw(cls, json_str: str) -> OpenLineageRawEvent:
        """Compatibility method: parse from raw JSON string."""
        return cls.from_json(json_str)

    @classmethod
    def parse_obj(cls, data: Any) -> OpenLineageRawEvent:
        """Compatibility method: parse from a Python object."""
        return cls(data=data)


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
    """

    run: Union[OpenLineageRun, None] = None
    job: Union[OpenLineageJob, None] = None
    event_type: Union[OpenLineageEventType, None] = msgspec.field(
        default=None, name="eventType"
    )
    inputs: Union[List[OpenLineageInputDataset], None] = msgspec.field(
        default_factory=list
    )
    outputs: Union[List[OpenLineageOutputDataset], None] = msgspec.field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if self.schema_url is None:
            self.schema_url = self._get_schema()
        if self.event_time is not None:
            self._validate_event_time(self.event_time)

    @staticmethod
    def _get_schema() -> str:
        return "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"

    @classmethod
    def creator(
        cls, run: OpenLineageRun, event_type: OpenLineageEventType
    ) -> OpenLineageEvent:
        """
        Builds the minimal object necessary to create an OpenLineage event.

        :param run: OpenLineage run for which to create a new event
        :param event_type: type of event to create
        :returns: the minimal request necessary to create the event
        """
        return OpenLineageEvent(
            run=run,
            job=run.job,
            producer=run.job and run.job.producer or "",
            event_type=event_type,
            event_time=datetime.now(tz=utc).isoformat(),
        )

    def emit(self, client: AtlanClient) -> None:
        """
        Send the OpenLineage event to Atlan to be processed.

        :param client: connectivity to an Atlan tenant
        :raises AtlanError: on any API communication issues
        """
        return client.open_lineage.send(
            request=self, connector_type=AtlanConnectorType.SPARK
        )

    @classmethod
    def emit_raw(
        cls,
        client: AtlanClient,
        event: Union[OpenLineageRawEvent, List[Dict[str, Any]], Dict[str, Any], str],
        connector_type: AtlanConnectorType = AtlanConnectorType.SPARK,
    ) -> None:
        """
        Send raw OpenLineage event data to Atlan to be processed.

        :param client: connectivity to an Atlan tenant
        :param event: Raw event(s) as JSON string, dict, list of dicts, or OpenLineageRawEvent
        :param connector_type: connector type for the OpenLineage event
        :raises AtlanError: on any API communication issues
        """
        return client.open_lineage.send(request=event, connector_type=connector_type)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this event to a dict, properly handling excluded fields
        (producer on Job, job on Run) and camelCase aliases.

        Mirrors Pydantic's ``model.json(by_alias=True, exclude_unset=True)``
        behaviour: fields that were *explicitly* passed at construction time
        appear even when empty; fields left at their factory default are omitted.
        """
        result: Dict[str, Any] = {}

        if self.event_time is not None:
            result["eventTime"] = self.event_time
        if self.producer is not None:
            result["producer"] = self.producer
        if self.schema_url is not None:
            result["schemaURL"] = self.schema_url

        if self.run is not None:
            # Exclude the 'job' field from run serialization
            run_dict: Dict[str, Any] = {}
            if self.run.run_id is not None:
                run_dict["runId"] = self.run.run_id
            # Always include facets (even when empty) — matches legacy behaviour
            if self.run.facets is not None:
                run_dict["facets"] = self.run.facets
            result["run"] = run_dict

        if self.job is not None:
            # Exclude the 'producer' field from job serialization
            job_dict: Dict[str, Any] = {}
            if self.job.namespace is not None:
                job_dict["namespace"] = self.job.namespace
            if self.job.name is not None:
                job_dict["name"] = self.job.name
            if self.job.facets is not None:
                job_dict["facets"] = (
                    msgspec.to_builtins(self.job.facets) if self.job.facets else {}
                )
            result["job"] = job_dict

        if self.event_type is not None:
            result["eventType"] = self.event_type.value

        if self.inputs:
            inputs_list = []
            for inp in self.inputs:
                inp_dict: Dict[str, Any] = {}
                if inp.namespace is not None:
                    inp_dict["namespace"] = inp.namespace
                if inp.name is not None:
                    inp_dict["name"] = inp.name
                # Include facets (even when empty) — matches legacy behaviour
                if inp.facets is not None:
                    inp_dict["facets"] = inp.facets
                # NOTE: inputFacets is intentionally omitted when it was not
                # explicitly set by the caller (mirrors exclude_unset=True).
                inputs_list.append(inp_dict)
            result["inputs"] = inputs_list

        if self.outputs:
            outputs_list = []
            for out in self.outputs:
                outputs_list.append(out.to_dict())
            result["outputs"] = outputs_list

        return result
