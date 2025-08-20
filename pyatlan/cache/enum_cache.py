# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict, Optional

from pyatlan.cache.common import EnumCacheCommon
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import EnumDef

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock: Lock = Lock()


class EnumCache:
    """
    Lazily-loaded cache for accessing details of an enumeration.
    """

    def __init__(self, client: AtlanClient):
        self.client: AtlanClient = client
        self.cache_by_name: Dict[str, EnumDef] = {}
        self.lock: Lock = Lock()

    def get_by_name(self, name: str) -> EnumDef:
        """
        Retrieve the enumeration definition by its name.

        :param name: human-readable name of the enumeration.
        :raises `NotFoundError`: if the enumeration with the given name does not exist.
        :returns: enumeration definition
        """
        if not (enum := self._get_by_name(name=name)):
            raise ErrorCode.ENUM_NOT_FOUND.exception_with_parameters(name)
        return enum

    def refresh_cache(self) -> None:
        """
        Refreshes the cache of enumerations by requesting the full set of enumerations from Atlan.
        """
        with self.lock:
            # Make API call directly
            response = self.client.typedef.get(type_category=AtlanTypeCategory.ENUM)
            if not response or not response.enum_defs:
                raise ErrorCode.EXPIRED_API_TOKEN.exception_with_parameters()

            # Process response using shared logic
            self.cache_by_name = EnumCacheCommon.refresh_cache_data(response)

    def _get_by_name(self, name: str) -> Optional[EnumDef]:
        """
        Retrieve the enumeration definition by its name, with potential cache refresh.

        :param name: human-readable name of the enumeration
        :returns: enumeration definition or None if not found
        """
        if not self.cache_by_name:
            self.refresh_cache()

        enum_def = self.cache_by_name.get(name)
        if not enum_def:
            self.refresh_cache()
            enum_def = self.cache_by_name.get(name)
        return enum_def
