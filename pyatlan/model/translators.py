from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

from pyatlan.model.structs import SourceTagAttachment

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class BaseTranslator(ABC):
    @abstractmethod
    def applies_to(self, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def translate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AtlanTagTranslator(BaseTranslator):
    _TAG_ID = "tag_id"
    _TYPE_NAME = "typeName"
    _SOURCE_ATTACHMENTS = "source_tag_attachements"
    _CLASSIFICATION_NAMES = {"classificationNames", "purposeClassifications"}
    _CLASSIFICATION_KEYS = {
        "classifications",
        "addOrUpdateClassifications",
        "removeClassifications",
    }

    def __init__(self, client: AtlanClient):
        self.client = client

    def applies_to(self, data: Dict[str, Any]) -> bool:
        return any(key in data for key in self._CLASSIFICATION_NAMES) or any(
            key in data for key in self._CLASSIFICATION_KEYS
        )

    def translate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        from pyatlan.model.constants import DELETED_

        raw_json = data.copy()

        # Convert classification hash ID → human-readable name
        for key in self._CLASSIFICATION_NAMES:
            if key in raw_json:
                raw_json[key] = [
                    self.client.atlan_tag_cache.get_name_for_id(tag_id) or DELETED_
                    for tag_id in raw_json[key]
                ]

        # Convert classification objects typeName hash ID → human-readable name
        for key in self._CLASSIFICATION_KEYS:
            if key in raw_json:
                for classification in raw_json[key]:
                    tag_id = classification.get(self._TYPE_NAME)
                    if tag_id:
                        tag_name = self.client.atlan_tag_cache.get_name_for_id(tag_id)
                        classification[self._TYPE_NAME] = (
                            tag_name if tag_name else DELETED_
                        )
                        classification[self._TAG_ID] = tag_id
                        # Check if the tag is a source tag (in that case tag has "attributes")
                        attr_id = self.client.atlan_tag_cache.get_source_tags_attr_id(
                            tag_id
                        )
                        if attr_id:
                            classification[self._SOURCE_ATTACHMENTS] = [
                                SourceTagAttachment(**source_tag["attributes"])
                                for source_tag in classification.get("attributes").get(
                                    attr_id
                                )
                                if isinstance(source_tag, dict)
                                and source_tag.get("attributes")
                            ]

        return raw_json
