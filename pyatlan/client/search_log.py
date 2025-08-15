from typing import Union

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller, SearchLogSearch
from pyatlan.errors import ErrorCode
from pyatlan.model.search_log import (
    SearchLogRequest,
    SearchLogResults,
    SearchLogViewResults,
)


class SearchLogClient:
    """
    This class can be used to configure and run a search against Atlan's searcg log.
    This class does not need to be instantiated directly but can be obtained
    through the search_log property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def search(
        self, criteria: SearchLogRequest, bulk=False
    ) -> Union[SearchLogViewResults, SearchLogResults]:
        """
        Search for search logs using the provided criteria.
        `Note:` if the number of results exceeds the predefined threshold
        (10,000 search logs) this will be automatically converted into an search log `bulk` search.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search to retrieve search logs that match the supplied criteria,
        for large numbers of results (> `10,000`), defaults to `False`. Note: this will reorder the results
        (based on creation timestamp) in order to iterate through a large number (more than `10,000`) results.
        :raises InvalidRequestError:

            - if search log bulk search is enabled (`bulk=True`) and any
              user-specified sorting options are found in the search request.
            - if search log bulk search is disabled (`bulk=False`) and the number of results
              exceeds the predefined threshold (i.e: `10,000` assets)
              and any user-specified sorting options are found in the search request.

        :raises AtlanError: on any API communication issue
        :returns: the results of the search
        """
        # Prepare request using shared logic
        endpoint, request_obj = SearchLogSearch.prepare_request(criteria, bulk)

        # Execute API call
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)

        # Process response using shared logic (which returns the final results)
        results = SearchLogSearch.process_response(
            raw_json, criteria, bulk, self._client
        )

        # If it's SearchLogResults (not SearchLogViewResults), check for bulk search conversion
        if isinstance(results, SearchLogResults):
            if SearchLogSearch.check_for_bulk_search(
                results.count, criteria, bulk, SearchLogResults
            ):
                # Recursive call with updated criteria
                return self.search(criteria)

        return results
