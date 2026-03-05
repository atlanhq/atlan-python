from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller, TaskSearch
from pyatlan.errors import ErrorCode
from pyatlan.model.task import TaskSearchRequest, TaskSearchResponse


class TaskClient:
    """
    A client for operating on tasks.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def search(self, request: TaskSearchRequest) -> TaskSearchResponse:
        """
        Search for tasks using the provided criteria.

        :param request: search request for tasks
        :returns: search results for tasks
        """
        endpoint, request_obj = TaskSearch.prepare_request(request)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        response_data = TaskSearch.process_response(raw_json)

        return TaskSearchResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=request,
            start=request.dsl.from_,
            size=request.dsl.size,
            count=response_data["count"],
            tasks=response_data["tasks"],
            aggregations=response_data["aggregations"],
        )
