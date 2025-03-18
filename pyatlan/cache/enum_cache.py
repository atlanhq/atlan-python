# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict, Optional

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
            response = self.client.typedef.get(type_category=AtlanTypeCategory.ENUM)
            if not response or not response.enum_defs:
                raise ErrorCode.EXPIRED_API_TOKEN.exception_with_parameters()
            self.cache_by_name = {}
            if response is not None:
                for enum in response.enum_defs:
                    type_name = enum.name
                    self.cache_by_name[type_name] = enum

    def _get_by_name(self, name: str) -> Optional[EnumDef]:
        """
        Retrieve the enumeration definition by its name.

        :param name: human-readable name of the enumeration
        :returns: the enumeration definition
        """
        if name:
            if enum_def := self.cache_by_name.get(name):
                return enum_def
            self.refresh_cache()
            return self.cache_by_name.get(name)
        return None
