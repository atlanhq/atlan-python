from typing import Dict, List

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import TASK_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import SortOrder
from pyatlan.model.search import SortItem
from pyatlan.model.task import AtlanTask, TaskSearchRequest, TaskSearchResponse


class TaskClient:
    """
    A client for operating on tasks.
    """

    TASK_COUNT = "approximateCount"

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @staticmethod
    def _parse_atlan_tasks(raw_json: Dict):
        atlan_tasks = []
        if "tasks" in raw_json:
            try:
                atlan_tasks = parse_obj_as(List[AtlanTask], raw_json.get("tasks"))
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        return atlan_tasks

    @staticmethod
    def _handle_sorting(sort: List[SortItem]):
        missing_time_sort = True
        missing_sort = True if not sort else False

        if not missing_sort:
            # If there is some sort, see whether time is already included
            for option in sort:
                if (
                    option.field
                    and option.field == AtlanTask.START_TIME.numeric_field_name
                ):
                    missing_time_sort = False
                    break

        if missing_time_sort:
            # If there is no sort by time, always add it as a final
            # (tie-breaker) criteria to ensure there is consistent paging
            # (unfortunately sorting by _doc still has duplicates across large number of pages)
            sort.append(
                SortItem(
                    field=AtlanTask.START_TIME.numeric_field_name,
                    order=SortOrder.ASCENDING,
                )
            )

    @validate_arguments
    def search(self, request: TaskSearchRequest) -> TaskSearchResponse:
        self._handle_sorting(request.dsl.sort)
        raw_json = self._client._call_api(TASK_SEARCH, request_obj=request)
        aggregations = raw_json.get("aggregations")
        count = raw_json.get(self.TASK_COUNT, 0)
        tasks = self._parse_atlan_tasks(raw_json)

        return TaskSearchResponse(
            client=self._client,
            endpoint=TASK_SEARCH,
            criteria=request,
            start=request.dsl.from_,
            size=request.dsl.size,
            count=count,
            tasks=tasks,
            aggregations=aggregations,
        )
