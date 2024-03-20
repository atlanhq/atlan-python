# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import copy
from collections import deque
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic.v1 import Field, StrictBool, StrictInt, StrictStr, validate_arguments

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.v1.dataclasses import dataclass

from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject, SearchRequest
from pyatlan.model.enums import AtlanComparisonOperator, EntityStatus, LineageDirection
from pyatlan.model.fields.atlan_fields import AtlanField, LineageFilter
from pyatlan.utils import validate_type


class LineageRelation(AtlanObject):
    from_entity_id: Optional[str]
    to_entity_id: Optional[str]
    process_id: Optional[str]
    relationship_id: Optional[str]

    @property
    def is_full_link(self):
        return self.process_id is not None


@dataclass(frozen=True)
class DirectedPair:
    process_guid: str
    target_guid: str


@dataclass(frozen=True)
class LineageGraph:
    downstream_list: Dict[str, Dict[DirectedPair, None]]
    upstream_list: Dict[str, Dict[DirectedPair, None]]

    @classmethod
    def create(cls, relations: List[LineageRelation]) -> "LineageGraph":
        downstream_list: Dict[str, Dict[DirectedPair, None]] = {}
        upstream_list: Dict[str, Dict[DirectedPair, None]] = {}

        def add_relation(_relation: LineageRelation):
            if (
                _relation.from_entity_id
                and _relation.process_id
                and _relation.to_entity_id
            ):
                add_edges(
                    _relation.from_entity_id,
                    _relation.process_id,
                    _relation.to_entity_id,
                )

        def add_edges(source_guid: str, process_guid: str, target_guid: str):
            if source_guid not in downstream_list:
                downstream_list[source_guid] = {}
            if target_guid not in upstream_list:
                upstream_list[target_guid] = {}
            downstream_list[source_guid][
                DirectedPair(process_guid=process_guid, target_guid=target_guid)
            ] = None
            upstream_list[target_guid][
                DirectedPair(process_guid=process_guid, target_guid=source_guid)
            ] = None

        for relation in relations:
            if relation.is_full_link:
                add_relation(relation)
            else:
                raise ErrorCode.NO_GRAPH_WITH_PROCESS.exception_with_parameters()
        return cls(downstream_list=downstream_list, upstream_list=upstream_list)

    @staticmethod
    def get_asset_guids(
        guid: str, guids: Dict[str, Dict[DirectedPair, None]]
    ) -> List[str]:
        if guid in guids:
            return list({pair.target_guid: None for pair in guids[guid].keys()}.keys())
        return []

    @staticmethod
    def get_process_guids(
        guid: str, guids: Dict[str, Dict[DirectedPair, None]]
    ) -> List[str]:
        if guid in guids:
            return list({pair.process_guid: None for pair in guids[guid].keys()}.keys())
        return []

    def get_downstream_asset_guids(self, guid: str) -> List[str]:
        return LineageGraph.get_asset_guids(guid, self.downstream_list)

    def get_downstream_process_guids(self, guid: str) -> List[str]:
        return LineageGraph.get_process_guids(guid, self.downstream_list)

    def get_upstream_asset_guids(self, guid: str) -> List[str]:
        return LineageGraph.get_asset_guids(guid, self.upstream_list)

    def get_upstream_process_guids(self, guid: str) -> List[str]:
        return LineageGraph.get_process_guids(guid, self.upstream_list)

    def get_all_downstream_asset_guids_dfs(self, guid: str) -> List[str]:
        visited: Dict[str, None] = {}
        stack: deque[str] = deque()
        stack.append(guid)
        while len(stack) > 0:
            to_traverse = stack.pop()
            if to_traverse not in visited:
                visited[to_traverse] = None
                for downstream_guid in self.get_downstream_asset_guids(to_traverse):
                    if downstream_guid not in visited:
                        stack.append(downstream_guid)
        return list(visited.keys())

    def get_all_upstream_asset_guids_dfs(self, guid: str) -> List[str]:
        visited: Dict[str, None] = {}
        stack: deque[str] = deque()
        stack.append(guid)
        while len(stack) > 0:
            to_traverse = stack.pop()
            if to_traverse not in visited:
                visited[to_traverse] = None
                for upstream_guid in self.get_upstream_asset_guids(to_traverse):
                    if upstream_guid not in visited:
                        stack.append(upstream_guid)
        return list(visited.keys())


class LineageResponse(AtlanObject):
    base_entity_guid: str
    lineage_direction: LineageDirection
    lineage_depth: int
    limit: int
    offset: int
    has_more_upstream_vertices: bool
    has_more_downstream_vertices: bool
    guid_entity_map: Dict[str, Asset]
    relations: List[LineageRelation]
    vertex_children_info: Optional[Dict[str, Any]]
    graph: Optional[LineageGraph] = None

    def get_graph(self):
        if self.graph is None:
            self.graph = LineageGraph.create(self.relations)
        return self.graph

    def get_all_downstream_asset_guids_dfs(
        self, guid: Optional[str] = None
    ) -> List[str]:
        return self.get_graph().get_all_downstream_asset_guids_dfs(
            guid or self.base_entity_guid
        )

    def get_all_downstream_assets_dfs(self, guid: Optional[str] = None) -> List[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_downstream_asset_guids_dfs(
                guid or self.base_entity_guid
            )
        ]

    def get_all_upstream_asset_guids_dfs(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_all_upstream_asset_guids_dfs(
            guid or self.base_entity_guid
        )

    def get_all_upstream_assets_dfs(self, guid: Optional[str] = None) -> List[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_upstream_asset_guids_dfs(
                guid or self.base_entity_guid
            )
        ]

    def get_downstream_asset_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_downstream_asset_guids(
            guid or self.base_entity_guid
        )

    def get_downstream_assets(self, guid: Optional[str] = None) -> List[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_downstream_asset_guids(
                guid or self.base_entity_guid
            )
        ]

    def get_downstream_process_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_downstream_process_guids(
            guid or self.base_entity_guid
        )

    def get_upstream_asset_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_upstream_asset_guids(guid or self.base_entity_guid)

    def get_upstream_assets(self, guid: Optional[str] = None) -> List[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_upstream_asset_guids(
                guid or self.base_entity_guid
            )
        ]

    def get_upstream_process_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_upstream_process_guids(
            guid or self.base_entity_guid
        )


class LineageRequest(AtlanObject):
    guid: str
    depth: int = Field(default=0)
    direction: LineageDirection = Field(default=LineageDirection.BOTH)
    hide_process: bool = Field(default=True)
    allow_deleted_process: bool = Field(default=False)


class EntityFilter(AtlanObject):
    attribute_name: str = Field(
        description="Name of the attribute on which filtering should be applied."
    )
    operator: AtlanComparisonOperator = Field(
        description="Comparison that should be used when checking attribute_name"
        " against the provided attribute_value."
    )
    attribute_value: str = Field(
        description="Value that attribute_name should be compared against."
    )


class FilterList(AtlanObject):
    class Condition(str, Enum):
        AND = "AND"
        OR = "OR"

    condition: FilterList.Condition = Field(
        default=Condition.AND,
        description="Whether the criteria must all match (AND) or any matching is sufficient (OR).",
    )
    criteria: List[EntityFilter] = Field(
        description="Basis on which to compare a result for inclusion.",
        alias="criterion",
    )


class LineageListRequest(SearchRequest):
    guid: str = Field(
        description="Unique identifier of the asset for which to retrieve lineage."
    )
    depth: int = Field(
        description="Number of degrees of separation (hops) across which lineage should be fetched."
        "A depth of 1 will fetch the immediate upstream or downstream assets, while 2"
        "will also fetch the immediate upstream or downstream assets of those assets,"
        "and so on. A large integer (for example, 1000000) will therefore in effect fetch"
        "all upstream or downstream assets. (BEWARE! This could take a long time and"
        "result in a very large response payload.)"
    )
    direction: LineageDirection = Field(
        description="Indicates whether to fetch upstream lineage only, or downstream lineage only. "
        "Note that you cannot fetch both upstream and downstream at the same time."
    )
    entity_filters: Optional[FilterList] = Field(
        default=None, description="Filters to apply on entities."
    )
    entity_traversal_filters: Optional[FilterList] = Field(
        default=None,
        description="Filters to apply for skipping traversal based on entities."
        "Any sub-graphs beyond the entities filtered out by these filters will not be included"
        "in the lineage result.",
    )
    relationship_traversal_filters: Optional[FilterList] = Field(
        default=None,
        description="Filters to apply for skipping traversal based on relationships."
        "Any sub-graphs beyond the relationships filtered out by these filters will not be included"
        "in the lineage result.",
    )
    offset: Optional[int] = Field(
        default=None, description="Starting point for pagination.", alias="from"
    )
    size: Optional[int] = Field(
        default=None, description="How many results to include in each page of results."
    )
    exclude_meanings: Optional[bool] = Field(
        default=None,
        description="Whether to include assigned terms for assets (false) or not (true).",
    )
    exclude_classifications: Optional[bool] = Field(
        default=None,
        description="Whether to include classifications for assets (false) or not (true).",
    )

    @staticmethod
    def create(
        guid: str,
    ) -> "LineageListRequest":
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["guid"],
            [guid],
        )
        return LineageListRequest(
            guid=guid,
            depth=1000000,
            direction=LineageDirection.DOWNSTREAM,
            offset=0,
            size=10,
            exclude_meanings=True,
            exclude_classifications=True,
        )  # type: ignore[call-arg]


class FluentLineage:
    """Lineage abstraction mechanism, to simplify the most common lineage requests against Atlan
    (removing the need to understand the guts of Elastic)."""

    ACTIVE: LineageFilter = Asset.STATUS.in_lineage.eq(EntityStatus.ACTIVE)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        *,
        starting_guid: StrictStr,
        depth: StrictInt = 1000000,
        direction: LineageDirection = LineageDirection.DOWNSTREAM,
        size: StrictInt = 10,
        exclude_meanings: StrictBool = True,
        exclude_atlan_tags: StrictBool = True,
        includes_on_results: Optional[
            Union[List[str], str, List[AtlanField], AtlanField]
        ] = None,
        includes_in_results: Optional[Union[List[LineageFilter], LineageFilter]] = None,
        includes_condition: FilterList.Condition = FilterList.Condition.AND,
        where_assets: Optional[Union[List[LineageFilter], LineageFilter]] = None,
        assets_condition: FilterList.Condition = FilterList.Condition.AND,
        where_relationships: Optional[Union[List[LineageFilter], LineageFilter]] = None,
        relationships_condition: FilterList.Condition = FilterList.Condition.AND,
    ):
        """Create a FluentLineage request.
        :param starting_guid: unique identifier (GUID) of the asset from which to start lineage
        :param depth: number of degrees of separation (hops) across which lineage should be fetched
        :param direction: direction of lineage to fetch (upstream or downstream)
        :param size: number of results to retrieve
        :param exclude_meanings: whether to include assigned terms for assets (False) or not (True)
        :param exclude_atlan_tags: whether to include Atlan tags for assets (False) or not (True)
        :param includes_on_results: attributes to retrieve for each asset in the lineage results
        :param includes_in_results: Assets to include in the results. Any assets not matching these filters will not
        be included in the results, but will still be traversed in the lineage so that any assets beyond them are still
        considered for inclusion in the results
        :param includes_condition: whether the `includes_in_results` criteria
        should be combined (AND) or any matching is sufficient (OR)
        :param where_assets: filters to apply on assets. Any assets excluded
        by the filters will exclude all assets beyond, as well
        :param assets_condition: whether the `where_assets` criteria
        should be combined (AND) or any matching is sufficient (OR)
        :param where_relationships: filters to apply on relationships.
        Any relationships excluded by the filters will exclude all assets and relationships beyond, as well
        :param relationships_condition: whether the `where_relationships` criteria
        should be combined (AND) or any matching is sufficient (OR)
        """

        self._depth: int = depth
        self._direction: LineageDirection = direction
        self._exclude_atlan_tags: bool = exclude_atlan_tags
        self._exclude_meanings: bool = exclude_meanings
        self._includes_on_results: List[Union[str, AtlanField]] = self._to_list(
            includes_on_results
        )
        self._includes_in_results: List[LineageFilter] = self._to_list(
            includes_in_results
        )
        self._includes_condition: FilterList.Condition = includes_condition
        self._size: int = size
        self._starting_guid = starting_guid
        self._where_assets: List[LineageFilter] = self._to_list(where_assets)
        self._assets_condition: FilterList.Condition = assets_condition
        self._where_relationships: List[LineageFilter] = self._to_list(
            where_relationships
        )
        self._relationships_condition: FilterList.Condition = relationships_condition

    @staticmethod
    def _to_list(value):
        return [] if value is None else value if isinstance(value, list) else [value]

    def _clone(self) -> "FluentLineage":
        """
        Returns a copy of the current FluentSearch that's ready for further operations.

        :returns: copy of the current FluentSearch
        """
        return copy.deepcopy(self)

    def depth(self, depth: StrictInt) -> "FluentLineage":
        """Adds the depth to traverse the lineage.
        :param depth: number of degrees of separation (hops) across which lineage should be fetched
        :returns: the FluentLineage with this depth criterion added"""
        validate_type(name="depth", _type=int, value=depth)
        clone = self._clone()
        clone._depth = depth
        return clone

    def direction(self, direction: LineageDirection) -> "FluentLineage":
        """Adds the direction to traverse the lineage.
        :param direction: direction of lineage to fetch (upstream or downstream)
        :returns: the FluentLineage with this direction criterion added"""
        validate_type(name="direction", _type=LineageDirection, value=direction)
        clone = self._clone()
        clone._direction = direction
        return clone

    def size(self, size: StrictInt) -> "FluentLineage":
        """Adds the size to traverse the lineage.
        :param size: number of results to retrieve
        :returns: the FluentLineage with this size criterion added"""
        validate_type(name="size", _type=int, value=size)
        clone = self._clone()
        clone._size = size
        return clone

    def exclude_atlan_tags(self, exclude_atlan_tags: StrictBool) -> "FluentLineage":
        """Adds the exclude_atlan_tags to traverse the lineage.
        :param exclude_atlan_tags: whether to include Atlan tags for assets (False) or not (True)
        :returns: the FluentLineage with this exclude_atlan_tags criterion added
        """
        validate_type(name="exclude_atlan_tags", _type=bool, value=exclude_atlan_tags)
        clone = self._clone()
        clone._exclude_atlan_tags = exclude_atlan_tags
        return clone

    def exclude_meanings(self, exclude_meanings: StrictBool) -> "FluentLineage":
        """Adds the exclude_meanings to traverse the lineage.
        :param exclude_meanings: whether to include assigned terms for assets (False) or not (True)
        :returns: the FluentLineage with this exclude_meanings criterion added"""
        validate_type(name="exclude_meanings", _type=bool, value=exclude_meanings)
        clone = self._clone()
        clone._exclude_meanings = exclude_meanings
        return clone

    def include_on_results(self, field: Union[str, AtlanField]) -> "FluentLineage":
        """Adds the include_on_results to traverse the lineage.
        :param field: attributes to retrieve for each asset in the lineage results
        :returns: the FluentLineage with this include_on_results criterion added"""
        validate_type(name="field", _type=(str, AtlanField), value=field)
        clone = self._clone()
        clone._includes_on_results.append(field)
        return clone

    def include_in_results(self, lineage_filter: LineageFilter) -> "FluentLineage":
        """
        Adds the include_on_results to traverse the lineage.
        :param lineage_filter: Assets to include in the results. Any assets not matching this filters will not be
        included in the results, but will still be traversed in the lineage so that any assets beyond them are still
        considered for inclusion in the results
        :returns: the FluentLineage with this include_in_results criterion added
        """
        validate_type(name="lineage_filter", _type=LineageFilter, value=lineage_filter)
        clone = self._clone()
        clone._includes_in_results.append(lineage_filter)
        return clone

    def includes_condition(
        self, includes_condition: FilterList.Condition
    ) -> "FluentLineage":
        """
        Adds the filter condition to `include_on_results`.
        :param includes_condition: whether the `includes_in_results`
        criteria should be combined (AND) or any matching is sufficient (OR)
        :returns: the FluentLineage with this includes_condition criterion added
        """
        validate_type(
            name="includes_condition",
            _type=FilterList.Condition,
            value=includes_condition,
        )
        clone = self._clone()
        clone._includes_condition = includes_condition
        return clone

    def where_assets(self, lineage_filter: LineageFilter) -> "FluentLineage":
        """
        Adds a filters to apply on assets.
        :param lineage_filter: a filter to apply on assets. Any assets excluded by the filters will exclude all
        assets beyond, as well
        :returns: the FluentLineage with this where_assets criterion added
        """
        validate_type(name="lineage_filter", _type=LineageFilter, value=lineage_filter)
        clone = self._clone()
        clone._where_assets.append(lineage_filter)
        return clone

    def assets_condition(
        self, assets_condition: FilterList.Condition
    ) -> "FluentLineage":
        """
        Adds the filter condition to `where_assets`.
        :param assets_condition: whether the `where_assets`
        criteria should be combined (AND) or any matching is sufficient (OR)
        :returns: the FluentLineage with this assets_condition criterion added
        """
        validate_type(
            name="assets_condition",
            _type=FilterList.Condition,
            value=assets_condition,
        )
        clone = self._clone()
        clone._assets_condition = assets_condition
        return clone

    def where_relationships(self, lineage_filter: LineageFilter) -> "FluentLineage":
        """Filters to apply on relationships.
        :param lineage_filter: any relationships excluded by the filter will exclude all assets and
        relationships beyond, as well.
        :returns: the FluentLineage with this where_relationships criterion added"""
        validate_type(name="lineage_filter", _type=LineageFilter, value=lineage_filter)
        clone = self._clone()
        clone._where_relationships.append(lineage_filter)
        return clone

    def relationships_condition(
        self, relationships_condition: FilterList.Condition
    ) -> "FluentLineage":
        """
        Adds the filter condition to `where_relationships`.
        :param relationships_condition: whether the `where_relationships`
        criteria should be combined (AND) or any matching is sufficient (OR)
        :returns: the FluentLineage with this relationships_condition criterion added
        """
        validate_type(
            name="relationships_condition",
            _type=FilterList.Condition,
            value=relationships_condition,
        )
        clone = self._clone()
        clone._relationships_condition = relationships_condition
        return clone

    @property
    def request(self) -> LineageListRequest:
        """
        :returns: the LineageListRequest that encapsulates information specified in this FluentLineage
        """
        request = LineageListRequest.create(guid=self._starting_guid)
        if self._depth:
            request.depth = self._depth
        if self._direction:
            request.direction = self._direction
        if self._exclude_atlan_tags is not None:
            request.exclude_classifications = self._exclude_atlan_tags
        if self._exclude_meanings is not None:
            request.exclude_meanings = self._exclude_meanings
        if self._includes_in_results:
            criteria = [
                EntityFilter(
                    attribute_name=_filter.field.internal_field_name,
                    operator=_filter.operator,
                    attribute_value=_filter.value,
                )
                for _filter in self._includes_in_results
            ]
            request.entity_filters = FilterList(condition=self._includes_condition, criteria=criteria)  # type: ignore
        if self._includes_on_results:
            request.attributes = [
                field.atlan_field_name if isinstance(field, AtlanField) else field
                for field in self._includes_on_results
            ]
        if self._size:
            request.size = self._size
        if self._where_assets:
            criteria = [
                EntityFilter(
                    attribute_name=_filter.field.internal_field_name,
                    operator=_filter.operator,
                    attribute_value=_filter.value,
                )
                for _filter in self._where_assets
            ]
            request.entity_traversal_filters = FilterList(
                condition=self._assets_condition, criteria=criteria
            )  # type: ignore[call-arg]
        if self._where_relationships:
            criteria = [
                EntityFilter(
                    attribute_name=_filter.field.internal_field_name,
                    operator=_filter.operator,
                    attribute_value=_filter.value,
                )
                for _filter in self._where_relationships
            ]
            request.relationship_traversal_filters = FilterList(
                condition=self._relationships_condition, criteria=criteria
            )  # type: ignore[call-arg]
        return request
