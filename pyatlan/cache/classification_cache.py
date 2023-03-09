# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import ClassificationDef


class ClassificationCache:

    cache_by_id: dict[str, ClassificationDef] = dict()
    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()
    deleted_ids: set[str] = set()
    deleted_names: set[str] = set()

    @classmethod
    def _refresh_cache(cls) -> None:
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        response = client.get_typedefs(type_category=AtlanTypeCategory.CLASSIFICATION)
        if response is not None:
            cls.cache_by_id = {}
            cls.map_id_to_name = {}
            cls.map_name_to_id = {}
            for classification in response.classification_defs:
                classification_id = classification.name
                classification_name = classification.display_name
                cls.cache_by_id[classification_id] = classification
                cls.map_id_to_name[classification_id] = classification_name
                cls.map_name_to_id[classification_name] = classification_id

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable classification name to its Atlan-internal ID string.
        """
        cls_id = cls.map_name_to_id.get(name)
        if not cls_id and name not in cls.deleted_names:
            # If not found, refresh the cache and look again (could be stale)
            cls._refresh_cache()
            cls_id = cls.map_name_to_id.get(name)
            if not cls_id:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                cls.deleted_names.add(name)
        return cls_id

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal classification ID string to the human-readable classification name.
        """
        cls_name = cls.map_id_to_name.get(idstr)
        if not cls_name and idstr not in cls.deleted_ids:
            # If not found, refresh the cache and look again (could be stale)
            cls._refresh_cache()
            cls_name = cls.map_id_to_name.get(idstr)
            if not cls_name:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                cls.deleted_ids.add(idstr)
        return cls_name
