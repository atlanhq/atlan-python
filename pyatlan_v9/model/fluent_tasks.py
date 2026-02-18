# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
v9 FluentTasks — search abstraction for Atlan's task queue.

Uses v9 DSL (msgspec.Struct) and v9 TaskSearchRequest instead of legacy
Pydantic models.  Query-building logic (Bool, SortItem, etc.) uses the
same re-exported dataclass types.
"""

from __future__ import annotations

import dataclasses
from copy import deepcopy
from typing import Dict, List, Optional

from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.search import Bool, Query, SortItem
from pyatlan.utils import validate_type
from pyatlan_v9.model.search import DSL
from pyatlan_v9.model.task import TaskSearchRequest, TaskSearchResponse


@dataclasses.dataclass
class FluentTasks:
    """
    Search abstraction mechanism, to simplify the most common searches
    against Atlan task queue (removing the need to understand the guts of Elastic).
    """

    sorts: Optional[List[SortItem]] = None
    aggregations: Optional[Dict[str, Aggregation]] = None
    _page_size: Optional[int] = None

    def __init__(
        self,
        wheres: Optional[List[Query]] = None,
        where_nots: Optional[List[Query]] = None,
        where_somes: Optional[List[Query]] = None,
        _min_somes: int = 1,
        sorts: Optional[List[SortItem]] = None,
        aggregations: Optional[Dict[str, Aggregation]] = None,
        _page_size: Optional[int] = None,
    ):
        self.wheres = wheres
        self.where_nots = where_nots
        self.where_somes = where_somes
        self._min_somes = _min_somes
        self.sorts = sorts
        self.aggregations = aggregations
        self._page_size = _page_size

    def _clone(self) -> FluentTasks:
        return deepcopy(self)

    def sort(self, by: SortItem) -> FluentTasks:
        validate_type(name="by", _type=SortItem, value=by)
        clone = self._clone()
        if clone.sorts is None:
            clone.sorts = []
        clone.sorts.append(by)
        return clone

    def aggregate(self, key: str, aggregation: Aggregation) -> FluentTasks:
        validate_type(name="key", _type=str, value=key)
        validate_type(name="aggregation", _type=Aggregation, value=aggregation)
        clone = self._clone()
        if clone.aggregations is None:
            clone.aggregations = {}
        clone.aggregations[key] = aggregation
        return clone

    def page_size(self, size: int) -> FluentTasks:
        validate_type(name="size", _type=int, value=size)
        clone = self._clone()
        clone._page_size = size
        return clone

    def where(self, query: Query) -> FluentTasks:
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.wheres is None:
            clone.wheres = []
        clone.wheres.append(query)
        return clone

    def where_not(self, query: Query) -> FluentTasks:
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.where_nots is None:
            clone.where_nots = []
        clone.where_nots.append(query)
        return clone

    def where_some(self, query: Query) -> FluentTasks:
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.where_somes is None:
            clone.where_somes = []
        clone.where_somes.append(query)
        return clone

    def min_somes(self, minimum: int) -> FluentTasks:
        validate_type(name="minimum", _type=int, value=minimum)
        clone = self._clone()
        clone._min_somes = minimum
        return clone

    def to_query(self) -> Query:
        q = Bool()
        q.filter = self.wheres or []
        q.must_not = self.where_nots or []
        if self.where_somes:
            q.should = self.where_somes
            q.minimum_should_match = self._min_somes
        return q

    def _dsl(self) -> DSL:
        return DSL(query=self.to_query())

    def to_request(self) -> TaskSearchRequest:
        dsl = self._dsl()
        if self._page_size:
            dsl.size = self._page_size
        if self.sorts:
            dsl.sort = self.sorts
        if self.aggregations:
            dsl.aggregations.update(self.aggregations)
        request = TaskSearchRequest(dsl=dsl)
        return request

    def count(self, client: AtlanClient) -> int:
        if not isinstance(client, AtlanClient):
            raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
        dsl = self._dsl()
        dsl.size = 1
        request = TaskSearchRequest(dsl=dsl)
        return client.tasks.search(request).count

    def execute(self, client: AtlanClient) -> TaskSearchResponse:
        if not isinstance(client, AtlanClient):
            raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
        return client.tasks.search(self.to_request())


from pyatlan.client.atlan import AtlanClient  # noqa: E402
