from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import RUN_QUERY
from pyatlan.errors import ErrorCode
from pyatlan.model.query import QueryRequest, QueryResponse


class QueryClient:
    """
    A client for running SQL queries.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def stream(self, request: QueryRequest) -> QueryResponse:
        """
        Runs the provided query and returns its results.

        :param: request query to run.
        :returns: results of the query.
        :raises : AtlanError on any issues with API communication.
        """
        es_responses = self._client._call_api(RUN_QUERY, request_obj=request)
        return QueryResponse(events=es_responses)
