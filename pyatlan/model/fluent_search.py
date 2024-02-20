from __future__ import annotations

import copy
import dataclasses
from typing import Dict, List, Optional, TypeVar, Union

from pyatlan.client.asset import IndexSearchResults
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.assets import Referenceable
from pyatlan.model.enums import EntityStatus
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Query, SortItem, Term

SelfQuery = TypeVar("SelfQuery", bound="CompoundQuery")


@dataclasses.dataclass
class CompoundQuery:
    """
    Class to compose compound queries combining various conditions.
    """

    wheres: Optional[List[Query]] = None
    where_nots: Optional[List[Query]] = None
    where_somes: Optional[List[Query]] = None
    _min_somes: int = 1

    @staticmethod
    def active_assets() -> Query:
        """
        Returns a query that will only match assets that are active in Atlan.

        :returns: a query that will only match assets that are active in Atlan
        """
        return Referenceable.STATUS.eq(EntityStatus.ACTIVE.value)

    @staticmethod
    def archived_assets() -> Query:
        """
        Returns a query that will only match assets that are archived (soft-deleted) in Atlan.

        :returns: a query that will only match assets that are archived (soft-deleted) in Atlan
        """
        return Referenceable.STATUS.eq(EntityStatus.DELETED.value)

    @staticmethod
    def asset_type(of: type) -> Query:
        """
        Returns a query that will only match assets of the type provided.

        :param of: type for assets to match
        :returns: a query that will only match assets of the type provided
        """
        return Referenceable.TYPE_NAME.eq(of.__name__)

    @staticmethod
    def asset_types(one_of: List[type]) -> Query:
        """
        Returns a query that will only match assets that are one of the types provided.

        :param one_of: types for assets to match
        :returns: a query that iwll only match assets of one of the types provided
        """
        return Referenceable.TYPE_NAME.within(list(map(lambda x: x.__name__, one_of)))

    @staticmethod
    def super_types(one_of: Union[type, List[type]]) -> Query:
        """
        Returns a query that will match all assets that are a subtype of at least one of
        the types provided.

        :param one_of: type name(s) of the supertypes for assets to match
        :returns: a query that will only match assets of a subtype of the types provided
        """
        if isinstance(one_of, list):
            return Referenceable.SUPER_TYPE_NAMES.within(
                list(map(lambda x: x.__name__, one_of))
            )
        return Referenceable.SUPER_TYPE_NAMES.eq(one_of.__name__)

    @staticmethod
    def tagged(
        with_one_of: Optional[List[str]] = None, directly: bool = False
    ) -> Query:
        """
        Returns a query that will only match assets that have at least one of the Atlan tags
        provided. This will match irrespective of the Atlan tag being directly applied to the
        asset, or if it was propagated to the asset.

        :param with_one_of: human-readable names of the Atlan tags
        :param directly: when True, the asset must have at least one Atlan tag directly assigned, otherwise
                         even propagated tags will suffice
        :returns: a query that will only match assets that have at least one of the Atlan tags provided
        """
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        values: List[str] = []
        if with_one_of:
            for name in with_one_of:
                if tag_id := AtlanTagCache.get_id_for_name(name):
                    values.append(tag_id)
                else:
                    raise ErrorCode.ATLAN_TAG_NOT_FOUND_BY_NAME.exception_with_parameters(
                        name
                    )
        if directly:
            if values:
                return FluentSearch(
                    wheres=[Referenceable.ATLAN_TAGS.within(values)]
                ).to_query()
            return FluentSearch(
                wheres=[Referenceable.ATLAN_TAGS.has_any_value()]
            ).to_query()
        if values:
            return FluentSearch(
                where_somes=[
                    Referenceable.ATLAN_TAGS.within(values),
                    Referenceable.PROPAGATED_ATLAN_TAGS.within(values),
                ],
                _min_somes=1,
            ).to_query()
        return FluentSearch(
            where_somes=[
                Referenceable.ATLAN_TAGS.has_any_value(),
                Referenceable.PROPAGATED_ATLAN_TAGS.has_any_value(),
            ],
            _min_somes=1,
        ).to_query()

    @staticmethod
    def assigned_term(qualified_names: Optional[List[str]] = None) -> Query:
        """
        Returns a query that will only match assets that have at least one term assigned.
        (If a list of qualified_names is specified, the assets that match must have at least
        one term assigned from within the list of qualified_names.)

        :param qualified_names: the qualified_names of the terms
        :returns: a query that will only match assets that have at least one term assigned
        """
        if qualified_names:
            return Referenceable.ASSIGNED_TERMS.within(qualified_names)
        return Referenceable.ASSIGNED_TERMS.has_any_value()

    def __init__(
        self,
        wheres: Optional[List[Query]] = None,
        where_nots: Optional[List[Query]] = None,
        where_somes: Optional[List[Query]] = None,
        _min_somes: int = 1,
    ):
        self.wheres = wheres
        self.where_nots = where_nots
        self.where_somes = where_somes
        self._min_somes = _min_somes

    def _clone(self: SelfQuery) -> SelfQuery:
        """
        Returns a copy of the current CompoundQuery that's ready for further operations.

        :returns: copy of the current CompoundQuery
        """
        return copy.deepcopy(self)

    def where(self: SelfQuery, query: Query) -> SelfQuery:
        """
        Add a single criterion that must be present on every search result.
        (Note: these are translated to filters.)

        :param query: the query to set as a criterion that must be present on every search result
        :returns: the compound query with this additional criterion added
        """
        clone = self._clone()
        if clone.wheres is None:
            clone.wheres = []
        clone.wheres.append(query)
        return clone

    def where_not(self: SelfQuery, query: Query) -> SelfQuery:
        """
        Add a single criterion that must not be present on any search result.

        :param query: the query to set as a criterion that must not be present on any search result
        :returns: the compound query with this additional criterion added
        """
        clone = self._clone()
        if clone.where_nots is None:
            clone.where_nots = []
        clone.where_nots.append(query)
        return clone

    def where_some(self: SelfQuery, query: Query) -> SelfQuery:
        """
        Add a single criterion at least some of which should be present on each search result.
        You can control "how many" of the criteria added this way are a minimum for each search
        result to match through the 'minimum' property.

        :param query: the query to set as a criterion some number of which should be present on a search result
        :returns: the compound query with this additional criterion added
        """
        clone = self._clone()
        if clone.where_somes is None:
            clone.where_somes = []
        clone.where_somes.append(query)
        return clone

    def min_somes(self: SelfQuery, minimum: int) -> SelfQuery:
        """
        Sets the minimum number of 'where_somes' that must match for a result to be included.

        :param minimum: minimum number of 'where_somes' that must match
        :returns: the compound query with this additional criterion applied
        """
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


@dataclasses.dataclass
class FluentSearch(CompoundQuery):
    """
    Class to compose compound queries combining various conditions.
    """

    sorts: Optional[List[SortItem]] = None
    aggregations: Optional[Dict[str, Aggregation]] = None
    _page_size: Optional[int] = None
    _includes_on_results: Optional[List[str]] = None
    _includes_on_relations: Optional[List[str]] = None

    @classmethod
    def select(cls, include_archived=False) -> "FluentSearch":
        """
        Start a fluent search that will return all assets.
        Additional conditions can be chained onto the returned object before any
        asset retrieval is attempted, ensuring all conditions are pushed-down for
        optimal retrieval. Only active (non-archived) assets will be included.

        :param include_archived: when True, archived (soft-deleted) assets will be included
        :returns: a fluent search that includes all assets
        """
        wheres = [Term.with_super_type_names("Asset")]
        if not include_archived:
            wheres.append(Term.with_state("ACTIVE"))
        return cls(
            wheres=wheres,
        )

    def __init__(
        self,
        wheres: Optional[List[Query]] = None,
        where_nots: Optional[List[Query]] = None,
        where_somes: Optional[List[Query]] = None,
        _min_somes: int = 1,
        sorts: Optional[List[SortItem]] = None,
        aggregations: Optional[Dict[str, Aggregation]] = None,
        _page_size: Optional[int] = None,
        _includes_on_results: Optional[List[str]] = None,
        _includes_on_relations: Optional[List[str]] = None,
    ):
        super().__init__(wheres, where_nots, where_somes, _min_somes)
        self.sorts = sorts
        self.aggregations = aggregations
        self._page_size = _page_size
        self._includes_on_results = _includes_on_results
        self._includes_on_relations = _includes_on_relations

    def _clone(self) -> "FluentSearch":
        """
        Returns a copy of the current FluentSearch that's ready for further operations.

        :returns: copy of the current FluentSearch
        """
        return copy.deepcopy(self)

    def sort(self, by: SortItem) -> "FluentSearch":
        """
        Add a criterion by which to sort the results.

        :param by: criterion by which to sort the results
        :returns: the fluent search with this sorting criterion added
        """
        clone = self._clone()
        if clone.sorts is None:
            clone.sorts = []
        clone.sorts.append(by)
        return clone

    def aggregate(self, key: str, aggregation: Aggregation) -> "FluentSearch":
        """
        Add an aggregation to run against the results of the search.
        You provide any key you want (you'll use it to look at the results of a specific aggregation).

        :param key: you want to use to look at the results of the aggregation
        :param aggregation: you want to calculate
        :returns: the fluent search with this aggregation added
        """
        clone = self._clone()
        if clone.aggregations is None:
            clone.aggregations = {}
        clone.aggregations[key] = aggregation
        return clone

    def page_size(self, size: int) -> "FluentSearch":
        """
        Set the number of results to retrieve per underlying API request.

        :param size: number of results to retrieve per underlying API request
        :returns: the fluent search with this parameter configured
        """
        clone = self._clone()
        clone._page_size = size
        return clone

    def include_on_results(self, field: Union[str, AtlanField]) -> "FluentSearch":
        """
        Add an attribute to retrieve for each asset in the results.

        :param field: attribute to retrieve for each result
        :returns: the fluent search with this parameter added
        """
        clone = self._clone()
        if clone._includes_on_results is None:
            clone._includes_on_results = []
        if isinstance(field, AtlanField):
            clone._includes_on_results.append(field.atlan_field_name)
        else:
            clone._includes_on_results.append(field)
        return clone

    def include_on_relations(self, field: Union[str, AtlanField]) -> "FluentSearch":
        """
        Add an attribute to retrieve for each asset related to the assets in the results.

        :param field: attribute to retrieve for each related asset of each result
        :returns: the fluent search with this parameter added
        """
        clone = self._clone()
        if clone._includes_on_relations is None:
            clone._includes_on_relations = []
        if isinstance(field, AtlanField):
            clone._includes_on_relations.append(field.atlan_field_name)
        else:
            clone._includes_on_relations.append(field)
        return clone

    def _dsl(self) -> DSL:
        """
        Translate the Atlan fluent search into an Atlan search DSL.

        :returns: an Atlan search DSL that encapsulates the fluent search
        """
        return DSL(query=self.to_query())

    def to_request(self) -> IndexSearchRequest:
        """
        Translate the Atlan fluent search into an Atlan search request.

        :returns: an Atlan search request that encapsulates the fluent search
        """
        dsl = self._dsl()
        if self._page_size:
            dsl.size = self._page_size
        if self.sorts:
            dsl.sort = self.sorts
        if self.aggregations:
            dsl.aggregations.update(self.aggregations)
        request = IndexSearchRequest(dsl=dsl)
        if self._includes_on_results:
            request.attributes = self._includes_on_results
        if self._includes_on_relations:
            request.relation_attributes = self._includes_on_relations
        return request

    def count(self, client: AtlanClient) -> int:
        """
        Return the total number of assets that will match the supplied criteria,
        using the most minimal query possible (retrieves minimal data).

        :param client: client through which to count the assets
        :returns: the count of assets that will match the supplied criteria
        """
        dsl = self._dsl()
        dsl.size = 1
        request = IndexSearchRequest(dsl=dsl)
        return client.asset.search(request).count

    def execute(self, client: AtlanClient) -> IndexSearchResults:
        """
        Run the fluent search to retrieve assets that match the supplied criteria.

        :param client: client through which to retrieve the assets
        :returns: an iterable list of assets that match the supplied criteria, lazily-fetched
        """
        return client.asset.search(self.to_request())


from pyatlan.client.atlan import AtlanClient  # noqa: E402
