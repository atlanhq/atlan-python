# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Optional, cast

from pyatlan.client.aio.batch import AsyncBatch as _LegacyAsyncBatch
from pyatlan_v9.model.assets import Asset, AtlasGlossaryTerm
from pyatlan_v9.model.response import AssetMutationResponse


class AsyncBatch(_LegacyAsyncBatch):
    """V9 wrapper around the legacy ``AsyncBatch`` class.

    Overrides ``add()`` to accept v9 ``msgspec.Struct`` assets without
    going through Pydantic's ``_convert_to_real_type_`` validator, and
    overrides the tracking helper so v9 ``AtlasGlossaryTerm`` instances
    are handled correctly.
    """

    async def add(self, single) -> Optional[AssetMutationResponse]:
        self._batch.append(single)
        return await self._process()

    @staticmethod
    def __track(tracker, candidate):
        if (
            isinstance(candidate, AtlasGlossaryTerm)
            or getattr(candidate, "type_name", None) == "AtlasGlossaryTerm"
        ):
            asset = cast(Asset, type(candidate).ref_by_guid(candidate.guid))
        else:
            asset = candidate.trim_to_required()
        # Preserve the candidate's real identity. trim_to_required() drops the
        # guid (leaving it UNSET) and ref_by_guid() drops the qualified_name,
        # which makes the tracked lists (created/updated/partial_updated/
        # restored) impossible to match back by guid or qualified_name. The
        # candidate carries the real values, so restore them here.
        if candidate.guid:
            asset.guid = candidate.guid
        if candidate.qualified_name:
            asset.qualified_name = candidate.qualified_name
        asset.name = candidate.name
        tracker.append(asset)
