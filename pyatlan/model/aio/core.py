# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pyatlan.model.aio.retranslators import AsyncAtlanTagRetranslator
from pyatlan.model.aio.translators import AsyncAtlanTagTranslator
from pyatlan.model.core import AtlanObject

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncAtlanResponse:
    """
    Async wrapper class to handle and translate raw JSON responses
    from the Atlan API into human-readable formats using async translators.
    """

    def __init__(self, raw_json: Dict[str, Any], client: AsyncAtlanClient):
        """
        Initialize the AsyncAtlanResponse with raw JSON and client.
        Translation must be done asynchronously via translate() method.
        """
        self.raw_json = raw_json
        self.client = client
        self.translators = [
            AsyncAtlanTagTranslator(client),
            # Register more async translators here
        ]
        self.translated: Optional[Union[Dict[str, Any], List[Any], Any]] = None

    async def translate(self) -> Union[Dict[str, Any], List[Any], Any]:
        """
        Asynchronously translate the raw JSON using registered translators.

        :returns: The translated JSON structure
        """
        self.translated = await self._deep_translate(self.raw_json)
        return self.translated

    async def _deep_translate(
        self, data: Union[Dict[str, Any], List[Any], Any]
    ) -> Union[Dict[str, Any], List[Any], Any]:
        """
        Recursively translate fields in a JSON structure using registered async translators.
        """
        if isinstance(data, dict):
            # Apply translators to this dict if any apply
            for translator in self.translators:
                if translator.applies_to(data):
                    data = await translator.translate(data)

            # Recursively apply to each value
            return {
                key: await self._deep_translate(value) for key, value in data.items()
            }

        elif isinstance(data, list):
            return [await self._deep_translate(item) for item in data]

        else:
            return data

    async def to_dict(self) -> Union[Dict[str, Any], List[Any], Any]:
        """
        Returns the translated version of the raw JSON response.
        If not yet translated, performs translation first.
        """
        if self.translated is None:
            await self.translate()
        return self.translated


class AsyncAtlanRequest:
    """
    Async wrapper class to handle and retranslate an AtlanObject instance
    into a backend-compatible JSON format by applying async retranslators.
    """

    def __init__(self, instance: AtlanObject, client: AsyncAtlanClient):
        """
        Initialize an AsyncAtlanRequest for a given asset/model instance.
        Retranslation must be done asynchronously via retranslate() method.
        """
        self.client = client
        self.instance = instance
        self.retranslators = [
            AsyncAtlanTagRetranslator(client),
            # add others...
        ]
        self.translated = None

    async def retranslate(self) -> Any:
        """
        Asynchronously retranslate the instance JSON using registered retranslators.

        :returns: The retranslated JSON structure
        """
        # Serialize the instance to JSON first
        try:
            # Use json_async if available for async clients
            if hasattr(self.instance, "json_async"):
                raw_json = await self.instance.json_async(
                    by_alias=True, exclude_unset=True, client=self.client
                )
            else:
                raw_json = self.instance.json(
                    by_alias=True, exclude_unset=True, client=self.client
                )
        except (TypeError, AttributeError):
            raw_json = self.instance.json(
                by_alias=True,
                exclude_unset=True,
            )
        parsed = json.loads(raw_json)
        self.translated = await self._deep_retranslate(parsed)
        return self.translated

    async def _deep_retranslate(self, data: Any) -> Any:
        """
        Recursively traverse and apply async retranslators to JSON-like data.
        """
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
        """
        Returns the fully retranslated JSON string, suitable for API calls.
        If not yet retranslated, performs retranslation first.
        """
        if self.translated is None:
            await self.retranslate()
        return json.dumps(self.translated, **kwargs)
