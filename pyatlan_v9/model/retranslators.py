# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Request retranslators for pyatlan_v9."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import msgspec

from pyatlan.model.constants import DELETED_
from pyatlan_v9.model.structs import SourceTagAttachment


class BaseRetranslator(ABC):
    """Abstract request retranslator."""

    @abstractmethod
    def applies_to(self, data: dict[str, Any]) -> bool:
        """Return whether this retranslator should process this dictionary."""

    @abstractmethod
    def retranslate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Retranslate dictionary values back into backend-compatible format."""


class AtlanTagRetranslator(BaseRetranslator):
    """
    Retranslator that converts human-readable tag names back to tag IDs.

    Also rebuilds source-tag attachment blocks under classification attributes
    using the attribute ID expected by the backend.
    """

    _TYPE_NAME = "typeName"
    _SOURCE_ATTACHMENTS = "sourceTagAttachments"
    _CLASSIFICATION_NAMES = {"classificationNames", "purposeClassifications"}
    _CLASSIFICATION_KEYS = {
        "classifications",
        "addOrUpdateClassifications",
        "removeClassifications",
    }

    def __init__(self, client: Any):
        self.client = client

    def applies_to(self, data: dict[str, Any]) -> bool:
        """Check whether classification-related keys are present."""
        return any(key in data for key in self._CLASSIFICATION_NAMES) or any(
            key in data for key in self._CLASSIFICATION_KEYS
        )

    def _attachment_to_dict(self, attachment: Any) -> dict[str, Any]:
        if isinstance(attachment, SourceTagAttachment):
            attrs = msgspec.to_builtins(attachment)
        else:
            attrs = msgspec.convert(attachment, type=dict[str, Any])
        return {
            "typeName": "SourceTagAttachment",
            "attributes": attrs,
        }

    def retranslate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Retranslate tag names into IDs on a copy of the provided dictionary."""
        translated = data.copy()

        for key in self._CLASSIFICATION_NAMES:
            if key in translated:
                translated[key] = [
                    self.client.atlan_tag_cache.get_id_for_name(str(name)) or DELETED_
                    for name in translated[key]
                ]

        for key in self._CLASSIFICATION_KEYS:
            if key not in translated:
                continue
            for classification in translated[key]:
                tag_name = str(classification.get(self._TYPE_NAME))
                if not tag_name:
                    continue
                tag_id = self.client.atlan_tag_cache.get_id_for_name(tag_name)
                classification[self._TYPE_NAME] = tag_id if tag_id else DELETED_

                attachments = classification.pop(self._SOURCE_ATTACHMENTS, None)
                if not attachments or not tag_id:
                    continue
                attr_id = self.client.atlan_tag_cache.get_source_tags_attr_id(tag_id)
                if not attr_id:
                    continue
                classification.setdefault("attributes", {})[attr_id] = [
                    self._attachment_to_dict(attachment) for attachment in attachments
                ]

        return translated
