# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

import json as json_lib
from typing import Any, ClassVar, Dict, Generator, List, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTaskStatus, AtlanTaskType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, TextField
from pyatlan_v9.model.search import DSL


class AtlanTask(msgspec.Struct, kw_only=True):
    """Representation of a task in Atlan's task queue."""

    TYPE: ClassVar[KeywordField] = KeywordField("type", "__task_type")
    """Type of the task."""
    GUID: ClassVar[KeywordField] = KeywordField("guid", "__task_guid")
    """Unique identifier of the task."""
    CREATED_BY: ClassVar[KeywordField] = KeywordField("createdBy", "__task_createdBy")
    """User who created the task."""
    CREATED_TIME: ClassVar[NumericField] = NumericField(
        "createdTime", "__task_timestamp"
    )
    """Time (epoch) at which the task was created, in milliseconds."""
    UPDATED_TIME: ClassVar[NumericField] = NumericField(
        "updatedTime", "__task_modificationTimestamp"
    )
    """Time (epoch) at which the task was last updated, in milliseconds."""
    START_TIME: ClassVar[NumericField] = NumericField("startTime", "__task_startTime")
    """Time (epoch) at which the task was started, in milliseconds."""
    END_TIME: ClassVar[NumericField] = NumericField("endTime", "__task_endTime")
    """Time (epoch) at which the task was ended, in milliseconds."""
    TIME_TAKEN_IN_SECONDS: ClassVar[NumericField] = NumericField(
        "timeTakenInSeconds", "__task_timeTakenInSeconds"
    )
    """Total time taken to complete the task, in seconds."""
    ATTEMPT_COUNT: ClassVar[NumericField] = NumericField(
        "attemptCount", "__task_attemptCount"
    )
    """Number of times the task has been attempted."""
    STATUS: ClassVar[TextField] = TextField("status", "__task_status")
    """Status of the task."""
    CLASSIFICATION_ID: ClassVar[KeywordField] = KeywordField(
        "classificationId", "__task_classificationId"
    )
    ENTITY_GUID: ClassVar[KeywordField] = KeywordField(
        "entityGuid", "__task_entityGuid"
    )
    """Unique identifier of the asset the task originated from."""

    type: Union[AtlanTaskType, None] = None
    """Type of the task."""
    guid: Union[str, None] = None
    """Unique identifier of the task."""
    created_by: Union[str, None] = None
    """User who created the task."""
    created_time: Union[int, None] = None
    """Time (epoch) at which the task was created, in milliseconds."""
    updated_time: Union[int, None] = None
    """Time (epoch) at which the task was last updated, in milliseconds."""
    start_time: Union[int, None] = None
    """Time (epoch) at which the task was started, in milliseconds."""
    end_time: Union[int, None] = None
    """Time (epoch) at which the task was ended, in milliseconds."""
    time_taken_in_seconds: Union[int, None] = None
    """Total time taken to complete the task, in seconds."""
    parameters: Union[dict[str, Any], None] = None
    """Parameters used for running the task."""
    attempt_count: Union[int, None] = None
    """Number of times the task has been attempted."""
    status: Union[AtlanTaskStatus, None] = None
    """Status of the task."""
    classification_id: Union[str, None] = None
    entity_guid: Union[str, None] = None
    """Unique identifier of the asset the task originated from."""


class TaskSearchRequest(msgspec.Struct, kw_only=True):
    """Class from which to configure and run a search against Atlan's task queue."""

    dsl: DSL
    attributes: List[str] = msgspec.field(default_factory=list)

    def json(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> str:
        """Serialize TaskSearchRequest to JSON string."""
        d: Dict[str, Any] = {
            "attributes": self.attributes,
            "dsl": json_lib.loads(
                self.dsl.json(by_alias=by_alias, exclude_none=exclude_none)
            ),
        }
        if exclude_none:
            d = {k: v for k, v in d.items() if v is not None}
        return json_lib.dumps(d)


class TaskSearchResponse:
    """Captures the response from a search against Atlan's task queue."""

    def __init__(
        self,
        client: Any,
        endpoint: Any,
        criteria: Any,
        start: int,
        size: int,
        count: int,
        tasks: list[AtlanTask],
        aggregations: Any,
    ):
        self._client = client
        self._endpoint = endpoint
        self._criteria = criteria
        self._start = start
        self._size = size
        self._count = count
        self._tasks = tasks
        self._aggregations = aggregations

    @property
    def count(self) -> int:
        """Total count of matching tasks."""
        return self._count

    def current_page(self) -> list[AtlanTask]:
        """Retrieve the current page of results."""
        return self._tasks

    def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._tasks else False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := self._get_next_page_json():
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    def _get_next_page_json(self) -> Union[dict, None]:
        """Fetch the next page of results and return raw JSON."""
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "tasks" not in raw_json or not raw_json["tasks"]:
            self._tasks = []
            return None
        try:
            self._tasks = msgspec.convert(
                raw_json["tasks"], list[AtlanTask], strict=False
            )
            return raw_json
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[AtlanTask, None, None]:
        """Iterate through all pages of results."""
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
