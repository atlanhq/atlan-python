# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
import contextlib
import copy
import json
import logging
import os
from typing import Generator, Optional, Type, TypeVar, Union

import requests
from pydantic import (
    BaseSettings,
    HttpUrl,
    PrivateAttr,
    parse_obj_as,
    validate_arguments,
)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pyatlan.client.constants import (
    BULK_UPDATE,
    CREATE_TYPE_DEFS,
    DELETE_ENTITY_BY_ATTRIBUTE,
    DELETE_ENTITY_BY_GUID,
    DELETE_TYPE_DEF_BY_NAME,
    GET_ALL_TYPE_DEFS,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_ROLES,
    INDEX_SEARCH,
    UPDATE_ENTITY_BY_ATTRIBUTE,
)
from pyatlan.error import AtlanError, NotFoundError
from pyatlan.exceptions import AtlanServiceException, InvalidRequestException
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    MaterialisedView,
    Referenceable,
    Schema,
    Table,
    View,
)
from pyatlan.model.core import (
    AssetResponse,
    AtlanObject,
    BulkRequest,
    Classification,
    ClassificationName,
    Classifications,
)
from pyatlan.model.enums import AtlanDeleteType, AtlanTypeCategory
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.role import RoleResponse
from pyatlan.model.search import IndexSearchRequest
from pyatlan.model.typedef import (
    ClassificationDef,
    CustomMetadataDef,
    TypeDef,
    TypeDefResponse,
)
from pyatlan.utils import HTTPStatus, get_logger

LOGGER = get_logger()
T = TypeVar("T", bound=Referenceable)
A = TypeVar("A", bound=Asset)
Assets = Union[
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    Schema,
    Table,
    View,
    MaterialisedView,
]
Asset_Types = Union[
    Type[AtlasGlossary],
    Type[AtlasGlossaryCategory],
    Type[AtlasGlossaryTerm],
    Type[Connection],
    Type[Database],
    Type[Schema],
    Type[Table],
    Type[View],
    Type[MaterialisedView],
]


def get_session():
    retry_strategy = Retry(
        total=6,
        backoff_factor=1,
        status_forcelist=[403, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.session()
    session.mount("https://", adapter)
    session.headers.update({"x-atlan-agent": "sdk", "x-atlan-agent-id": "python"})
    return session


class AtlanClient(BaseSettings):
    host: HttpUrl
    api_key: str
    _session: requests.Session = PrivateAttr(default_factory=get_session)
    _request_params: dict = PrivateAttr()

    class Config:
        env_prefix = "atlan_"

    class SearchResults:
        def __init__(
            self,
            client: "AtlanClient",
            criteria: IndexSearchRequest,
            start: int,
            size: int,
            count: int,
            assets: list[Asset],
        ):
            self._client = client
            self._criteria = criteria
            self._start = start
            self._size = size
            self.count = count
            self._assets = assets

        def current_page(self) -> list[Asset]:
            return self._assets

        def next_page(self, start=None, size=None) -> bool:
            self._start = start or self._start + self._size
            if size:
                self._size = size
            return self._get_next_page() if self._assets else False

        # TODO Rename this here and in `next_page`
        def _get_next_page(self):
            self._criteria.dsl.from_ = self._start
            self._criteria.dsl.size = self._size
            raw_json = self._client._call_api(
                INDEX_SEARCH,
                request_obj=self._criteria,
            )
            if "entities" not in raw_json:
                return False
            self._assets = parse_obj_as(list[Asset], raw_json["entities"])
            return True

        def __iter__(self) -> Generator[Asset, None, None]:
            while True:
                yield from self.current_page()
                if not self.next_page():
                    break

    def __init__(self, **data):
        super().__init__(**data)
        self._request_params = {"headers": {"authorization": f"Bearer {self.api_key}"}}

    def _call_api(self, api, query_params=None, request_obj=None):
        params, path = self._create_params(api, query_params, request_obj)
        response = self._session.request(api.method.value, path, **params)
        if response is not None:
            LOGGER.debug("HTTP Status: %s", response.status_code)
        if response is None:
            return None
        if response.status_code == api.expected_status:
            try:
                if (
                    response.content is None
                    or response.status_code == HTTPStatus.NO_CONTENT
                ):
                    return None
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "<== __call_api(%s,%s,%s), result = %s",
                        vars(api),
                        params,
                        request_obj,
                        response,
                    )
                    LOGGER.debug(response.json())
                return response.json()
            except Exception as e:
                print(e)
                LOGGER.exception(
                    "Exception occurred while parsing response with msg: %s", e
                )
                raise AtlanServiceException(api, response) from e
        elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            LOGGER.error(
                "Atlas Service unavailable. HTTP Status: %s",
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

            return None
        else:
            with contextlib.suppress(ValueError):
                error_info = json.loads(response.text)
                error_code = error_info.get("errorCode", 0)
                error_message = error_info.get("errorMessage", "")
                if error_code and error_message:
                    raise AtlanError(
                        message=error_message,
                        code=error_code,
                        status_code=response.status_code,
                    )
            raise AtlanServiceException(api, response)

    def _create_params(self, api, query_params, request_obj):
        params = copy.deepcopy(self._request_params)
        path = os.path.join(self.host, api.path)
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        if query_params is not None:
            params["params"] = query_params
        if request_obj is not None:
            if isinstance(request_obj, AtlanObject):
                params["data"] = request_obj.json(by_alias=True, exclude_none=True)
            else:
                params["data"] = json.dumps(request_obj)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("------------------------------------------------------")
            LOGGER.debug("Call         : %s %s", api.method, path)
            LOGGER.debug("Content-type_ : %s", api.consumes)
            LOGGER.debug("Accept       : %s", api.produces)
        return params, path

    def get_roles(
        self,
        limit: int,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        if post_filter is None:
            post_filter = ""
        if sort is None:
            sort = ""
        query_params = {
            "filter": post_filter,
            "sort": sort,
            "count": count,
            "offset": offset,
            "limit": limit,
        }
        raw_json = self._call_api(GET_ROLES.format_path_with_params(), query_params)
        return RoleResponse(**raw_json)

    def get_all_roles(self) -> RoleResponse:
        """
        Retrieve all roles defined in Atlan.
        """
        raw_json = self._call_api(GET_ROLES.format_path_with_params())
        return RoleResponse(**raw_json)

    @validate_arguments()
    def get_asset_by_qualified_name(
        self,
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        query_params = {
            "attr:qualifiedName": qualified_name,
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }
        try:
            raw_json = self._call_api(
                GET_ENTITY_BY_UNIQUE_ATTRIBUTE.format_path_with_params(
                    asset_type.__name__
                ),
                query_params,
            )
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
            asset = AssetResponse[A](**raw_json).entity
            asset.is_incomplete = False
            if not isinstance(asset, asset_type):
                raise NotFoundError(
                    message=f"Asset with qualifiedName {qualified_name} "
                    f"is not of the type requested: {asset_type.__name__}.",
                    code="ATLAN-PYTHON-404-002",
                )
            return asset
        except AtlanError as ae:
            if ae.status_code == HTTPStatus.NOT_FOUND:
                raise NotFoundError(message=ae.user_message, code=ae.code) from ae
            raise ae

    @validate_arguments()
    def get_asset_by_guid(
        self,
        guid: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        query_params = {
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }

        try:
            raw_json = self._call_api(
                GET_ENTITY_BY_GUID.format_path_with_params(guid),
                query_params,
            )
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
            raw_json["entity"]["relationshipAttributes"] = {}
            asset = AssetResponse[A](**raw_json).entity
            asset.is_incomplete = False
            if not isinstance(asset, asset_type):
                raise NotFoundError(
                    message=f"Asset with GUID {guid} is not of the type requested: {asset_type.__name__}.",
                    code="ATLAN-PYTHON-404-002",
                )
            return asset
        except AtlanError as ae:
            if ae.status_code == HTTPStatus.NOT_FOUND:
                raise NotFoundError(message=ae.user_message, code=ae.code) from ae
            raise ae

    def upsert(
        self,
        entity: Union[Asset, list[Asset]],
        replace_classifications: bool = False,
        replace_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        query_params = {
            "replaceClassifications": replace_classifications,
            "replaceBusinessAttributes": replace_custom_metadata,
        }
        entities: list[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)
        for asset in entities:
            asset.validate_required()
        request = BulkRequest[Asset](entities=entities)
        raw_json = self._call_api(BULK_UPDATE, query_params, request)
        return AssetMutationResponse(**raw_json)

    def purge_entity_by_guid(self, guid) -> AssetMutationResponse:
        raw_json = self._call_api(
            DELETE_ENTITY_BY_GUID.format_path_with_params(guid),
            {"deleteType": AtlanDeleteType.HARD.value},
        )
        return AssetMutationResponse(**raw_json)

    def search(self, criteria: IndexSearchRequest) -> SearchResults:
        raw_json = self._call_api(
            INDEX_SEARCH,
            request_obj=criteria,
        )
        if "entities" in raw_json:
            assets = parse_obj_as(list[Asset], raw_json["entities"])
        else:
            assets = []
        count = raw_json["approximateCount"] if "approximateCount" in raw_json else 0
        return AtlanClient.SearchResults(
            client=self,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            assets=assets,
        )

    def get_all_typedefs(self) -> TypeDefResponse:
        raw_json = self._call_api(GET_ALL_TYPE_DEFS)
        return TypeDefResponse(**raw_json)

    def get_typedefs(self, type_: AtlanTypeCategory) -> TypeDefResponse:
        query_params = {"type": type_.value}
        raw_json = self._call_api(
            GET_ALL_TYPE_DEFS.format_path_with_params(),
            query_params,
        )
        return TypeDefResponse(**raw_json)

    def create_typedef(self, typedef: TypeDef) -> TypeDefResponse:
        payload = None
        if isinstance(typedef, ClassificationDef):
            # Set up the request payload...
            payload = TypeDefResponse(
                classification_defs=[typedef],
                enum_defs=[],
                struct_defs=[],
                entity_defs=[],
                relationship_defs=[],
                custom_metadata_defs=[],
            )
        elif isinstance(typedef, CustomMetadataDef):
            # Set up the request payload...
            payload = TypeDefResponse(
                classification_defs=[],
                enum_defs=[],
                struct_defs=[],
                entity_defs=[],
                relationship_defs=[],
                custom_metadata_defs=[typedef],
            )
        else:
            raise InvalidRequestException(
                "Unable to create new type definitions of category: "
                + typedef.category.value,
                param="category",
            )
            # Throw an invalid request exception
        raw_json = self._call_api(CREATE_TYPE_DEFS, request_obj=payload)
        return TypeDefResponse(**raw_json)

    def purge_typedef(self, internal_name: str) -> None:
        self._call_api(DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name))

    @validate_arguments()
    def add_classifications(
        self,
        asset_type: Type[A],
        qualified_name: str,
        classification_names: list[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propogation: bool = True,
    ) -> None:
        classifications = Classifications(
            __root__=[
                Classification(
                    type_name=ClassificationName(display_text=name),
                    propagate=propagate,
                    remove_propagations_on_entity_delete=remove_propagation_on_delete,
                    restrict_propagation_through_lineage=restrict_lineage_propogation,
                )
                for name in classification_names
            ]
        )
        query_params = {"attr:qualifiedName": qualified_name}
        self._call_api(
            UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classifications"
            ),
            query_params,
            classifications,
        )

    @validate_arguments()
    def remove_classification(
        self, asset_type: Type[A], qualified_name: str, classification_name: str
    ) -> None:
        from pyatlan.cache.classification_cache import ClassificationCache

        classification_id = ClassificationCache.get_id_for_name(classification_name)
        if not classification_id:
            raise ValueError(f"{classification_name} is not a valid Classification")
        query_params = {"attr:qualifiedName": qualified_name}
        self._call_api(
            DELETE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classification", classification_id
            ),
            query_params,
        )
