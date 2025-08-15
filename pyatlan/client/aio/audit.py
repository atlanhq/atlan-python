# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import logging

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller, AuditSearch
from pyatlan.errors import ErrorCode
from pyatlan.model.aio.audit import AsyncAuditSearchResults
from pyatlan.model.audit import AuditSearchRequest

LOGGER = logging.getLogger(__name__)


class AsyncAuditClient:
    """
    Async version of AuditClient that can be used to configure and run a search against Atlan's activity log.
    This class does not need to be instantiated directly but can be obtained through the audit property of AsyncAtlanClient.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def search(
        self, criteria: AuditSearchRequest, bulk=False
    ) -> AsyncAuditSearchResults:
        """
        Search for assets using the provided criteria (async version).
        `Note:` if the number of results exceeds the predefined threshold
        (10,000 assets) this will be automatically converted into an audit `bulk` search.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search to retrieve assets that match the supplied criteria,
        for large numbers of results (> `10,000`), defaults to `False`. Note: this will reorder the results
        (based on creation timestamp) in order to iterate through a large number (more than `10,000`) results.
        :raises InvalidRequestError:

            - if audit bulk search is enabled (`bulk=True`) and any
              user-specified sorting options are found in the search request.
            - if audit bulk search is disabled (`bulk=False`) and the number of results
              exceeds the predefined threshold (i.e: `10,000` assets)
              and any user-specified sorting options are found in the search request.

        :raises AtlanError: on any API communication issue
        :returns: the results of the search
        """
        # Prepare request using shared logic
        endpoint, request_obj = AuditSearch.prepare_request(criteria, bulk)

        # Execute async API call
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)

        # Process response using shared logic
        response = AuditSearch.process_response(raw_json)

        # Check if we need to convert to bulk search using shared logic
        if AuditSearch.check_for_bulk_search(
            response["count"], criteria, bulk, AsyncAuditSearchResults
        ):
            # Recursive async call with updated criteria
            return await self.search(criteria)

        # Create and return async search results
        return AsyncAuditSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=response["count"],
            entity_audits=response["entity_audits"],
            bulk=bulk,
            aggregations=response["aggregations"],
        )
