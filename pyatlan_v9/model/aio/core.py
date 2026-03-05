# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
V9 async core models using msgspec.

Uses v9-native async translators/retranslators that produce AtlanTagName
objects and camelCase keys directly, without post-processing workarounds.
"""

from __future__ import annotations

import json as json_lib
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import msgspec

from pyatlan_v9.model.aio.retranslators import AsyncAtlanTagRetranslator
from pyatlan_v9.model.aio.translators import AsyncAtlanTagTranslator
from pyatlan_v9.model.core import AtlanTagName

if TYPE_CHECKING:
    from pyatlan_v9.client.aio.atlan import AsyncAtlanClient


def _enc_hook(obj: Any) -> Any:
    """Handle custom types that msgspec cannot natively encode."""
    import datetime

    if isinstance(obj, AtlanTagName):
        return str(obj)
    from enum import Enum

    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime.date):
        # Convert date to timestamp in milliseconds (epoch time)
        dt = datetime.datetime.combine(obj, datetime.time.min)
        return int(dt.timestamp() * 1000)
    if isinstance(obj, datetime.datetime):
        # Convert datetime to timestamp in milliseconds
        return int(obj.timestamp() * 1000)
    raise NotImplementedError(f"Cannot serialize {type(obj)}")


class AsyncAtlanResponse:
    """
    Async wrapper for API responses with tag ID -> AtlanTagName translation.
    """

    def __init__(self, raw_json: Dict[str, Any], client: AsyncAtlanClient):
        self.raw_json = raw_json
        self.client = client
        self.translators = [
            AsyncAtlanTagTranslator(client),
        ]
        self.translated: Optional[Union[Dict[str, Any], List[Any], Any]] = None

    async def translate(self) -> Union[Dict[str, Any], List[Any], Any]:
        self.translated = await self._deep_translate(self.raw_json)
        return self.translated

    async def _deep_translate(
        self, data: Union[Dict[str, Any], List[Any], Any]
    ) -> Union[Dict[str, Any], List[Any], Any]:
        if isinstance(data, dict):
            for translator in self.translators:
                if translator.applies_to(data):
                    data = await translator.translate(data)
            return {
                key: await self._deep_translate(value) for key, value in data.items()
            }
        elif isinstance(data, list):
            return [await self._deep_translate(item) for item in data]
        else:
            return data

    async def to_dict(self) -> Union[Dict[str, Any], List[Any], Any]:
        if self.translated is None:
            await self.translate()
        return self.translated


class AsyncAtlanRequest:
    """
    Async wrapper for requests with AtlanTagName -> tag ID retranslation.
    """

    def __init__(self, instance: Any, client: AsyncAtlanClient):
        self.client = client
        self.instance = instance
        self.retranslators = [
            AsyncAtlanTagRetranslator(client),
        ]
        self.translated = None

    async def retranslate(self) -> Any:
        if isinstance(self.instance, (dict, list)):
            parsed = self.instance
        elif hasattr(self.instance, "to_json") and callable(self.instance.to_json):
            parsed = json_lib.loads(self.instance.to_json(nested=True))
        elif hasattr(self.instance, "to_dict") and callable(self.instance.to_dict):
            parsed = self.instance.to_dict()
        else:
            parsed = msgspec.to_builtins(self.instance, enc_hook=_enc_hook)

        self.translated = await self._deep_retranslate(parsed)
        return self.translated

    async def _deep_retranslate(self, data: Any) -> Any:
        if isinstance(data, dict):
            for retranslator in self.retranslators:
                if retranslator.applies_to(data):
                    data = await retranslator.retranslate(data)
            return {
                key: await self._deep_retranslate(value) for key, value in data.items()
            }
        elif isinstance(data, list):
            return [await self._deep_retranslate(item) for item in data]
        return data

    async def json(self, **kwargs) -> str:
        if self.translated is None:
            await self.retranslate()
        return json_lib.dumps(self.translated, **kwargs)
