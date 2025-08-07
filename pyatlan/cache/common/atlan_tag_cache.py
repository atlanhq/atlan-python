# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for Atlan tag cache operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Set

from pyatlan.model.typedef import AtlanTagDef

if TYPE_CHECKING:
    from pyatlan.model.typedef import TypeDefResponse


class AtlanTagCacheCommon:
    """Shared logic for Atlan tag cache operations."""

    @staticmethod
    def refresh_cache_data(response: TypeDefResponse) -> tuple:
        """
        Process typedef response to extract Atlan tag cache data.

        :param response: TypeDefResponse from API
        :returns: tuple of (cache_by_id, map_id_to_name, map_name_to_id, map_id_to_source_tags_attr_id)
        """
        cache_by_id: Dict[str, AtlanTagDef] = {}
        map_id_to_name: Dict[str, str] = {}
        map_name_to_id: Dict[str, str] = {}
        map_id_to_source_tags_attr_id: Dict[str, str] = {}

        if response and response.atlan_tag_defs:
            for atlan_tag in response.atlan_tag_defs:
                atlan_tag_id = atlan_tag.name
                atlan_tag_name = atlan_tag.display_name
                cache_by_id[atlan_tag_id] = atlan_tag
                map_id_to_name[atlan_tag_id] = atlan_tag_name
                map_name_to_id[atlan_tag_name] = atlan_tag_id
                source_tags_id = ""
                for attr_def in atlan_tag.attribute_defs or []:
                    if attr_def.display_name == "sourceTagAttachment":
                        source_tags_id = attr_def.name or ""
                map_id_to_source_tags_attr_id[atlan_tag_id] = source_tags_id

        return (
            cache_by_id,
            map_id_to_name,
            map_name_to_id,
            map_id_to_source_tags_attr_id,
        )

    @staticmethod
    def get_id_for_name(
        name: str, map_name_to_id: Dict[str, str], deleted_names: Set[str]
    ) -> tuple[Optional[str], bool]:
        """
        Get ID by name.

        :param name: human-readable name
        :param map_name_to_id: name to ID mapping
        :param deleted_names: set of deleted names
        :returns: tuple of (ID string or None, should_refresh_and_retry)
        """
        cls_id = map_name_to_id.get(name)
        if not cls_id and name not in deleted_names:
            # If not found, indicate refresh is needed
            return None, True
        return cls_id, False

    @staticmethod
    def get_id_for_name_after_refresh(
        name: str, map_name_to_id: Dict[str, str], deleted_names: Set[str]
    ) -> Optional[str]:
        """
        Get ID by name after refresh attempt.

        :param name: human-readable name
        :param map_name_to_id: name to ID mapping
        :param deleted_names: set of deleted names
        :returns: ID string or None if not found
        """
        cls_id = map_name_to_id.get(name)
        if not cls_id:
            # If still not found after refresh, mark it as deleted (could be
            # an entry in an audit log that refers to a classification that
            # no longer exists)
            deleted_names.add(name)
        return cls_id

    @staticmethod
    def get_name_for_id(
        idstr: str, map_id_to_name: Dict[str, str], deleted_ids: Set[str]
    ) -> tuple[Optional[str], bool]:
        """
        Get name by ID.

        :param idstr: ID string
        :param map_id_to_name: ID to name mapping
        :param deleted_ids: set of deleted IDs
        :returns: tuple of (name or None, should_refresh_and_retry)
        """
        cls_name = map_id_to_name.get(idstr)
        if not cls_name and idstr not in deleted_ids:
            # If not found, indicate refresh is needed
            return None, True
        return cls_name, False

    @staticmethod
    def get_name_for_id_after_refresh(
        idstr: str, map_id_to_name: Dict[str, str], deleted_ids: Set[str]
    ) -> Optional[str]:
        """
        Get name by ID after refresh attempt.

        :param idstr: ID string
        :param map_id_to_name: ID to name mapping
        :param deleted_ids: set of deleted IDs
        :returns: name or None if not found
        """
        cls_name = map_id_to_name.get(idstr)
        if not cls_name:
            # If still not found after refresh, mark it as deleted (could be
            # an entry in an audit log that refers to a classification that
            # no longer exists)
            deleted_ids.add(idstr)
        return cls_name

    @staticmethod
    def get_source_tags_attr_id(
        idstr: str, map_id_to_source_tags_attr_id: Dict[str, str], deleted_ids: Set[str]
    ) -> tuple[Optional[str], bool]:
        """
        Get source tags attribute ID.

        :param idstr: tag ID string
        :param map_id_to_source_tags_attr_id: mapping from tag ID to source tags attr ID
        :param deleted_ids: set of deleted IDs
        :returns: tuple of (source tags attribute ID or None, should_refresh_and_retry)
        """
        if idstr and idstr.strip():
            attr_id = map_id_to_source_tags_attr_id.get(idstr)
            if attr_id is not None or idstr in deleted_ids:
                return attr_id, False
            return None, True
        return None, False

    @staticmethod
    def get_source_tags_attr_id_after_refresh(
        idstr: str, map_id_to_source_tags_attr_id: Dict[str, str], deleted_ids: Set[str]
    ) -> Optional[str]:
        """
        Get source tags attribute ID after refresh attempt.

        :param idstr: tag ID string
        :param map_id_to_source_tags_attr_id: mapping from tag ID to source tags attr ID
        :param deleted_ids: set of deleted IDs
        :returns: source tags attribute ID or None
        """
        if idstr and idstr.strip():
            if attr_id := map_id_to_source_tags_attr_id.get(idstr):
                return attr_id
            deleted_ids.add(idstr)
        return None
