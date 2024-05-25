# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from pyatlan.utils import (
    API,
    APPLICATION_ENCODED_FORM,
    APPLICATION_JSON,
    APPLICATION_OCTET_STREAM,
    MULTIPART_FORM_DATA,
    EndPoint,
    HTTPMethod,
    HTTPStatus,
)

ROLE_API = "roles"
GROUP_API = "groups"
USER_API = "users"
QUERY_API = "query"
IMAGE_API = "images"
LOGS_API = "events"
TOKENS_API = "apikeys"

# Role APIs
GET_ROLES = API(ROLE_API, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES)

# Group APIs
GET_GROUPS = API(GROUP_API, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES)
CREATE_GROUP = API(
    GROUP_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
UPDATE_GROUP = API(
    GROUP_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
DELETE_GROUP = API(
    GROUP_API + "/{group_guid}/delete",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
GET_GROUP_MEMBERS = API(
    GROUP_API + "/{group_guid}/members",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
REMOVE_USERS_FROM_GROUP = API(
    GROUP_API + "/{group_guid}/members/remove",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)

# User APIs
GET_USERS = API(USER_API, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES)
CREATE_USERS = API(USER_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES)
UPDATE_USER = API(USER_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES)
DELETE_USER = API(
    USER_API + "/{user_guid}/delete",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
GET_USER_GROUPS = API(
    USER_API + "/{user_guid}/groups",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
ADD_USER_TO_GROUPS = API(
    USER_API + "/{user_guid}/groups",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
CHANGE_USER_ROLE = API(
    USER_API + "/{user_guid}/roles/update",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
GET_CURRENT_USER = API(
    f"{USER_API}/current", HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)

# SQL parsing APIs
PARSE_QUERY = API(
    f"{QUERY_API}/parse", HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HEKA
)

# For running SQL queries
EVENT_STREAM = "text/event-stream"
RUN_QUERY = API(
    f"{QUERY_API}/stream",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HEKA,
    consumes=EVENT_STREAM,
    produces=EVENT_STREAM,
)

# File upload APIs
UPLOAD_IMAGE = API(
    IMAGE_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)

# Keycloak event APIs
KEYCLOAK_EVENTS = API(
    f"{LOGS_API}/login", HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
ADMIN_EVENTS = API(
    f"{LOGS_API}/main", HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)

# API token APIs
GET_API_TOKENS = API(
    TOKENS_API, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
UPSERT_API_TOKEN = API(
    TOKENS_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
DELETE_API_TOKEN = API(
    TOKENS_API, HTTPMethod.DELETE, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)

GET_TOKEN = API(
    "/auth/realms/default/protocol/openid-connect/token",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.IMPERSONATION,
    consumes=APPLICATION_ENCODED_FORM,
    produces=APPLICATION_ENCODED_FORM,
)

ENTITY_API = "entity/"
PREFIX_ATTR = "attr:"
PREFIX_ATTR_ = "attr_"
ADMIN_API = "admin/"
ENTITY_PURGE_API = f"{ADMIN_API}purge/"
ENTITY_BULK_API = f"{ENTITY_API}bulk/"
BULK_SET_CLASSIFICATIONS = "bulk/setClassifications"
BULK_HEADERS = "bulk/headers"

BULK_UPDATE = API(
    ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
# Lineage APIs
GET_LINEAGE = API(
    "lineage/getlineage", HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
GET_LINEAGE_LIST = API(
    "lineage/list", HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
# Entity APIs
GET_ENTITY_BY_GUID = API(
    f"{ENTITY_API}guid", HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
GET_ENTITY_BY_UNIQUE_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
GET_ENTITIES_BY_GUIDS = API(
    ENTITY_BULK_API, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
GET_ENTITIES_BY_UNIQUE_ATTRIBUTE = API(
    f"{ENTITY_BULK_API}uniqueAttribute/type",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
GET_ENTITY_HEADER_BY_GUID = API(
    ENTITY_API + "guid/{entity_guid}/header",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
GET_ENTITY_HEADER_BY_UNIQUE_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/header",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)

GET_AUDIT_EVENTS = API(
    ENTITY_API + "{guid}/audit", HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
CREATE_ENTITY = API(ENTITY_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS)
CREATE_ENTITIES = API(
    ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
UPDATE_ENTITY = API(ENTITY_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS)
UPDATE_ENTITY_BY_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type/",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
UPDATE_ENTITIES = API(
    ENTITY_BULK_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type/",
    HTTPMethod.PUT,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
PARTIAL_UPDATE_ENTITY_BY_GUID = API(
    ENTITY_API + "guid/{entity_guid}",
    HTTPMethod.PUT,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
DELETE_ENTITY_BY_GUID = API(
    f"{ENTITY_API}guid", HTTPMethod.DELETE, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
DELETE_ENTITY_BY_ATTRIBUTE = API(
    f"{ENTITY_API}uniqueAttribute/type/",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DELETE_ENTITIES_BY_GUIDS = API(
    ENTITY_BULK_API, HTTPMethod.DELETE, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
PURGE_ENTITIES_BY_GUIDS = API(
    ENTITY_PURGE_API, HTTPMethod.PUT, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)

# Classification APIs
GET_CLASSIFICATIONS = API(
    ENTITY_API + "guid/{guid}/classifications",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
GET_FROM_CLASSIFICATION = API(
    ENTITY_API + "guid/{entity_guid}/classification/{classification}",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
ADD_CLASSIFICATIONS = API(
    ENTITY_API + "guid/{guid}/classifications",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
ADD_CLASSIFICATION = API(
    f"{ENTITY_BULK_API}/classification",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
ADD_CLASSIFICATION_BY_TYPE_AND_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/classifications",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
UPDATE_CLASSIFICATIONS = API(
    ENTITY_API + "guid/{guid}/classifications",
    HTTPMethod.PUT,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
UPDATE_CLASSIFICATION_BY_TYPE_AND_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/classifications",
    HTTPMethod.PUT,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
UPDATE_BULK_SET_CLASSIFICATIONS = API(
    ENTITY_API + BULK_SET_CLASSIFICATIONS,
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
)
DELETE_CLASSIFICATION = API(
    ENTITY_API + "guid/{guid}/classification/{classification_name}",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DELETE_CLASSIFICATION_BY_TYPE_AND_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/classification/{"
    "classification_name}",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
GET_BULK_HEADERS = API(
    ENTITY_API + BULK_HEADERS, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)

# Business Attributes APIs
ADD_BUSINESS_ATTRIBUTE = API(
    ENTITY_API + "guid/{entity_guid}/businessmetadata/",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
ADD_BUSINESS_ATTRIBUTE_BY_ID = API(
    ENTITY_API + "guid/{entity_guid}/businessmetadata/{bm_id}",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
ADD_BUSINESS_ATTRIBUTE_BY_NAME = API(
    ENTITY_API + "guid/{entity_guid}/businessmetadata/{bm_name}",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DELETE_BUSINESS_ATTRIBUTE = API(
    ENTITY_API + "guid/{entity_guid}/businessmetadata",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DELETE_BUSINESS_ATTRIBUTE_BY_NAME = API(
    ENTITY_API + "guid/{entity_guid}/businessmetadata/{bm_name}",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
GET_BUSINESS_METADATA_TEMPLATE = API(
    f"{ENTITY_API}businessmetadata/import/template",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
    consumes=APPLICATION_JSON,
    produces=APPLICATION_OCTET_STREAM,
)
IMPORT_BUSINESS_METADATA = API(
    f"{ENTITY_API}businessmetadata/import",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.ATLAS,
    consumes=MULTIPART_FORM_DATA,
    produces=APPLICATION_JSON,
)
# Glossary APIS
GLOSSARY_URI = "glossary"

GET_ALL_GLOSSARIES = API(
    GLOSSARY_URI, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)

# Labels APIs
ADD_LABELS = API(
    ENTITY_API + "guid/{entity_guid}/labels",
    HTTPMethod.PUT,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
ADD_LABELS_BY_UNIQUE_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/labels",
    HTTPMethod.PUT,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
SET_LABELS = API(
    f"{ENTITY_API}guid/%s/labels",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
SET_LABELS_BY_UNIQUE_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{entity_guid}/labels",
    HTTPMethod.POST,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DELETE_LABELS = API(
    ENTITY_API + "guid/{entity_guid}/labels",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DELETE_LABELS_BY_UNIQUE_ATTRIBUTE = API(
    ENTITY_API + "uniqueAttribute/type/{type_name}/labels",
    HTTPMethod.DELETE,
    HTTPStatus.NO_CONTENT,
    endpoint=EndPoint.ATLAS,
)
DEFAULT_LIMIT = -1
DEFAULT_OFFSET = 0
DEFAULT_SORT = "ASC"
LIMIT = "limit"
OFFSET = "offset"

INDEX_API = "search/indexsearch"
INDEX_SEARCH = API(INDEX_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS)
WORKFLOW_INDEX_API = "workflows/indexsearch"
WORKFLOW_INDEX_RUN_API = "runs/indexsearch"
WORKFLOW_INDEX_SEARCH = API(
    WORKFLOW_INDEX_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
WORKFLOW_INDEX_RUN_SEARCH = API(
    WORKFLOW_INDEX_RUN_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
WORKFLOW_RERUN_API = "workflows/submit"
WORKFLOW_RERUN = API(
    WORKFLOW_RERUN_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
WORKFLOW_RUN_API = "workflows?submit=true"
WORKFLOW_RUN = API(
    WORKFLOW_RUN_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
WORKFLOW_API = "workflows"
WORKFLOW_UPDATE = API(
    WORKFLOW_API + "/{workflow_name}",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
WORKFLOW_ARCHIVE = API(
    WORKFLOW_API + "/{workflow_name}/archive",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
WORKFLOW_SCHEDULE_RUN = "runs"
GET_ALL_SCHEDULE_RUNS = API(
    WORKFLOW_SCHEDULE_RUN + "/cron",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
GET_SCHEDULE_RUN = API(
    WORKFLOW_SCHEDULE_RUN + "/cron/{workflow_name}",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
STOP_WORKFLOW_RUN = API(
    WORKFLOW_SCHEDULE_RUN + "/{workflow_run_id}/stop",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
CREDENTIALS_API = "credentials"
TEST_CREDENTIAL_API = CREDENTIALS_API + "/test"
TEST_CREDENTIAL = API(
    TEST_CREDENTIAL_API,
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
GET_CREDENTIAL_BY_GUID = API(
    CREDENTIALS_API + "/{credential_guid}",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
UPDATE_CREDENTIAL_BY_GUID = API(
    CREDENTIALS_API + "/{credential_guid}",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
AUDIT_API = "entity/auditSearch"
AUDIT_SEARCH = API(AUDIT_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS)
SEARCH_LOG_API = "search/searchlog"
SEARCH_LOG = API(
    SEARCH_LOG_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
TASK_API = "task/search"
TASK_SEARCH = API(TASK_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS)

TYPES_API = "types/"
TYPEDEFS_API = f"{TYPES_API}typedefs/"
TYPEDEF_BY_NAME = f"{TYPES_API}typedef/name/"
TYPEDEF_BY_GUID = f"{TYPES_API}typedef/guid/"
GET_BY_NAME_TEMPLATE = TYPES_API + "{path_type}/name/{name}"
GET_BY_GUID_TEMPLATE = TYPES_API + "{path_type}/guid/{guid}"

GET_TYPE_DEF_BY_NAME = API(
    TYPEDEF_BY_NAME, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
GET_TYPE_DEF_BY_GUID = API(
    TYPEDEF_BY_GUID, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
GET_ALL_TYPE_DEFS = API(
    TYPEDEFS_API, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
GET_ALL_TYPE_DEF_HEADERS = API(
    f"{TYPEDEFS_API}headers", HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
UPDATE_TYPE_DEFS = API(
    TYPEDEFS_API, HTTPMethod.PUT, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
CREATE_TYPE_DEFS = API(
    TYPEDEFS_API, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.ATLAS
)
DELETE_TYPE_DEFS = API(
    TYPEDEFS_API, HTTPMethod.DELETE, HTTPStatus.NO_CONTENT, endpoint=EndPoint.ATLAS
)
DELETE_TYPE_DEF_BY_NAME = API(
    TYPEDEF_BY_NAME, HTTPMethod.DELETE, HTTPStatus.NO_CONTENT, endpoint=EndPoint.ATLAS
)

SSO_API = "idp/"
SSO_GROUP_MAPPER = SSO_API + "{sso_alias}/mappers"

GET_SSO_GROUP_MAPPING = API(
    SSO_GROUP_MAPPER + "/{group_map_id}",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
GET_ALL_SSO_GROUP_MAPPING = API(
    SSO_GROUP_MAPPER, HTTPMethod.GET, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
CREATE_SSO_GROUP_MAPPING = API(
    SSO_GROUP_MAPPER, HTTPMethod.POST, HTTPStatus.OK, endpoint=EndPoint.HERACLES
)
UPDATE_SSO_GROUP_MAPPING = API(
    SSO_GROUP_MAPPER + "/{group_map_id}",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
DELETE_SSO_GROUP_MAPPING = API(
    SSO_GROUP_MAPPER + "/{group_map_id}/delete",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
FILES_API = "files"
PRESIGNED_URL = API(
    FILES_API + "/presignedUrl",
    HTTPMethod.POST,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
PRESIGNED_URL_UPLOAD = API(
    "{presigned_url_put}",
    HTTPMethod.PUT,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
)
PRESIGNED_URL_DOWNLOAD = API(
    "{presigned_url_get}",
    HTTPMethod.GET,
    HTTPStatus.OK,
    endpoint=EndPoint.HERACLES,
    consumes=EVENT_STREAM,
    produces=EVENT_STREAM,
)
