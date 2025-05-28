from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class BaseRetranslator(ABC):
    @abstractmethod
    def applies_to(self, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AtlanTagRetranslator(BaseRetranslator):
    _TYPE_NAME = "typeName"
    _CLASSIFICATIONS = "classifications"
    _CLASSIFICATION_NAMES = "classificationNames"
    _SOURCE_ATTACHMENTS = "source_tag_attachements"

    def __init__(self, client: "AtlanClient"):
        self.client = client

    def applies_to(self, data: Dict[str, Any]) -> bool:
        return self._CLASSIFICATION_NAMES in data or self._CLASSIFICATIONS in data

    def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data = data.copy()

        if self._CLASSIFICATION_NAMES in data:
            data[self._CLASSIFICATION_NAMES] = [
                self.client.atlan_tag_cache.get_id_for_name(str(name))
                for name in data[self._CLASSIFICATION_NAMES]
            ]

        if self._CLASSIFICATIONS in data:
            for classification in data[self._CLASSIFICATIONS]:
                tag_name = str(classification.get(self._TYPE_NAME))
                if tag_name:
                    tag_id = self.client.atlan_tag_cache.get_id_for_name(tag_name)
                    classification[self._TYPE_NAME] = tag_id

                    # Rebuild source tag structure if `source_tag_attachements` are present
                    attachments = classification.pop(self._SOURCE_ATTACHMENTS, None)
                    if attachments:
                        attr_id = self.client.atlan_tag_cache.get_source_tags_attr_id(
                            str(tag_id)
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
