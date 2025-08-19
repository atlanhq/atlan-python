# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, List

from pyatlan.client.common import GetLineageList
from pyatlan.model.assets import Asset
from pyatlan.model.lineage import LineageListRequest

if TYPE_CHECKING:
    from pyatlan.client.protocol import AsyncApiCaller


class AsyncLineageListResults:
    """
    Async version of LineageListResults for lineage retrieval.

    Captures the response from a lineage retrieval against Atlan. Also provides the ability to
    iteratively page through results, without needing to track or re-run the original query.
    """

    def __init__(
        self,
        client: AsyncApiCaller,
        criteria: LineageListRequest,
        start: int,
        size: int,
        has_more: bool,
        assets: List[Asset],
    ):
        self._client = client
        self._criteria = criteria
        self._start = start
        self._size = size
        self._has_more = has_more
        self._assets = assets

    def current_page(self) -> List[Asset]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._assets

    @property
    def has_more(self) -> bool:
        """Check if there are more pages of results."""
        return self._has_more

    async def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        if not self._has_more:
            return False

        self._start = start or self._start + self._size
        if size:
            self._size = size

        # Update criteria for next page
        self._criteria.offset = self._start
        self._criteria.size = self._size

        endpoint, request_obj = GetLineageList.prepare_request(self._criteria)
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        response = GetLineageList.process_response(raw_json, self._criteria)

        self._assets = response["assets"]
        self._has_more = response["has_more"]

        return self._has_more

    async def __aiter__(self):
        """
        Async iterator through the results, lazily-fetching
        each next page until there are no more results.

        :returns: an async iterable form of each result, across all pages
        """
        while True:
            for asset in self.current_page():
                yield asset
            if not self.has_more:
                break
            await self.next_page()
