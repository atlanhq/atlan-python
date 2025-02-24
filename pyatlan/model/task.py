from __future__ import annotations

from typing import Any, ClassVar, Dict, Generator, Iterable, List, Optional

from pydantic.v1 import Field, ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.core import AtlanObject, SearchRequest
from pyatlan.model.enums import AtlanTaskStatus, AtlanTaskType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, TextField
from pyatlan.model.search import DSL, Query, SortItem
from pyatlan.utils import API


class AtlanTask(AtlanObject):
    TYPE: ClassVar[KeywordField] = KeywordField("type", "__task_type")
    """Type of the task."""

    GUID: ClassVar[TextField] = TextField("guid", "__task_guid")
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
    """TBC"""

    ENTITY_GUID: ClassVar[KeywordField] = KeywordField(
        "entityGuid", "__task_entityGuid"
    )
    """Unique identifier of the asset the task originated from."""

    type: Optional[AtlanTaskType] = Field(None, description="Type of the task.")
    guid: Optional[str] = Field(None, description="Unique identifier of the task.")
    created_by: Optional[str] = Field(None, description="User who created the task.")
    created_time: Optional[int] = Field(
        None, description="Time (epoch) at which the task was created, in milliseconds."
    )
    updated_time: Optional[int] = Field(
        None,
        description="Time (epoch) at which the task was last updated, in milliseconds.",
    )
    start_time: Optional[int] = Field(
        None, description="Time (epoch) at which the task was started, in milliseconds."
    )
    end_time: Optional[int] = Field(
        None, description="Time (epoch) at which the task was ended, in milliseconds."
    )
    time_taken_in_seconds: Optional[int] = Field(
        None, description="Total time taken to complete the task, in seconds."
    )
    parameters: Optional[Dict[str, Any]] = Field(
        None, description="Parameters used for running the task."
    )
    attempt_count: Optional[int] = Field(
        None, description="Number of times the task has been attempted."
    )
    status: Optional[AtlanTaskStatus] = Field(None, description="Status of the task.")
    classification_id: Optional[str] = Field(None, description="To Be Confirmed (TBC).")
    entity_guid: Optional[str] = Field(
        None, description="Unique identifier of the asset the task originated from."
    )


class TaskSearchRequest(SearchRequest):
    """Class from which to configure and run a search against Atlan's task queue."""

    dsl: DSL

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}


class TaskSearchResponse(Iterable):
    """Captures the response from a search against Atlan's task queue."""

    def __init__(
        self,
        client: ApiCaller,
        endpoint: API,
        criteria: TaskSearchRequest,
        start: int,
        size: int,
        count: int,
        tasks: List[AtlanTask],
        aggregations: Dict[str, Aggregation],
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
        return self._count

    def current_page(self) -> List[AtlanTask]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._tasks

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._tasks else False

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := self._get_next_page_json():
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "tasks" not in raw_json or not raw_json["tasks"]:
            self._tasks = []
            return None
        try:
            self._tasks = parse_obj_as(List[AtlanTask], raw_json["tasks"])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[AtlanTask, None, None]:
        """
        Iterates through the results, lazily-fetching
        each next page until there are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
