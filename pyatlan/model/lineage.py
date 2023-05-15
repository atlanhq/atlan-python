# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from collections import deque
from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from pyatlan.error import InvalidRequestError
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import LineageDirection


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
                raise InvalidRequestError(
                    param="",
                    code="ATLAN-JAVA-400-013",
                    message="Lineage was retrieved using hideProces=false. "
                    "We do not provide a graph view in this case.",
                )
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
            guid if guid else self.base_entity_guid
        )

    def get_all_downstream_assets_dfs(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_downstream_asset_guids_dfs(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_all_upstream_asset_guids_dfs(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_all_upstream_asset_guids_dfs(
            guid if guid else self.base_entity_guid
        )

    def get_all_upstream_assets_dfs(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_all_upstream_asset_guids_dfs(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_downstream_asset_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_downstream_asset_guids(
            guid if guid else self.base_entity_guid
        )

    def get_downstream_assets(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_downstream_asset_guids(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_downstream_process_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_downstream_process_guids(
            guid if guid else self.base_entity_guid
        )

    def get_upstream_asset_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_upstream_asset_guids(
            guid if guid else self.base_entity_guid
        )

    def get_upstream_assets(self, guid: Optional[str] = None) -> list[Asset]:
        return [
            self.guid_entity_map[guid]
            for guid in self.get_graph().get_upstream_asset_guids(
                guid if guid else self.base_entity_guid
            )
        ]

    def get_upstream_process_guids(self, guid: Optional[str] = None) -> list[str]:
        return self.get_graph().get_upstream_process_guids(
            guid if guid else self.base_entity_guid
        )


class LineageRequest(AtlanObject):
    guid: str
    depth: int = Field(default=0)
    direction: LineageDirection = Field(default=LineageDirection.BOTH)
    hide_process: bool = Field(default=True)
    allow_deleted_process: bool = Field(default=False)
