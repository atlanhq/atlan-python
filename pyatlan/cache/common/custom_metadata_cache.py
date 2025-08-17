# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for custom metadata cache operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Set

from pyatlan.errors import ErrorCode
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef

if TYPE_CHECKING:
    from pyatlan.model.typedef import TypeDefResponse


class CustomMetadataCacheCommon:
    """Shared logic for custom metadata cache operations."""

    @staticmethod
    def refresh_cache_data(response: TypeDefResponse) -> tuple:
        """
        Process typedef response to extract custom metadata cache data.

        :param response: TypeDefResponse from API
        :returns: tuple of cache data dictionaries
        :raises LogicError: if duplicate custom attributes are detected
        """
        cache_by_id: Dict[str, CustomMetadataDef] = {}
        attr_cache_by_id: Dict[str, AttributeDef] = {}
        map_id_to_name: Dict[str, str] = {}
        map_name_to_id: Dict[str, str] = {}
        map_attr_id_to_name: Dict[str, Dict[str, str]] = {}
        map_attr_name_to_id: Dict[str, Dict[str, str]] = {}
        archived_attr_ids: Dict[str, str] = {}
        types_by_asset: Dict[str, Set[type]] = {}

        if response and response.custom_metadata_defs:
            for cm in response.custom_metadata_defs:
                cm_id = cm.name
                cm_name = cm.display_name
                cache_by_id[cm_id] = cm
                map_id_to_name[cm_id] = cm_name
                map_name_to_id[cm_name] = cm_id
                map_attr_id_to_name[cm_id] = {}
                map_attr_name_to_id[cm_id] = {}

                # Process attributes
                if cm.attribute_defs:
                    for attr_def in cm.attribute_defs:
                        attr_id = attr_def.name
                        attr_name = attr_def.display_name
                        attr_cache_by_id[attr_id] = attr_def
                        map_attr_id_to_name[cm_id][attr_id] = attr_name
                        map_attr_name_to_id[cm_id][attr_name] = attr_id

                        # Check for archived attributes
                        if hasattr(attr_def, "options") and attr_def.options:
                            # Handle both dictionary and Options object cases
                            if hasattr(attr_def.options, "get"):
                                # Dictionary case
                                archived_id = attr_def.options.get(
                                    "archivedAttributeId"
                                )
                            else:
                                # Options object case
                                archived_id = getattr(
                                    attr_def.options, "archivedAttributeId", None
                                )
                            if archived_id:
                                archived_attr_ids[archived_id] = attr_id

                        # Process applicable types
                        if hasattr(attr_def, "options") and attr_def.options:
                            # Handle both dictionary and Options object cases
                            if hasattr(attr_def.options, "get"):
                                # Dictionary case
                                applicable_types_str = attr_def.options.get(
                                    "applicableEntityTypes"
                                )
                            else:
                                # Options object case
                                applicable_types_str = getattr(
                                    attr_def.options, "applicableEntityTypes", None
                                )
                            if applicable_types_str:
                                try:
                                    import json

                                    applicable_types = json.loads(applicable_types_str)
                                    if isinstance(applicable_types, list):
                                        for type_name in applicable_types:
                                            if type_name not in types_by_asset:
                                                types_by_asset[type_name] = set()
                                            # Import asset type dynamically
                                            try:
                                                from pyatlan.model.assets import Asset

                                                asset_type = getattr(
                                                    Asset, type_name, None
                                                )
                                                if asset_type:
                                                    types_by_asset[type_name].add(
                                                        asset_type
                                                    )
                                            except (AttributeError, ImportError):
                                                pass
                                except json.JSONDecodeError:
                                    pass

        return (
            cache_by_id,
            attr_cache_by_id,
            map_id_to_name,
            map_name_to_id,
            map_attr_id_to_name,
            map_attr_name_to_id,
            archived_attr_ids,
            types_by_asset,
        )

    @staticmethod
    def get_id_for_name(name: str, map_name_to_id: Dict[str, str]):
        """
        Get custom metadata ID by name.

        :param name: human-readable name
        :param map_name_to_id: name to ID mapping
        :returns: ID string or None if not found, plus validation check
        :raises InvalidRequestError: if no name provided
        """
        if not name:
            raise ErrorCode.MISSING_CM_NAME.exception_with_parameters()

        cm_id = map_name_to_id.get(name)
        return cm_id

    @staticmethod
    def validate_cm_found_by_name(name: str, cm_id: Optional[str]):
        """
        Validate that custom metadata was found by name.

        :param name: human-readable name
        :param cm_id: the ID that was found (or None)
        :raises NotFoundError: if custom metadata not found
        """
        if not cm_id:
            raise ErrorCode.CM_NOT_FOUND_BY_NAME.exception_with_parameters(name)

    @staticmethod
    def get_name_for_id(idstr: str, map_id_to_name: Dict[str, str]) -> tuple[str, bool]:
        """
        Shared logic for getting custom metadata name by ID with lazy loading.

        :param idstr: ID string
        :param map_id_to_name: ID to name mapping
        :param refresh_callback: function to call to refresh cache
        :returns: name string
        :raises InvalidRequestError: if no ID provided
        :raises NotFoundError: if custom metadata not found
        """
        if not idstr:
            raise ErrorCode.MISSING_CM_ID.exception_with_parameters()

        cm_name = map_id_to_name.get(idstr)
        return cm_name

    @staticmethod
    def validate_cm_found_by_id(idstr: str, cm_name: Optional[str]):
        """
        Validate that custom metadata was found by ID.

        :param idstr: ID string
        :param cm_name: the name that was found (or None)
        :raises NotFoundError: if custom metadata not found
        """
        if not cm_name:
            raise ErrorCode.CM_NOT_FOUND_BY_ID.exception_with_parameters(idstr)

    @staticmethod
    def get_attr_id_for_name(
        cm_name: str,
        attr_name: str,
        map_name_to_id: Dict[str, str],
        map_attr_name_to_id: Dict[str, Dict[str, str]],
    ) -> tuple[str, bool]:
        """
        Shared logic for getting attribute ID by names with lazy loading.

        :param cm_name: custom metadata set name
        :param attr_name: attribute name
        :param map_name_to_id: custom metadata name to ID mapping
        :param map_attr_name_to_id: attribute name to ID mapping
        :param refresh_callback: function to call to refresh cache
        :returns: attribute ID string
        :raises InvalidRequestError: if names not provided
        :raises NotFoundError: if not found
        """
        if not cm_name:
            raise ErrorCode.MISSING_CM_NAME.exception_with_parameters()
        if not attr_name:
            raise ErrorCode.MISSING_CM_ATTR_NAME.exception_with_parameters()

        cm_id = map_name_to_id.get(cm_name)
        if not cm_id:
            raise ErrorCode.CM_NOT_FOUND_BY_NAME.exception_with_parameters(cm_name)

        attr_id = map_attr_name_to_id.get(cm_id, {}).get(attr_name)
        if not attr_id:
            raise ErrorCode.CM_ATTR_NOT_FOUND_BY_NAME.exception_with_parameters(
                attr_name, cm_name
            )

        return attr_id

    @staticmethod
    def get_attribute_def(
        attr_id: str, attr_cache_by_id: Dict[str, AttributeDef]
    ) -> tuple[AttributeDef, bool]:
        """
        Shared logic for getting attribute definition by ID with lazy loading.

        :param attr_id: attribute ID
        :param attr_cache_by_id: attribute cache mapping
        :param refresh_callback: function to call to refresh cache
        :returns: AttributeDef object
        :raises NotFoundError: if attribute not found
        """
        if not attr_id:
            raise ErrorCode.MISSING_CM_ATTR_ID.exception_with_parameters()

        attr_def = attr_cache_by_id.get(attr_id)
        if not attr_def:
            raise ErrorCode.CM_ATTR_NOT_FOUND_BY_ID.exception_with_parameters(attr_id)

        return attr_def
