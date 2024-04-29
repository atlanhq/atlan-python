# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from __future__ import annotations

import contextlib
import copy
import json
import logging
import shutil
import uuid
from contextvars import ContextVar
from importlib.resources import read_text
from types import SimpleNamespace
from typing import (
    Any,
    ClassVar,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Set,
    Type,
    Union,
)
from urllib.parse import urljoin
from warnings import warn

import requests
from pydantic.v1 import (
    BaseSettings,
    HttpUrl,
    PrivateAttr,
    StrictStr,
    constr,
    validate_arguments,
)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pyatlan.client.admin import AdminClient
from pyatlan.client.asset import A, AssetClient, IndexSearchResults, LineageListResults
from pyatlan.client.audit import AuditClient
from pyatlan.client.common import CONNECTION_RETRY, HTTP_PREFIX, HTTPS_PREFIX
from pyatlan.client.constants import EVENT_STREAM, PARSE_QUERY, UPLOAD_IMAGE
from pyatlan.client.credential import CredentialClient
from pyatlan.client.file import FileClient
from pyatlan.client.group import GroupClient
from pyatlan.client.impersonate import ImpersonationClient
from pyatlan.client.query import QueryClient
from pyatlan.client.role import RoleClient
from pyatlan.client.search_log import SearchLogClient
from pyatlan.client.sso import SSOClient
from pyatlan.client.task import TaskClient
from pyatlan.client.token import TokenClient
from pyatlan.client.typedef import TypeDefClient
from pyatlan.client.user import UserClient
from pyatlan.client.workflow import WorkflowClient
from pyatlan.errors import ERROR_CODE_FOR_HTTP_STATUS, AtlanError, ErrorCode
from pyatlan.model.api_tokens import ApiToken, ApiTokenResponse
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Persona,
    Purpose,
)
from pyatlan.model.atlan_image import AtlanImage
from pyatlan.model.core import Announcement, AtlanObject
from pyatlan.model.custom_metadata import CustomMetadataDict
from pyatlan.model.enums import AtlanConnectorType, AtlanTypeCategory, CertificateStatus
from pyatlan.model.group import AtlanGroup, CreateGroupResponse, GroupResponse
from pyatlan.model.lineage import LineageListRequest, LineageRequest, LineageResponse
from pyatlan.model.query import ParsedQuery, QueryParserRequest
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.role import RoleResponse
from pyatlan.model.search import IndexSearchRequest
from pyatlan.model.typedef import TypeDef, TypeDefResponse
from pyatlan.model.user import AtlanUser, UserMinimalResponse, UserResponse
from pyatlan.multipart_data_generator import MultipartDataGenerator
from pyatlan.utils import (
    API,
    APPLICATION_ENCODED_FORM,
    AuthorizationFilter,
    HTTPStatus,
    RequestIdAdapter,
)

request_id_var = ContextVar("request_id", default=None)


def get_adapter() -> logging.LoggerAdapter:
    """
    This function creates a LoggerAdapter that will provide the requestid from the ContextVar request_id_var
    :returns: the LogAdapter
    """
    logger = logging.getLogger(__name__)
    logger.addFilter(AuthorizationFilter())
    return RequestIdAdapter(logger=logger, contextvar=request_id_var)


LOGGER = get_adapter()

DEFAULT_RETRY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[403, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    raise_on_status=False,
)

VERSION = read_text("pyatlan", "version.txt").strip()


def log_response(response, *args, **kwargs):
    LOGGER.debug("HTTP Status: %s", response.status_code)
    LOGGER.debug("URL: %s", response.request.url)


def get_session():
    retry_strategy = DEFAULT_RETRY
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.session()
    session.mount(HTTPS_PREFIX, adapter)
    session.mount(HTTP_PREFIX, adapter)
    session.headers.update(
        {
            "x-atlan-agent": "sdk",
            "x-atlan-agent-id": "python",
            "User-Agent": f"Atlan-PythonSDK/{VERSION}",
        }
    )
    session.hooks["response"].append(log_response)
    return session


class AtlanClient(BaseSettings):
    _default_client: "ClassVar[Optional[AtlanClient]]" = None
    base_url: Union[Literal["INTERNAL"], HttpUrl]
    api_key: str
    _session: requests.Session = PrivateAttr(default_factory=get_session)
    _request_params: dict = PrivateAttr()
    _workflow_client: Optional[WorkflowClient] = PrivateAttr(default=None)
    _credential_client: Optional[CredentialClient] = PrivateAttr(default=None)
    _admin_client: Optional[AdminClient] = PrivateAttr(default=None)
    _audit_client: Optional[AuditClient] = PrivateAttr(default=None)
    _search_log_client: Optional[SearchLogClient] = PrivateAttr(default=None)
    _group_client: Optional[GroupClient] = PrivateAttr(default=None)
    _role_client: Optional[RoleClient] = PrivateAttr(default=None)
    _asset_client: Optional[AssetClient] = PrivateAttr(default=None)
    _typedef_client: Optional[TypeDefClient] = PrivateAttr(default=None)
    _token_client: Optional[TokenClient] = PrivateAttr(default=None)
    _user_client: Optional[UserClient] = PrivateAttr(default=None)
    _impersonate_client: Optional[ImpersonationClient] = PrivateAttr(default=None)
    _query_client: Optional[QueryClient] = PrivateAttr(default=None)
    _task_client: Optional[TaskClient] = PrivateAttr(default=None)
    _sso_client: Optional[SSOClient] = PrivateAttr(default=None)
    _file_client: Optional[FileClient] = PrivateAttr(default=None)

    class Config:
        env_prefix = "atlan_"

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
            }
        }
        AtlanClient._default_client = self

    @property
    def cache_key(self) -> int:
        return f"{self.base_url}/{self.api_key}".__hash__()

    @property
    def admin(self) -> AdminClient:
        if self._admin_client is None:
            self._admin_client = AdminClient(client=self)
        return self._admin_client

    @property
    def audit(self) -> AuditClient:
        if self._audit_client is None:
            self._audit_client = AuditClient(client=self)
        return self._audit_client

    @property
    def search_log(self) -> SearchLogClient:
        if self._search_log_client is None:
            self._search_log_client = SearchLogClient(client=self)
        return self._search_log_client

    @property
    def workflow(self) -> WorkflowClient:
        if self._workflow_client is None:
            self._workflow_client = WorkflowClient(client=self)
        return self._workflow_client

    @property
    def credentials(self) -> CredentialClient:
        if self._credential_client is None:
            self._credential_client = CredentialClient(client=self)
        return self._credential_client

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
    def asset(self) -> AssetClient:
        if self._asset_client is None:
            self._asset_client = AssetClient(client=self)
        return self._asset_client

    @property
    def impersonate(self) -> ImpersonationClient:
        if self._impersonate_client is None:
            self._impersonate_client = ImpersonationClient(client=self)
        return self._impersonate_client

    @property
    def queries(self) -> QueryClient:
        if self._query_client is None:
            self._query_client = QueryClient(client=self)
        return self._query_client

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

    @property
    def tasks(self) -> TaskClient:
        if self._task_client is None:
            self._task_client = TaskClient(client=self)
        return self._task_client

    @property
    def sso(self) -> SSOClient:
        if self._sso_client is None:
            self._sso_client = SSOClient(client=self)
        return self._sso_client

    @property
    def files(self) -> FileClient:
        if self._file_client is None:
            self._file_client = FileClient(client=self)
        return self._file_client

    def update_headers(self, header: Dict[str, str]):
        self._session.headers.update(header)

    def _handle_file_download(self, raw_response: Any, file_path: str) -> str:
        try:
            download_file = open(file_path, "wb")
            shutil.copyfileobj(raw_response, download_file)
        except Exception as err:
            raise ErrorCode.UNABLE_TO_DOWNLOAD_FILE.exception_with_parameters(
                str((hasattr(err, "strerror") and err.strerror) or err), file_path
            )
        return file_path

    def _call_api_internal(
        self, api, path, params, binary_data=None, download_file_path=None
    ):
        token = request_id_var.set(str(uuid.uuid4()))
        try:
            params["headers"]["X-Atlan-Request-Id"] = request_id_var.get()
            if binary_data:
                response = self._session.request(
                    api.method.value, path, data=binary_data, **params
                )
            elif api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                response = self._session.request(
                    api.method.value, path, **params, stream=True
                )
                if download_file_path:
                    return self._handle_file_download(response.raw, download_file_path)
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
                    events = []
                    if LOGGER.isEnabledFor(logging.DEBUG):
                        LOGGER.debug(
                            "<== __call_api(%s,%s), result = %s",
                            vars(api),
                            params,
                            response,
                        )
                    if api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                        for line in response.iter_lines(decode_unicode=True):
                            if not line:
                                continue
                            if not line.startswith("data: "):
                                raise ErrorCode.UNABLE_TO_DESERIALIZE.exception_with_parameters(
                                    line
                                )
                            events.append(json.loads(line.split("data: ")[1]))
                    response_json = events if events else response.json()
                    LOGGER.debug(response_json)
                    return response_json
                except (
                    requests.exceptions.JSONDecodeError,
                    json.decoder.JSONDecodeError,
                ) as e:
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
                    error_code = error_info.get("errorCode", 0) or error_info.get(
                        "code", 0
                    )
                    error_message = error_info.get(
                        "errorMessage", ""
                    ) or error_info.get("message", "")
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
        finally:
            request_id_var.reset(token)

    def _api_logger(self, api: API, path: str):
        LOGGER.debug("------------------------------------------------------")
        LOGGER.debug("Call         : %s %s", api.method, path)
        LOGGER.debug("Content-type_ : %s", api.consumes)
        LOGGER.debug("Accept       : %s", api.produces)

    def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset: bool = True
    ):
        path = self._create_path(api)
        params = self._create_params(api, query_params, request_obj, exclude_unset)
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return self._call_api_internal(api, path, params)

    def _create_path(self, api: API):
        if self.base_url == "INTERNAL":
            return urljoin(api.endpoint.service, api.path)
        else:
            return urljoin(urljoin(self.base_url, api.endpoint.prefix), api.path)

    def _upload_file(self, api, file=None, filename=None):
        generator = MultipartDataGenerator()
        generator.add_file(file=file, filename=filename)
        post_data = generator.get_post_data()
        api.produces = f"multipart/form-data; boundary={generator.boundary}"
        path = self._create_path(api)
        params = self._create_params(
            api, query_params=None, request_obj=None, exclude_unset=True
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return self._call_api_internal(api, path, params, binary_data=post_data)

    def _s3_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return self._call_api_internal(api, path, params, binary_data=upload_file)

    def _presigned_url_file_download(self, api: API, file_path: str):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return self._call_api_internal(api, path, params, download_file_path=file_path)

    def _create_params(
        self, api: API, query_params, request_obj, exclude_unset: bool = True
    ):
        params = copy.deepcopy(self._request_params)
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        if query_params is not None:
            params["params"] = query_params
        if request_obj is not None:
            if isinstance(request_obj, AtlanObject):
                params["data"] = request_obj.json(
                    by_alias=True, exclude_unset=exclude_unset
                )
            elif api.consumes == APPLICATION_ENCODED_FORM:
                params["data"] = request_obj
            else:
                params["data"] = json.dumps(request_obj)
        return params

    @validate_arguments
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
        user_ids: Optional[List[str]] = None,
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
    ) -> List[AtlanGroup]:
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
    ) -> Optional[List[AtlanGroup]]:
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

    def remove_users_from_group(self, guid: str, user_ids=List[str]) -> None:
        """Deprecated - use group.remove_users() instead."""
        warn(
            "This method is deprecated, please use 'group.remove_users' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.group.remove_users(guid=guid, user_ids=user_ids)

    def create_users(
        self,
        users: List[AtlanUser],
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
        group_ids: List[str],
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
    ) -> List[AtlanUser]:
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
    ) -> Optional[List[AtlanUser]]:
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

    @validate_arguments
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

    @validate_arguments
    def get_asset_by_qualified_name(
        self,
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        """Deprecated - use asset.get_by_qualified_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.get_by_qualified_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.get_by_qualified_name(
            qualified_name=qualified_name,
            asset_type=asset_type,
            min_ext_info=min_ext_info,
            ignore_relationships=ignore_relationships,
        )

    @validate_arguments
    def get_asset_by_guid(
        self,
        guid: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        """Deprecated - use asset.get_by_guid() instead."""
        warn(
            "This method is deprecated, please use 'asset.get_by_guid' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.get_by_guid(
            guid=guid,
            asset_type=asset_type,
            min_ext_info=min_ext_info,
            ignore_relationships=ignore_relationships,
        )

    @validate_arguments
    def retrieve_minimal(self, guid: str, asset_type: Type[A]) -> A:
        """Deprecated - use asset.retrieve_minimal() instead."""
        warn(
            "This method is deprecated, please use 'asset.retrieve_minimal' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.retrieve_minimal(guid=guid, asset_type=asset_type)

    def upsert(
        self,
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        """Deprecated - use asset.save() instead."""
        warn(
            "This method is deprecated, please use 'asset.save' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
        )

    def save(
        self,
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        """Deprecated - use asset.save() instead."""
        warn(
            "This method is deprecated, please use 'asset.save' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
        )

    def upsert_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use asset.save_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'asset.save_merging_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def save_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use asset.save_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'asset.save_merging_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def update_merging_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use asset.update_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'asset.update_merging_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.update_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def upsert_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tagss: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use asset.save_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'asset.save_replacing_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tagss
        )

    def save_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use asset.save_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'asset.save_replacing_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def update_replacing_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use asset.update_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'asset.update_replacing_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.update_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    def purge_entity_by_guid(
        self, guid: Union[str, List[str]]
    ) -> AssetMutationResponse:
        """Deprecated - use asset.purge_by_guid() instead."""
        warn(
            "This method is deprecated, please use 'asset.purge_by_guid' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.purge_by_guid(guid=guid)

    def delete_entity_by_guid(
        self, guid: Union[str, List[str]]
    ) -> AssetMutationResponse:
        """Deprecated - use asset.delete_by_guid() instead."""
        warn(
            "This method is deprecated, please use 'asset.delete_by_guid' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.delete_by_guid(guid=guid)

    def restore(self, asset_type: Type[A], qualified_name: str) -> bool:
        """Deprecated - use asset.restore() instead."""
        warn(
            "This method is deprecated, please use 'asset.restore' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.restore(asset_type=asset_type, qualified_name=qualified_name)

    def search(self, criteria: IndexSearchRequest) -> IndexSearchResults:
        """Deprecated - use asset.search() instead."""
        warn(
            "This method is deprecated, please use 'asset.search' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.search(criteria=criteria)

    def get_all_typedefs(self) -> TypeDefResponse:
        """Deprecated - use typedef.get_all() instead."""
        warn(
            "This method is deprecated, please use 'typedef.get_all' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.typedef.get_all()

    def get_typedefs(
        self, type_category: Union[AtlanTypeCategory, List[AtlanTypeCategory]]
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

    @validate_arguments
    def add_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> None:
        """Deprecated - use asset.add_atlan_tags() instead."""
        warn(
            "This method is deprecated, please use 'asset.add_atlan_tags' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.asset.add_atlan_tags(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_names=atlan_tag_names,
            propagate=propagate,
            remove_propagation_on_delete=remove_propagation_on_delete,
            restrict_lineage_propagation=restrict_lineage_propagation,
            restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
        )

    @validate_arguments
    def remove_atlan_tag(
        self, asset_type: Type[A], qualified_name: str, atlan_tag_name: str
    ) -> None:
        """Deprecated - use asset.remove_atlan_tag() instead."""
        warn(
            "This method is deprecated, please use 'asset.remove_atlan_tag' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.asset.remove_atlan_tag(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_name=atlan_tag_name,
        )

    @validate_arguments
    def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        message: Optional[str] = None,
    ) -> Optional[A]:
        """Deprecated - use asset.update_certificate() instead."""
        warn(
            "This method is deprecated, please use 'asset.update_certificate' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.update_certificate(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            certificate_status=certificate_status,
            message=message,
        )

    @validate_arguments
    def remove_certificate(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        """Deprecated - use asset.remove_certificate() instead."""
        warn(
            "This method is deprecated, please use 'asset.remove_certificate' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.remove_certificate(
            asset_type=asset_type, qualified_name=qualified_name, name=name
        )

    @validate_arguments
    def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
    ) -> Optional[A]:
        """Deprecated - use asset.update_announcement() instead."""
        warn(
            "This method is deprecated, please use 'asset.update_announcement' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.update_announcement(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            announcement=announcement,
        )

    @validate_arguments
    def remove_announcement(
        self, asset_type: Type[A], qualified_name: str, name: str
    ) -> Optional[A]:
        """Deprecated - use asset.remove_announcement() instead."""
        warn(
            "This method is deprecated, please use 'asset.remove_announcement' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.remove_announcement(
            asset_type=asset_type, qualified_name=qualified_name, name=name
        )

    def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        """Deprecated - use asset.update_custom_metadata_attributes() instead."""
        warn(
            "This method is deprecated, please use 'asset.update_custom_metadata_attributes' instead, which offers "
            "identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.asset.update_custom_metadata_attributes(
            guid=guid, custom_metadata=custom_metadata
        )

    def replace_custom_metadata(self, guid: str, custom_metadata: CustomMetadataDict):
        """Deprecated - use asset.replace_custom_metadata() instead."""
        warn(
            "This method is deprecated, please use 'asset.replace_custom_metadata' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.asset.replace_custom_metadata(guid=guid, custom_metadata=custom_metadata)

    def remove_custom_metadata(self, guid: str, cm_name: str):
        """Deprecated - use asset.remove_custom_metadata() instead."""
        warn(
            "This method is deprecated, please use 'asset.remove_custom_metadata' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.asset.remove_custom_metadata(guid=guid, cm_name=cm_name)

    @validate_arguments
    def append_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """Deprecated - use asset.append_terms() instead."""
        warn(
            "This method is deprecated, please use 'asset.append_terms' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.append_terms(
            asset_type=asset_type, terms=terms, guid=guid, qualified_name=qualified_name
        )

    @validate_arguments
    def replace_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """Deprecated - use asset.replace_terms() instead."""
        warn(
            "This method is deprecated, please use 'asset.replace_terms' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.replace_terms(
            asset_type=asset_type, terms=terms, guid=guid, qualified_name=qualified_name
        )

    @validate_arguments
    def remove_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """Deprecated - use asset.remove_terms() instead."""
        warn(
            "This method is deprecated, please use 'asset.remove_terms' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.remove_terms(
            asset_type=asset_type, terms=terms, guid=guid, qualified_name=qualified_name
        )

    @validate_arguments
    def find_connections_by_name(
        self,
        name: str,
        connector_type: AtlanConnectorType,
        attributes: Optional[List[str]] = None,
    ) -> List[Connection]:
        """Deprecated - use asset.find_connections_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_connections_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_connections_by_name(
            name=name, connector_type=connector_type, attributes=attributes
        )

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
        return self.asset.get_lineage(lineage_request=lineage_request)

    def get_lineage_list(
        self, lineage_request: LineageListRequest
    ) -> LineageListResults:
        """Deprecated - use asset.get_lineage_list() instead."""
        warn(
            "This method is deprecated, please use 'asset.get_lineage_list' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.get_lineage_list(lineage_request=lineage_request)

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
        personas: Optional[Set[str]] = None,
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
        personas: Optional[Set[str]] = None,
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
        """Deprecated - use admin.get_keycloak_events() instead."""
        warn(
            "This method is deprecated, please use 'admin.get_keycloak_events' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.admin.get_keycloak_events(keycloak_request=keycloak_request)

    def get_admin_events(self, admin_request: AdminEventRequest) -> AdminEventResponse:
        """Deprecated - use admin.get_admin_events() instead."""
        warn(
            "This method is deprecated, please use 'admin.get_admin_events' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.admin.get_admin_events(admin_request=admin_request)

    @validate_arguments
    def find_personas_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[Persona]:
        """Deprecated - use asset.find_personas_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_personas_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_personas_by_name(name=name, attributes=attributes)

    def find_purposes_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[Purpose]:
        """Deprecated - use asset.find_personas_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_purposes_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_purposes_by_name(name=name, attributes=attributes)

    @validate_arguments
    def find_glossary_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossary:
        """Deprecated - use asset.find_glossary_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_glossary_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_glossary_by_name(name=name, attributes=attributes)

    @validate_arguments
    def find_category_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """Deprecated - use asset.find_category_fast_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_category_fast_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary_qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    def find_category_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """Deprecated - use asset.find_category_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_category_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_category_by_name(
            name=name, glossary_name=glossary_name, attributes=attributes
        )

    @validate_arguments
    def find_term_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """Deprecated - use asset.find_category_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_category_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary_qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    def find_term_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """Deprecated - use asset.find_term_by_name() instead."""
        warn(
            "This method is deprecated, please use 'asset.find_term_by_name' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.find_term_by_name(
            name=name, glossary_name=glossary_name, attributes=attributes
        )

    @contextlib.contextmanager
    def max_retries(
        self, max_retries: Retry = CONNECTION_RETRY
    ) -> Generator[None, None, None]:
        """Creates a context manger that can used to temporarily change parameters used for retrying connnections.
        The original Retry information will be restored when the context is exited."""
        if self.base_url == "INTERNAL":
            adapter = self._session.adapters[HTTP_PREFIX]
        else:
            adapter = self._session.adapters[HTTPS_PREFIX]
        current_max = adapter.max_retries
        adapter.max_retries = max_retries
        LOGGER.debug(
            "max_retries set to total: %s force_list: %s",
            max_retries.total,
            max_retries.status_forcelist,
        )
        try:
            LOGGER.debug("Entering max_retries")
            yield None
            LOGGER.debug("Exiting max_retries")
        except requests.exceptions.RetryError as err:
            LOGGER.exception("Exception in max retries")
            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err
        finally:
            adapter.max_retries = current_max
            LOGGER.debug(
                "max_retries restored to total: %s force_list: %s",
                adapter.max_retries.total,
                adapter.max_retries.status_forcelist,
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
    AdminEventRequest,
    AdminEventResponse,
    KeycloakEventRequest,
    KeycloakEventResponse,
)
