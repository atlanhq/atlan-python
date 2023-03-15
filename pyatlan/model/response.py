# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from typing import Any, Optional, Type, TypeVar

from pydantic import Field

from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject


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
