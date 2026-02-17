# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Data mesh models for pyatlan_v9, migrated from pyatlan/model/data_mesh.py.

This module provides:
- DataProductsAssetsDSL: Data products assets DSL for defining asset selection.
"""

from __future__ import annotations

from json import dumps, loads
from typing import Any, Dict, List

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan_v9.model.search import DSL, IndexSearchRequest

_ATTR_LIST: List[str] = [
    "__traitNames",
    "connectorName",
    "__customAttributes",
    "certificateStatus",
    "tenantId",
    "anchor",
    "parentQualifiedName",
    "Query.parentQualifiedName",
    "AtlasGlossaryTerm.anchor",
    "databaseName",
    "schemaName",
    "parent",
    "connectionQualifiedName",
    "collectionQualifiedName",
    "announcementMessage",
    "announcementTitle",
    "announcementType",
    "announcementUpdatedAt",
    "announcementUpdatedBy",
    "allowQuery",
    "allowQueryPreview",
    "adminGroups",
    "adminRoles",
    "adminUsers",
    "category",
    "credentialStrategy",
    "connectionSSOCredentialGuid",
    "certificateStatus",
    "certificateUpdatedAt",
    "certificateUpdatedBy",
    "classifications",
    "connectionId",
    "connectionQualifiedName",
    "connectorName",
    "dataType",
    "defaultDatabaseQualifiedName",
    "defaultSchemaQualifiedName",
    "description",
    "displayName",
    "links",
    "link",
    "meanings",
    "name",
    "ownerGroups",
    "ownerUsers",
    "qualifiedName",
    "typeName",
    "userDescription",
    "displayDescription",
    "subDataType",
    "rowLimit",
    "queryTimeout",
    "previewCredentialStrategy",
    "policyStrategy",
    "policyStrategyForSamplePreview",
    "useObjectStorage",
    "objectStorageUploadThreshold",
    "outputPortDataProducts",
]


class DataProductsAssetsDSL(msgspec.Struct, kw_only=True):
    """Data products assets DSL for defining asset selection in data products."""

    query: IndexSearchRequest
    """Parameters for the search itself."""

    filter_scrubbed: bool = True
    """Whether or not to filter scrubbed records."""

    def _exclude_nulls(self, dict_: Dict[str, Any]) -> Dict[str, Any]:
        """Remove null/empty values from a dictionary."""
        return {
            key: value for key, value in dict_.items() if value not in (None, [], {})
        }

    def _contruct_dsl_str(self, asset_selection_dsl: Dict[str, Any]) -> str:
        """Restructure DSL for data products format."""
        try:
            filter_condition = asset_selection_dsl["query"]["dsl"]["query"]["bool"].pop(
                "filter"
            )
            asset_selection_dsl["query"]["dsl"]["query"]["bool"]["filter"] = {
                "bool": {"filter": filter_condition}
            }
        except KeyError:
            raise ErrorCode.UNABLE_TO_TRANSLATE_ASSETS_DSL.exception_with_parameters() from None
        return dumps(asset_selection_dsl)

    def to_string(self) -> str:
        """
        Convert to selected assets DSL JSON string for the data product.

        :returns: selected assets DSL JSON string for the data product.
        :raises: InvalidRequestError if the query provided is invalid.
        """
        search_request = IndexSearchRequest(
            dsl=DSL(
                track_total_hits=None,
                query=self.query.dsl.query,
            ),
            suppress_logs=True,
            request_metadata=None,
            exclude_meanings=None,
            show_search_score=None,
            exclude_atlan_tags=None,
            allow_deleted_relations=None,
            attributes=_ATTR_LIST,
        )
        inner = DataProductsAssetsDSL(query=search_request)
        # Serialize, excluding sort/size from DSL
        inner_dict = {
            "query": search_request.to_dict(),
            "filter_scrubbed": inner.filter_scrubbed,
        }
        # Remove sort and size from the inner DSL
        if "dsl" in inner_dict.get("query", {}):
            inner_dict["query"]["dsl"].pop("sort", None)
            inner_dict["query"]["dsl"].pop("size", None)
        dsl_json_str = dumps(inner_dict)
        asset_selection_dsl = dict(loads(dsl_json_str, object_hook=self._exclude_nulls))
        return self._contruct_dsl_str(asset_selection_dsl)

    @staticmethod
    def get_asset_selection(search_request: IndexSearchRequest) -> str:
        """
        Returns the selection of assets for the data product.

        :param search_request: index search request that
        defines the assets to include in the data product
        :returns: search DSL used to define
        which assets are part of this data product.
        """
        return DataProductsAssetsDSL(query=search_request).to_string()
