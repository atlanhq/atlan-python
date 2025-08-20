# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, List, Optional, Set

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

    async def get_attr_id_for_name(self, set_name: str, attr_name: str) -> str:
        """
        Translate the provided human-readable names to the Atlan-internal ID string for the attribute.

        :param cm_name: human-readable name of the custom metadata set
        :param attr_name: human-readable name of the attribute
        :returns: Atlan-internal ID string of the attribute
        :raises InvalidRequestError: if no name was provided for the custom metadata set or attribute
        :raises NotFoundError: if the custom metadata set or attribute cannot be found
        """
        return await self._get_attr_id_for_name(cm_name=set_name, attr_name=attr_name)

    async def get_attribute_def(self, attr_id: str) -> AttributeDef:
        """
        Retrieve the full attribute definition for the attribute.

        :param attr_id: Atlan-internal ID string for the attribute
        :returns: attribute definition
        :raises InvalidRequestError: if no attr_id was provided
        :raises NotFoundError: if the attribute cannot be found
        """
        return await self._get_attribute_def(attr_id=attr_id)

    async def get_custom_metadata_def(self, name: str) -> CustomMetadataDef:
        """
        Retrieve the full custom metadata structure definition.

        :param name: human-readable name of the custom metadata set
        :returns: the full custom metadata structure definition for that set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return await self._get_custom_metadata_def(name=name)

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

    async def get_attributes_for_search_results(
        self, set_name: str
    ) -> Optional[List[str]]:
        """
        Retrieve the full set of custom attributes to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve attribute names
        :returns: a list of the attribute names, strictly useful for inclusion in search results
        """
        return await self._get_attributes_for_search_results(set_name=set_name)

    async def get_attribute_for_search_results(
        self, set_name: str, attr_name: str
    ) -> Optional[str]:
        """
        Retrieve a single custom attribute name to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve the custom metadata
                         attribute name
        :param attr_name: human-readable name of the attribute
        :returns: the attribute name, strictly useful for inclusion in search results
        """
        return await self._get_attribute_for_search_results(
            set_name=set_name, attr_name=attr_name
        )

    async def is_attr_archived(self, attr_id: str) -> bool:
        """
        Determine if an attribute is archived
        :param attr_id: Atlan-internal ID string for the attribute
        :returns: True if the attribute has been archived
        """
        return await self._is_attr_archived(attr_id=attr_id)

    async def _get_attributes_for_search_results_(
        self, set_id: str
    ) -> Optional[List[str]]:
        """Helper method to get attributes for search results by set ID."""
        if sub_map := self.map_attr_name_to_id.get(set_id):
            attr_ids = sub_map.values()
            return [f"{set_id}.{idstr}" for idstr in attr_ids]
        return None

    async def _get_attribute_for_search_results_(
        self, set_id: str, attr_name: str
    ) -> Optional[str]:
        """Helper method to get single attribute for search results by set ID and attribute name."""
        if sub_map := self.map_attr_name_to_id.get(set_id):
            return sub_map.get(attr_name, None)
        return None

    async def _get_attributes_for_search_results(
        self, set_name: str
    ) -> Optional[List[str]]:
        """
        Retrieve the full set of custom attributes to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve attribute names
        :returns: a list of the attribute names, strictly useful for inclusion in search results
        """
        if set_id := await self._get_id_for_name(set_name):
            if dot_names := await self._get_attributes_for_search_results_(set_id):
                return dot_names
            await self._refresh_cache()
            return await self._get_attributes_for_search_results_(set_id)
        return None

    async def _get_attribute_for_search_results(
        self, set_name: str, attr_name: str
    ) -> Optional[str]:
        """
        Retrieve a single custom attribute name to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve the custom metadata
                         attribute name
        :param attr_name: human-readable name of the attribute
        :returns: the attribute name, strictly useful for inclusion in search results
        """
        if set_id := await self._get_id_for_name(set_name):
            if attr_id := await self._get_attribute_for_search_results_(
                set_id, attr_name
            ):
                return attr_id
            await self._refresh_cache()
            return await self._get_attribute_for_search_results_(set_id, attr_name)
        return None

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

    async def _get_custom_metadata_def(self, name: str) -> CustomMetadataDef:
        """
        Retrieve the full custom metadata structure definition.

        :param name: human-readable name of the custom metadata set
        :returns: the full custom metadata structure definition for that set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        ba_id = await self._get_id_for_name(name)
        if typedef := self.cache_by_id.get(ba_id):
            return typedef
        else:
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

        result = {}
        for cm_id, cm_def in self.cache_by_id.items():
            cm_name = await self._get_name_for_id(cm_id)
            if not cm_name:
                continue
            attribute_defs = cm_def.attribute_defs
            if include_deleted:
                to_include = attribute_defs
            else:
                to_include = []
                if attribute_defs:
                    # Use exact same logic as sync: check attr.options and attr.options.is_archived
                    to_include.extend(
                        attr
                        for attr in attribute_defs
                        if not attr.options or not attr.options.is_archived
                    )
            result[cm_name] = to_include

        return result

    async def get_attr_name_for_id(self, set_id: str, attr_id: str) -> str:
        """
        Translate the provided Atlan-internal ID strings to the human-readable name for the attribute.

        :param set_id: Atlan-internal ID string of the custom metadata set
        :param attr_id: Atlan-internal ID string of the attribute
        :returns: human-readable name of the attribute
        :raises InvalidRequestError: if no set_id or attr_id was provided
        :raises NotFoundError: if the custom metadata set or attribute cannot be found
        """
        return await self._get_attr_name_for_id(set_id=set_id, attr_id=attr_id)

    async def get_attr_map_for_id(self, set_id: str) -> Dict[str, str]:
        """
        Get the attribute map for a custom metadata set ID.

        :param set_id: Atlan-internal ID string of the custom metadata set
        :returns: dict mapping attribute IDs to names
        """
        if not self.cache_by_id:
            await self._refresh_cache()
        return self.map_attr_id_to_name.get(set_id, {})

    async def _get_attr_name_for_id(self, set_id: str, attr_id: str) -> str:
        """
        Translate the provided Atlan-internal ID strings to the human-readable name for the attribute.

        :param set_id: Atlan-internal ID string of the custom metadata set
        :param attr_id: Atlan-internal ID string of the attribute
        :returns: human-readable name of the attribute
        :raises InvalidRequestError: if no set_id or attr_id was provided
        :raises NotFoundError: if the custom metadata set or attribute cannot be found
        """
        if not set_id or not set_id.strip():
            raise ErrorCode.MISSING_CM_ID.exception_with_parameters()
        if not attr_id or not attr_id.strip():
            raise ErrorCode.MISSING_CM_ATTR_ID.exception_with_parameters()

        if not self.cache_by_id:
            await self._refresh_cache()

        attr_name = self.map_attr_id_to_name.get(set_id, {}).get(attr_id)
        if not attr_name:
            await self._refresh_cache()
            attr_name = self.map_attr_id_to_name.get(set_id, {}).get(attr_id)
            if not attr_name:
                raise ErrorCode.CM_ATTR_NOT_FOUND_BY_ID.exception_with_parameters(
                    attr_id
                )

        return attr_name

    async def _is_attr_archived(self, attr_id: str) -> bool:
        """
        Indicates whether the provided attribute has been archived (deleted) (true) or not (false).

        :param attr_id: Atlan-internal ID string for the attribute
        :returns: true if the attribute has been archived, otherwise false
        """
        if not self.cache_by_id:
            await self._refresh_cache()
        return attr_id in self.archived_attr_ids
