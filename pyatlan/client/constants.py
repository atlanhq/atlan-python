# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from pyatlan.utils import (
    ADMIN_URI,
    API,
    APPLICATION_JSON,
    APPLICATION_OCTET_STREAM,
    BASE_URI,
    MULTIPART_FORM_DATA,
    SQL_URI,
    HTTPMethod,
    HTTPStatus,
)

ROLE_API = f"{ADMIN_URI}roles"
GROUP_API = f"{ADMIN_URI}groups"
USER_API = f"{ADMIN_URI}users"
QUERY_API = f"{SQL_URI}query"
IMAGE_API = f"{ADMIN_URI}images"
LOGS_API = f"{ADMIN_URI}events"
TOKENS_API = f"{ADMIN_URI}apikeys"

# Role APIs
GET_ROLES = API(ROLE_API, HTTPMethod.GET, HTTPStatus.OK)

# Group APIs
GET_GROUPS = API(GROUP_API, HTTPMethod.GET, HTTPStatus.OK)
CREATE_GROUP = API(GROUP_API, HTTPMethod.POST, HTTPStatus.OK)
UPDATE_GROUP = API(GROUP_API, HTTPMethod.POST, HTTPStatus.OK)
DELETE_GROUP = API(GROUP_API + "/{group_guid}/delete", HTTPMethod.POST, HTTPStatus.OK)
GET_GROUP_MEMBERS = API(
    GROUP_API + "/{group_guid}/members", HTTPMethod.GET, HTTPStatus.OK
)
REMOVE_USERS_FROM_GROUP = API(
    GROUP_API + "/{group_guid}/members/remove", HTTPMethod.POST, HTTPStatus.OK
)

# User APIs
GET_USERS = API(USER_API, HTTPMethod.GET, HTTPStatus.OK)
CREATE_USERS = API(USER_API, HTTPMethod.POST, HTTPStatus.OK)
UPDATE_USER = API(USER_API, HTTPMethod.POST, HTTPStatus.OK)
DELETE_USER = API(USER_API + "/{user_guid}/delete", HTTPMethod.POST, HTTPStatus.OK)
GET_USER_GROUPS = API(USER_API + "/{user_guid}/groups", HTTPMethod.GET, HTTPStatus.OK)
ADD_USER_TO_GROUPS = API(
    USER_API + "/{user_guid}/groups", HTTPMethod.POST, HTTPStatus.OK
)
CHANGE_USER_ROLE = API(
    USER_API + "/{user_guid}/roles/update", HTTPMethod.POST, HTTPStatus.OK
)
GET_CURRENT_USER = API(f"{USER_API}/current", HTTPMethod.GET, HTTPStatus.OK)

# SQL parsing APIs
PARSE_QUERY = API(f"{QUERY_API}/parse", HTTPMethod.POST, HTTPStatus.OK)

# File upload APIs
UPLOAD_IMAGE = API(IMAGE_API, HTTPMethod.POST, HTTPStatus.OK)

# Keycloak event APIs
KEYCLOAK_EVENTS = API(f"{LOGS_API}/login", HTTPMethod.GET, HTTPStatus.OK)
ADMIN_EVENTS = API(f"{LOGS_API}/main", HTTPMethod.GET, HTTPStatus.OK)

# API token APIs
GET_API_TOKENS = API(TOKENS_API, HTTPMethod.GET, HTTPStatus.OK)
UPSERT_API_TOKEN = API(TOKENS_API, HTTPMethod.POST, HTTPStatus.OK)
DELETE_API_TOKEN = API(TOKENS_API, HTTPMethod.DELETE, HTTPStatus.OK)

ENTITY_API = f"{BASE_URI}entity/"
PREFIX_ATTR = "attr:"
PREFIX_ATTR_ = "attr_"
ADMIN_API = f"{BASE_URI}admin/"
ENTITY_PURGE_API = f"{ADMIN_API}purge/"
ENTITY_BULK_API = f"{ENTITY_API}bulk/"
BULK_SET_CLASSIFICATIONS = "bulk/setClassifications"
BULK_HEADERS = "bulk/headers"

BULK_UPDATE = API(ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK)
# Lineage APIs
GET_LINEAGE = API(f"{BASE_URI}lineage/getlineage", HTTPMethod.POST, HTTPStatus.OK)
GET_LINEAGE_LIST = API(f"{BASE_URI}lineage/list", HTTPMethod.POST, HTTPStatus.OK)
# Entity APIs
GET_ENTITY_BY_GUID = API(f"{ENTITY_API}guid", HTTPMethod.GET, HTTPStatus.OK)
GET_ENTITY_BY_UNIQUE_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type", HTTPMethod.GET, HTTPStatus.OK
)
GET_ENTITIES_BY_GUIDS = API(ENTITY_BULK_API, HTTPMethod.GET, HTTPStatus.OK)
GET_ENTITIES_BY_UNIQUE_ATTRIBUTE = API(
    f"{ENTITY_BULK_API}uniqueAttribute/type", HTTPMethod.GET, HTTPStatus.OK
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
    f"{ENTITY_API}uniqueAttribute/type/",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
)
UPDATE_ENTITIES = API(ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK)
PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type/",
    HTTPMethod.PUT,
    HTTPStatus.OK,
)
PARTIAL_UPDATE_ENTITY_BY_GUID = API(
    ENTITY_API + "guid/{entity_guid}", HTTPMethod.PUT, HTTPStatus.OK
)
DELETE_ENTITY_BY_GUID = API(f"{ENTITY_API}guid", HTTPMethod.DELETE, HTTPStatus.OK)
DELETE_ENTITY_BY_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type/",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
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
    f"{ENTITY_BULK_API}/classification", HTTPMethod.POST, HTTPStatus.NO_CONTENT
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
    ENTITY_API + "guid/{entity_guid}/businessmetadata/",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
)
ADD_BUSINESS_ATTRIBUTE_BY_ID = API(
    ENTITY_API + "guid/{entity_guid}/businessmetadata/{bm_id}",
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
    f"{ENTITY_API}businessmetadata/import/template",
    HTTPMethod.GET,
    HTTPStatus.OK,
    APPLICATION_JSON,
    APPLICATION_OCTET_STREAM,
)
IMPORT_BUSINESS_METADATA = API(
    f"{ENTITY_API}businessmetadata/import",
    HTTPMethod.POST,
    HTTPStatus.OK,
    MULTIPART_FORM_DATA,
    APPLICATION_JSON,
)
# Glossary APIS
GLOSSARY_URI = f"{BASE_URI}glossary"

GET_ALL_GLOSSARIES = API(GLOSSARY_URI, HTTPMethod.GET, HTTPStatus.OK)

# Labels APIs
ADD_LABELS = API(
    ENTITY_API + "guid/{entity_guid}/labels", HTTPMethod.PUT, HTTPStatus.NO_CONTENT
)
ADD_LABELS_BY_UNIQUE_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/labels",
    HTTPMethod.PUT,
    HTTPStatus.NO_CONTENT,
)
SET_LABELS = API(f"{ENTITY_API}guid/%s/labels", HTTPMethod.POST, HTTPStatus.NO_CONTENT)
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
DEFAULT_LIMIT = -1
DEFAULT_OFFSET = 0
DEFAULT_SORT = "ASC"
LIMIT = "limit"
OFFSET = "offset"

INDEX_API = f"{BASE_URI}search/indexsearch"
INDEX_SEARCH = API(INDEX_API, HTTPMethod.POST, HTTPStatus.OK)

TYPES_API = f"{BASE_URI}types/"
TYPEDEFS_API = f"{TYPES_API}typedefs/"
TYPEDEF_BY_NAME = f"{TYPES_API}typedef/name/"
TYPEDEF_BY_GUID = f"{TYPES_API}typedef/guid/"
GET_BY_NAME_TEMPLATE = TYPES_API + "{path_type}/name/{name}"
GET_BY_GUID_TEMPLATE = TYPES_API + "{path_type}/guid/{guid}"

GET_TYPEDEF_BY_NAME = API(TYPEDEF_BY_NAME, HTTPMethod.GET, HTTPStatus.OK)
GET_TYPEDEF_BY_GUID = API(TYPEDEF_BY_GUID, HTTPMethod.GET, HTTPStatus.OK)
GET_ALL_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.GET, HTTPStatus.OK)
GET_ALL_TYPE_DEF_HEADERS = API(f"{TYPEDEFS_API}headers", HTTPMethod.GET, HTTPStatus.OK)
UPDATE_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.PUT, HTTPStatus.OK)
CREATE_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.POST, HTTPStatus.OK)
DELETE_TYPE_DEFS = API(TYPEDEFS_API, HTTPMethod.DELETE, HTTPStatus.NO_CONTENT)
DELETE_TYPE_DEF_BY_NAME = API(TYPEDEF_BY_NAME, HTTPMethod.DELETE, HTTPStatus.NO_CONTENT)
