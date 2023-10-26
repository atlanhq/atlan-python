# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import copy
from collections import deque
from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject, SearchRequest
from pyatlan.model.enums import AtlanComparisonOperator, LineageDirection
from pyatlan.model.fields.atlan_fields import AtlanField, LineageFilter


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
    downstream_list: dict[str, dict[DirectedPair, None]]
    upstream_list: dict[str, dict[DirectedPair, None]]

    @classmethod
    def create(cls, relations: list[LineageRelation]) -> "LineageGraph":
        downstream_list: dict[str, dict[DirectedPair, None]] = {}
        upstream_list: dict[str, dict[DirectedPair, None]] = {}

        def add_relation(relation: LineageRelation):
            if (
                relation.from_entity_id
                and relation.process_id
                and relation.to_entity_id
            ):
                add_edges(
                    relation.from_entity_id, relation.process_id, relation.to_entity_id
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
        guid: str, guids: dict[str, dict[DirectedPair, None]]
    ) -> list[str]:
        if guid in guids:
            return list({pair.target_guid: None for pair in guids[guid].keys()}.keys())
        return []

    @staticmethod
    def get_process_guids(
        guid: str, guids: dict[str, dict[DirectedPair, None]]
    ) -> list[str]:
        if guid in guids:
            return list({pair.process_guid: None for pair in guids[guid].keys()}.keys())
        return []

    def get_downstream_asset_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_asset_guids(guid, self.downstream_list)

    def get_downstream_process_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_process_guids(guid, self.downstream_list)

    def get_upstream_asset_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_asset_guids(guid, self.upstream_list)

    def get_upstream_process_guids(self, guid: str) -> list[str]:
        return LineageGraph.get_process_guids(guid, self.upstream_list)

    def get_all_downstream_asset_guids_dfs(self, guid: str) -> list[str]:
        visited: dict[str, None] = {}
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

    def get_all_upstream_asset_guids_dfs(self, guid: str) -> list[str]:
        visited: dict[str, None] = {}
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
    guid_entity_map: dict[str, Asset]
    relations: list[LineageRelation]
    vertex_children_info: Optional[dict[str, Any]]
    graph: Optional[LineageGraph] = None

    def get_graph(self):
        if self.graph is None:
            self.graph = LineageGraph.create(self.relations)
        return self.graph

    def get_all_downstream_asset_guids_dfs(
        self, guid: Optional[str] = None
    ) -> list[str]:
        return self.get_graph().get_all_downstream_asset_guids_dfs(
            guid or self.base_entity_guid
        )

    def get_all_downstream_assets_dfs(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_downstream_asset_guids_dfs(
                guid or self.base_entity_guid
            )
        ]

    def get_all_upstream_asset_guids_dfs(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_all_upstream_asset_guids_dfs(
            guid or self.base_entity_guid
        )

    def get_all_upstream_assets_dfs(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_upstream_asset_guids_dfs(
                guid or self.base_entity_guid
            )
        ]

    def get_downstream_asset_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_downstream_asset_guids(
            guid or self.base_entity_guid
        )

    def get_downstream_assets(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_downstream_asset_guids(
                guid or self.base_entity_guid
            )
        ]

    def get_downstream_process_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_downstream_process_guids(
            guid or self.base_entity_guid
        )

    def get_upstream_asset_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_upstream_asset_guids(guid or self.base_entity_guid)

    def get_upstream_assets(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_upstream_asset_guids(
                guid or self.base_entity_guid
            )
        ]

    def get_upstream_process_guids(self, guid: Optional[str] = None) -> list[str]:
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
    condition: str = Field(
        description="Whether the criteria must all match (AND) or any matching is sufficient (OR)."
    )
    criteria: list[EntityFilter] = Field(
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
        description="Filters to apply on entities."
    )
    entity_traversal_filters: Optional[FilterList] = Field(
        description="Filters to apply for skipping traversal based on entities."
        "Any sub-graphs beyond the entities filtered out by these filters will not be included"
        "in the lineage result."
    )
    relationship_traversal_filters: Optional[FilterList] = Field(
        description="Filters to apply for skipping traversal based on relationships."
        "Any sub-graphs beyond the relationships filtered out by these filters will not be included"
        "in the lineage result."
    )
    offset: Optional[int] = Field(
        description="Starting point for pagination.", alias="from"
    )
    size: Optional[int] = Field(
        description="How many results to include in each page of results."
    )
    exclude_meanings: Optional[bool] = Field(
        description="Whether to include assigned terms for assets (false) or not (true)."
    )
    exclude_classifications: Optional[bool] = Field(
        description="Whether to include classifications for assets (false) or not (true)."
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
        )


class AltanField:
    pass


class FluentLineage:
    """Lineage abstraction mechanism, to simplify the most common lineage requests against Atlan
    (removing the need to understand the guts of Elastic)."""

    def __init__(
        self,
        starting_guid: str,
        depth: int = 1000000,
        direction: LineageDirection = LineageDirection.DOWNSTREAM,
        size: int = 10,
        exclude_meanings: bool = True,
        exclude_classifications: bool = True,
    ):
        self._depth: int = depth
        self._direction: LineageDirection = direction
        self._exclude_classifications: bool = exclude_classifications
        self._exclude_meanings: bool = exclude_meanings
        self._includes_in_results: list[LineageFilter] = []
        self._include_on_results: list[AtlanField] = []
        self._size: int = size
        self._starting_guid = starting_guid
        self._where_assets: list[LineageFilter] = []
        self._where_relationships: list[LineageFilter] = []

    def _clone(self) -> "FluentLineage":
        """
        Returns a copy of the current FluentSearch that's ready for further operations.

        :returns: copy of the current FluentSearch
        """
        return copy.deepcopy(self)

    def includes_in_results(self, lineage_filter: LineageFilter):
        """Assets to include in the results. Any assets not matching these filters will not be included in the results,
        but will still be traversed in the lineage so that any assets beyond them are still considered for inclusion
        in the results."""
        clone = self._clone()
        clone._includes_in_results.append(lineage_filter)
        return clone

    def include_on_results(self, field: AtlanField):
        """Attributes to retrieve for each asset in the lineage results."""
        clone = self._clone()
        clone._include_on_results.append(field)

    def where_assets(self, lineage_filter: LineageFilter):
        """Filters to apply on assets. Any assets excluded by the filters will exclude all assets beyond, as well."""
        clone = self._clone()
        clone._where_assets.append(lineage_filter)
        return clone

    def where_relationships(self, lineage_filter: LineageFilter):
        """Filters to apply on relationships. Any relationships excluded by the filters will exclude all assets and
        relationships beyond, as well."""
        clone = self._clone()
        clone._where_relationships.append(lineage_filter)
        return clone

    @property
    def request(self) -> LineageListRequest:
        request = LineageListRequest.create(guid=self._starting_guid)
        if self._depth:
            request.depth = self._depth
        if self._direction:
            request.direction = self._direction
        if self._exclude_classifications is not None:
            request.exclude_classifications = self._exclude_classifications
        if self._exclude_meanings is not None:
            request.exclude_meanings = self._exclude_meanings
        if self._includes_in_results:
            criteria = [
                EntityFilter(
                    attribute_name=filter.field.internal_field_name,
                    operator=filter.operator,
                    attribute_value=filter.value,
                )
                for filter in self._includes_in_results
            ]
            request.entity_filters = FilterList(condition="AND", criteria=criteria)
        if self._include_on_results:
            request.attributes = [
                field.atlan_field_name for field in self._include_on_results
            ]
        if self._size:
            request.size = self._size
        if self._where_assets:
            criteria = [
                EntityFilter(
                    attribute_name=filter.field.internal_field_name,
                    operator=filter.operator,
                    attribute_value=filter.value,
                )
                for filter in self._where_assets
            ]
            request.entity_traversal_filters = FilterList(
                condition="AND", criteria=criteria
            )
        if self._where_relationships:
            criteria = [
                EntityFilter(
                    attribute_name=filter.field.internal_field_name,
                    operator=filter.operator,
                    attribute_value=filter.value,
                )
                for filter in self._where_relationships
            ]
            request.relationship_traversal_filters = FilterList(
                condition="AND", criteria=criteria
            )
        return request
