# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import copy
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import msgspec

from pyatlan.model.enums import AtlanComparisonOperator, LineageDirection
from pyatlan.model.fields.atlan_fields import AtlanField, LineageFilter

# ---------------------------------------------------------------------------
# Re-export plain dataclass / frozen-dataclass classes from legacy.
# These are NOT Pydantic models — no migration needed.
# ---------------------------------------------------------------------------
from pyatlan.model.lineage import DirectedPair, LineageGraph  # noqa: F401
from pyatlan.utils import validate_type

# ---------------------------------------------------------------------------
# msgspec.Struct models — genuine Pydantic → msgspec migrations
# ---------------------------------------------------------------------------


class LineageRelation(msgspec.Struct, kw_only=True):
    from_entity_id: Optional[str] = None
    to_entity_id: Optional[str] = None
    process_id: Optional[str] = None
    relationship_id: Optional[str] = None

    @property
    def is_full_link(self):
        return self.process_id is not None


class LineageResponse(msgspec.Struct, kw_only=True):
    base_entity_guid: str
    lineage_direction: LineageDirection
    lineage_depth: int
    limit: int
    offset: int
    has_more_upstream_vertices: bool
    has_more_downstream_vertices: bool
    guid_entity_map: Dict[str, Any]  # Dict[str, Asset]
    relations: List[LineageRelation]
    vertex_children_info: Optional[Dict[str, Any]] = None
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

    def get_all_downstream_assets_dfs(self, guid: Optional[str] = None) -> List[Any]:
        return [
            self.guid_entity_map[g]
            for g in self.get_graph().get_all_downstream_asset_guids_dfs(
                guid or self.base_entity_guid
            )
        ]

    def get_all_upstream_asset_guids_dfs(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_all_upstream_asset_guids_dfs(
            guid or self.base_entity_guid
        )

    def get_all_upstream_assets_dfs(self, guid: Optional[str] = None) -> List[Any]:
        return [
            self.guid_entity_map[g]
            for g in self.get_graph().get_all_upstream_asset_guids_dfs(
                guid or self.base_entity_guid
            )
        ]

    def get_downstream_asset_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_downstream_asset_guids(
            guid or self.base_entity_guid
        )

    def get_downstream_assets(self, guid: Optional[str] = None) -> List[Any]:
        return [
            self.guid_entity_map[g]
            for g in self.get_graph().get_downstream_asset_guids(
                guid or self.base_entity_guid
            )
        ]

    def get_downstream_process_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_downstream_process_guids(
            guid or self.base_entity_guid
        )

    def get_upstream_asset_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_upstream_asset_guids(guid or self.base_entity_guid)

    def get_upstream_assets(self, guid: Optional[str] = None) -> List[Any]:
        return [
            self.guid_entity_map[g]
            for g in self.get_graph().get_upstream_asset_guids(
                guid or self.base_entity_guid
            )
        ]

    def get_upstream_process_guids(self, guid: Optional[str] = None) -> List[str]:
        return self.get_graph().get_upstream_process_guids(
            guid or self.base_entity_guid
        )


class LineageRequest(msgspec.Struct, kw_only=True):
    guid: str
    depth: int = 0
    direction: LineageDirection = LineageDirection.BOTH
    hide_process: bool = True
    allow_deleted_process: bool = False


class EntityFilter(msgspec.Struct, kw_only=True):
    attribute_name: str
    operator: AtlanComparisonOperator
    attribute_value: str


class FilterList(msgspec.Struct, kw_only=True):
    class Condition(str, Enum):
        AND = "AND"
        OR = "OR"

    condition: Condition = Condition.AND
    criteria: List[EntityFilter] = msgspec.field(default_factory=list, name="criterion")


class LineageListRequest(msgspec.Struct, kw_only=True):
    guid: str
    depth: int = 0
    direction: LineageDirection = LineageDirection.DOWNSTREAM
    entity_filters: Optional[FilterList] = None
    entity_traversal_filters: Optional[FilterList] = None
    relation_attributes: Optional[List[str]] = None
    relationship_traversal_filters: Optional[FilterList] = None
    attributes: Optional[List[str]] = msgspec.field(default_factory=list)
    offset: Optional[int] = msgspec.field(default=None, name="from")
    size: Optional[int] = None
    exclude_meanings: Optional[bool] = None
    exclude_classifications: Optional[bool] = None
    immediate_neighbors: Optional[bool] = msgspec.field(
        default=None, name="immediateNeighbours"
    )

    @staticmethod
    def create(guid: str) -> "LineageListRequest":
        from pyatlan.utils import validate_required_fields

        validate_required_fields(["guid"], [guid])
        return LineageListRequest(
            guid=guid,
            depth=1000000,
            direction=LineageDirection.DOWNSTREAM,
            offset=0,
            size=10,
            exclude_meanings=True,
            exclude_classifications=True,
        )


# ---------------------------------------------------------------------------
# FluentLineage — plain class that constructs v9 msgspec model objects.
# Kept in v9 (not re-exported from legacy) because it builds v9
# EntityFilter / FilterList / LineageListRequest instances.
# ---------------------------------------------------------------------------


class FluentLineage:
    """Lineage abstraction mechanism, to simplify the most common lineage requests against Atlan
    (removing the need to understand the guts of Elastic)."""

    ACTIVE: LineageFilter = None  # type: ignore[assignment]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def __init__(
        self,
        *,
        starting_guid: str,
        depth: int = 1000000,
        direction: LineageDirection = LineageDirection.DOWNSTREAM,
        size: int = 10,
        exclude_meanings: bool = True,
        exclude_atlan_tags: bool = True,
        immediate_neighbors: bool = False,
        includes_on_results: Optional[
            Union[List[str], str, List[AtlanField], AtlanField]
        ] = None,
        includes_in_results: Optional[Union[List[LineageFilter], LineageFilter]] = None,
        includes_on_relations: Optional[
            Union[List[str], str, List[AtlanField], AtlanField]
        ] = None,
        includes_condition: FilterList.Condition = FilterList.Condition.AND,
        where_assets: Optional[Union[List[LineageFilter], LineageFilter]] = None,
        assets_condition: FilterList.Condition = FilterList.Condition.AND,
        where_relationships: Optional[Union[List[LineageFilter], LineageFilter]] = None,
        relationships_condition: FilterList.Condition = FilterList.Condition.AND,
    ):
        self._depth: int = depth
        self._direction: LineageDirection = direction
        self._exclude_atlan_tags: bool = exclude_atlan_tags
        self._exclude_meanings: bool = exclude_meanings
        self._immediate_neighbors: bool = immediate_neighbors
        self._includes_on_results: List[Union[str, AtlanField]] = self._to_list(
            includes_on_results
        )
        self._includes_in_results: List[LineageFilter] = self._to_list(
            includes_in_results
        )
        self._includes_on_relations: List[Union[str, AtlanField]] = self._to_list(
            includes_on_relations
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
        return copy.deepcopy(self)

    def depth(self, depth: int) -> "FluentLineage":
        validate_type(name="depth", _type=int, value=depth)
        clone = self._clone()
        clone._depth = depth
        return clone

    def direction(self, direction: LineageDirection) -> "FluentLineage":
        validate_type(name="direction", _type=LineageDirection, value=direction)
        clone = self._clone()
        clone._direction = direction
        return clone

    def size(self, size: int) -> "FluentLineage":
        validate_type(name="size", _type=int, value=size)
        clone = self._clone()
        clone._size = size
        return clone

    def exclude_atlan_tags(self, exclude_atlan_tags: bool) -> "FluentLineage":
        validate_type(name="exclude_atlan_tags", _type=bool, value=exclude_atlan_tags)
        clone = self._clone()
        clone._exclude_atlan_tags = exclude_atlan_tags
        return clone

    def exclude_meanings(self, exclude_meanings: bool) -> "FluentLineage":
        validate_type(name="exclude_meanings", _type=bool, value=exclude_meanings)
        clone = self._clone()
        clone._exclude_meanings = exclude_meanings
        return clone

    def immediate_neighbors(self, immediate_neighbors: bool) -> "FluentLineage":
        validate_type(name="immediate_neighbors", _type=bool, value=immediate_neighbors)
        clone = self._clone()
        clone._immediate_neighbors = immediate_neighbors
        return clone

    def include_on_results(self, field: Union[str, AtlanField]) -> "FluentLineage":
        validate_type(name="field", _type=(str, AtlanField), value=field)
        clone = self._clone()
        clone._includes_on_results.append(field)
        return clone

    def include_in_results(self, lineage_filter: LineageFilter) -> "FluentLineage":
        validate_type(name="lineage_filter", _type=LineageFilter, value=lineage_filter)
        clone = self._clone()
        clone._includes_in_results.append(lineage_filter)
        return clone

    def include_on_relations(self, field: Union[str, AtlanField]) -> "FluentLineage":
        validate_type(name="field", _type=(str, AtlanField), value=field)
        clone = self._clone()
        clone._includes_on_relations.append(field)
        return clone

    def includes_condition(
        self, includes_condition: FilterList.Condition
    ) -> "FluentLineage":
        validate_type(
            name="includes_condition",
            _type=FilterList.Condition,
            value=includes_condition,
        )
        clone = self._clone()
        clone._includes_condition = includes_condition
        return clone

    def where_assets(self, lineage_filter: LineageFilter) -> "FluentLineage":
        validate_type(name="lineage_filter", _type=LineageFilter, value=lineage_filter)
        clone = self._clone()
        clone._where_assets.append(lineage_filter)
        return clone

    def assets_condition(
        self, assets_condition: FilterList.Condition
    ) -> "FluentLineage":
        validate_type(
            name="assets_condition",
            _type=FilterList.Condition,
            value=assets_condition,
        )
        clone = self._clone()
        clone._assets_condition = assets_condition
        return clone

    def where_relationships(self, lineage_filter: LineageFilter) -> "FluentLineage":
        validate_type(name="lineage_filter", _type=LineageFilter, value=lineage_filter)
        clone = self._clone()
        clone._where_relationships.append(lineage_filter)
        return clone

    def relationships_condition(
        self, relationships_condition: FilterList.Condition
    ) -> "FluentLineage":
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
        request = LineageListRequest.create(guid=self._starting_guid)
        if self._depth:
            request.depth = self._depth
        if self._direction:
            request.direction = self._direction
        if self._exclude_atlan_tags is not None:
            request.exclude_classifications = self._exclude_atlan_tags
        if self._exclude_meanings is not None:
            request.exclude_meanings = self._exclude_meanings
        if self._immediate_neighbors is not None:
            request.immediate_neighbors = self._immediate_neighbors
        if self._includes_in_results:
            criteria = [
                EntityFilter(
                    attribute_name=_filter.field.internal_field_name,
                    operator=_filter.operator,
                    attribute_value=_filter.value,
                )
                for _filter in self._includes_in_results
            ]
            request.entity_filters = FilterList(
                condition=self._includes_condition, criteria=criteria
            )
        if self._includes_on_results:
            request.attributes = [
                field.atlan_field_name if isinstance(field, AtlanField) else field
                for field in self._includes_on_results
            ]
        if self._includes_on_relations:
            request.relation_attributes = [
                field.atlan_field_name if isinstance(field, AtlanField) else field
                for field in self._includes_on_relations
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
            )
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
            )
        return request
