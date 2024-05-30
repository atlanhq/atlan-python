# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from threading import Lock
from typing import Dict, Optional

from pyatlan.client.typedef import TypeDefClient
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import EnumDef

lock: Lock = Lock()


class EnumCache:
    """
    Lazily-loaded cache for accessing details of an enumeration.
    """

    caches: Dict[int, "EnumCache"] = {}

    @classmethod
    def get_cache(cls) -> "EnumCache":
        from pyatlan.client.atlan import AtlanClient

        with lock:
            client = AtlanClient.get_default_client()
            cache_key = client.cache_key
            if cache_key not in cls.caches:
                cls.caches[cache_key] = EnumCache(typedef_client=client.typedef)
            return cls.caches[cache_key]

    @classmethod
    def refresh_cache(cls) -> None:
        """
        Refreshes the cache of enumerations by requesting the full set of enumerations from Atlan.
        """
        cls.get_cache()._refresh_cache()

    @classmethod
    def get_by_name(cls, name: str) -> EnumDef:
        """
        Retrieve the enumeration definition by its name.

        :param name: human-readable name of the enumeration.
        :raises `NotFoundError`: if the enumeration with the given name does not exist.
        :returns: enumeration definition
        """
        if not (enum := cls.get_cache()._get_by_name(name=name)):
            raise ErrorCode.ENUM_NOT_FOUND.exception_with_parameters(name)
        return enum

    def __init__(self, typedef_client: TypeDefClient):
        self.typedef_client: TypeDefClient = typedef_client
        self.cache_by_name: Dict[str, EnumDef] = {}
        self.lock: Lock = Lock()

    def _refresh_cache(self) -> None:
        """
        Refreshes the cache of enumerations by requesting the full set of enumerations from Atlan.
        """
        with self.lock:
            response = self.typedef_client.get(type_category=AtlanTypeCategory.ENUM)
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
            self._refresh_cache()
            return self.cache_by_name.get(name)
        return None
