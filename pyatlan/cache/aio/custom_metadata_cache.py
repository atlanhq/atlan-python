# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, List, Set

from pyatlan.cache.common import CustomMetadataCacheCommon
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient


class AsyncCustomMetadataCache:
    """
    Async lazily-loaded cache for translating between Atlan-internal ID strings
    and human-readable names for custom metadata (including attributes).
    """

    def __init__(self, client: AsyncAtlanClient):
        self.client: AsyncAtlanClient = client
        self.cache_by_id: Dict[str, CustomMetadataDef] = {}
        self.attr_cache_by_id: Dict[str, AttributeDef] = {}
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.map_attr_id_to_name: Dict[str, Dict[str, str]] = {}
        self.map_attr_name_to_id: Dict[str, Dict[str, str]] = {}
        self.archived_attr_ids: Dict[str, str] = {}
        self.types_by_asset: Dict[str, Set[type]] = {}
        self.lock: asyncio.Lock = asyncio.Lock()

    async def refresh_cache(self) -> None:
        """
        Refreshes the cache of custom metadata structures by requesting the full set of custom metadata
        structures from Atlan.
        :raises LogicError: if duplicate custom attributes are detected
        """
        await self._refresh_cache()

    async def get_id_for_name(self, name: str) -> str:
        """
        Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.

        :param name: human-readable name of the custom metadata set
        :returns: Atlan-internal ID string of the custom metadata set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return await self._get_id_for_name(name=name)

    async def get_name_for_id(self, idstr: str) -> str:
        """
        Translate the provided Atlan-internal custom metadata ID string to the human-readable custom metadata set name.

        :param idstr: Atlan-internal ID string of the custom metadata set
        :returns: human-readable name of the custom metadata set
        :raises InvalidRequestError: if no ID was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return await self._get_name_for_id(idstr=idstr)

    async def get_attr_id_for_name(self, cm_name: str, attr_name: str) -> str:
        """
        Translate the provided human-readable names to the Atlan-internal ID string for the attribute.

        :param cm_name: human-readable name of the custom metadata set
        :param attr_name: human-readable name of the attribute
        :returns: Atlan-internal ID string of the attribute
        :raises InvalidRequestError: if no name was provided for the custom metadata set or attribute
        :raises NotFoundError: if the custom metadata set or attribute cannot be found
        """
        return await self._get_attr_id_for_name(cm_name=cm_name, attr_name=attr_name)

    async def get_attribute_def(self, attr_id: str) -> AttributeDef:
        """
        Retrieve the full attribute definition for the attribute.

        :param attr_id: Atlan-internal ID string for the attribute
        :returns: attribute definition
        :raises InvalidRequestError: if no attr_id was provided
        :raises NotFoundError: if the attribute cannot be found
        """
        return await self._get_attribute_def(attr_id=attr_id)

    async def get_all_custom_attributes(
        self, include_deleted: bool = False, force_refresh: bool = False
    ) -> Dict[str, List[AttributeDef]]:
        """
        Retrieve all the custom metadata attributes. The dict will be keyed by custom metadata set
        name, and the value will be a listing of all the attributes within that set (with all the details
        of each of those attributes).

        :param include_deleted: if True, include the archived (deleted) custom attributes; otherwise only
                                include active custom attributes
        :param force_refresh: if True, will refresh the custom metadata cache; if False, will only refresh the
                              cache if it is empty
        :returns: a dict from custom metadata set name to all details about its attributes
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return await self._get_all_custom_attributes(
            include_deleted=include_deleted, force_refresh=force_refresh
        )

    async def _refresh_cache(self) -> None:
        """
        Refreshes the cache of custom metadata structures by requesting the full set of custom metadata
        structures from Atlan.
        :raises LogicError: if duplicate custom attributes are detected
        """
        async with self.lock:
            # Make async API call directly
            response = await self.client.typedef.get(
                type_category=[
                    AtlanTypeCategory.CUSTOM_METADATA,
                    AtlanTypeCategory.STRUCT,
                ]
            )

            if not response or not response.struct_defs:
                raise ErrorCode.EXPIRED_API_TOKEN.exception_with_parameters()

            # Process response using shared logic
            (
                self.cache_by_id,
                self.attr_cache_by_id,
                self.map_id_to_name,
                self.map_name_to_id,
                self.map_attr_id_to_name,
                self.map_attr_name_to_id,
                self.archived_attr_ids,
                self.types_by_asset,
            ) = CustomMetadataCacheCommon.refresh_cache_data(response)

    async def _get_id_for_name(self, name: str) -> str:
        """
        Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.

        :param name: human-readable name of the custom metadata set
        :returns: Atlan-internal ID string of the custom metadata set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        if not name or not name.strip():
            raise ErrorCode.MISSING_CM_NAME.exception_with_parameters()
        if cm_id := self.map_name_to_id.get(name):
            return cm_id
        # If not found, refresh the cache and look again (could be stale)
        await self._refresh_cache()
        if cm_id := self.map_name_to_id.get(name):
            return cm_id
        raise ErrorCode.CM_NOT_FOUND_BY_NAME.exception_with_parameters(name)

    async def _get_name_for_id(self, idstr: str) -> str:
        """
        Translate the provided Atlan-internal custom metadata ID string to the human-readable custom metadata set name.

        :param idstr: Atlan-internal ID string of the custom metadata set
        :returns: human-readable name of the custom metadata set
        :raises InvalidRequestError: if no ID was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        if not idstr or not idstr.strip():
            raise ErrorCode.MISSING_CM_ID.exception_with_parameters()
        if cm_name := self.map_id_to_name.get(idstr):
            return cm_name
        # If not found, refresh the cache and look again (could be stale)
        await self._refresh_cache()
        if cm_name := self.map_id_to_name.get(idstr):
            return cm_name
        raise ErrorCode.CM_NOT_FOUND_BY_ID.exception_with_parameters(idstr)

    async def _get_attr_id_for_name(self, cm_name: str, attr_name: str) -> str:
        """
        Translate the provided human-readable names to the Atlan-internal ID string for the attribute.

        :param cm_name: human-readable name of the custom metadata set
        :param attr_name: human-readable name of the attribute
        :returns: Atlan-internal ID string of the attribute
        :raises InvalidRequestError: if no name was provided for the custom metadata set or attribute
        :raises NotFoundError: if the custom metadata set or attribute cannot be found
        """
        if not cm_name or not cm_name.strip():
            raise ErrorCode.MISSING_CM_NAME.exception_with_parameters()
        if not attr_name or not attr_name.strip():
            raise ErrorCode.MISSING_CM_ATTR_NAME.exception_with_parameters()

        if not self.cache_by_id:
            await self._refresh_cache()

        cm_id = self.map_name_to_id.get(cm_name)
        if not cm_id:
            await self._refresh_cache()
            cm_id = self.map_name_to_id.get(cm_name)
            if not cm_id:
                raise ErrorCode.CM_NOT_FOUND_BY_NAME.exception_with_parameters(cm_name)

        attr_id = self.map_attr_name_to_id.get(cm_id, {}).get(attr_name)
        if not attr_id:
            await self._refresh_cache()
            attr_id = self.map_attr_name_to_id.get(cm_id, {}).get(attr_name)
            if not attr_id:
                raise ErrorCode.CM_ATTR_NOT_FOUND_BY_NAME.exception_with_parameters(
                    attr_name, cm_name
                )

        return attr_id

    async def _get_attribute_def(self, attr_id: str) -> AttributeDef:
        """
        Retrieve the full attribute definition for the attribute.

        :param attr_id: Atlan-internal ID string for the attribute
        :returns: attribute definition
        :raises InvalidRequestError: if no attr_id was provided
        :raises NotFoundError: if the attribute cannot be found
        """
        if not attr_id or not attr_id.strip():
            raise ErrorCode.MISSING_CM_ATTR_ID.exception_with_parameters()

        if not self.cache_by_id:
            await self._refresh_cache()

        attr_def = self.attr_cache_by_id.get(attr_id)
        if not attr_def:
            await self._refresh_cache()
            attr_def = self.attr_cache_by_id.get(attr_id)
            if not attr_def:
                raise ErrorCode.CM_ATTR_NOT_FOUND_BY_ID.exception_with_parameters(
                    attr_id
                )

        return attr_def

    async def _get_all_custom_attributes(
        self, include_deleted: bool = False, force_refresh: bool = False
    ) -> Dict[str, List[AttributeDef]]:
        """
        Retrieve all the custom metadata attributes. The dict will be keyed by custom metadata set
        name, and the value will be a listing of all the attributes within that set (with all the details
        of each of those attributes).

        :param include_deleted: if True, include the archived (deleted) custom attributes; otherwise only
                                include active custom attributes
        :param force_refresh: if True, will refresh the custom metadata cache; if False, will only refresh the
                              cache if it is empty
        :returns: a dict from custom metadata set name to all details about its attributes
        :raises NotFoundError: if the custom metadata cannot be found
        """
        if force_refresh or not self.cache_by_id:
            await self._refresh_cache()

        ret_map: Dict[str, List[AttributeDef]] = {}
        for cm_id, cm_def in self.cache_by_id.items():
            cm_name = self.map_id_to_name.get(cm_id)
            if cm_name:
                ret_map[cm_name] = []
                if cm_def.attribute_defs:
                    for attr_def in cm_def.attribute_defs:
                        attr_id = attr_def.name
                        if include_deleted or attr_id not in self.archived_attr_ids:
                            ret_map[cm_name].append(attr_def)

        return ret_map
