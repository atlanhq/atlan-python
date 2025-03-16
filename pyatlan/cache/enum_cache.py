# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from threading import Lock, local
from typing import TYPE_CHECKING, Dict, Optional

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import EnumDef

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock: Lock = Lock()
enum_cache_tls = local()  # Thread-local storage (TLS)


class EnumCache:
    """
    Lazily-loaded cache for accessing details of an enumeration.
    """

    def __init__(self, client: AtlanClient):
        self.client: AtlanClient = client
        self.cache_by_name: Dict[str, EnumDef] = {}
        self.lock: Lock = Lock()

    @classmethod
    def get_cache(cls, client: Optional[AtlanClient] = None) -> EnumCache:
        from pyatlan.client.atlan import AtlanClient

        with lock:
            client = client or AtlanClient.get_default_client()
            cache_key = client.cache_key

            if not hasattr(enum_cache_tls, "caches"):
                enum_cache_tls.caches = {}

            if cache_key not in enum_cache_tls.caches:
                cache_instance = EnumCache(client=client)
                cache_instance._refresh_cache()  # Refresh on new cache instance
                enum_cache_tls.caches[cache_key] = cache_instance

            return enum_cache_tls.caches[cache_key]

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

    def _refresh_cache(self) -> None:
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
            self._refresh_cache()
            return self.cache_by_name.get(name)
        return None
