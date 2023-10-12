# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import abc
from abc import ABC
from typing import Generator, Iterable, Optional
from warnings import warn

from pydantic import ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import GET_LINEAGE, GET_LINEAGE_LIST, INDEX_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregations
from pyatlan.model.assets import Asset
from pyatlan.model.core import SearchRequest
from pyatlan.model.lineage import (
    LineageDirection,
    LineageListRequest,
    LineageRequest,
    LineageResponse,
)
from pyatlan.model.search import IndexSearchRequest
from pyatlan.utils import API, unflatten_custom_metadata_for_entity


class AssetClient:
    """
    This class can be used to retrieve information about roles. This class does not need to be instantiated
    directly but can be obtained through the role property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def search(self, criteria: IndexSearchRequest) -> IndexSearchResults:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(
            INDEX_SEARCH,
            request_obj=criteria,
        )
        if "entities" in raw_json:
            try:
                for entity in raw_json["entities"]:
                    unflatten_custom_metadata_for_entity(
                        entity=entity, attributes=criteria.attributes
                    )
                assets = parse_obj_as(list[Asset], raw_json["entities"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            assets = []
        aggregations = self._get_aggregations(raw_json)
        count = raw_json["approximateCount"] if "approximateCount" in raw_json else 0
        return IndexSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            assets=assets,
            aggregations=aggregations,
        )

    def _get_aggregations(self, raw_json) -> Optional[Aggregations]:
        if "aggregations" in raw_json:
            try:
                aggregations = Aggregations.parse_obj(raw_json["aggregations"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            aggregations = None
        return aggregations

    def get_lineage(self, lineage_request: LineageRequest) -> LineageResponse:
        """
        Deprecated — this is an older, slower operation to retrieve lineage that will not receive further enhancements.
        Use the get_lineage_list operation instead.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises AtlanError: on any API communication issue
        """
        warn(
            "Lineage retrieval using this method is deprecated, please use 'get_lineage_list' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        raw_json = self._client._call_api(
            GET_LINEAGE, None, lineage_request, exclude_unset=False
        )
        return LineageResponse(**raw_json)

    def get_lineage_list(
        self, lineage_request: LineageListRequest
    ) -> LineageListResults:
        """
        Retrieve lineage using the higher-performance "list" API.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises InvalidRequestError: if the requested lineage direction is 'BOTH' (unsupported for this operation)
        :raises AtlanError: on any API communication issue
        """
        if lineage_request.direction == LineageDirection.BOTH:
            raise ErrorCode.INVALID_LINEAGE_DIRECTION.exception_with_parameters()
        raw_json = self._client._call_api(
            GET_LINEAGE_LIST, None, request_obj=lineage_request, exclude_unset=True
        )
        if "entities" in raw_json:
            try:
                assets = parse_obj_as(list[Asset], raw_json["entities"])
                has_more = parse_obj_as(bool, raw_json["hasMore"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            assets = []
            has_more = False
        return LineageListResults(
            client=self._client,
            criteria=lineage_request,
            start=lineage_request.offset or 0,
            size=lineage_request.size or 10,
            has_more=has_more,
            assets=assets,
        )


class SearchResults(ABC, Iterable):
    """
    Abstract class that encapsulates results returned by various searches.
    """

    def __init__(
        self,
        client: ApiCaller,
        endpoint: API,
        criteria: SearchRequest,
        start: int,
        size: int,
        assets: list[Asset],
    ):
        self._client = client
        self._endpoint = endpoint
        self._criteria = criteria
        self._start = start
        self._size = size
        self._assets = assets

    def current_page(self) -> list[Asset]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._assets

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._assets else False

    @abc.abstractmethod
    def _get_next_page(self):
        """
        Abstract method that must be implemented in subclasses, used to
        fetch the next page of results.
        """

    # TODO Rename this here and in `next_page`
    def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "entities" not in raw_json:
            self._assets = []
            return None
        try:
            for entity in raw_json["entities"]:
                unflatten_custom_metadata_for_entity(
                    entity=entity, attributes=self._criteria.attributes
                )
            self._assets = parse_obj_as(list[Asset], raw_json["entities"])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[Asset, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break


class IndexSearchResults(SearchResults, Iterable):
    """
    Captures the response from a search against Atlan. Also provides the ability to
    iteratively page through results, without needing to track or re-run the original
    query.
    """

    def __init__(
        self,
        client: ApiCaller,
        criteria: IndexSearchRequest,
        start: int,
        size: int,
        count: int,
        assets: list[Asset],
        aggregations: Optional[Aggregations],
    ):
        super().__init__(client, INDEX_SEARCH, criteria, start, size, assets)
        self._count = count
        self._aggregations = aggregations

    @property
    def aggregations(self) -> Optional[Aggregations]:
        return self._aggregations

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := super()._get_next_page_json():
            self._count = (
                raw_json["approximateCount"] if "approximateCount" in raw_json else 0
            )
            return True
        return False

    @property
    def count(self) -> int:
        return self._count


class LineageListResults(SearchResults, Iterable):
    """
    Captures the response from a lineage retrieval against Atlan. Also provides the ability to
    iteratively page through results, without needing to track or re-run the original query.
    """

    def __init__(
        self,
        client: ApiCaller,
        criteria: LineageListRequest,
        start: int,
        size: int,
        has_more: bool,
        assets: list[Asset],
    ):
        super().__init__(client, GET_LINEAGE_LIST, criteria, start, size, assets)
        self._has_more = has_more

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.offset = self._start
        self._criteria.size = self._size
        if raw_json := super()._get_next_page_json():
            self._has_more = parse_obj_as(bool, raw_json["hasMore"])
            return True
        return False

    @property
    def has_more(self) -> bool:
        return self._has_more
