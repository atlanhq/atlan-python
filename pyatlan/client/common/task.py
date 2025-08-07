# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from typing import Dict, List

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import TASK_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import SortOrder
from pyatlan.model.search import SortItem
from pyatlan.model.task import AtlanTask, TaskSearchRequest


class TaskSearch:
    """Shared logic for task search operations."""

    TASK_COUNT = "approximateCount"

    @classmethod
    def prepare_request(cls, request: TaskSearchRequest) -> tuple:
        """
        Prepare the request for task search.

        :param request: search request for tasks
        :returns: tuple of (endpoint, request_obj)
        """
        cls._handle_sorting(request.dsl.sort)
        return TASK_SEARCH, request

    @classmethod
    def process_response(cls, raw_json: Dict) -> Dict:
        """
        Process the raw API response into task search results.

        :param raw_json: raw API response
        :returns: dictionary with tasks, count, and aggregations
        """
        aggregations = raw_json.get("aggregations")
        count = raw_json.get(cls.TASK_COUNT, 0)
        tasks = cls._parse_atlan_tasks(raw_json)

        return {
            "tasks": tasks,
            "count": count,
            "aggregations": aggregations,
        }

    @staticmethod
    def _parse_atlan_tasks(raw_json: Dict) -> List[AtlanTask]:
        """
        Parse tasks from the raw API response.

        :param raw_json: raw API response
        :returns: list of AtlanTask objects
        """
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
    def _handle_sorting(sort: List[SortItem]) -> None:
        """
        Ensure consistent sorting by time for task searches.

        :param sort: list of sort items to modify in-place
        """
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
