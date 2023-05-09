# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from typing import Any, Optional, Type, TypeVar

from pydantic import Field

from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import LineageDirection


class MutatedEntities(AtlanObject):
    CREATE: Optional[list[Asset]] = Field(
        None,
        description="Assets that were created. The detailed properties of the returned asset will vary based on the "
        "type of asset, but listed in the example are the common set of properties across assets.",
        alias="CREATE",
    )
    UPDATE: Optional[list[Asset]] = Field(
        None,
        description="Assets that were assets_updated. The detailed properties of the returned asset will vary based on"
        " the type of asset, but listed in the example are the common set of properties across assets.",
        alias="UPDATE",
    )
    DELETE: Optional[list[Asset]] = Field(
        None,
        description="Assets that were deleted. The detailed properties of the returned asset will vary based on the "
        "type of asset, but listed in the example are the common set of properties across assets.",
        alias="DELETE",
    )
    PARTIAL_UPDATE: Optional[list[Asset]] = Field(
        None,
        description="Assets that were partially updated. The detailed properties of the returned asset will "
        "vary based on the type of asset, but listed in the example are the common set of properties across assets.",
        alias="DELETE",
    )


A = TypeVar("A", bound=Asset)


class AssetMutationResponse(AtlanObject):
    guid_assignments: dict[str, Any] = Field(
        None, description="Map of assigned unique identifiers for the changed assets."
    )
    mutated_entities: Optional[MutatedEntities] = Field(
        None, description="Assets that were changed."
    )
    partial_updated_entities: Optional[list[Asset]] = Field(
        None, description="Assets that were partially updated"
    )

    def assets_created(self, asset_type: Type[A]) -> list[A]:
        if self.mutated_entities and self.mutated_entities.CREATE:
            return [
                asset
                for asset in self.mutated_entities.CREATE
                if isinstance(asset, asset_type)
            ]
        return []

    def assets_updated(self, asset_type: Type[A]) -> list[A]:
        if self.mutated_entities and self.mutated_entities.UPDATE:
            return [
                asset
                for asset in self.mutated_entities.UPDATE
                if isinstance(asset, asset_type)
            ]
        return []

    def assets_deleted(self, asset_type: Type[A]) -> list[A]:
        if self.mutated_entities and self.mutated_entities.DELETE:
            return [
                asset
                for asset in self.mutated_entities.DELETE
                if isinstance(asset, asset_type)
            ]
        return []

    def assets_partially_updated(self, asset_type: Type[A]) -> list[A]:
        if self.mutated_entities and self.mutated_entities.PARTIAL_UPDATE:
            return [
                asset
                for asset in self.mutated_entities.PARTIAL_UPDATE
                if isinstance(asset, asset_type)
            ]
        return []


class LineageRelation(AtlanObject):
    from_entity_id: Optional[str]
    to_entity_id: Optional[str]
    process_id: Optional[str]
    relationship_id: Optional[str]


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


class LineageRequest(AtlanObject):
    guid: str
    depth: int = Field(default=0)
    direction: LineageDirection = Field(default=LineageDirection.BOTH)
    hide_process: bool = Field(default=True)
    allow_deleted_process: bool = Field(default=False)
