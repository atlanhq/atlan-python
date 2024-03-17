from __future__ import annotations

from json import dumps, loads
from typing import Any, Dict

from pydantic.v1 import Field

from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.search import DSL, IndexSearchRequest, Query, SortItem


class DataProductsAssetsDSL(AtlanObject):
    query: IndexSearchRequest = Field(description="Parameters for the search itself.")
    filter_scrubbed: bool = Field(
        default=True, description="Whether or not to filter scrubbed records."
    )
    _ATTR_LIST = [
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

    def _exclude_nulls(self, dict_: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: value for key, value in dict_.items() if value not in (None, [], {})
        }

    def _contruct_dsl_str(self, asset_selection_dsl: Dict[str, Any]) -> str:
        try:
            # For data products -- these require a `filter` as a nested dict construct within
            # an outer bool, not a list (which is all the default Elastic client will serialize)
            filter_condition = asset_selection_dsl["query"]["dsl"]["query"]["bool"].pop(
                "filter"
            )
            asset_selection_dsl["query"]["dsl"]["query"]["bool"]["filter"] = {
                "bool": {"filter": filter_condition}
            }
        except KeyError:
            raise ErrorCode.UNABLE_TO_TRANSLATE_ASSETS_DSL.exception_with_parameters() from None
        return dumps(asset_selection_dsl)

    def to_string(self):
        """
        :returns: selected assets DSL JSON string for the data product.
        :raises: `InvalidRequestError` If the query provided
        in the `IndexSearchRequest` is invalid.
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
            attributes=self._ATTR_LIST,
        )
        dsl_json_str = DataProductsAssetsDSL(query=search_request).json(
            by_alias=True, exclude={"query": {"dsl": {"sort", "size"}}}
        )
        asset_selection_dsl = dict(loads(dsl_json_str, object_hook=self._exclude_nulls))
        return self._contruct_dsl_str(asset_selection_dsl)

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}
