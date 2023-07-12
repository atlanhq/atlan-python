# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from __future__ import annotations

import abc
import contextlib
import copy
import json
import logging
import os
from abc import ABC
from typing import ClassVar, Generator, Optional, Type, TypeVar, Union

import requests
from pydantic import (
    BaseSettings,
    HttpUrl,
    PrivateAttr,
    StrictStr,
    ValidationError,
    constr,
    parse_obj_as,
    validate_arguments,
)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pyatlan.client.constants import (
    ADD_BUSINESS_ATTRIBUTE_BY_ID,
    ADD_USER_TO_GROUPS,
    BULK_UPDATE,
    CHANGE_USER_ROLE,
    CREATE_GROUP,
    CREATE_TYPE_DEFS,
    CREATE_USERS,
    DELETE_ENTITY_BY_ATTRIBUTE,
    DELETE_ENTITY_BY_GUID,
    DELETE_GROUP,
    DELETE_TYPE_DEF_BY_NAME,
    DELETE_USER,
    GET_ALL_TYPE_DEFS,
    GET_CURRENT_USER,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_GROUP_MEMBERS,
    GET_GROUPS,
    GET_LINEAGE,
    GET_LINEAGE_LIST,
    GET_ROLES,
    GET_USER_GROUPS,
    GET_USERS,
    INDEX_SEARCH,
    PARSE_QUERY,
    PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE,
    REMOVE_USERS_FROM_GROUP,
    UPDATE_ENTITY_BY_ATTRIBUTE,
    UPDATE_GROUP,
    UPDATE_TYPE_DEFS,
    UPDATE_USER,
    UPLOAD_IMAGE,
)
from pyatlan.error import AtlanError, InvalidRequestError, LogicError, NotFoundError
from pyatlan.exceptions import AtlanServiceException, InvalidRequestException
from pyatlan.model.enums import (
    AtlanConnectorType,
    AtlanDeleteType,
    AtlanTypeCategory,
    CertificateStatus,
    LineageDirection,
)
from pyatlan.model.utils import Announcement
from pyatlan.multipart_data_generator import MultipartDataGenerator
from pyatlan.utils import (
    API,
    HTTPStatus,
    get_logger,
    unflatten_custom_metadata_for_entity,
)

LOGGER = get_logger()

T = TypeVar("T", bound="Referenceable")
A = TypeVar("A", bound="Asset")


def get_session():
    retry_strategy = Retry(
        total=10,
        backoff_factor=1,
        status_forcelist=[403, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.session()
    session.mount("https://", adapter)
    session.headers.update({"x-atlan-agent": "sdk", "x-atlan-agent-id": "python"})
    return session


def _build_typedef_request(typedef: TypeDef) -> TypeDefResponse:
    if isinstance(typedef, AtlanTagDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[typedef],
            enum_defs=[],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[],
        )
    elif isinstance(typedef, CustomMetadataDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[],
            enum_defs=[],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[typedef],
        )
    elif isinstance(typedef, EnumDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[],
            enum_defs=[typedef],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[],
        )
    else:
        raise InvalidRequestException(
            f"Unable to update type definitions of category: {typedef.category.value}",
            param="category",
        )
        # Throw an invalid request exception
    return payload


class AtlanClient(BaseSettings):
    class AtlanTagCache:
        _cache_by_id: dict[str, AtlanTagDef] = dict()
        _map_id_to_name: dict[str, str] = dict()
        _map_name_to_id: dict[str, str] = dict()
        _deleted_ids: set[str] = set()
        _deleted_names: set[str] = set()

        def __init__(self, client: "AtlanClient"):
            self._client = client

        def refresh_cache(self) -> None:
            response = self._client.get_typedefs(
                type_category=AtlanTypeCategory.CLASSIFICATION
            )
            if response is not None:
                self._cache_by_id = {}
                self._map_id_to_name = {}
                self._map_name_to_id = {}
                for atlan_tag in response.atlan_tag_defs:
                    atlan_tag_id = atlan_tag.name
                    atlan_tag_name = atlan_tag.display_name
                    self._cache_by_id[atlan_tag_id] = atlan_tag
                    self._map_id_to_name[atlan_tag_id] = atlan_tag_name
                    self._map_name_to_id[atlan_tag_name] = atlan_tag_id

        def get_id_for_name(self, name: str) -> Optional[str]:
            """
            Translate the provided human-readable classification name to its Atlan-internal ID string.
            """
            cls_id = self._map_name_to_id.get(name)
            if not cls_id and name not in self._deleted_names:
                # If not found, refresh the cache and look again (could be stale)
                self.refresh_cache()
                cls_id = self._map_name_to_id.get(name)
                if not cls_id:
                    # If still not found after refresh, mark it as deleted (could be
                    # an entry in an audit log that refers to a classification that
                    # no longer exists)
                    self._deleted_names.add(name)
            return cls_id

        def get_name_for_id(self, idstr: str) -> Optional[str]:
            """
            Translate the provided Atlan-internal classification ID string to the human-readable classification name.
            """
            cls_name = self._map_id_to_name.get(idstr)
            if not cls_name and idstr not in self._deleted_ids:
                # If not found, refresh the cache and look again (could be stale)
                self.refresh_cache()
                cls_name = self._map_id_to_name.get(idstr)
                if not cls_name:
                    # If still not found after refresh, mark it as deleted (could be
                    # an entry in an audit log that refers to a classification that
                    # no longer exists)
                    self._deleted_ids.add(idstr)
            return cls_name

    class CustomMetadataCache:
        _cache_by_id: dict[str, CustomMetadataDef] = dict()
        _map_id_to_name: dict[str, str] = dict()
        _map_id_to_type: dict[str, type] = dict()
        _map_name_to_id: dict[str, str] = dict()
        _map_attr_id_to_name: dict[str, dict[str, str]] = dict()
        _map_attr_name_to_id: dict[str, dict[str, str]] = dict()
        _archived_attr_ids: dict[str, str] = dict()
        _types_by_asset: dict[str, set[type]] = dict()

        def __init__(self, client: "AtlanClient"):
            self._client = client

        def refresh_cache(self) -> None:
            response = self._client.get_typedefs(
                type_category=AtlanTypeCategory.CUSTOM_METADATA
            )
            if response is not None:
                self._map_id_to_name = {}
                self._map_name_to_id = {}
                self._map_attr_id_to_name = {}
                self._map_attr_name_to_id = {}
                self._archived_attr_ids = {}
                self._cache_by_id = {}
                for cm in response.custom_metadata_defs:
                    type_id = cm.name
                    type_name = cm.display_name
                    self._cache_by_id[type_id] = cm
                    self._map_id_to_name[type_id] = type_name
                    self._map_name_to_id[type_name] = type_id
                    self._map_attr_id_to_name[type_id] = {}
                    self._map_attr_name_to_id[type_id] = {}
                    if cm.attribute_defs:
                        for attr in cm.attribute_defs:
                            attr_id = str(attr.name)
                            attr_name = str(attr.display_name)
                            self._map_attr_id_to_name[type_id][attr_id] = attr_name
                            if attr.options and attr.options.is_archived:
                                self._archived_attr_ids[attr_id] = attr_name
                            elif attr_name in self._map_attr_name_to_id[type_id]:
                                raise LogicError(
                                    f"Multiple custom attributes with exactly the same name ({attr_name}) "
                                    f"found for: {type_name}",
                                    code="ATLAN-PYTHON-500-100",
                                )
                            else:
                                self._map_attr_name_to_id[type_id][attr_name] = attr_id

        def get_id_for_name(self, name: str) -> str:
            """
            Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.
            """
            if name is None or not name.strip():
                raise InvalidRequestError(
                    message="No name was provided when attempting to retrieve custom metadata.",
                    code="ATLAN-PYTHON-404-008",
                    param="",
                )
            if cm_id := self._map_name_to_id.get(name):
                return cm_id
            # If not found, refresh the cache and look again (could be stale)
            self.refresh_cache()
            if cm_id := self._map_name_to_id.get(name):
                return cm_id
            raise NotFoundError(
                message=f"Custom metadata with name {name} does not exist.",
                code="ATLAN-PYTHON-404-009",
            )

        def get_name_for_id(self, idstr: str) -> str:
            """
            Translate the provided Atlan-internal custom metadata ID string
            to the human-readable custom metadata set name.
            """
            if idstr is None or not idstr.strip():
                raise InvalidRequestError(
                    message="No ID was provided when attempting to retrieve custom metadata.",
                    code="ATLAN-PYTHON-404-008",
                    param="",
                )
            if cm_name := self._map_id_to_name.get(idstr):
                return cm_name
            # If not found, refresh the cache and look again (could be stale)
            self.refresh_cache()
            if cm_name := self._map_id_to_name.get(idstr):
                return cm_name
            raise NotFoundError(
                message=f"Custom metadata with ID {idstr} does not exist.",
                code="ATLAN-PYTHON-404-009",
            )

        def get_type_for_id(self, idstr: str) -> Optional[type]:
            if cm_type := self._map_id_to_type.get(idstr):
                return cm_type
            self.refresh_cache()
            return self._map_id_to_type.get(idstr)

        def get_all_custom_attributes(
            self, include_deleted: bool = False, force_refresh: bool = False
        ) -> dict[str, list[AttributeDef]]:
            """
            Retrieve all the custom metadata attributes. The map will be keyed by custom metadata set
            name, and the value will be a listing of all the attributes within that set (with all the details
            of each of those attributes).
            """
            if len(self._cache_by_id) == 0 or force_refresh:
                self.refresh_cache()
            m = {}
            for type_id, cm in self._cache_by_id.items():
                type_name = self.get_name_for_id(type_id)
                if not type_name:
                    raise NotFoundError(
                        f"The type_name for {type_id} could not be found.", code="fixme"
                    )
                attribute_defs = cm.attribute_defs
                if include_deleted:
                    to_include = attribute_defs
                else:
                    to_include = []
                    if attribute_defs:
                        to_include.extend(
                            attr
                            for attr in attribute_defs
                            if not attr.options or not attr.options.is_archived
                        )
                m[type_name] = to_include
            return m

        def get_attr_id_for_name(self, set_name: str, attr_name: str) -> str:
            """
            Translate the provided human-readable custom metadata set and attribute names
            to the Atlan-internal ID string for the attribute.
            """
            set_id = self.get_id_for_name(set_name)
            if sub_map := self._map_attr_name_to_id.get(set_id):
                attr_id = sub_map.get(attr_name)
                if attr_id:
                    # If found, return straight away
                    return attr_id
            # Otherwise, refresh the cache and look again (could be stale)
            self.refresh_cache()
            if sub_map := self._map_attr_name_to_id.get(set_id):
                attr_id = sub_map.get(attr_name)
                if attr_id:
                    # If found, return straight away
                    return attr_id
                raise NotFoundError(
                    message=f"Custom metadata property with name {attr_name} does not exist"
                    f"in custom metadata {set_name}.",
                    code="ATLAN-PYTHON-404-009",
                )
            raise NotFoundError(
                message=f"Custom metadata with ID {set_id} does not exist.",
                code="ATLAN-PYTHON-404-009",
            )

        def get_attr_name_for_id(self, set_id: str, attr_id: str) -> str:
            """
            Given the Atlan-internal ID stringfor the set and the Atlan-internal ID for the attribute return the
            human-readable custom metadata name for the attribute.
            """
            if sub_map := self._map_attr_id_to_name.get(set_id):
                if attr_name := sub_map.get(attr_id):
                    return attr_name
                self.refresh_cache()
                if sub_map := self._map_attr_id_to_name.get(set_id):
                    if attr_name := sub_map.get(attr_id):
                        return attr_name
            raise NotFoundError(
                message=f"Custom metadata property with ID {attr_id} does not exist in the custom metadata {set_id}.",
                code="ATLAN-PYTHON-404-009",
            )

        def _get_attributes_for_search_results(
            self, set_id: str
        ) -> Optional[list[str]]:
            if sub_map := self._map_attr_name_to_id.get(set_id):
                attr_ids = sub_map.values()
                return [f"{set_id}.{idstr}" for idstr in attr_ids]
            return None

        def get_attributes_for_search_results(
            self, set_name: str
        ) -> Optional[list[str]]:
            """
            Retrieve the full set of custom attributes to include on search results.
            """
            if set_id := self.get_id_for_name(set_name):
                if dot_names := self._get_attributes_for_search_results(set_id):
                    return dot_names
                self.refresh_cache()
                return self._get_attributes_for_search_results(set_id)
            return None

        def get_custom_metadata_def(self, name: str) -> CustomMetadataDef:
            """
            Retrieve the full custom metadata structure definition.
            """
            ba_id = self.get_id_for_name(name)
            if ba_id is None:
                raise ValueError(f"No custom metadata with the name: {name} exist")
            if typedef := self._cache_by_id.get(ba_id):
                return typedef
            else:
                raise ValueError(f"No custom metadata with the name: {name} found")

    class EnumCache:
        _cache_by_name: dict[str, EnumDef] = dict()

        def __init__(self, client: "AtlanClient"):
            self._client = client

        def refresh_cache(self) -> None:
            response = self._client.get_typedefs(type_category=AtlanTypeCategory.ENUM)
            self._cache_by_name = {}
            if response is not None:
                for enum in response.enum_defs:
                    type_name = enum.name
                    self._cache_by_name[type_name] = enum

        def get_by_name(self, name: str) -> Optional[EnumDef]:
            """
            Retrieve the enumeration definition by its name.
            """
            if name:
                if enum_def := self._cache_by_name.get(name):
                    return enum_def
                self.refresh_cache()
                return self._cache_by_name.get(name)
            return None

    class GroupCache:
        _map_id_to_name: dict[str, str] = dict()
        _map_name_to_id: dict[str, str] = dict()
        _map_alias_to_id: dict[str, str] = dict()

        def __init__(self, client: "AtlanClient"):
            self._client = client

        def _refresh_cache(self) -> None:
            groups = self._client.get_all_groups()
            if groups is not None:
                self._map_id_to_name = {}
                self._map_name_to_id = {}
                self._map_alias_to_id = {}
                for group in groups:
                    group_id = str(group.id)
                    group_name = str(group.name)
                    group_alias = str(group.alias)
                    self._map_id_to_name[group_id] = group_name
                    self._map_name_to_id[group_name] = group_id
                    self._map_alias_to_id[group_alias] = group_id

        def get_id_for_name(self, name: str) -> Optional[str]:
            """
            Translate the provided human-readable group name to its GUID.
            """
            if group_id := self._map_name_to_id.get(name):
                return group_id
            self._refresh_cache()
            return self._map_name_to_id.get(name)

        def get_id_for_alias(self, alias: str) -> Optional[str]:
            """
            Translate the provided alias to its GUID.
            """
            if group_id := self._map_alias_to_id.get(alias):
                return group_id
            self._refresh_cache()
            return self._map_alias_to_id.get(alias)

        def get_name_for_id(self, idstr: str) -> Optional[str]:
            """
            Translate the provided group GUID to the human-readable group name.
            """
            if group_name := self._map_id_to_name.get(idstr):
                return group_name
            self._refresh_cache()
            return self._map_id_to_name.get(idstr)

    class RoleCache:
        _cache_by_id: dict[str, AtlanRole] = dict()
        _map_id_to_name: dict[str, str] = dict()
        _map_name_to_id: dict[str, str] = dict()

        def __init__(self, client: "AtlanClient"):
            self._client = client

        def _refresh_cache(self) -> None:
            response = self._client.get_roles(
                limit=100, post_filter='{"name":{"$ilike":"$%"}}'
            )
            if response is not None:
                self._cache_by_id = {}
                self._map_id_to_name = {}
                self._map_name_to_id = {}
                for role in response.records:
                    role_id = role.id
                    role_name = role.name
                    self._cache_by_id[role_id] = role
                    self._map_id_to_name[role_id] = role_name
                    self._map_name_to_id[role_name] = role_id

        def get_id_for_name(self, name: str) -> Optional[str]:
            """
            Translate the provided human-readable role name to its GUID.
            """
            if role_id := self._map_name_to_id.get(name):
                return role_id
            self._refresh_cache()
            return self._map_name_to_id.get(name)

        def get_name_for_id(self, idstr: str) -> Optional[str]:
            """
            Translate the provided role GUID to the human-readable role name.
            """
            if role_name := self._map_id_to_name.get(idstr):
                return role_name
            self._refresh_cache()
            return self._map_id_to_name.get(idstr)

    class UserCache:
        _map_id_to_name: dict[str, str] = dict()
        _map_name_to_id: dict[str, str] = dict()
        _map_email_to_id: dict[str, str] = dict()

        def __init__(self, client: "AtlanClient"):
            self._client = client

        def _refresh_cache(self) -> None:
            users = self._client.get_all_users()
            if users is not None:
                self._map_id_to_name = {}
                self._map_name_to_id = {}
                self._map_email_to_id = {}
                for user in users:
                    user_id = str(user.id)
                    username = str(user.username)
                    user_email = str(user.email)
                    self._map_id_to_name[user_id] = username
                    self._map_name_to_id[username] = user_id
                    self._map_email_to_id[user_email] = user_id

        def get_id_for_name(self, name: str) -> Optional[str]:
            """
            Translate the provided human-readable username to its GUID.
            """
            if user_id := self._map_name_to_id.get(name):
                return user_id
            self._refresh_cache()
            return self._map_name_to_id.get(name)

        def get_id_for_email(self, email: str) -> Optional[str]:
            """
            Translate the provided email to its GUID.
            """
            if user_id := self._map_email_to_id.get(email):
                return user_id
            self._refresh_cache()
            return self._map_email_to_id.get(email)

        def get_name_for_id(self, idstr: str) -> Optional[str]:
            """
            Translate the provided user GUID to the human-readable username.
            """
            if username := self._map_id_to_name.get(idstr):
                return username
            self._refresh_cache()
            return self._map_id_to_name.get(idstr)

    _default_client: "ClassVar[Optional[AtlanClient]]" = None
    base_url: HttpUrl
    api_key: str
    _session: requests.Session = PrivateAttr(default_factory=get_session)
    _request_params: dict = PrivateAttr()
    _atlan_tag_cache: AtlanClient.AtlanTagCache = PrivateAttr()
    _custom_metadata_cache: AtlanClient.CustomMetadataCache = PrivateAttr()
    _enum_cache: AtlanClient.EnumCache = PrivateAttr()
    _group_cache: AtlanClient.GroupCache = PrivateAttr()
    _role_cache: AtlanClient.RoleCache = PrivateAttr()
    _user_cache: AtlanClient.UserCache = PrivateAttr()

    class Config:
        env_prefix = "atlan_"

    class SearchResults(ABC):
        def __init__(
            self,
            client: "AtlanClient",
            endpoint: API,
            criteria: SearchRequest,
            start: int,
            size: int,
            assets: list[Asset],
        ):
            self._client = client
            self._endpoint = endpoint
            self._criteria = criteria
            self._start = start
            self._size = size
            self._assets = assets

        def current_page(self) -> list[Asset]:
            return self._assets

        def next_page(self, start=None, size=None) -> bool:
            self._start = start or self._start + self._size
            if size:
                self._size = size
            return self._get_next_page() if self._assets else False

        @abc.abstractmethod
        def _get_next_page(self):
            pass

        # TODO Rename this here and in `next_page`
        def _get_next_page_json(self):
            raw_json = self._client._call_api(
                self._endpoint,
                request_obj=self._criteria,
            )
            if "entities" not in raw_json:
                self._assets = []
                return None
            self._assets = parse_obj_as(list[Asset], raw_json["entities"])
            return raw_json

        def __iter__(self) -> Generator[Asset, None, None]:
            while True:
                yield from self.current_page()
                if not self.next_page():
                    break

    class IndexSearchResults(SearchResults):
        def __init__(
            self,
            client: "AtlanClient",
            criteria: IndexSearchRequest,
            start: int,
            size: int,
            count: int,
            assets: list[Asset],
        ):
            super().__init__(client, INDEX_SEARCH, criteria, start, size, assets)
            self._count = count

        def _get_next_page(self):
            self._criteria.dsl.from_ = self._start
            self._criteria.dsl.size = self._size
            if raw_json := super()._get_next_page_json():
                self._count = (
                    raw_json["approximateCount"]
                    if "approximateCount" in raw_json
                    else 0
                )
                return True
            return False

        @property
        def count(self) -> int:
            return self._count

    class LineageListResults(SearchResults):
        def __init__(
            self,
            client: "AtlanClient",
            criteria: LineageListRequest,
            start: int,
            size: int,
            has_more: bool,
            assets: list[Asset],
        ):
            super().__init__(client, GET_LINEAGE_LIST, criteria, start, size, assets)
            self._has_more = has_more

        def _get_next_page(self):
            self._criteria.offset = self._start
            self._criteria.size = self._size
            if raw_json := super()._get_next_page_json():
                self._has_more = parse_obj_as(bool, raw_json["hasMore"])
                return True
            return False

        @property
        def has_more(self) -> bool:
            return self._has_more

    @classmethod
    def register_client(cls, client: "AtlanClient"):
        if not isinstance(client, AtlanClient):
            raise ValueError("client must be an instance of AtlanClient")
        cls._default_client = client

    @classmethod
    def get_default_client(cls) -> "Optional[AtlanClient]":
        return cls._default_client

    @classmethod
    def get_default_client_or_fail(cls) -> "AtlanClient":
        if not cls._default_client:
            raise ValueError("No default client configured.")
        return cls._default_client

    @classmethod
    def reset_default_client(cls):
        """Sets the default_client to None"""
        cls._default_client = None

    def __init__(self, **data):
        super().__init__(**data)
        self._request_params = {"headers": {"authorization": f"Bearer {self.api_key}"}}
        self._atlan_tag_cache = AtlanClient.AtlanTagCache(self)
        self._custom_metadata_cache = AtlanClient.CustomMetadataCache(self)
        self._enum_cache = AtlanClient.EnumCache(self)
        self._group_cache = AtlanClient.GroupCache(self)
        self._role_cache = AtlanClient.RoleCache(self)
        self._user_cache = AtlanClient.UserCache(self)

    @property
    def atlan_tag_cache(self) -> AtlanClient.AtlanTagCache:
        return self._atlan_tag_cache

    @property
    def custom_metadata_cache(self) -> AtlanClient.CustomMetadataCache:
        return self._custom_metadata_cache

    @property
    def enum_cache(self) -> AtlanClient.EnumCache:
        return self._enum_cache

    @property
    def group_cache(self) -> AtlanClient.GroupCache:
        return self._group_cache

    @property
    def role_cache(self) -> AtlanClient.RoleCache:
        return self._role_cache

    @property
    def user_cache(self) -> AtlanClient.UserCache:
        return self._user_cache

    def _call_api_internal(self, api, path, params, binary_data=None):
        if binary_data:
            response = self._session.request(
                api.method.value, path, data=binary_data, **params
            )
        else:
            response = self._session.request(api.method.value, path, **params)
        if response is not None:
            LOGGER.debug("HTTP Status: %s", response.status_code)
        if response is None:
            return None
        if response.status_code == api.expected_status:
            try:
                if (
                    response.content is None
                    or response.content == "null"
                    or len(response.content) == 0
                    or response.status_code == HTTPStatus.NO_CONTENT
                ):
                    return None
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "<== __call_api(%s,%s), result = %s",
                        vars(api),
                        params,
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
            with contextlib.suppress(ValueError, json.decoder.JSONDecodeError):
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

    def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset: bool = True
    ):
        params, path = self._create_params(
            api, query_params, request_obj, exclude_unset
        )
        return self._call_api_internal(api, path, params)

    def _upload_file(self, api, file=None, filename=None):
        generator = MultipartDataGenerator()
        generator.add_file(file=file, filename=filename)
        post_data = generator.get_post_data()
        api.produces = f"multipart/form-data; boundary={generator.boundary}"
        params, path = self._create_params(
            api, query_params=None, request_obj=None, exclude_unset=True
        )
        return self._call_api_internal(api, path, params, binary_data=post_data)

    def _create_params(
        self, api, query_params, request_obj, exclude_unset: bool = True
    ):
        params = copy.deepcopy(self._request_params)
        path = os.path.join(self.base_url, api.path)
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        if query_params is not None:
            params["params"] = query_params
        if request_obj is not None:
            if isinstance(request_obj, AtlanObject):
                params["data"] = request_obj.json(
                    by_alias=True, exclude_unset=exclude_unset
                )
            else:
                params["data"] = json.dumps(request_obj)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("------------------------------------------------------")
            LOGGER.debug("Call         : %s %s", api.method, path)
            LOGGER.debug("Content-type_ : %s", api.consumes)
            LOGGER.debug("Accept       : %s", api.produces)
        return params, path

    def _refresh_caches(self, typedef: TypeDef) -> None:
        if isinstance(typedef, AtlanTagDef):
            self.atlan_tag_cache.refresh_cache()
        if isinstance(typedef, CustomMetadataDef):
            self.custom_metadata_cache.refresh_cache()
        if isinstance(typedef, EnumDef):
            self.enum_cache.refresh_cache()

    def upload_image(self, file, filename: str) -> AtlanImage:
        raw_json = self._upload_file(UPLOAD_IMAGE, file=file, filename=filename)
        return AtlanImage(**raw_json)

    def get_roles(
        self,
        limit: int,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        query_params: dict[str, str] = {
            "count": str(count),
            "offset": str(offset),
            "limit": str(limit),
        }
        if post_filter:
            query_params["filter"] = post_filter
        if sort:
            query_params["sort"] = sort
        raw_json = self._call_api(GET_ROLES.format_path_with_params(), query_params)
        return RoleResponse(**raw_json)

    def get_all_roles(self) -> RoleResponse:
        """
        Retrieve all roles defined in Atlan.
        """
        raw_json = self._call_api(GET_ROLES.format_path_with_params())
        return RoleResponse(**raw_json)

    def create_group(
        self,
        group: AtlanGroup,
        user_ids: Optional[list[str]] = None,
    ) -> CreateGroupResponse:
        payload = CreateGroupRequest(group=group)
        if user_ids:
            payload.users = user_ids
        raw_json = self._call_api(CREATE_GROUP, request_obj=payload, exclude_unset=True)
        return CreateGroupResponse(**raw_json)

    def update_group(
        self,
        group: AtlanGroup,
    ) -> None:
        self._call_api(
            UPDATE_GROUP.format_path_with_params(group.id),
            request_obj=group,
            exclude_unset=True,
        )

    def purge_group(
        self,
        guid: str,
    ) -> None:
        self._call_api(DELETE_GROUP.format_path({"group_guid": guid}))

    def get_groups(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> GroupResponse:
        query_params: dict[str, str] = {
            "count": str(count),
            "offset": str(offset),
        }
        if limit is not None:
            query_params["limit"] = str(limit)
        if post_filter is not None:
            query_params["filter"] = post_filter
        if sort is not None:
            query_params["sort"] = sort
        raw_json = self._call_api(GET_GROUPS.format_path_with_params(), query_params)
        return GroupResponse(**raw_json)

    def get_all_groups(self) -> list[AtlanGroup]:
        """
        Retrieve all groups defined in Atlan.
        """
        groups: list[AtlanGroup] = []
        offset = 0
        limit = 100
        response: Optional[GroupResponse] = self.get_groups(
            offset=offset, limit=limit, sort="createdAt"
        )
        while response:
            if page := response.records:
                groups.extend(page)
                offset += limit
                response = self.get_groups(offset=offset, limit=limit, sort="createdAt")
            else:
                response = None
        return groups

    def get_group_by_name(
        self, alias: str, limit: int = 100
    ) -> Optional[list[AtlanGroup]]:
        """
        Retrieve all groups with a name that contains the provided string.
        (This could include a complete group name, in which case there should be at most
        a single item in the returned list, or could be a partial group name to retrieve
        all groups with that naming convention.)
        """
        if response := self.get_groups(
            offset=0,
            limit=limit,
            post_filter='{"$and":[{"alias":{"$ilike":"%' + alias + '%"}}]}',
        ):
            return response.records
        return None

    def get_group_members(self, guid: str) -> UserResponse:
        """
        Retrieves the members (users) of a group.
        """
        raw_json = self._call_api(GET_GROUP_MEMBERS.format_path({"group_guid": guid}))
        return UserResponse(**raw_json)

    def remove_users_from_group(self, guid: str, user_ids=list[str]) -> None:
        """
        Remove one or more users from a group.
        """
        rfgr = RemoveFromGroupRequest(users=user_ids)
        self._call_api(
            REMOVE_USERS_FROM_GROUP.format_path({"group_guid": guid}),
            request_obj=rfgr,
            exclude_unset=True,
        )

    def create_users(
        self,
        users: list[AtlanUser],
    ) -> None:
        cur = CreateUserRequest(users=[])
        for user in users:
            role_name = str(user.workspace_role)
            if role_id := self.role_cache.get_id_for_name(role_name):
                to_create = CreateUserRequest.CreateUser(
                    email=user.email,
                    role_name=role_name,
                    role_id=role_id,
                )
                cur.users.append(to_create)
        self._call_api(CREATE_USERS, request_obj=cur, exclude_unset=True)

    def update_user(
        self,
        guid: str,
        user: AtlanUser,
    ) -> UserMinimalResponse:
        raw_json = self._call_api(
            UPDATE_USER.format_path_with_params(guid),
            request_obj=user,
            exclude_unset=True,
        )
        return UserMinimalResponse(**raw_json)

    def purge_user(
        self,
        guid: str,
    ) -> None:
        self._call_api(DELETE_USER.format_path({"user_guid": guid}))

    def get_groups_for_user(
        self,
        guid: str,
    ) -> GroupResponse:
        raw_json = self._call_api(GET_USER_GROUPS.format_path({"user_guid": guid}))
        return GroupResponse(**raw_json)

    def add_user_to_groups(
        self,
        guid: str,
        group_ids: list[str],
    ) -> None:
        atgr = AddToGroupsRequest(groups=group_ids)
        self._call_api(
            ADD_USER_TO_GROUPS.format_path({"user_guid": guid}),
            request_obj=atgr,
            exclude_unset=True,
        )

    def change_user_role(
        self,
        guid: str,
        role_id: str,
    ) -> None:
        crr = ChangeRoleRequest(role_id=role_id)
        self._call_api(
            CHANGE_USER_ROLE.format_path({"user_guid": guid}),
            request_obj=crr,
            exclude_unset=True,
        )

    def get_current_user(
        self,
    ) -> UserMinimalResponse:
        raw_json = self._call_api(GET_CURRENT_USER)
        return UserMinimalResponse(**raw_json)

    def get_users(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> UserResponse:
        query_params: dict[str, str] = {
            "count": str(count),
            "offset": str(offset),
        }
        if limit is not None:
            query_params["limit"] = str(limit)
        if post_filter is not None:
            query_params["filter"] = post_filter
        if sort is not None:
            query_params["sort"] = sort
        raw_json = self._call_api(GET_USERS.format_path_with_params(), query_params)
        return UserResponse(**raw_json)

    def get_all_users(self) -> list[AtlanUser]:
        """
        Retrieve all users defined in Atlan.
        """
        users: list[AtlanUser] = []
        offset = 0
        limit = 100
        response: Optional[UserResponse] = self.get_users(
            offset=offset, limit=limit, sort="username"
        )
        while response:
            if page := response.records:
                users.extend(page)
                offset += limit
                response = self.get_users(offset=offset, limit=limit, sort="username")
            else:
                response = None
        return users

    def get_users_by_email(
        self, email: str, limit: int = 100
    ) -> Optional[list[AtlanUser]]:
        """
        Retrieves all users with email addresses that contain the provided email.
        (This could include a complete email address, in which case there should be at
        most a single item in the returned list, or could be a partial email address
        such as "@example.com" to retrieve all users with that domain in their email
        address.)
        """
        if response := self.get_users(
            offset=0,
            limit=limit,
            post_filter='{"email":{"$ilike":"%' + email + '%"}}',
        ):
            return response.records
        return None

    def get_user_by_username(self, username: str) -> Optional[AtlanUser]:
        """
        Retrieves a user based on the username. (This attempts an exact match on username
        rather than a contains search.)
        """
        if response := self.get_users(
            offset=0,
            limit=5,
            post_filter='{"username":"' + username + '"}',
        ):
            if response.records and len(response.records) >= 1:
                return response.records[0]
        return None

    def parse_query(self, query: QueryParserRequest) -> Optional[ParsedQuery]:
        """
        Parses the provided query to describe its component parts.
        """
        raw_json = self._call_api(
            PARSE_QUERY,
            request_obj=query,
            exclude_unset=True,
        )
        return ParsedQuery(**raw_json)

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
            asset = self.handle_relationships(raw_json)
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
            asset = self.handle_relationships(raw_json)
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

    def handle_relationships(self, raw_json):
        if (
            "relationshipAttributes" in raw_json["entity"]
            and raw_json["entity"]["relationshipAttributes"]
        ):
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
        raw_json["entity"]["relationshipAttributes"] = {}
        asset = AssetResponse[A](**raw_json).entity
        asset.is_incomplete = False
        return asset

    @validate_arguments()
    def retrieve_minimal(self, guid: str, asset_type: Type[A]) -> A:
        return self.get_asset_by_guid(
            guid=guid,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )

    def upsert(
        self,
        entity: Union[Asset, list[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        query_params = {
            "replaceClassifications": replace_atlan_tags,
            "replaceBusinessAttributes": replace_custom_metadata,
            "overwriteBusinessAttributes": overwrite_custom_metadata,
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

    def upsert_merging_cm(
        self, entity: Union[Asset, list[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        query_params = {
            "replaceClassifications": replace_atlan_tags,
            "replaceBusinessAttributes": True,
            "overwriteBusinessAttributes": False,
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

    def upsert_replacing_cm(
        self, entity: Union[Asset, list[Asset]], replace_atlan_tagss: bool = False
    ) -> AssetMutationResponse:
        query_params = {
            "replaceClassifications": replace_atlan_tagss,
            "replaceBusinessAttributes": True,
            "overwriteBusinessAttributes": True,
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

    def delete_entity_by_guid(self, guid) -> AssetMutationResponse:
        raw_json = self._call_api(
            DELETE_ENTITY_BY_GUID.format_path_with_params(guid),
            {"deleteType": AtlanDeleteType.SOFT.value},
        )
        return AssetMutationResponse(**raw_json)

    def search(self, criteria: IndexSearchRequest) -> IndexSearchResults:
        raw_json = self._call_api(
            INDEX_SEARCH,
            request_obj=criteria,
        )
        if "entities" in raw_json:
            try:
                for entity in raw_json["entities"]:
                    unflatten_custom_metadata_for_entity(
                        entity=entity, attributes=criteria.attributes
                    )
                assets = parse_obj_as(list[Asset], raw_json["entities"])
            except ValidationError as err:
                LOGGER.error("Problem parsing JSON: %s", raw_json["entities"])
                raise err
        else:
            assets = []
        count = raw_json["approximateCount"] if "approximateCount" in raw_json else 0
        return AtlanClient.IndexSearchResults(
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

    def get_typedefs(self, type_category: AtlanTypeCategory) -> TypeDefResponse:
        query_params = {"type": type_category.value}
        raw_json = self._call_api(
            GET_ALL_TYPE_DEFS.format_path_with_params(),
            query_params,
        )
        return TypeDefResponse(**raw_json)

    def create_typedef(self, typedef: TypeDef) -> TypeDefResponse:
        payload = _build_typedef_request(typedef)
        raw_json = self._call_api(
            CREATE_TYPE_DEFS, request_obj=payload, exclude_unset=True
        )
        self._refresh_caches(typedef)
        return TypeDefResponse(**raw_json)

    def update_typedef(self, typedef: TypeDef) -> TypeDefResponse:
        payload = _build_typedef_request(typedef)
        raw_json = self._call_api(
            UPDATE_TYPE_DEFS, request_obj=payload, exclude_unset=True
        )
        self._refresh_caches(typedef)
        return TypeDefResponse(**raw_json)

    def purge_typedef(self, name: str, typedef_type: type) -> None:
        if typedef_type == CustomMetadataDef:
            internal_name = self.custom_metadata_cache.get_id_for_name(name)
        elif typedef_type == EnumDef:
            internal_name = name
        elif typedef_type == AtlanTagDef:
            internal_name = str(self.atlan_tag_cache.get_id_for_name(name))
        else:
            raise InvalidRequestException(
                message=f"Unable to purge type definitions of type: {typedef_type}",
            )
            # Throw an invalid request exception
        if internal_name:
            self._call_api(
                DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name)
            )
        else:
            raise NotFoundError(
                message=f"Unable to find {typedef_type} with name: {name}",
                code="ATLAN-PYTHON-404-000",
            )

        if typedef_type == CustomMetadataDef:
            self.custom_metadata_cache.refresh_cache()
        elif typedef_type == EnumDef:
            self.enum_cache.refresh_cache()
        elif typedef_type == AtlanTagDef:
            self.atlan_tag_cache.refresh_cache()

    @validate_arguments()
    def add_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: list[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
    ) -> None:
        atlan_tags = AtlanTags(
            __root__=[
                AtlanTag(
                    type_name=AtlanTagName(display_text=name),
                    propagate=propagate,
                    remove_propagations_on_entity_delete=remove_propagation_on_delete,
                    restrict_propagation_through_lineage=restrict_lineage_propagation,
                )
                for name in atlan_tag_names
            ]
        )
        query_params = {"attr:qualifiedName": qualified_name}
        self._call_api(
            UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classifications"
            ),
            query_params,
            atlan_tags,
        )

    @validate_arguments()
    def remove_atlan_tag(
        self, asset_type: Type[A], qualified_name: str, atlan_tag_name: str
    ) -> None:
        classification_id = self.atlan_tag_cache.get_id_for_name(atlan_tag_name)
        if not classification_id:
            raise ValueError(f"{atlan_tag_name} is not a valid AtlanTag")
        query_params = {"attr:qualifiedName": qualified_name}
        self._call_api(
            DELETE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classification", classification_id
            ),
            query_params,
        )

    @validate_arguments()
    def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        message: str,
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.certificate_status = certificate_status
        asset.name = name
        asset.certificate_status_message = message
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    def _update_asset_by_attribute(self, asset, asset_type, qualified_name: str):
        query_params = {"attr:qualifiedName": qualified_name}
        raw_json = self._call_api(
            PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__
            ),
            query_params,
            AssetRequest[Asset](entity=asset),
        )
        response = AssetMutationResponse(**raw_json)
        if assets := response.assets_partially_updated(asset_type=asset_type):
            return assets[0]
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return None

    @validate_arguments()
    def remove_certificate(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_certificate()
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments()
    def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.set_announcement(announcement)
        asset.name = name
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments()
    def remove_announcement(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_announcement()
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        custom_metadata_request = CustomMetadataRequest.create(
            client=self, custom_metadata_dict=custom_metadata
        )
        self._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {
                    "entity_guid": guid,
                    "bm_id": custom_metadata_request.custom_metadata_set_id,
                }
            ),
            None,
            custom_metadata_request,
        )

    def replace_custom_metadata(self, guid: str, custom_metadata: CustomMetadataDict):
        # clear unset attributes so that they are removed
        custom_metadata.clear_unset()
        custom_metadata_request = CustomMetadataRequest.create(
            client=self, custom_metadata_dict=custom_metadata
        )
        self._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {
                    "entity_guid": guid,
                    "bm_id": custom_metadata_request.custom_metadata_set_id,
                }
            ),
            None,
            custom_metadata_request,
        )

    def remove_custom_metadata(self, guid: str, cm_name: str):
        custom_metadata = CustomMetadataDict(client=self, name=cm_name)
        # invoke clear_all so all attributes are set to None and consequently removed
        custom_metadata.clear_all()
        custom_metadata_request = CustomMetadataRequest.create(
            client=self, custom_metadata_dict=custom_metadata
        )
        self._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {
                    "entity_guid": guid,
                    "bm_id": custom_metadata_request.custom_metadata_set_id,
                }
            ),
            None,
            custom_metadata_request,
        )

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def append_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        if guid:
            if qualified_name:
                raise ValueError(
                    "Either guid or qualified_name can be be specified not both"
                )
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ValueError("Either guid or qualified name must be specified")
        if not terms:
            return asset
        replacement_terms: list[AtlasGlossaryTerm] = []
        if existing_terms := asset.assigned_terms:
            replacement_terms.extend(
                term for term in existing_terms if term.relationship_status != "DELETED"
            )
        replacement_terms.extend(terms)
        asset.assigned_terms = replacement_terms
        response = self.upsert(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def replace_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        if guid:
            if qualified_name:
                raise ValueError(
                    "Either guid or qualified_name can be be specified not both"
                )
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ValueError("Either guid or qualified name must be specified")
        asset.assigned_terms = terms
        response = self.upsert(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def remove_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        if not terms:
            raise ValueError("A list of assigned_terms to remove must be specified")
        if guid:
            if qualified_name:
                raise ValueError(
                    "Either guid or qualified_name can be be specified not both"
                )
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ValueError("Either guid or qualified name must be specified")
        replacement_terms: list[AtlasGlossaryTerm] = []
        guids_to_be_removed = {t.guid for t in terms}
        if existing_terms := asset.assigned_terms:
            replacement_terms.extend(
                term
                for term in existing_terms
                if term.relationship_status != "DELETED"
                and term.guid not in guids_to_be_removed
            )
        asset.assigned_terms = replacement_terms
        response = self.upsert(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def find_connections_by_name(
        self,
        name: str,
        connector_type: AtlanConnectorType,
        attributes: Optional[list[str]] = None,
    ) -> list[Connection]:
        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name("CONNECTION")
            + Term.with_name(name)
            + Term(field="connectorName", value=connector_type.value)
        )
        dsl = DSL(query=query)
        search_request = IndexSearchRequest(
            dsl=dsl,
            attributes=attributes,
        )
        results = self.search(search_request)
        return [asset for asset in results if isinstance(asset, Connection)]

    def get_lineage(self, lineage_request: LineageRequest) -> LineageResponse:
        raw_json = self._call_api(
            GET_LINEAGE, None, lineage_request, exclude_unset=False
        )
        return LineageResponse(**raw_json)

    def get_lineage_list(
        self, lineage_request: LineageListRequest
    ) -> LineageListResults:
        if lineage_request.direction == LineageDirection.BOTH:
            raise InvalidRequestException(
                message="Unable to request both directions of lineage at the same time through the lineage list API.",
            )
        raw_json = self._call_api(
            GET_LINEAGE_LIST, None, request_obj=lineage_request, exclude_unset=True
        )
        if "entities" in raw_json:
            try:
                assets = parse_obj_as(list[Asset], raw_json["entities"])
                has_more = parse_obj_as(bool, raw_json["hasMore"])
            except ValidationError as err:
                LOGGER.error("Problem parsing JSON: %s", raw_json["entities"])
                raise err
        else:
            assets = []
            has_more = False
        return AtlanClient.LineageListResults(
            client=self,
            criteria=lineage_request,
            start=lineage_request.offset or 0,
            size=lineage_request.size or 10,
            has_more=has_more,
            assets=assets,
        )

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def find_personas_by_name(
        self,
        name: str,
        attributes: Optional[list[str]] = None,
    ) -> list[Persona]:
        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name("PERSONA")
            + Term.with_name(name)
        )
        dsl = DSL(query=query)
        search_request = IndexSearchRequest(
            dsl=dsl,
            attributes=attributes,
        )
        results = self.search(search_request)
        return [asset for asset in results if isinstance(asset, Persona)]

    def find_purposes_by_name(
        self,
        name: str,
        attributes: Optional[list[str]] = None,
    ) -> list[Purpose]:
        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name("PURPOSE")
            + Term.with_name(name)
        )
        dsl = DSL(query=query)
        search_request = IndexSearchRequest(
            dsl=dsl,
            attributes=attributes,
        )
        results = self.search(search_request)
        return [asset for asset in results if isinstance(asset, Purpose)]

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def find_glossary_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> AtlasGlossary:
        if attributes is None:
            attributes = []
        query = with_active_glossary(name=name)
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def find_category_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> AtlasGlossaryCategory:
        if attributes is None:
            attributes = []
        query = with_active_category(
            name=name, glossary_qualified_name=glossary_qualified_name
        )
        return self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=AtlasGlossaryCategory,
            attributes=attributes,
        )

    @validate_arguments()
    def find_category_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ):
        glossary = self.find_glossary_by_name(name=glossary_name)
        return self.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,  # type: ignore
            attributes=attributes,
        )

    def _search_for_asset_with_name(
        self,
        query: Query,
        name: str,
        asset_type: Type[A],
        attributes: Optional[list[StrictStr]],
    ) -> A:
        dsl = DSL(query=query)
        search_request = IndexSearchRequest(
            dsl=dsl,
            attributes=attributes,
        )
        results = self.search(search_request)
        if results.count > 0 and (
            assets := [
                asset
                for asset in results.current_page()
                if isinstance(asset, asset_type)
            ]
        ):
            if len(assets) > 1:
                LOGGER.warning(
                    "More than 1 %s found with the name '%s', returning only the first.",
                    asset_type.__name__,
                    name,
                )
            return assets[0]
        raise NotFoundError(
            f"The {asset_type.__name__} asset could not be found by name: {name}.",
            "ATLAN-PYTHON-404-014",
        )

    # @validate_arguments()  # Does not work with forward references: https://github.com/pydantic/pydantic/issues/2901
    def find_term_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        if attributes is None:
            attributes = []
        query = with_active_term(
            name=name, glossary_qualified_name=glossary_qualified_name
        )
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossaryTerm, attributes=attributes
        )

    @validate_arguments()
    def find_term_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ):
        glossary = self.find_glossary_by_name(name=glossary_name)
        return self.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,  # type: ignore
            attributes=attributes,
        )


from pyatlan.model.assets import (  # noqa: E402
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    MaterialisedView,
    Persona,
    Purpose,
    Referenceable,
    Schema,
    Table,
    View,
)
from pyatlan.model.atlan_image import AtlanImage  # noqa: E402
from pyatlan.model.core import (  # noqa: E402
    AssetRequest,
    AssetResponse,
    AtlanObject,
    AtlanTag,
    AtlanTagName,
    AtlanTags,
    BulkRequest,
    SearchRequest,
)
from pyatlan.model.custom_metadata import (  # noqa: E402
    CustomMetadataDict,
    CustomMetadataRequest,
)
from pyatlan.model.group import (  # noqa: E402
    AtlanGroup,
    CreateGroupRequest,
    CreateGroupResponse,
    GroupResponse,
    RemoveFromGroupRequest,
)
from pyatlan.model.lineage import (  # noqa: E402
    LineageListRequest,
    LineageRequest,
    LineageResponse,
)
from pyatlan.model.query import ParsedQuery, QueryParserRequest  # noqa: E402
from pyatlan.model.response import AssetMutationResponse  # noqa: E402
from pyatlan.model.role import AtlanRole, RoleResponse  # noqa: E402
from pyatlan.model.search import (  # noqa: E402
    DSL,
    IndexSearchRequest,
    Query,
    Term,
    with_active_category,
    with_active_glossary,
    with_active_term,
)
from pyatlan.model.typedef import (  # noqa: E402
    AtlanTagDef,
    AttributeDef,
    CustomMetadataDef,
    EnumDef,
    TypeDef,
    TypeDefResponse,
)
from pyatlan.model.user import (  # noqa: E402
    AddToGroupsRequest,
    AtlanUser,
    ChangeRoleRequest,
    CreateUserRequest,
    UserMinimalResponse,
    UserResponse,
)

# Assets = Union[
#     AtlasGlossary,  # type: ignore
#     AtlasGlossaryCategory,  # type: ignore
#     AtlasGlossaryTerm,  # type: ignore
#     Connection,  # type: ignore
#     Database,  # type: ignore
#     Schema,  # type: ignore
#     Table,  # type: ignore
#     View,  # type: ignore
#     MaterialisedView,  # type: ignore
# ]
Asset_Types = Union[
    Type[AtlasGlossary],  # type: ignore
    Type[AtlasGlossaryCategory],  # type: ignore
    Type[AtlasGlossaryTerm],  # type: ignore
    Type[Connection],  # type: ignore
    Type[Database],  # type: ignore
    Type[Schema],  # type: ignore
    Type[Table],  # type: ignore
    Type[View],  # type: ignore
    Type[MaterialisedView],  # type: ignore
]

AtlanClient.update_forward_refs()
AssetResponse[A].update_forward_refs()
