# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for custom metadata cache operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Set

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

                        # Skip if either ID or name is None
                        if attr_id is None or attr_name is None:
                            continue

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
