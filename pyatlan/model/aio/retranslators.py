# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

from pyatlan.model.constants import DELETED_

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncBaseRetranslator(ABC):
    """
    Abstract base class for async retranslators that reverse-translate structured
    API-ready payloads from user-friendly form to internal backend format.
    """

    @abstractmethod
    def applies_to(self, data: Dict[str, Any]) -> bool:
        """
        Determines if this retranslator should process the provided data.
        """
        pass

    @abstractmethod
    async def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async conversion of user-friendly values (like tag names)
        into backend-compatible values (like hashed tag IDs).
        """
        pass


class AsyncAtlanTagRetranslator(AsyncBaseRetranslator):
    """
    Async retranslator that converts human-readable Atlan tag names into
    hashed ID representations, and re-injects source tag attributes
    under the correct format for API submission.
    """

    _TYPE_NAME = "typeName"
    _SOURCE_ATTACHMENTS = "source_tag_attachments"
    _CLASSIFICATION_NAMES = {"classificationNames", "purposeClassifications"}
    _CLASSIFICATION_KEYS = {
        "classifications",
        "addOrUpdateClassifications",
        "removeClassifications",
    }

    def __init__(self, client: AsyncAtlanClient):
        """
        Initializes the retranslator with an async client instance to access the Atlan tag cache.
        """
        self.client = client

    def applies_to(self, data: Dict[str, Any]) -> bool:
        """
        Checks whether the input dictionary contains fields related to classifications or tags.
        """
        return any(key in data for key in self._CLASSIFICATION_NAMES) or any(
            key in data for key in self._CLASSIFICATION_KEYS
        )

    async def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async replacement of tag names with tag IDs, and reconstruction of source tag attachment blocks
        in their expected API form (including nested attributes).
        """

        data = data.copy()

        # Convert classification human-readable name → hash ID
        for key in self._CLASSIFICATION_NAMES:
            if key in data:
                tag_ids = []
                for name in data[key]:
                    tag_id = await self.client.atlan_tag_cache.get_id_for_name(
                        str(name)
                    )
                    tag_ids.append(tag_id or DELETED_)
                data[key] = tag_ids

        # Convert classification objects human-readable name typeName → hash ID
        for key in self._CLASSIFICATION_KEYS:
            if key in data:
                for classification in data[key]:
                    tag_name = str(classification.get(self._TYPE_NAME))
                    if tag_name:
                        tag_id = await self.client.atlan_tag_cache.get_id_for_name(
                            tag_name
                        )
                        classification[self._TYPE_NAME] = tag_id if tag_id else DELETED_

                        # Rebuild source tag attributes
                        attachments = classification.pop(self._SOURCE_ATTACHMENTS, None)
                        if attachments and tag_id:
                            attr_id = await self.client.atlan_tag_cache.get_source_tags_attr_id(
                                tag_id
                            )
                            if attr_id:
                                classification.setdefault("attributes", {})[attr_id] = [
                                    {
                                        "typeName": "SourceTagAttachment",
                                        "attributes": attachment.dict(),
                                    }
                                    for attachment in attachments
                                ]
        return data
