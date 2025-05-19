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
    _TYPE_NAME = "typeName"
    _CLASSIFICATIONS = "classifications"
    _CLASSIFICATION_NAMES = "classificationNames"

    def __init__(self, client: AtlanClient):
        self.client = client

    def applies_to(self, data: Dict[str, Any]) -> bool:
        return self._CLASSIFICATION_NAMES in data or self._CLASSIFICATIONS in data

    def translate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raw_json = data.copy()

        if self._CLASSIFICATION_NAMES in raw_json:
            raw_json[self._CLASSIFICATION_NAMES] = [
                self.client.atlan_tag_cache.get_name_for_id(tag_id)
                for tag_id in raw_json[self._CLASSIFICATION_NAMES]
            ]

        if self._CLASSIFICATIONS in raw_json:
            for classification in raw_json[self._CLASSIFICATIONS]:
                tag_id = classification.get(self._TYPE_NAME)
                if tag_id:
                    tag_name = self.client.atlan_tag_cache.get_name_for_id(tag_id)
                    if not tag_name:
                        return
                    classification[self._TYPE_NAME] = tag_name
                    # Check if the tag is a source tag (in that case tag has "attributes")
                    attr_id = self.client.atlan_tag_cache.get_source_tags_attr_id(
                        tag_id
                    )
                    if attr_id:
                        classification["source_tag_attachements"] = [
                            SourceTagAttachment(**source_tag["attributes"])
                            for source_tag in classification.get("attributes").get(
                                attr_id
                            )
                            if isinstance(source_tag, dict)
                            and source_tag.get("attributes")
                        ]

        return raw_json
