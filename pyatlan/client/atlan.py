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
import time
import uuid
from abc import ABC
from types import SimpleNamespace
from typing import ClassVar, Generator, Iterable, Optional, Type, TypeVar, Union
from warnings import warn

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
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from urllib3.util.retry import Retry

from pyatlan.client.audit import AuditClient
from pyatlan.client.constants import (
    ADD_BUSINESS_ATTRIBUTE_BY_ID,
    ADMIN_EVENTS,
    BULK_UPDATE,
    DELETE_ENTITIES_BY_GUIDS,
    DELETE_ENTITY_BY_ATTRIBUTE,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_LINEAGE,
    GET_LINEAGE_LIST,
    INDEX_SEARCH,
    KEYCLOAK_EVENTS,
    PARSE_QUERY,
    PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE,
    UPDATE_ENTITY_BY_ATTRIBUTE,
    UPLOAD_IMAGE,
)
from pyatlan.client.group import GroupClient
from pyatlan.client.role import RoleClient
from pyatlan.client.token import TokenClient
from pyatlan.client.typedef import TypeDefClient
from pyatlan.client.user import UserClient
from pyatlan.client.workflow import WorkflowClient
from pyatlan.errors import ERROR_CODE_FOR_HTTP_STATUS, AtlanError, ErrorCode
from pyatlan.model.aggregation import Aggregations
from pyatlan.model.api_tokens import ApiToken, ApiTokenResponse
from pyatlan.model.assets import (
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
from pyatlan.model.atlan_image import AtlanImage
from pyatlan.model.core import (
    Announcement,
    AssetRequest,
    AssetResponse,
    AtlanObject,
    AtlanTag,
    AtlanTagName,
    AtlanTags,
    BulkRequest,
    SearchRequest,
)
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataRequest
from pyatlan.model.enums import (
    AtlanConnectorType,
    AtlanDeleteType,
    AtlanTypeCategory,
    CertificateStatus,
    EntityStatus,
    LineageDirection,
)
from pyatlan.model.group import AtlanGroup, CreateGroupResponse, GroupResponse
from pyatlan.model.lineage import LineageListRequest, LineageRequest, LineageResponse
from pyatlan.model.query import ParsedQuery, QueryParserRequest
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.role import RoleResponse
from pyatlan.model.search import (
    DSL,
    IndexSearchRequest,
    Query,
    Term,
    with_active_category,
    with_active_glossary,
    with_active_term,
)
from pyatlan.model.typedef import TypeDef, TypeDefResponse
from pyatlan.model.user import AtlanUser, UserMinimalResponse, UserResponse
from pyatlan.multipart_data_generator import MultipartDataGenerator
from pyatlan.utils import (
    API,
    HTTPStatus,
    get_logger,
    unflatten_custom_metadata_for_entity,
)

SERVICE_ACCOUNT_ = "service-account-"

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
HTTPS_PREFIX = "https://"

DEFAULT_RETRY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[403, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
)
CONNECTION_RETRY = Retry(
    total=10,
    backoff_factor=1,
    status_forcelist=[403],
    allowed_methods=["GET"],
)


def get_session():
    retry_strategy = DEFAULT_RETRY
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.session()
    session.mount(HTTPS_PREFIX, adapter)
    session.headers.update({"x-atlan-agent": "sdk", "x-atlan-agent-id": "python"})
    return session


class AtlanClient(BaseSettings):
    _default_client: "ClassVar[Optional[AtlanClient]]" = None
    base_url: HttpUrl
    api_key: str
    _session: requests.Session = PrivateAttr(default_factory=get_session)
    _request_params: dict = PrivateAttr()
    _workflow_client: Optional[WorkflowClient] = PrivateAttr(default=None)
    _audit_client: Optional[AuditClient] = PrivateAttr(default=None)
    _group_client: Optional[GroupClient] = PrivateAttr(default=None)
    _role_client: Optional[RoleClient] = PrivateAttr(default=None)
    _typedef_client: Optional[TypeDefClient] = PrivateAttr(default=None)
    _token_client: Optional[TokenClient] = PrivateAttr(default=None)
    _user_client: Optional[UserClient] = PrivateAttr(default=None)

    class Config:
        env_prefix = "atlan_"

    class SearchResults(ABC, Iterable):
        """
        Abstract class that encapsulates results returned by various searches.
        """

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
            """
            Retrieve the current page of results.

            :returns: list of assets on the current page of results
            """
            return self._assets

        def next_page(self, start=None, size=None) -> bool:
            """
            Indicates whether there is a next page of results.

            :returns: True if there is a next page of results, otherwise False
            """
            self._start = start or self._start + self._size
            if size:
                self._size = size
            return self._get_next_page() if self._assets else False

        @abc.abstractmethod
        def _get_next_page(self):
            """
            Abstract method that must be implemented in subclasses, used to
            fetch the next page of results.
            """

        # TODO Rename this here and in `next_page`
        def _get_next_page_json(self):
            """
            Fetches the next page of results and returns the raw JSON of the retrieval.

            :returns: JSON for the next page of results, as-is
            """
            raw_json = self._client._call_api(
                self._endpoint,
                request_obj=self._criteria,
            )
            if "entities" not in raw_json:
                self._assets = []
                return None
            try:
                for entity in raw_json["entities"]:
                    unflatten_custom_metadata_for_entity(
                        entity=entity, attributes=self._criteria.attributes
                    )
                self._assets = parse_obj_as(list[Asset], raw_json["entities"])
                return raw_json
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err

        def __iter__(self) -> Generator[Asset, None, None]:
            """
            Iterates through the results, lazily-fetching each next page until there
            are no more results.

            :returns: an iterable form of each result, across all pages
            """
            while True:
                yield from self.current_page()
                if not self.next_page():
                    break

    class IndexSearchResults(SearchResults, Iterable):
        """
        Captures the response from a search against Atlan. Also provides the ability to
        iteratively page through results, without needing to track or re-run the original
        query.
        """

        def __init__(
            self,
            client: "AtlanClient",
            criteria: IndexSearchRequest,
            start: int,
            size: int,
            count: int,
            assets: list[Asset],
            aggregations: Optional[Aggregations],
        ):
            super().__init__(client, INDEX_SEARCH, criteria, start, size, assets)
            self._count = count
            self._aggregations = aggregations

        @property
        def aggregations(self) -> Optional[Aggregations]:
            return self._aggregations

        def _get_next_page(self):
            """
            Fetches the next page of results.

            :returns: True if the next page of results was fetched, False if there was no next page
            """
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

    class LineageListResults(SearchResults, Iterable):
        """
        Captures the response from a lineage retrieval against Atlan. Also provides the ability to
        iteratively page through results, without needing to track or re-run the original query.
        """

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
            """
            Fetches the next page of results.

            :returns: True if the next page of results was fetched, False if there was no next page
            """
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
    def set_default_client(cls, client: "AtlanClient"):
        """
        Sets the default client to be used by caches
        """
        if not isinstance(client, AtlanClient):
            raise ErrorCode.MISSING_ATLAN_CLIENT.exception_with_parameters()
        cls._default_client = client

    @classmethod
    def get_default_client(cls) -> AtlanClient:
        """
        Retrieves the default client.

        :returns: the default client
        """
        if cls._default_client is None:
            raise ErrorCode.NO_ATLAN_CLIENT_AVAILABLE.exception_with_parameters()
        return cls._default_client

    def __init__(self, **data):
        super().__init__(**data)
        self._request_params = {
            "headers": {
                "authorization": f"Bearer {self.api_key}",
                "User-Agent": "Atlan-PythonSDK/0.5.0",
                "x-atlan-agent": "sdk",
                "x-atlan-agent-id": "python",
            }
        }
        AtlanClient._default_client = self

    @property
    def cache_key(self) -> int:
        return f"{self.base_url}/{self.api_key}".__hash__()

    @property
    def audit(self) -> AuditClient:
        if self._audit_client is None:
            self._audit_client = AuditClient(client=self)
        return self._audit_client

    @property
    def workflow(self) -> WorkflowClient:
        if self._workflow_client is None:
            self._workflow_client = WorkflowClient(client=self)
        return self._workflow_client

    @property
    def group(self) -> GroupClient:
        if self._group_client is None:
            self._group_client = GroupClient(client=self)
        return self._group_client

    @property
    def role(self) -> RoleClient:
        if self._role_client is None:
            self._role_client = RoleClient(client=self)
        return self._role_client

    @property
    def token(self) -> TokenClient:
        if self._token_client is None:
            self._token_client = TokenClient(client=self)
        return self._token_client

    @property
    def typedef(self) -> TypeDefClient:
        if self._typedef_client is None:
            self._typedef_client = TypeDefClient(client=self)
        return self._typedef_client

    @property
    def user(self) -> UserClient:
        if self._user_client is None:
            self._user_client = UserClient(client=self)
        return self._user_client

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
            except requests.exceptions.JSONDecodeError as e:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    response.text, response.status_code, str(e)
                ) from e
        elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            LOGGER.error(
                "Atlas Service unavailable. HTTP Status: %s",
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

            return None
        else:
            with contextlib.suppress(ValueError, json.decoder.JSONDecodeError):
                error_info = json.loads(response.text)
                error_code = error_info.get("errorCode", 0) or error_info.get("code", 0)
                error_message = error_info.get("errorMessage", "") or error_info.get(
                    "message", ""
                )
                if error_code and error_message:
                    error = ERROR_CODE_FOR_HTTP_STATUS.get(
                        response.status_code, ErrorCode.ERROR_PASSTHROUGH
                    )
                    raise error.exception_with_parameters(error_code, error_message)
            raise AtlanError(
                SimpleNamespace(
                    http_error_code=response.status_code,
                    error_id=f"ATLAN-PYTHON-{response.status_code}-000",
                    error_message="",
                    user_action=ErrorCode.ERROR_PASSTHROUGH.user_action,
                )
            )

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
        request_id = str(uuid.uuid4())
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        params["headers"]["X-Atlan-Request-Id"] = request_id
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
            LOGGER.debug("Request ID   : %s", request_id)
        return params, path

    def upload_image(self, file, filename: str) -> AtlanImage:
        """
        Uploads an image from the provided local file.

        :param file: local file to upload
        :param filename: name of the file to be uploaded
        :returns: details of the uploaded image
        :raises AtlanError: on any API communication issue
        """
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
        """Deprecated - use role.get() instead."""
        warn(
            "This method is deprecated, please use 'role.get' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.role.get(
            limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
        )

    def get_all_roles(self) -> RoleResponse:
        """Deprecated - use self.role.get_all() instead."""
        warn(
            "This method is deprecated, please use 'self.role.get_all' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.role.get_all()

    def create_group(
        self,
        group: AtlanGroup,
        user_ids: Optional[list[str]] = None,
    ) -> CreateGroupResponse:
        """Deprecated - use group.create() instead."""
        warn(
            "This method is deprecated, please use 'group.create' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.group.create(group=group, user_ids=user_ids)

    def update_group(
        self,
        group: AtlanGroup,
    ) -> None:
        """Deprecated - use group.update() instead."""
        warn(
            "This method is deprecated, please use 'group.update' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.group.update(group=group)

    def purge_group(
        self,
        guid: str,
    ) -> None:
        """Deprecated - use group.purge() instead."""
        warn(
            "This method is deprecated, please use 'group.purge' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.group.purge(guid=guid)

    def get_groups(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> GroupResponse:
        """Deprecated - use group.get() instead."""
        warn(
            "This method is deprecated, please use 'group.get' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.group.get(
            limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
        )

    def get_all_groups(
        self,
        limit: int = 20,
    ) -> list[AtlanGroup]:
        """Deprecated - use group.get_all() instead."""
        warn(
            "This method is deprecated, please use 'group.get_all' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.group.get_all(limit=limit)

    def get_group_by_name(
        self,
        alias: str,
        limit: int = 20,
    ) -> Optional[list[AtlanGroup]]:
        """Deprecated - use group.get_by_name() instead."""
        warn(
            "This method is deprecated, please use 'group.get_by_name' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.group.get_by_name(alias=alias, limit=limit)

    def get_group_members(self, guid: str) -> UserResponse:
        """Deprecated - use group.get_members() instead."""
        warn(
            "This method is deprecated, please use 'group.get_members' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.group.get_members(guid=guid)

    def remove_users_from_group(self, guid: str, user_ids=list[str]) -> None:
        """Deprecated - use group.remove_users() instead."""
        warn(
            "This method is deprecated, please use 'group.remove_users' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.group.remove_users(guid=guid, user_ids=user_ids)

    def create_users(
        self,
        users: list[AtlanUser],
    ) -> None:
        """Deprecated - use user.create() instead."""
        warn(
            "This method is deprecated, please use 'user.create' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.user.create(users=users)

    def update_user(
        self,
        guid: str,
        user: AtlanUser,
    ) -> UserMinimalResponse:
        """Deprecated - use user.update() instead."""
        warn(
            "This method is deprecated, please use 'user.update' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.update(guid=guid, user=user)

    def get_groups_for_user(
        self,
        guid: str,
    ) -> GroupResponse:
        """Deprecated - use user.get_groups() instead."""
        warn(
            "This method is deprecated, please use 'user.get_groups' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.get_groups(guid=guid)

    def add_user_to_groups(
        self,
        guid: str,
        group_ids: list[str],
    ) -> None:
        """Deprecated - use user.add_to_groups() instead."""
        warn(
            "This method is deprecated, please use 'user.add_to_groups' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.user.add_to_groups(guid=guid, group_ids=group_ids)

    def change_user_role(
        self,
        guid: str,
        role_id: str,
    ) -> None:
        """Deprecated - use user.change_role() instead."""
        warn(
            "This method is deprecated, please use 'user.change_role' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.user.change_role(guid=guid, role_id=role_id)

    def get_current_user(
        self,
    ) -> UserMinimalResponse:
        """Deprecated - use user.get_current() instead."""
        warn(
            "This method is deprecated, please use 'user.get_current' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.get_current()

    def get_users(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> UserResponse:
        """Deprecated - use user.get() instead."""
        warn(
            "This method is deprecated, please use 'user.get' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.get(
            limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
        )

    def get_all_users(
        self,
        limit: int = 20,
    ) -> list[AtlanUser]:
        """Deprecated - use user.get_all() instead."""
        warn(
            "This method is deprecated, please use 'user.get_all' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.get_all(limit=limit)

    def get_users_by_email(
        self,
        email: str,
        limit: int = 20,
    ) -> Optional[list[AtlanUser]]:
        """Deprecated - use user.get_by_email() instead."""
        warn(
            "This method is deprecated, please use 'user.get_by_email' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.get_by_email(email=email, limit=limit)

    def get_user_by_username(self, username: str) -> Optional[AtlanUser]:
        """Deprecated - use user.get_by_username() instead."""
        warn(
            "This method is deprecated, please use 'user.get_by_username' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.get_by_username(username=username)

    def parse_query(self, query: QueryParserRequest) -> Optional[ParsedQuery]:
        """
        Parses the provided query to describe its component parts.

        :param query: query to parse and configuration options
        :returns: parsed explanation of the query
        :raises AtlanError: on any API communication issue
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
        """
        Retrieves an asset by its qualified_name.

        :param qualified_name: qualified_name of the asset to be retrieved
        :param asset_type: type of asset to be retrieved ( must be the actual asset type not a super type)
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist
        :raises AtlanError: on any API communication issue
        """
        query_params = {
            "attr:qualifiedName": qualified_name,
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }
        raw_json = self._call_api(
            GET_ENTITY_BY_UNIQUE_ATTRIBUTE.format_path_with_params(asset_type.__name__),
            query_params,
        )
        if raw_json["entity"]["typeName"] != asset_type.__name__:
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, qualified_name
            )
        asset = self._handle_relationships(raw_json)
        if not isinstance(asset, asset_type):
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, qualified_name
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
        """
        Retrieves an asset by its GUID.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist, or is not of the type requested
        :raises AtlanError: on any API communication issue
        """
        query_params = {
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }

        raw_json = self._call_api(
            GET_ENTITY_BY_GUID.format_path_with_params(guid),
            query_params,
        )
        asset = self._handle_relationships(raw_json)
        if not isinstance(asset, asset_type):
            raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                guid, asset_type.__name__
            )
        return asset

    def _handle_relationships(self, raw_json):
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
        """
        Retrieves an asset by its GUID, without any of its relationships.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved
        :returns: the asset, without any of its relationships
        :raises NotFoundError: if the asset does not exist
        """
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
        """Deprecated - use save() instead."""
        warn(
            "This method is deprecated, please use 'save' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
        )

    def save(
        self,
        entity: Union[Asset, list[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        """
        If an asset with the same qualified_name exists, updates the existing asset. Otherwise, creates the asset.
        If an asset does exist, opertionally overwrites any Atlan tags. Custom metadata will either be
        overwritten or merged depending on the options provided.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        :raises ApiError: if a connection was created and blocking until policies are synced overruns the retry limit
        """
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
        response = AssetMutationResponse(**raw_json)
        if connections_created := response.assets_created(Connection):
            self._wait_for_connections_to_be_created(connections_created)
        return response

    def _wait_for_connections_to_be_created(self, connections_created):
        adapter = self._session.adapters[HTTPS_PREFIX]
        adapter.max_retries = CONNECTION_RETRY
        try:
            for connection in connections_created:
                guid = connection.guid
                self.retrieve_minimal(guid=guid, asset_type=Connection)
        except requests.exceptions.RetryError as err:
            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err
        finally:
            adapter.max_retries = DEFAULT_RETRY

    def upsert_merging_cm(
        self, entity: Union[Asset, list[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_merging_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def save_merging_cm(
        self, entity: Union[Asset, list[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, has the same behavior as the upsert() method, while also setting
        any custom metadata provided. If an asset does exist, optionally overwrites any Atlan tags.
        Will merge any provided custom metadata with any custom metadata that already exists on the asset.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the created or updated assets
        """
        return self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=True,
            overwrite_custom_metadata=False,
        )

    def update_merging_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, fails with a NotFoundError. Will merge any provided
        custom metadata with any custom metadata that already exists on the asset.
        If an asset does exist, optionally overwrites any Atlan tags.

        :param entity: the asset to update
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the updated asset
        :raises NotFoundError: if the asset does not exist (will not create it)
        """
        self.get_asset_by_qualified_name(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            min_ext_info=True,
            ignore_relationships=True,
        )  # Allow this to throw the NotFoundError if the entity does not exist
        return self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def upsert_replacing_cm(
        self, entity: Union[Asset, list[Asset]], replace_atlan_tagss: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_replacing_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tagss
        )

    def save_replacing_cm(
        self, entity: Union[Asset, list[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, has the same behavior as the upsert() method, while also setting
        any custom metadata provided.
        If an asset does exist, optionally overwrites any Atlan tags.
        Will overwrite all custom metadata on any existing asset with only the custom metadata provided
        (wiping out any other custom metadata on an existing asset that is not provided in the request).

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the created or updated assets
        :raises AtlanError: on any API communication issue
        """

        query_params = {
            "replaceClassifications": replace_atlan_tags,
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

    def update_replacing_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, fails with a NotFoundError.
        Will overwrite all custom metadata on any existing asset with only the custom metadata provided
        (wiping out any other custom metadata on an existing asset that is not provided in the request).
        If an asset does exist, optionally overwrites any Atlan tags.

        :param entity: the asset to update
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the updated asset
        :raises NotFoundError: if the asset does not exist (will not create it)
        """

        self.get_asset_by_qualified_name(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            min_ext_info=True,
            ignore_relationships=True,
        )  # Allow this to throw the NotFoundError if the entity does not exist
        return self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def purge_entity_by_guid(
        self, guid: Union[str, list[str]]
    ) -> AssetMutationResponse:
        """
        Hard-deletes (purges) one or more assets by their unique identifier (GUID).
        This operation is irreversible.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to hard-delete
        :returns: details of the hard-deleted asset(s)
        :raises AtlanError: on any API communication issue
        """
        guids: list[str] = []
        if isinstance(guid, list):
            guids.extend(guid)
        else:
            guids.append(guid)
        query_params = {"deleteType": AtlanDeleteType.PURGE.value, "guid": guids}
        raw_json = self._call_api(DELETE_ENTITIES_BY_GUIDS, query_params=query_params)
        return AssetMutationResponse(**raw_json)

    def delete_entity_by_guid(
        self, guid: Union[str, list[str]]
    ) -> AssetMutationResponse:
        """
        Soft-deletes (archives) one or more assets by their unique identifier (GUID).
        This operation can be reversed by updating the asset and its status to ACTIVE.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to soft-delete
        :returns: details of the soft-deleted asset(s)
        :raises AtlanError: on any API communication issue
        :raises ApiError: if the retry limit is overrun waiting for confirmation the asset is deleted
        """
        guids: list[str] = []
        if isinstance(guid, list):
            guids.extend(guid)
        else:
            guids.append(guid)
        query_params = {"deleteType": AtlanDeleteType.SOFT.value, "guid": guids}
        raw_json = self._call_api(DELETE_ENTITIES_BY_GUIDS, query_params=query_params)
        response = AssetMutationResponse(**raw_json)
        for asset in response.assets_deleted(asset_type=Asset):
            self._wait_till_deleted(asset)
        return response

    @retry(
        reraise=True,
        retry=(retry_if_exception_type(AtlanError)),
        stop=stop_after_attempt(20),
        wait=wait_fixed(1),
    )
    def _wait_till_deleted(self, asset: Asset):
        try:
            asset = self.retrieve_minimal(guid=asset.guid, asset_type=Asset)
            if asset.status == EntityStatus.DELETED:
                return
        except requests.exceptions.RetryError as err:
            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err

    def restore(self, asset_type: Type[A], qualified_name: str) -> bool:
        """
        Restore an archived (soft-deleted) asset to active.

        :param asset_type: type of the asset to restore
        :param qualified_name: of the asset to restore
        :returns: True if the asset is now restored, or False if not
        :raises AtlanError: on any API communication issue
        """
        return self._restore(asset_type, qualified_name, 0)

    def _restore(self, asset_type: Type[A], qualified_name: str, retries: int) -> bool:
        existing = self.get_asset_by_qualified_name(
            asset_type=asset_type, qualified_name=qualified_name
        )
        if not existing:
            # Nothing to restore, so cannot be restored
            return False
        elif existing.status is EntityStatus.ACTIVE:
            # Already active, but could be due to the async nature of delete handlers
            if retries < 10:
                time.sleep(2)
                return self._restore(asset_type, qualified_name, retries + 1)
            else:
                # If we have exhausted the retries, though, we will short-circuit
                return True
        else:
            response = self._restore_asset(existing)
            return response is not None and response.guid_assignments is not None

    def _restore_asset(self, asset: Asset) -> AssetMutationResponse:
        to_restore = asset.trim_to_required()
        to_restore.status = EntityStatus.ACTIVE
        query_params = {
            "replaceClassifications": False,
            "replaceBusinessAttributes": False,
            "overwriteBusinessAttributes": False,
        }
        request = BulkRequest[Asset](entities=[to_restore])
        raw_json = self._call_api(BULK_UPDATE, query_params, request)
        return AssetMutationResponse(**raw_json)

    def search(self, criteria: IndexSearchRequest) -> IndexSearchResults:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
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
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            assets = []
        aggregations = self.get_aggregations(raw_json)
        count = raw_json["approximateCount"] if "approximateCount" in raw_json else 0
        return AtlanClient.IndexSearchResults(
            client=self,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            assets=assets,
            aggregations=aggregations,
        )

    def get_aggregations(self, raw_json) -> Optional[Aggregations]:
        if "aggregations" in raw_json:
            try:
                aggregations = Aggregations.parse_obj(raw_json["aggregations"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            aggregations = None
        return aggregations

    def get_all_typedefs(self) -> TypeDefResponse:
        """Deprecated - use typedef.get_all() instead."""
        warn(
            "This method is deprecated, please use 'typedef.get_all' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.typedef.get_all()

    def get_typedefs(
        self, type_category: Union[AtlanTypeCategory, list[AtlanTypeCategory]]
    ) -> TypeDefResponse:
        """Deprecated - use typedef.get() instead."""
        warn(
            "This method is deprecated, please use 'typedef.get' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.typedef.get(type_category=type_category)

    def create_typedef(self, typedef: TypeDef) -> TypeDefResponse:
        """Deprecated - use typedef.create() instead."""
        warn(
            "This method is deprecated, please use 'typedef.create' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.typedef.create(typedef=typedef)

    def update_typedef(self, typedef: TypeDef) -> TypeDefResponse:
        """Deprecated - use typedef.update() instead."""
        warn(
            "This method is deprecated, please use 'typedef.update' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.typedef.update(typedef=typedef)

    def purge_typedef(self, name: str, typedef_type: type) -> None:
        """Deprecated - use typedef.purge() instead."""
        warn(
            "This method is deprecated, please use 'typedef.purge' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.typedef.purge(name=name, typedef_type=typedef_type)

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
        """
        Add one or more Atlan tags to the provided asset.
        Note: if one or more of the provided Atlan tags already exist on the asset, an error
        will be raised. (In other words, this operation is NOT idempotent.)

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset to which to add the Atlan tags
        :param atlan_tag_names: human-readable names of the Atlan tags to add to the asset
        :param propagate: whether to propagate the Atlan tag (True) or not (False)
        :param remove_propagation_on_delete: whether to remove the propagated Atlan tags when the Atlan tag is removed
                                             from this asset (True) or not (False)
        :param restrict_lineage_propagation: whether to avoid propagating through lineage (True) or do propagate
                                             through lineage (False)
        :raises AtlanError: on any API communication issue
        """
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
        """
        Removes a single Atlan tag from the provided asset.
        Note: if the provided Atlan tag does not exist on the asset, an error will be raised.
        (In other words, this operation is NOT idempotent.)

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset to which to add the Atlan tags
        :param atlan_tag_name: human-readable name of the Atlan tag to remove from the asset
        :raises AtlanError: on any API communication issue
        """
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        classification_id = AtlanTagCache.get_id_for_name(atlan_tag_name)
        if not classification_id:
            raise ErrorCode.ATLAN_TAG_NOT_FOUND_BY_NAME.exception_with_parameters(
                atlan_tag_name
            )
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
        message: Optional[str] = None,
    ) -> Optional[A]:
        """
        Update the certificate on an asset.

        :param asset_type: type of asset on which to update the certificate
        :param qualified_name: the qualified_name of the asset on which to update the certificate
        :param name: the name of the asset on which to update the certificate
        :param certificate_status: specific certificate to set on the asset
        :param message: (optional) message to set (or None for no message)
        :returns: the result of the update, or None if the update failed
        :raises AtlanError: on any API communication issue
        """
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
        """
        Remove the certificate from an asset.

        :param asset_type: type of asset from which to remove the certificate
        :param qualified_name: the qualified_name of the asset from which to remove the certificate
        :param name: the name of the asset from which to remove the certificate
        :returns: the result of the removal, or None if the removal failed
        """
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
        """
        Update the announcement on an asset.

        :param asset_type: type of asset on which to update the announcement
        :param qualified_name: the qualified_name of the asset on which to update the announcement
        :param name: the name of the asset on which to update the announcement
        :param announcement: to apply to the asset
        :returns: the result of the update, or None if the update failed
        """
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.set_announcement(announcement)
        asset.name = name
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments()
    def remove_announcement(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        """
        Remove the announcement from an asset.

        :param asset_type: type of asset from which to remove the announcement
        :param qualified_name: the qualified_name of the asset from which to remove the announcement
        :param name: the name of the asset from which to remove the announcement
        :returns: the result of the removal, or None if the removal failed
        """
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_announcement()
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        """
        Update only the provided custom metadata attributes on the asset. This will leave all
        other custom metadata attributes, even within the same named custom metadata, unchanged.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to update, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        custom_metadata_request = CustomMetadataRequest.create(
            custom_metadata_dict=custom_metadata
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
        """
        Replace specific custom metadata on the asset. This will replace everything within the named
        custom metadata, but will not change any of hte other named custom metadata on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to replace, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        # clear unset attributes so that they are removed
        custom_metadata.clear_unset()
        custom_metadata_request = CustomMetadataRequest.create(
            custom_metadata_dict=custom_metadata
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
        """
        Remove specific custom metadata from an asset.

        :param guid: unique identifier (GUID) of the asset
        :param cm_name: human-readable name of the custom metadata to remove
        :raises AtlanError: on any API communication issue
        """
        custom_metadata = CustomMetadataDict(name=cm_name)
        # invoke clear_all so all attributes are set to None and consequently removed
        custom_metadata.clear_all()
        custom_metadata_request = CustomMetadataRequest.create(
            custom_metadata_dict=custom_metadata
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

    @validate_arguments()
    def append_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Link additional terms to an asset, without replacing existing terms linked to the asset.
        Note: this operation must make two API calls — one to retrieve the asset's existing terms,
        and a second to append the new terms. (At least one of the GUID or qualified_name must be
        supplied, but both are not necessary.)

        :param asset_type: type of the asset
        :param terms: the list of terms to append to the asset
        :param guid: unique identifier (GUID) of the asset to which to link the terms
        :param qualified_name: the qualified_name of the asset to which to link the terms
        :returns: the asset that was updated (note that it will NOT contain details of the appended terms)
        """
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()
        if not terms:
            return asset
        replacement_terms: list[AtlasGlossaryTerm] = []
        if existing_terms := asset.assigned_terms:
            replacement_terms.extend(
                term for term in existing_terms if term.relationship_status != "DELETED"
            )
        replacement_terms.extend(terms)
        asset.assigned_terms = replacement_terms
        response = self.save(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments()
    def replace_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Replace the terms linked to an asset.
        (At least one of the GUID or qualified_name must be supplied, but both are not necessary.)

        :param asset_type: type of the asset
        :param terms: the list of terms to replace on the asset, or an empty list to remove all terms from an asset
        :param guid: unique identifier (GUID) of the asset to which to replace the terms
        :param qualified_name: the qualified_name of the asset to which to replace the terms
        :returns: the asset that was updated (note that it will NOT contain details of the replaced terms)
        """
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()
        asset.assigned_terms = terms
        response = self.save(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments()
    def remove_terms(
        self,
        asset_type: Type[A],
        terms: list[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Remove terms from an asset, without replacing all existing terms linked to the asset.
        Note: this operation must make two API calls — one to retrieve the asset's existing terms,
        and a second to remove the provided terms.

        :param asset_type: type of the asset
        :param terms: the list of terms to remove from the asset (note: these must be references by GUID to efficiently
                      remove any existing terms)
        :param guid: unique identifier (GUID) of the asset from which to remove the terms
        :param qualified_name: the qualified_name of the asset from which to remove the terms
        :returns: the asset that was updated (note that it will NOT contain details of the resulting terms)
        """
        if not terms:
            raise ErrorCode.MISSING_TERMS.exception_with_parameters()
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
            asset = self.get_asset_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_asset_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()
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
        response = self.save(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments()
    def find_connections_by_name(
        self,
        name: str,
        connector_type: AtlanConnectorType,
        attributes: Optional[list[str]] = None,
    ) -> list[Connection]:
        """
        Find a connection by its human-readable name and type.

        :param name: of the connection
        :param connector_type: of the connection
        :param attributes: (optional) collection of attributes to retrieve for the connection
        :returns: all connections with that name and type, if found
        :raises NotFoundError: if the connection does not exist
        """
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
        """
        Deprecated — this is an older, slower operation to retrieve lineage that will not receive further enhancements.
        Use the get_lineage_list operation instead.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises AtlanError: on any API communication issue
        """
        warn(
            "Lineage retrieval using this method is deprecated, please use 'get_lineage_list' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        raw_json = self._call_api(
            GET_LINEAGE, None, lineage_request, exclude_unset=False
        )
        return LineageResponse(**raw_json)

    def get_lineage_list(
        self, lineage_request: LineageListRequest
    ) -> LineageListResults:
        """
        Retrieve lineage using the higher-performance "list" API.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises InvalidRequestError: if the requested lineage direction is 'BOTH' (unsupported for this operation)
        :raises AtlanError: on any API communication issue
        """
        if lineage_request.direction == LineageDirection.BOTH:
            raise ErrorCode.INVALID_LINEAGE_DIRECTION.exception_with_parameters()
        raw_json = self._call_api(
            GET_LINEAGE_LIST, None, request_obj=lineage_request, exclude_unset=True
        )
        if "entities" in raw_json:
            try:
                assets = parse_obj_as(list[Asset], raw_json["entities"])
                has_more = parse_obj_as(bool, raw_json["hasMore"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
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

    def add_api_token_as_admin(
        self, asset_guid: str, impersonation_token: str
    ) -> Optional[AssetMutationResponse]:
        """Deprecated - use user.add_as_admin() instead."""
        warn(
            "This method is deprecated, please use 'user.add_as_admin' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.add_as_admin(
            asset_guid=asset_guid, impersonation_token=impersonation_token
        )

    def add_api_token_as_viewer(
        self, asset_guid: str, impersonation_token: str
    ) -> Optional[AssetMutationResponse]:
        """Deprecated - use user.add_as_viewer() instead."""
        warn(
            "This method is deprecated, please use 'user.add_as_viewer' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.user.add_as_viewer(
            asset_guid=asset_guid, impersonation_token=impersonation_token
        )

    def get_api_tokens(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> ApiTokenResponse:
        """Deprecated - use token.get() instead."""
        warn(
            "This method is deprecated, please use 'token.get' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.token.get(
            limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
        )

    def get_api_token_by_name(self, display_name: str) -> Optional[ApiToken]:
        """Deprecated - use token.get_by_name() instead."""
        warn(
            "This method is deprecated, please use 'token.get_by_name' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.token.get_by_name(display_name=display_name)

    def get_api_token_by_id(self, client_id: str) -> Optional[ApiToken]:
        """Deprecated - use token.get_by_id() instead."""
        warn(
            "This method is deprecated, please use 'token.get_by_id' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.token.get_by_id(client_id=client_id)

    def create_api_token(
        self,
        display_name: str,
        description: str = "",
        personas: Optional[set[str]] = None,
        validity_seconds: int = -1,
    ) -> ApiToken:
        """Deprecated - use token.create() instead."""
        warn(
            "This method is deprecated, please use 'token.create' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.token.create(
            display_name=display_name,
            description=description,
            personas=personas,
            validity_seconds=validity_seconds,
        )

    def update_api_token(
        self,
        guid: str,
        display_name: str,
        description: str = "",
        personas: Optional[set[str]] = None,
    ) -> ApiToken:
        """Deprecated - use token.update() instead."""
        warn(
            "This method is deprecated, please use 'token.update' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.token.update(
            guid=guid,
            display_name=display_name,
            description=description,
            personas=personas,
        )

    def purge_api_token(self, guid: str) -> None:
        """Deprecated - use token.purge() instead."""
        warn(
            "This method is deprecated, please use 'token.purge' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.token.purge(guid=guid)

    def get_keycloak_events(
        self, keycloak_request: KeycloakEventRequest
    ) -> KeycloakEventResponse:
        """
        Retrieve all events, based on the supplied filters.

        :param keycloak_request: details of the filters to apply when retrieving events
        :returns: the events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        if raw_json := self._call_api(
            KEYCLOAK_EVENTS,
            query_params=keycloak_request.query_params,
            exclude_unset=True,
        ):
            try:
                events = parse_obj_as(list[KeycloakEvent], raw_json)
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            events = []
        return KeycloakEventResponse(
            client=self,
            criteria=keycloak_request,
            start=keycloak_request.offset or 0,
            size=keycloak_request.size or 100,
            events=events,
        )

    def get_admin_events(self, admin_request: AdminEventRequest) -> AdminEventResponse:
        """
        Retrieve admin events based on the supplied filters.

        :param admin_request: details of the filters to apply when retrieving admin events
        :returns: the admin events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        if raw_json := self._call_api(
            ADMIN_EVENTS, query_params=admin_request.query_params, exclude_unset=True
        ):
            try:
                events = parse_obj_as(list[AdminEvent], raw_json)
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            events = []
        return AdminEventResponse(
            client=self,
            criteria=admin_request,
            start=admin_request.offset or 0,
            size=admin_request.size or 100,
            events=events,
        )

    @validate_arguments()
    def find_personas_by_name(
        self,
        name: str,
        attributes: Optional[list[str]] = None,
    ) -> list[Persona]:
        """
        Find a persona by its human-readable name.

        :param name: of the persona
        :param attributes: (optional) collection of attributes to retrieve for the persona
        :returns: all personas with that name, if found
        :raises NotFoundError: if no persona with the provided name exists
        """
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
        """
        Find a purpose by its human-readable name.

        :param name: of the purpose
        :param attributes: (optional) collection of attributes to retrieve for the purpose
        :returns: all purposes with that name, if found
        :raises NotFoundError: if no purpose with the provided name exists
        """
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

    @validate_arguments()
    def find_glossary_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> AtlasGlossary:
        """
        Find a glossary by its human-readable name.

        :param name: of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the glossary
        :returns: the glossary, if found
        :raises NotFoundError: if no glossary with the provided name exists
        """
        if attributes is None:
            attributes = []
        query = with_active_glossary(name=name)
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )[0]

    @validate_arguments()
    def find_category_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> list[AtlasGlossaryCategory]:
        """
        Find a category by its human-readable name.
        Note: this operation requires first knowing the qualified_name of the glossary in which the
        category exists. Note that categories are not unique by name, so there may be
        multiple results.

        :param name: of the category
        :param glossary_qualified_name: qualified_name of the glossary in which the category exists
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists in the glossary
        """
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
            allow_multiple=True,
        )

    @validate_arguments()
    def find_category_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> list[AtlasGlossaryCategory]:
        """
        Find a category by its human-readable name.
        Note: this operation must run two separate queries to first resolve the qualified_name of the
        glossary, so will be somewhat slower. If you already have the qualified_name of the glossary, use
        find_category_by_name_fast instead. Note that categories are not unique by name, so there may be
        multiple results.

        :param name: of the category
        :param glossary_name: human-readable name of the glossary in which the category exists
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists in the glossary
        """
        glossary = self.find_glossary_by_name(name=glossary_name)
        return self.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    def _search_for_asset_with_name(
        self,
        query: Query,
        name: str,
        asset_type: Type[A],
        attributes: Optional[list[StrictStr]],
        allow_multiple: bool = False,
    ) -> list[A]:
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
            if not allow_multiple and len(assets) > 1:
                LOGGER.warning(
                    "More than 1 %s found with the name '%s', returning only the first.",
                    asset_type.__name__,
                    name,
                )
            return assets
        raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
            asset_type.__name__, name
        )

    @validate_arguments()
    def find_term_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Find a term by its human-readable name.
        Note: this operation requires first knowing the qualified_name of the glossary in which the
        term exists.

        :param name: of the term
        :param glossary_qualified_name: qualified_name of the glossary in which the term exists
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists in the glossary
        """
        if attributes is None:
            attributes = []
        query = with_active_term(
            name=name, glossary_qualified_name=glossary_qualified_name
        )
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossaryTerm, attributes=attributes
        )[0]

    @validate_arguments()
    def find_term_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[list[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Find a term by its human-readable name.
        Note: this operation must run two separate queries to first resolve the qualified_name of the
        glossary, so will be somewhat slower. If you already have the qualified_name of the glossary, use
        find_term_by_name_fast instead.

        :param name: of the term
        :param glossary_name: human-readable name of the glossary in which the term exists
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists in the glossary
        """
        glossary = self.find_glossary_by_name(name=glossary_name)
        return self.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )


@contextlib.contextmanager
def client_connection(
    base_url: Optional[HttpUrl] = None, api_key: Optional[str] = None
) -> Generator[AtlanClient, None, None]:
    """
    Creates a new client created with the given base_url and/api_key. The AtlanClient.default_client will
    be set to the new client. AtlanClient.default_client will be reset to the current default_client before
    exiting the context.
    :param base_url: the base_url to be used for the new connection. If not specified the current value will be used
    :param api_key: the api_key to be used for the new connection. If not specified the current value will be used
    """
    current_client = AtlanClient.get_default_client()
    tmp_client = AtlanClient(
        base_url=base_url or current_client.base_url,
        api_key=api_key or current_client.api_key,
    )
    try:
        yield tmp_client
    finally:
        AtlanClient.set_default_client(current_client)


from pyatlan.model.keycloak_events import (  # noqa: E402
    AdminEvent,
    AdminEventRequest,
    AdminEventResponse,
    KeycloakEvent,
    KeycloakEventRequest,
    KeycloakEventResponse,
)
