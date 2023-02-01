#!/usr/bin/env/python
# Copyright 2022 Atlan Pte, Ltd
# Copyright [2015-2021] The Apache Software Foundation
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy
import json
import logging
import os
from typing import Generator, Optional, Type, TypeVar, Union

import requests
from pydantic import (
    BaseSettings,
    Field,
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
    DELETE_ENTITY_BY_GUID,
    DELETE_TYPE_DEF_BY_NAME,
    GET_ALL_TYPE_DEFS,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_ROLES,
    INDEX_SEARCH,
)
from pyatlan.error import NotFoundError
from pyatlan.exceptions import AtlanServiceException, InvalidRequestException
from pyatlan.model.assets import (
    Asset,
    AssetMutationResponse,
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
from pyatlan.model.core import AssetResponse, AtlanObject, BulkRequest
from pyatlan.model.enums import AtlanDeleteType, AtlanTypeCategory
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
    return session


class AtlanClient(BaseSettings):
    host: HttpUrl
    api_key: str
    session: requests.Session = Field(default_factory=get_session)
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
            if start:
                self._start = start
            else:
                self._start = self._start + self._size
            if size:
                self._size = size
            if self._assets:
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
            else:
                return False

        def __iter__(self) -> Generator[Asset, None, None]:
            while True:
                for asset in self.current_page():
                    yield asset
                if not self.next_page():
                    break

    def __init__(self, **data):
        super().__init__(**data)
        self._request_params = {"headers": {"authorization": f"Bearer {self.api_key}"}}

    def _call_api(self, api, query_params=None, request_obj=None):
        params, path = self._create_params(api, query_params, request_obj)
        response = self.session.request(api.method.value, path, **params)
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
        filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        if filter is None:
            filter = ""
        if sort is None:
            sort = ""
        query_params = {
            "filter": filter,
            "sort": sort,
            "count": count,
            "offset": offset,
            "limit": limit,
        }
        raw_json = self._call_api(GET_ROLES.format_path_with_params(), query_params)
        response = RoleResponse(**raw_json)
        return response

    def get_all_roles(self) -> RoleResponse:
        """
        Retrieve all roles defined in Atlan.
        """
        raw_json = self._call_api(GET_ROLES.format_path_with_params())
        response = RoleResponse(**raw_json)
        return response

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
        raw_json = self._call_api(
            GET_ENTITY_BY_UNIQUE_ATTRIBUTE.format_path_with_params(asset_type.__name__),
            query_params,
        )
        raw_json["entity"]["attributes"].update(
            raw_json["entity"]["relationshipAttributes"]
        )
        asset = AssetResponse[A](**raw_json).entity
        if not isinstance(asset, asset_type):
            raise NotFoundError(
                message=f"Asset with qualifiedName {qualified_name} "
                f"is not of the type requested: {asset_type.__name__}.",
                code="ATLAN-PYTHON-404-002",
            )
        return asset

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

        raw_json = self._call_api(
            GET_ENTITY_BY_GUID.format_path_with_params(guid),
            query_params,
        )
        raw_json["entity"]["attributes"].update(
            raw_json["entity"]["relationshipAttributes"]
        )
        raw_json["entity"]["relationshipAttributes"] = {}
        asset = AssetResponse[A](**raw_json).entity
        if not isinstance(asset, asset_type):
            raise NotFoundError(
                message=f"Asset with GUID {guid} is not of the type requested: {asset_type.__name__}.",
                code="ATLAN-PYTHON-404-002",
            )
        return asset

    def upsert(self, entity: Union[Asset, list[Asset]]) -> AssetMutationResponse:
        entities: list[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)
        for asset in entities:
            asset.validate_required()
        request = BulkRequest[Asset](entities=entities)
        raw_json = self._call_api(BULK_UPDATE, None, request)
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
        if "approximateCount" in raw_json:
            count = raw_json["approximateCount"]
        else:
            count = 0
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

    def get_typedefs(self, type: AtlanTypeCategory) -> TypeDefResponse:
        query_params = {"type": type.value}
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
                businessMetadataDefs=[],
            )
        elif isinstance(typedef, CustomMetadataDef):
            # Set up the request payload...
            payload = TypeDefResponse(
                classification_defs=[],
                enum_defs=[],
                struct_defs=[],
                entity_defs=[],
                relationship_defs=[],
                businessMetadataDefs=[typedef],
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
