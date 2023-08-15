# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import EnumDef


class EnumCache:
    """
    Lazily-loaded cache for accessing details of an enumeration.
    """

    cache_by_name: dict[str, EnumDef] = dict()

    @classmethod
    def refresh_cache(cls) -> None:
        """
        Refreshes the cache of enumerations by requesting the full set of enumerations from Atlan.
        """
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        response = client.get_typedefs(type_category=AtlanTypeCategory.ENUM)
        cls.cache_by_name = {}
        if response is not None:
            for enum in response.enum_defs:
                type_name = enum.name
                cls.cache_by_name[type_name] = enum

    @classmethod
    def get_by_name(cls, name: str) -> Optional[EnumDef]:
        """
        Retrieve the enumeration definition by its name.

        :param name: human-readable name of the enumeration
        :returns: the enumeration definition
        """
        if name:
            if enum_def := cls.cache_by_name.get(name):
                return enum_def
            cls.refresh_cache()
            return cls.cache_by_name.get(name)
        return None
