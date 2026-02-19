# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Response translators for pyatlan_v9."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import msgspec

from pyatlan.model.constants import DELETED_
from pyatlan_v9.model.structs import SourceTagAttachment


class BaseTranslator(ABC):
    """Abstract response translator."""

    @abstractmethod
    def applies_to(self, data: dict[str, Any]) -> bool:
        """Return whether this translator should process this dictionary."""

    @abstractmethod
    def translate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Translate the dictionary to a more user-friendly representation."""


class AtlanTagTranslator(BaseTranslator):
    """
    Translator that converts tag IDs into human-readable Atlan tag names.

    Also extracts source-tag attachments from classification attributes and
    places them under `sourceTagAttachments` for easier consumption.
    """

    _TAG_ID = "tagId"
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

    def translate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Translate tag identifiers in-place on a copy of the provided dictionary."""
        raw_json = data.copy()

        for key in self._CLASSIFICATION_NAMES:
            if key in raw_json:
                raw_json[key] = [
                    self.client.atlan_tag_cache.get_name_for_id(tag_id) or DELETED_
                    for tag_id in raw_json[key]
                ]

        for key in self._CLASSIFICATION_KEYS:
            if key not in raw_json:
                continue
            for classification in raw_json[key]:
                tag_id = classification.get(self._TYPE_NAME)
                if not tag_id:
                    continue
                tag_name = self.client.atlan_tag_cache.get_name_for_id(tag_id)
                classification[self._TYPE_NAME] = tag_name if tag_name else DELETED_
                classification[self._TAG_ID] = tag_id

                attr_id = self.client.atlan_tag_cache.get_source_tags_attr_id(tag_id)
                if not attr_id:
                    continue
                attributes = classification.get("attributes")
                if not attributes or not attributes.get(attr_id):
                    continue
                classification[self._SOURCE_ATTACHMENTS] = [
                    msgspec.convert(source_tag["attributes"], type=SourceTagAttachment)
                    for source_tag in attributes.get(attr_id)
                    if isinstance(source_tag, dict) and source_tag.get("attributes")
                ]

        return raw_json
