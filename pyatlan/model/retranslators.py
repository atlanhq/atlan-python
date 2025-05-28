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
    _CLASSIFICATION_NAMES = "classificationNames"
    _SOURCE_ATTACHMENTS = "source_tag_attachements"
    _CLASSIFICATION_KEYS = {
        "classifications",
        "addOrUpdateClassifications",
        "removeClassifications",
    }

    def __init__(self, client: "AtlanClient"):
        self.client = client

    def applies_to(self, data: Dict[str, Any]) -> bool:
        return self._CLASSIFICATION_NAMES in data or any(
            key in data for key in self._CLASSIFICATION_KEYS
        )

    def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data = data.copy()

        # Convert classification names → IDs
        if self._CLASSIFICATION_NAMES in data:
            data[self._CLASSIFICATION_NAMES] = [
                self.client.atlan_tag_cache.get_id_for_name(str(name))
                for name in data[self._CLASSIFICATION_NAMES]
            ]

        # Convert classification objects
        for key in self._CLASSIFICATION_KEYS:
            if key in data:
                for classification in data[key]:
                    tag_name = str(classification.get(self._TYPE_NAME))
                    if tag_name:
                        tag_id = self.client.atlan_tag_cache.get_id_for_name(tag_name)
                        classification[self._TYPE_NAME] = tag_id

                        # Rebuild source tag attributes
                        attachments = classification.pop(self._SOURCE_ATTACHMENTS, None)
                        if attachments:
                            attr_id = (
                                self.client.atlan_tag_cache.get_source_tags_attr_id(
                                    tag_id
                                )
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
