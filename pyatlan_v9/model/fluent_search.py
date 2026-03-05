# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""V9-native FluentSearch that produces msgspec IndexSearchRequest."""

from __future__ import annotations

import copy
import dataclasses
import logging
from typing import TYPE_CHECKING, Dict, List, Optional, TypeVar, Union

from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.assets import Referenceable, Tag
from pyatlan.model.enums import EntityStatus
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.search import (
    Bool,
    Query,
    SortItem,
    SpanNear,
    SpanOr,
    SpanTerm,
    SpanWithin,
    Term,
)
from pyatlan_v9.model.search import DSL, IndexSearchRequest

if TYPE_CHECKING:
    from pyatlan_v9.client.aio.atlan import AsyncAtlanClient
    from pyatlan_v9.client.atlan import AtlanClient

LOGGER = logging.getLogger(__name__)

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
        return Referenceable.STATUS.eq(EntityStatus.ACTIVE.value)

    @staticmethod
    def archived_assets() -> Query:
        return Referenceable.STATUS.eq(EntityStatus.DELETED.value)

    @staticmethod
    def asset_type(of: type) -> Query:
        return Referenceable.TYPE_NAME.eq(of.__name__)

    @staticmethod
    def asset_types(one_of: List[type]) -> Query:
        return Referenceable.TYPE_NAME.within(list(map(lambda x: x.__name__, one_of)))

    @staticmethod
    def super_types(one_of: Union[type, List[type]]) -> Query:
        if isinstance(one_of, list):
            return Referenceable.SUPER_TYPE_NAMES.within(
                list(map(lambda x: x.__name__, one_of))
            )
        return Referenceable.SUPER_TYPE_NAMES.eq(one_of.__name__)

    @staticmethod
    def tagged(
        client: AtlanClient,
        with_one_of: Optional[List[str]] = None,
        directly: bool = False,
    ) -> Query:
        values: List[str] = []
        if with_one_of:
            for name in with_one_of:
                if tag_id := client.atlan_tag_cache.get_id_for_name(name):
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
    def tagged_with_value(
        client: "AtlanClient",
        atlan_tag_name: str,
        value: str,
        directly: bool = False,
        source_tag_qualified_name: Optional[str] = None,
    ) -> Query:
        big_spans: List = []
        little_spans: List = []
        tag_id = client.atlan_tag_cache.get_id_for_name(atlan_tag_name) or ""
        synced_tags = [
            tag
            for tag in (
                FluentSearch()
                .select()
                .where(Tag.MAPPED_CLASSIFICATION_NAME.eq(tag_id))
                .execute(client=client)
            )
        ]
        if len(synced_tags) > 1 and source_tag_qualified_name is None:
            synced_tag_qn = synced_tags[0].qualified_name or ""
            LOGGER.warning(
                "Multiple mapped source-synced tags found for tag %s -- using only the first: %s. "
                "You can specify the `source_tag_qualified_name` so we can match to the specific one.",
                atlan_tag_name,
                synced_tag_qn,
            )
        elif synced_tags:
            synced_tag_qn = (
                source_tag_qualified_name or synced_tags[0].qualified_name or ""
            )
        else:
            synced_tag_qn = "NON_EXISTENT"

        little_spans.append(
            SpanTerm(field="__classificationsText.text", value="tagAttachmentValue")
        )
        for token in value.split(" "):
            little_spans.append(
                SpanTerm(field="__classificationsText.text", value=token)
            )
        span_or_clauses = [
            SpanTerm(field="__classificationsText.text", value="tagAttachmentKey"),
            SpanTerm(field="__classificationsText.text", value="sourceTagName"),
            SpanTerm(
                field="__classificationsText.text", value="sourceTagQualifiedName"
            ),
            SpanTerm(field="__classificationsText.text", value="sourceTagGuid"),
            SpanTerm(
                field="__classificationsText.text", value="sourceTagConnectorName"
            ),
            SpanTerm(field="__classificationsText.text", value="isSourceTagSynced"),
            SpanTerm(
                field="__classificationsText.text", value="sourceTagSyncTimestamp"
            ),
            SpanTerm(field="__classificationsText.text", value="sourceTagValue"),
        ]
        little_spans.append(SpanOr(clauses=span_or_clauses))  # type: ignore

        big_spans.append(SpanTerm(field="__classificationsText.text", value=tag_id))
        big_spans.append(
            SpanTerm(field="__classificationsText.text", value=synced_tag_qn)
        )

        span = SpanWithin(
            little=SpanNear(clauses=little_spans, slop=0, in_order=True),
            big=SpanNear(clauses=big_spans, slop=10000000, in_order=True),
        )

        if directly:
            return (
                FluentSearch()
                .where(Referenceable.ATLAN_TAGS.eq(tag_id))
                .where(span)
                .to_query()
            )
        return (
            FluentSearch()
            .where_some(Referenceable.ATLAN_TAGS.eq(tag_id))
            .where_some(Referenceable.PROPAGATED_ATLAN_TAGS.eq(tag_id))
            .min_somes(1)
            .where(span)
            .to_query()
        )

    @staticmethod
    async def tagged_with_value_async(
        client: "AsyncAtlanClient",
        atlan_tag_name: str,
        value: str,
        directly: bool = False,
        source_tag_qualified_name: Optional[str] = None,
    ) -> Query:
        big_spans: List = []
        little_spans: List = []
        tag_id = await client.atlan_tag_cache.get_id_for_name(atlan_tag_name) or ""
        synced_tags = [
            tag
            async for tag in (
                await FluentSearch()
                .select()
                .where(Tag.MAPPED_CLASSIFICATION_NAME.eq(tag_id))
                .execute_async(client=client)
            )
        ]
        if len(synced_tags) > 1 and source_tag_qualified_name is None:
            synced_tag_qn = synced_tags[0].qualified_name or ""
            LOGGER.warning(
                "Multiple mapped source-synced tags found for tag %s -- using only the first: %s. "
                "You can specify the `source_tag_qualified_name` so we can match to the specific one.",
                atlan_tag_name,
                synced_tag_qn,
            )
        elif synced_tags:
            synced_tag_qn = (
                source_tag_qualified_name or synced_tags[0].qualified_name or ""
            )
        else:
            synced_tag_qn = "NON_EXISTENT"

        little_spans.append(
            SpanTerm(field="__classificationsText.text", value="tagAttachmentValue")
        )
        for token in value.split(" "):
            little_spans.append(
                SpanTerm(field="__classificationsText.text", value=token)
            )
        span_or_clauses = [
            SpanTerm(field="__classificationsText.text", value="tagAttachmentKey"),
            SpanTerm(field="__classificationsText.text", value="sourceTagName"),
            SpanTerm(
                field="__classificationsText.text", value="sourceTagQualifiedName"
            ),
            SpanTerm(field="__classificationsText.text", value="sourceTagGuid"),
            SpanTerm(
                field="__classificationsText.text", value="sourceTagConnectorName"
            ),
            SpanTerm(field="__classificationsText.text", value="isSourceTagSynced"),
            SpanTerm(
                field="__classificationsText.text", value="sourceTagSyncTimestamp"
            ),
            SpanTerm(field="__classificationsText.text", value="sourceTagValue"),
        ]
        little_spans.append(SpanOr(clauses=span_or_clauses))  # type: ignore

        big_spans.append(SpanTerm(field="__classificationsText.text", value=tag_id))
        big_spans.append(
            SpanTerm(field="__classificationsText.text", value=synced_tag_qn)
        )

        span = SpanWithin(
            little=SpanNear(clauses=little_spans, slop=0, in_order=True),
            big=SpanNear(clauses=big_spans, slop=10000000, in_order=True),
        )

        if directly:
            return (
                FluentSearch()
                .where(Referenceable.ATLAN_TAGS.eq(tag_id))
                .where(span)
                .to_query()
            )
        return (
            FluentSearch()
            .where_some(Referenceable.ATLAN_TAGS.eq(tag_id))
            .where_some(Referenceable.PROPAGATED_ATLAN_TAGS.eq(tag_id))
            .min_somes(1)
            .where(span)
            .to_query()
        )

    @staticmethod
    def assigned_term(qualified_names: Optional[List[str]] = None) -> Query:
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
        return copy.deepcopy(self)

    def where(self: SelfQuery, query: Query) -> SelfQuery:
        clone = self._clone()
        if clone.wheres is None:
            clone.wheres = []
        clone.wheres.append(query)
        return clone

    def where_not(self: SelfQuery, query: Query) -> SelfQuery:
        clone = self._clone()
        if clone.where_nots is None:
            clone.where_nots = []
        clone.where_nots.append(query)
        return clone

    def where_some(self: SelfQuery, query: Query) -> SelfQuery:
        clone = self._clone()
        if clone.where_somes is None:
            clone.where_somes = []
        clone.where_somes.append(query)
        return clone

    def min_somes(self: SelfQuery, minimum: int) -> SelfQuery:
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


@dataclasses.dataclass
class FluentSearch(CompoundQuery):
    """
    V9-native FluentSearch that produces msgspec IndexSearchRequest.
    """

    sorts: Optional[List[SortItem]] = None
    aggregations: Optional[Dict[str, Aggregation]] = None
    _page_size: Optional[int] = None
    _includes_on_results: Optional[List[str]] = None
    _includes_on_relations: Optional[List[str]] = None

    @classmethod
    def select(cls, include_archived=False) -> "FluentSearch":
        wheres = [Term.with_super_type_names("Asset")]
        if not include_archived:
            wheres.append(Term.with_state("ACTIVE"))
        return cls(wheres=wheres)

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
        _include_relationship_attributes: Optional[bool] = False,
        _enable_full_restriction: Optional[bool] = False,
    ):
        super().__init__(wheres, where_nots, where_somes, _min_somes)
        self.sorts = sorts
        self.aggregations = aggregations
        self._page_size = _page_size
        self._includes_on_results = _includes_on_results
        self._includes_on_relations = _includes_on_relations
        self._include_relationship_attributes = _include_relationship_attributes
        self._enable_full_restriction = _enable_full_restriction

    def _clone(self) -> "FluentSearch":
        return copy.deepcopy(self)

    def sort(self, by: SortItem) -> "FluentSearch":
        clone = self._clone()
        if clone.sorts is None:
            clone.sorts = []
        clone.sorts.append(by)
        return clone

    def aggregate(self, key: str, aggregation: Aggregation) -> "FluentSearch":
        clone = self._clone()
        if clone.aggregations is None:
            clone.aggregations = {}
        clone.aggregations[key] = aggregation
        return clone

    def page_size(self, size: int) -> "FluentSearch":
        clone = self._clone()
        clone._page_size = size
        return clone

    def include_on_results(self, field: Union[str, AtlanField]) -> "FluentSearch":
        clone = self._clone()
        if clone._includes_on_results is None:
            clone._includes_on_results = []
        if isinstance(field, AtlanField):
            clone._includes_on_results.append(field.atlan_field_name)
        else:
            clone._includes_on_results.append(field)
        return clone

    def include_on_relations(self, field: Union[str, AtlanField]) -> "FluentSearch":
        clone = self._clone()
        if clone._includes_on_relations is None:
            clone._includes_on_relations = []
        if isinstance(field, AtlanField):
            clone._includes_on_relations.append(field.atlan_field_name)
        else:
            clone._includes_on_relations.append(field)
        return clone

    def include_relationship_attributes(self, include: bool) -> "FluentSearch":
        clone = self._clone()
        clone = self.include_on_relations("name")
        clone._include_relationship_attributes = include
        return clone

    def enable_full_restriction(self, enable: bool) -> "FluentSearch":
        clone = self._clone()
        clone._enable_full_restriction = enable
        return clone

    def _dsl(self) -> DSL:
        return DSL(query=self.to_query())

    def to_request(self) -> IndexSearchRequest:
        dsl = self._dsl()
        if self._page_size is not None:
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
        if self._include_relationship_attributes:
            request.include_relationship_attributes = (
                self._include_relationship_attributes
            )
        if self._enable_full_restriction:
            request.enable_full_restriction = self._enable_full_restriction
        return request

    def count(self, client: "AtlanClient") -> int:
        dsl = self._dsl()
        dsl.size = 1
        request = IndexSearchRequest(dsl=dsl)
        return client.asset.search(request).count

    def execute(self, client: "AtlanClient", bulk: bool = False):
        return client.asset.search(criteria=self.to_request(), bulk=bulk)

    async def execute_async(self, client: "AsyncAtlanClient", bulk: bool = False):
        return await client.asset.search(criteria=self.to_request(), bulk=bulk)
