from __future__ import annotations

import dataclasses
from copy import deepcopy
from typing import Dict, List, Optional

from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.search import DSL, Bool, Query, SortItem
from pyatlan.model.task import TaskSearchRequest, TaskSearchResponse
from pyatlan.utils import validate_type


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
        """
        Returns a copy of the current `FluentTasks`
        that's ready for further operations.

        :returns: copy of the current `FluentTasks`
        """
        return deepcopy(self)

    def sort(self, by: SortItem) -> FluentTasks:
        """
        Add a criterion by which to sort the results.

        :param by: criterion by which to sort the results
        :returns: the `FluentTasks` with this sorting criterion added
        """
        validate_type(name="by", _type=SortItem, value=by)
        clone = self._clone()
        if clone.sorts is None:
            clone.sorts = []
        clone.sorts.append(by)
        return clone

    def aggregate(self, key: str, aggregation: Aggregation) -> FluentTasks:
        """
        Add an aggregation to run against the results of the search.
        You provide any key you want (you'll use it to look at the
        results of a specific aggregation).

        :param key: you want to use to look at the results of the aggregation
        :param aggregation: you want to calculate
        :returns: the `FluentTasks` with this aggregation added
        """
        validate_type(name="key", _type=str, value=key)
        validate_type(name="aggregation", _type=Aggregation, value=aggregation)
        clone = self._clone()
        if clone.aggregations is None:
            clone.aggregations = {}
        clone.aggregations[key] = aggregation
        return clone

    def page_size(self, size: int) -> FluentTasks:
        """
        Set the number of results to retrieve per underlying API request.

        :param size: number of results to retrieve per underlying API request
        :returns: the `FluentTasks` with this parameter configured
        """
        validate_type(name="size", _type=int, value=size)
        clone = self._clone()
        clone._page_size = size
        return clone

    def where(self, query: Query) -> FluentTasks:
        """
        Add a single criterion that must be present
        on every search result. (Note: these are translated to filters.)

        :param query: the query to set as a criterion
        that must be present on every search result
        :returns: the `FluentTasks` with this `where` criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.wheres is None:
            clone.wheres = []
        clone.wheres.append(query)
        return clone

    def where_not(self, query: Query) -> FluentTasks:
        """
        Add a single criterion that must not be present on any search result.

        :param query: the query to set as a criterion
        that must not be present on any search result
        :returns: the `FluentTasks` with this `where_not` criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.where_nots is None:
            clone.where_nots = []
        clone.where_nots.append(query)
        return clone

    def where_some(self, query: Query) -> FluentTasks:
        """
        Add a single criterion at least some of which should
        be present on each search result. You can control "how many"
        of the criteria added this way are a minimum for each search
        result to match through the 'minimum' property.

        :param query: the query to set as a criterion
        some number of which should be present on a search result
        :returns: the `FluentTasks` with this `where_some` criterion added
        """
        validate_type(name="query", _type=Query, value=query)
        clone = self._clone()
        if clone.where_somes is None:
            clone.where_somes = []
        clone.where_somes.append(query)
        return clone

    def min_somes(self, minimum: int) -> FluentTasks:
        """
        Sets the minimum number of 'where_somes'
        that must match for a result to be included.

        :param minimum: minimum number of 'where_somes' that must match
        :returns: the `FluentTasks` with this `min_somes` criterion added
        """
        validate_type(name="minimum", _type=int, value=minimum)
        clone = self._clone()
        clone._min_somes = minimum
        return clone

    def to_query(self) -> Query:
        """
        Translate the Atlan compound query into an Elastic Query object.

        :returns: an Elastic Query object that represents the compound query
        """
        q = Bool()
        q.filter = self.wheres or []
        q.must_not = self.where_nots or []
        if self.where_somes:
            q.should = self.where_somes
            q.minimum_should_match = self._min_somes
        return q

    def _dsl(self) -> DSL:
        """
        Translate the Atlan fluent into an Atlan tasks search DSL.

        :returns: an Atlan tasks search DSL that encapsulates the fluent tasks
        """
        return DSL(query=self.to_query())

    def to_request(self) -> TaskSearchRequest:
        """
        :returns: the TaskSearchRequest that encapsulates
        information specified in this FluentTasks
        """
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
        """
        Return the total number of tasks that will match the supplied criteria,
        using the most minimal query possible (retrieves minimal data).

        :param client: client through which to count the tasks
        :raises: `InvalidRequestError` if no atlan client has been provided
        :returns: the count of tasks that will match the supplied criteria
        """
        if not isinstance(client, AtlanClient):
            raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
        dsl = self._dsl()
        dsl.size = 1
        request = TaskSearchRequest(dsl=dsl)
        return client.tasks.search(request).count

    def execute(self, client: AtlanClient) -> TaskSearchResponse:
        """
        Run the fluent search to retrieve tasks that match the supplied criteria.

        :param client: client through which to retrieve the tasks
        :raises: `InvalidRequestError` if no atlan client has been provided
        :returns: an iterable list of tasks that match the supplied criteria, lazily-fetched
        """
        if not isinstance(client, AtlanClient):
            raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
        return client.tasks.search(self.to_request())


from pyatlan.client.atlan import AtlanClient  # noqa: E402
