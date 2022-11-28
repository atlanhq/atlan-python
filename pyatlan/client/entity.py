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
from typing import Type, TypeVar

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.core import AssetResponse
from pyatlan.utils import (
    API,
    APPLICATION_JSON,
    APPLICATION_OCTET_STREAM,
    BASE_URI,
    MULTIPART_FORM_DATA,
    HTTPMethod,
    HTTPStatus,
)

T = TypeVar("T")


class EntityClient:
    ENTITY_API = BASE_URI + "entity/"
    PREFIX_ATTR = "attr:"
    PREFIX_ATTR_ = "attr_"
    ADMIN_API = BASE_URI + "admin/"
    ENTITY_PURGE_API = ADMIN_API + "purge/"
    ENTITY_BULK_API = ENTITY_API + "bulk/"
    BULK_SET_CLASSIFICATIONS = "bulk/setClassifications"
    BULK_HEADERS = "bulk/headers"

    # Entity APIs
    GET_ENTITY_BY_GUID = API(ENTITY_API + "guid", HTTPMethod.GET, HTTPStatus.OK)
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type", HTTPMethod.GET, HTTPStatus.OK
    )
    GET_ENTITIES_BY_GUIDS = API(ENTITY_BULK_API, HTTPMethod.GET, HTTPStatus.OK)
    GET_ENTITIES_BY_UNIQUE_ATTRIBUTE = API(
        ENTITY_BULK_API + "uniqueAttribute/type", HTTPMethod.GET, HTTPStatus.OK
    )
    GET_ENTITY_HEADER_BY_GUID = API(
        ENTITY_API + "guid/{entity_guid}/header", HTTPMethod.GET, HTTPStatus.OK
    )
    GET_ENTITY_HEADER_BY_UNIQUE_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{type_name}/header",
        HTTPMethod.GET,
        HTTPStatus.OK,
    )

    GET_AUDIT_EVENTS = API(ENTITY_API + "{guid}/audit", HTTPMethod.GET, HTTPStatus.OK)
    CREATE_ENTITY = API(ENTITY_API, HTTPMethod.POST, HTTPStatus.OK)
    CREATE_ENTITIES = API(ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK)
    UPDATE_ENTITY = API(ENTITY_API, HTTPMethod.POST, HTTPStatus.OK)
    UPDATE_ENTITY_BY_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/", HTTPMethod.PUT, HTTPStatus.OK
    )
    UPDATE_ENTITIES = API(ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK)
    PARTIAL_UPDATE_ENTITY_BY_GUID = API(
        ENTITY_API + "guid/{entity_guid}", HTTPMethod.PUT, HTTPStatus.OK
    )
    DELETE_ENTITY_BY_GUID = API(ENTITY_API + "guid", HTTPMethod.DELETE, HTTPStatus.OK)
    DELETE_ENTITY_BY_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/", HTTPMethod.DELETE, HTTPStatus.OK
    )
    DELETE_ENTITIES_BY_GUIDS = API(ENTITY_BULK_API, HTTPMethod.DELETE, HTTPStatus.OK)
    PURGE_ENTITIES_BY_GUIDS = API(ENTITY_PURGE_API, HTTPMethod.PUT, HTTPStatus.OK)

    # Classification APIs
    GET_CLASSIFICATIONS = API(
        ENTITY_API + "guid/{guid}/classifications", HTTPMethod.GET, HTTPStatus.OK
    )
    GET_FROM_CLASSIFICATION = API(
        ENTITY_API + "guid/{entity_guid}/classification/{classification}",
        HTTPMethod.GET,
        HTTPStatus.OK,
    )
    ADD_CLASSIFICATIONS = API(
        ENTITY_API + "guid/{guid}/classifications",
        HTTPMethod.POST,
        HTTPStatus.NO_CONTENT,
    )
    ADD_CLASSIFICATION = API(
        ENTITY_BULK_API + "/classification", HTTPMethod.POST, HTTPStatus.NO_CONTENT
    )
    ADD_CLASSIFICATION_BY_TYPE_AND_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{type_name}/classifications",
        HTTPMethod.POST,
        HTTPStatus.NO_CONTENT,
    )
    UPDATE_CLASSIFICATIONS = API(
        ENTITY_API + "guid/{guid}/classifications",
        HTTPMethod.PUT,
        HTTPStatus.NO_CONTENT,
    )
    UPDATE_CLASSIFICATION_BY_TYPE_AND_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{type_name}/classifications",
        HTTPMethod.PUT,
        HTTPStatus.NO_CONTENT,
    )
    UPDATE_BULK_SET_CLASSIFICATIONS = API(
        ENTITY_API + BULK_SET_CLASSIFICATIONS, HTTPMethod.POST, HTTPStatus.OK
    )
    DELETE_CLASSIFICATION = API(
        ENTITY_API + "guid/{guid}/classification/{classification_name}",
        HTTPMethod.DELETE,
        HTTPStatus.NO_CONTENT,
    )
    DELETE_CLASSIFICATION_BY_TYPE_AND_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{type_name}/classification/{"
        "classification_name}",
        HTTPMethod.DELETE,
        HTTPStatus.NO_CONTENT,
    )
    GET_BULK_HEADERS = API(ENTITY_API + BULK_HEADERS, HTTPMethod.GET, HTTPStatus.OK)

    # Business Attributes APIs
    ADD_BUSINESS_ATTRIBUTE = API(
        ENTITY_API + "guid/{entity_guid}/businessmetadata",
        HTTPMethod.POST,
        HTTPStatus.NO_CONTENT,
    )
    ADD_BUSINESS_ATTRIBUTE_BY_NAME = API(
        ENTITY_API + "guid/{entity_guid}/businessmetadata/{bm_name}",
        HTTPMethod.POST,
        HTTPStatus.NO_CONTENT,
    )
    DELETE_BUSINESS_ATTRIBUTE = API(
        ENTITY_API + "guid/{entity_guid}/businessmetadata",
        HTTPMethod.DELETE,
        HTTPStatus.NO_CONTENT,
    )
    DELETE_BUSINESS_ATTRIBUTE_BY_NAME = API(
        ENTITY_API + "guid/{entity_guid}/businessmetadata/{bm_name}",
        HTTPMethod.DELETE,
        HTTPStatus.NO_CONTENT,
    )
    GET_BUSINESS_METADATA_TEMPLATE = API(
        ENTITY_API + "businessmetadata/import/template",
        HTTPMethod.GET,
        HTTPStatus.OK,
        APPLICATION_JSON,
        APPLICATION_OCTET_STREAM,
    )
    IMPORT_BUSINESS_METADATA = API(
        ENTITY_API + "businessmetadata/import",
        HTTPMethod.POST,
        HTTPStatus.OK,
        MULTIPART_FORM_DATA,
        APPLICATION_JSON,
    )

    # Labels APIs
    ADD_LABELS = API(
        ENTITY_API + "guid/{entity_guid}/labels", HTTPMethod.PUT, HTTPStatus.NO_CONTENT
    )
    ADD_LABELS_BY_UNIQUE_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{type_name}/labels",
        HTTPMethod.PUT,
        HTTPStatus.NO_CONTENT,
    )
    SET_LABELS = API(
        ENTITY_API + "guid/%s/labels", HTTPMethod.POST, HTTPStatus.NO_CONTENT
    )
    SET_LABELS_BY_UNIQUE_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{entity_guid}/labels",
        HTTPMethod.POST,
        HTTPStatus.NO_CONTENT,
    )
    DELETE_LABELS = API(
        ENTITY_API + "guid/{entity_guid}/labels",
        HTTPMethod.DELETE,
        HTTPStatus.NO_CONTENT,
    )
    DELETE_LABELS_BY_UNIQUE_ATTRIBUTE = API(
        ENTITY_API + "uniqueAttribute/type/{type_name}/labels",
        HTTPMethod.DELETE,
        HTTPStatus.NO_CONTENT,
    )

    def __init__(self, client: AtlanClient):
        self.client = client

    def get_entity_by_guid(
        self,
        guid,
        asset_type: Type[T],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> T:
        query_params = {
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }

        raw_json = self.client.call_api(
            EntityClient.GET_ENTITY_BY_GUID.format_path_with_params(guid),
            query_params,
        )
        raw_json["entity"]["attributes"].update(
            raw_json["entity"]["relationshipAttributes"]
        )
        raw_json["entity"]["relationshipAttributes"] = {}
        response = AssetResponse[asset_type](**raw_json)
        return response.entity
