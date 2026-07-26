from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class BaseRetranslator(ABC):
    """
    Abstract base class for retranslators that reverse-translate structured
    API-ready payloads from user-friendly form to internal backend format.
    """

    @abstractmethod
    def applies_to(self, data: Dict[str, Any]) -> bool:
        """
        Determines if this retranslator should process the provided data.
        """
        pass

    @abstractmethod
    def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts user-friendly values (like tag names)
        into backend-compatible values (like hashed tag IDs).
        """
        pass


class AtlanTagRetranslator(BaseRetranslator):
    """
    Retranslator that converts human-readable Atlan tag names into
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

    def __init__(self, client: AtlanClient):
        """
        Initializes the retranslator with a client instance to access the Atlan tag cache.
        """
        self.client = client

    def applies_to(self, data: Dict[str, Any]) -> bool:
        """
        Checks whether the input dictionary contains fields related to classifications or tags.
        """
        return any(key in data for key in self._CLASSIFICATION_NAMES) or any(
            key in data for key in self._CLASSIFICATION_KEYS
        )

    def retranslate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replaces tag names with tag IDs, and reconstructs source tag attachment blocks
        in their expected API form (including nested attributes).

        This is a write/serialization path (tag name -> hashed ID for API
        submission). A user-supplied tag name that does not resolve in the tag
        cache is a client-side error: raise ``NotFoundError`` naming the tag.
        Previously the ``(DELETED)`` sentinel was substituted and sent to Atlas,
        which rejected it with an opaque ``ATLAS-404-00-008: Given classification
        (DELETED) was invalid`` that named neither the tag nor the cause, and
        misled customers into thinking a tag was deleted when it may simply never
        have existed (BLDX-1530).

        The one exception is the sentinel itself: an asset READ with an
        already-deleted tag surfaces ``(DELETED)`` (ID -> name), and
        re-serializing that asset must stay lossless, so a name that IS the
        sentinel is preserved rather than raised on.
        """
        from pyatlan.errors import ErrorCode
        from pyatlan.model.constants import DELETED_

        data = data.copy()

        # Convert classification human-readable name → hash ID.
        # NOTE: this NAMES path backs purpose/persona *policy* definitions, whose
        # serde is intentionally tolerant of already-deleted tag references (they
        # round-trip through the (DELETED) sentinel). The strict "raise on an
        # unresolvable name" check below is applied only to the asset-tag write
        # path (classification objects), which is where the customer-facing bug
        # (add_atlan_tags on a non-existent tag) occurs.
        for key in self._CLASSIFICATION_NAMES:
            if key in data and data[key] is not None:
                data[key] = [
                    self.client.atlan_tag_cache.get_id_for_name(str(name)) or DELETED_
                    for name in data[key]
                ]

        # Convert classification objects human-readable name typeName → hash ID
        for key in self._CLASSIFICATION_KEYS:
            if key in data and data[key] is not None:
                for classification in data[key]:
                    raw_name = classification.get(self._TYPE_NAME)
                    if not raw_name:
                        continue
                    tag_name = str(raw_name)
                    tag_id = self.client.atlan_tag_cache.get_id_for_name(tag_name)
                    # get_id_for_name returns None for a soft-deleted tag AND for a
                    # name that never existed, and the cache's deleted_names set
                    # conflates the two (a never-existed name is added to it after a
                    # refresh miss). So the only reliable "genuinely deleted" signal
                    # is the (DELETED) sentinel *string* itself, produced by a read
                    # of a deleted tag: preserve it (lossless round-trip). Any other
                    # unresolvable name is a client error — raise, naming the tag.
                    if not tag_id and tag_name != DELETED_:
                        raise ErrorCode.ATLAN_TAG_NOT_FOUND_BY_NAME.exception_with_parameters(
                            tag_name
                        )
                    classification[self._TYPE_NAME] = tag_id if tag_id else DELETED_

                    # Rebuild source tag attributes
                    attachments = classification.pop(self._SOURCE_ATTACHMENTS, None)
                    if attachments and tag_id:
                        attr_id = self.client.atlan_tag_cache.get_source_tags_attr_id(
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
