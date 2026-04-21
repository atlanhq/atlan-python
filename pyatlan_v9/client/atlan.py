# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import contextlib
import copy
import json
import logging
import os
import uuid
from contextlib import _GeneratorContextManager
from contextvars import ContextVar
from http import HTTPStatus
from importlib.resources import read_text
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Union
from urllib.parse import urljoin

import httpx
import msgspec
from httpx_retries import Retry
from msgspec import UNSET, UnsetType

from pyatlan.cache.atlan_tag_cache import AtlanTagCache
from pyatlan.cache.connection_cache import ConnectionCache
from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.cache.dq_template_config_cache import DQTemplateConfigCache
from pyatlan.cache.enum_cache import EnumCache
from pyatlan.cache.group_cache import GroupCache
from pyatlan.cache.role_cache import RoleCache
from pyatlan.cache.source_tag_cache import SourceTagCache
from pyatlan.cache.user_cache import UserCache
from pyatlan.client.common import CONNECTION_RETRY
from pyatlan.client.constants import EVENT_STREAM, PARSE_QUERY, UPLOAD_IMAGE
from pyatlan.client.oauth import OAuthTokenManager
from pyatlan.errors import ERROR_CODE_FOR_HTTP_STATUS, AtlanError, ErrorCode
from pyatlan.model.core import AtlanObject as LegacyAtlanObject
from pyatlan.model.core import AtlanRequest as LegacyAtlanRequest
from pyatlan.multipart_data_generator import MultipartDataGenerator
from pyatlan.utils import (
    API,
    APPLICATION_ENCODED_FORM,
    AuthorizationFilter,
    RequestIdAdapter,
    get_python_version,
)
from pyatlan_v9.client.admin import V9AdminClient
from pyatlan_v9.client.asset import V9AssetClient
from pyatlan_v9.client.audit import V9AuditClient
from pyatlan_v9.client.contract import V9ContractClient
from pyatlan_v9.client.credential import V9CredentialClient
from pyatlan_v9.client.file import V9FileClient
from pyatlan_v9.client.group import V9GroupClient
from pyatlan_v9.client.impersonate import V9ImpersonationClient
from pyatlan_v9.client.oauth_client import V9OAuthClient
from pyatlan_v9.client.open_lineage import V9OpenLineageClient
from pyatlan_v9.client.query import V9QueryClient
from pyatlan_v9.client.role import V9RoleClient
from pyatlan_v9.client.search_log import V9SearchLogClient
from pyatlan_v9.client.sso import V9SSOClient
from pyatlan_v9.client.task import V9TaskClient
from pyatlan_v9.client.token import V9TokenClient
from pyatlan_v9.client.transport import PyatlanSyncTransport
from pyatlan_v9.client.typedef import V9TypeDefClient
from pyatlan_v9.client.user import V9UserClient
from pyatlan_v9.client.workflow import V9WorkflowClient
from pyatlan_v9.model.atlan_image import AtlanImage
from pyatlan_v9.model.core import AtlanRequest, AtlanResponse
from pyatlan_v9.model.enums import AtlanTypeCategory
from pyatlan_v9.model.query import ParsedQuery, QueryParserRequest

if TYPE_CHECKING:
    from pyatlan_v9.model.assets import Asset
    from pyatlan_v9.model.core import AssetMutationResponse

request_id_var = ContextVar("request_id", default=None)


def get_adapter() -> logging.LoggerAdapter:
    """
    Creates a LoggerAdapter that provides the requestid from the ContextVar.

    :returns: the LogAdapter
    """
    logger = logging.getLogger(__name__)
    logger.addFilter(AuthorizationFilter())
    return RequestIdAdapter(logger=logger, contextvar=request_id_var)


LOGGER = get_adapter()

DEFAULT_RETRY = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[302, 403, 429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    respect_retry_after_header=True,
)

VERSION = read_text("pyatlan", "version.txt").strip()


def log_response(response, *args, **kwargs):
    LOGGER.debug("HTTP Status: %s", response.status_code)
    LOGGER.debug("URL: %s", response.request.url)


class AtlanClient(msgspec.Struct, kw_only=True):
    """
    AtlanClient for Atlan's Atlas API using msgspec.Struct.

    Migrated from Pydantic BaseSettings to msgspec.Struct for consistency
    with the v9 model layer. Configuration is read from constructor
    arguments with environment variable fallbacks.

    Environment variables (with ATLAN_ prefix):
        ATLAN_BASE_URL: Base URL for the Atlan service
        ATLAN_API_KEY: API key for authentication
        ATLAN_OAUTH_CLIENT_ID: OAuth client ID
        ATLAN_OAUTH_CLIENT_SECRET: OAuth client secret

    Example::

        client = AtlanClient(
            base_url="https://myinstance.atlan.com",
            api_key="my-api-key",
        )
        # Or with environment variables:
        client = AtlanClient()
    """

    # --- Configuration fields (user-facing) ---
    base_url: Union[str, None] = None
    api_key: Union[str, None] = None
    oauth_client_id: Union[str, None] = None
    oauth_client_secret: Union[str, None] = None
    connect_timeout: float = 30.0
    read_timeout: float = 900.0
    retry: Any = None  # Defaults to DEFAULT_RETRY in __post_init__
    proxy: Any = None  # None = no proxy (may be overridden by env vars)
    verify: Union[Any, UnsetType] = UNSET  # UNSET = not provided → default True

    # --- Internal state (initialized in __post_init__) ---
    _session: Any = None
    _request_params: Any = None
    _401_has_retried: Any = None
    _user_id: Union[str, None] = None
    _user_client: Any = None
    _oauth_token_manager: Any = None
    _clients: Any = None  # Lazy dict of sub-clients
    _caches: Any = None  # Lazy dict of caches

    def __post_init__(self):
        # Apply defaults
        if self.retry is None:
            self.retry = DEFAULT_RETRY

        # Track whether verify was explicitly provided before resolving
        _verify_explicit = self.verify is not UNSET
        if not _verify_explicit:
            self.verify = True  # Default

        # Read from environment variables (matching legacy BaseSettings behavior)
        if self.base_url is None:
            self.base_url = os.environ.get("ATLAN_BASE_URL", "INTERNAL")
        if self.api_key is None:
            self.api_key = os.environ.get("ATLAN_API_KEY")
        if self.oauth_client_id is None:
            self.oauth_client_id = os.environ.get("ATLAN_OAUTH_CLIENT_ID")
        if self.oauth_client_secret is None:
            self.oauth_client_secret = os.environ.get("ATLAN_OAUTH_CLIENT_SECRET")

        # Initialize internal state
        self._401_has_retried = ContextVar("_401_has_retried", default=False)
        self._clients = {}
        self._caches = {}

        # Setup authentication
        if self.oauth_client_id and self.oauth_client_secret and self.api_key is None:
            LOGGER.debug("API KEY not provided. Using OAuth flow for authentication")
            self._oauth_token_manager = OAuthTokenManager(
                base_url=self.base_url,
                client_id=self.oauth_client_id,
                client_secret=self.oauth_client_secret,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
            )
            self._request_params = {"headers": {}}
        else:
            self._request_params = (
                {"headers": {"authorization": f"Bearer {self.api_key}"}}
                if self.api_key and self.api_key.strip()
                else {"headers": {}}
            )

        # Resolve proxy from environment variables if not explicitly provided
        if self.proxy is None:
            env_proxy = (
                os.environ.get("HTTPS_PROXY")
                or os.environ.get("https_proxy")
                or os.environ.get("HTTP_PROXY")
                or os.environ.get("http_proxy")
            )
            if env_proxy:
                self.proxy = env_proxy

        # Resolve verify from environment variables if not explicitly provided
        if not _verify_explicit:
            ssl_cert_file = os.environ.get("SSL_CERT_FILE") or os.environ.get(
                "REQUESTS_CA_BUNDLE"
            )
            if ssl_cert_file:
                self.verify = ssl_cert_file

        # Build transport kwargs
        transport_kwargs: Dict[str, Any] = {}
        if self.proxy is not None:
            transport_kwargs["proxy"] = self.proxy
        if _verify_explicit or self.verify is not True:
            transport_kwargs["verify"] = self.verify

        # Create httpx session with custom transport
        self._session = httpx.Client(
            transport=PyatlanSyncTransport(retry=self.retry, **transport_kwargs),
            headers={
                "x-atlan-agent": "sdk",
                "x-atlan-agent-id": "python",
                "x-atlan-client-origin": "product_sdk",
                "x-atlan-python-version": get_python_version(),
                "x-atlan-client-type": "sync",
                "User-Agent": f"Atlan-PythonSDK/{VERSION}",
            },
            event_hooks={"response": [log_response]},
        )
        self._401_has_retried.set(False)

    # --- Sub-client properties (lazy-initialized via _clients dict) ---

    def _get_client(self, key: str, factory):
        if key not in self._clients:
            self._clients[key] = factory(client=self)
        return self._clients[key]

    def _get_cache(self, key: str, factory):
        if key not in self._caches:
            self._caches[key] = factory(client=self)
        return self._caches[key]

    @property
    def admin(self) -> V9AdminClient:
        return self._get_client("admin", V9AdminClient)

    @property
    def audit(self) -> V9AuditClient:
        return self._get_client("audit", V9AuditClient)

    @property
    def search_log(self) -> V9SearchLogClient:
        return self._get_client("search_log", V9SearchLogClient)

    @property
    def workflow(self) -> V9WorkflowClient:
        return self._get_client("workflow", V9WorkflowClient)

    @property
    def credentials(self) -> V9CredentialClient:
        return self._get_client("credentials", V9CredentialClient)

    @property
    def group(self) -> V9GroupClient:
        return self._get_client("group", V9GroupClient)

    @property
    def role(self) -> V9RoleClient:
        return self._get_client("role", V9RoleClient)

    @property
    def asset(self) -> V9AssetClient:
        return self._get_client("asset", V9AssetClient)

    @property
    def impersonate(self) -> V9ImpersonationClient:
        return self._get_client("impersonate", V9ImpersonationClient)

    @property
    def queries(self) -> V9QueryClient:
        return self._get_client("queries", V9QueryClient)

    @property
    def token(self) -> V9TokenClient:
        return self._get_client("token", V9TokenClient)

    @property
    def oauth_client(self) -> V9OAuthClient:
        return self._get_client("oauth_client", V9OAuthClient)

    @property
    def typedef(self) -> V9TypeDefClient:
        return self._get_client("typedef", V9TypeDefClient)

    @property
    def user(self) -> V9UserClient:
        return self._get_client("user", V9UserClient)

    @property
    def tasks(self) -> V9TaskClient:
        return self._get_client("tasks", V9TaskClient)

    @property
    def sso(self) -> V9SSOClient:
        return self._get_client("sso", V9SSOClient)

    @property
    def open_lineage(self) -> V9OpenLineageClient:
        return self._get_client("open_lineage", V9OpenLineageClient)

    @property
    def files(self) -> V9FileClient:
        return self._get_client("files", V9FileClient)

    @property
    def contracts(self) -> V9ContractClient:
        return self._get_client("contracts", V9ContractClient)

    # --- Cache properties ---

    @property
    def atlan_tag_cache(self) -> AtlanTagCache:
        return self._get_cache("atlan_tag", AtlanTagCache)

    @property
    def enum_cache(self) -> EnumCache:
        return self._get_cache("enum", EnumCache)

    @property
    def group_cache(self) -> GroupCache:
        return self._get_cache("group", GroupCache)

    @property
    def role_cache(self) -> RoleCache:
        return self._get_cache("role", RoleCache)

    @property
    def user_cache(self) -> UserCache:
        return self._get_cache("user", UserCache)

    @property
    def custom_metadata_cache(self) -> CustomMetadataCache:
        return self._get_cache("custom_metadata", CustomMetadataCache)

    @property
    def connection_cache(self) -> ConnectionCache:
        return self._get_cache("connection", ConnectionCache)

    @property
    def source_tag_cache(self) -> SourceTagCache:
        return self._get_cache("source_tag", SourceTagCache)

    @property
    def dq_template_config_cache(self) -> DQTemplateConfigCache:
        return self._get_cache("dq_template_config", DQTemplateConfigCache)

    # --- Class methods ---

    @classmethod
    def from_token_guid(
        cls,
        guid: str,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> "AtlanClient":
        from pyatlan.client.common.impersonate import ImpersonateUser
        from pyatlan.client.constants import GET_TOKEN
        from pyatlan.model.response import AccessTokenResponse

        final_base_url = base_url or os.environ.get("ATLAN_BASE_URL", "INTERNAL")
        client = cls(base_url=final_base_url, api_key="")
        client_info = ImpersonateUser.get_client_info(
            client_id=client_id, client_secret=client_secret
        )
        argo_credentials = {
            "grant_type": "client_credentials",
            "client_id": client_info.client_id,
            "client_secret": client_info.client_secret,
            "scope": "openid",
        }
        from pyatlan.errors import AtlanError, ErrorCode

        try:
            raw_json = client._call_api(GET_TOKEN, request_obj=argo_credentials)
            argo_token = AccessTokenResponse(**raw_json).access_token
            temp_argo_client = cls(base_url=final_base_url, api_key=argo_token)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE_WITH_PARAM.exception_with_parameters(
                "Failed to obtain Atlan-Argo token"
            ) from atlan_err
        token_secret = temp_argo_client.impersonate.get_client_secret(client_guid=guid)
        token_client_id = temp_argo_client.token.get_by_guid(guid=guid).client_id
        token_credentials = {
            "grant_type": "client_credentials",
            "client_id": token_client_id,
            "client_secret": token_secret,
            "scope": "openid",
        }
        try:
            raw_json = client._call_api(GET_TOKEN, request_obj=token_credentials)
            token_api_key = AccessTokenResponse(**raw_json).access_token
            return cls(base_url=final_base_url, api_key=token_api_key)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE_WITH_PARAM.exception_with_parameters(
                "Failed to obtain access token for API token"
            ) from atlan_err

    # --- Core API methods ---

    def update_headers(self, header: Dict[str, str]):
        self._session.headers.update(header)

    def _handle_file_download(self, raw_response: Any, file_path: str) -> str:
        try:
            with open(file_path, "wb") as download_file:
                for chunk in raw_response:
                    download_file.write(chunk)
        except Exception as err:
            raise ErrorCode.UNABLE_TO_DOWNLOAD_FILE.exception_with_parameters(
                str((hasattr(err, "strerror") and err.strerror) or err), file_path
            )
        return file_path

    def _call_api_internal(
        self,
        api,
        path,
        params,
        binary_data=None,
        download_file_path=None,
        text_response=False,
    ):
        token = request_id_var.set(str(uuid.uuid4()))
        try:
            params["headers"]["X-Atlan-Request-Id"] = request_id_var.get()
            timeout = httpx.Timeout(
                None, connect=self.connect_timeout, read=self.read_timeout
            )
            if binary_data:
                response = self._session.request(
                    api.method.value,
                    path,
                    data=binary_data,
                    **params,
                    timeout=timeout,
                )
            elif api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                with self._session.stream(
                    api.method.value,
                    path,
                    **params,
                    timeout=timeout,
                ) as stream_response:
                    if download_file_path:
                        return self._handle_file_download(
                            stream_response.iter_raw(), download_file_path
                        )

                    content = stream_response.read()
                    text = content.decode("utf-8") if content else ""
                    lines = []

                    if stream_response.status_code == api.expected_status:
                        lines = text.splitlines() if text else []

                    response_data = {
                        "status_code": stream_response.status_code,
                        "headers": stream_response.headers,
                        "text": text,
                        "content": content,
                        "lines": lines,
                    }

                    response = SimpleNamespace(
                        status_code=response_data["status_code"],
                        headers=response_data["headers"],
                        text=response_data["text"],
                        content=response_data["content"],
                        _stream_lines=response_data["lines"],
                        json=lambda: (
                            json.loads(response_data["text"])
                            if response_data["text"]
                            else {}
                        ),
                    )
            else:
                response = self._session.request(
                    api.method.value,
                    path,
                    **params,
                    timeout=timeout,
                )
            if response is not None:
                LOGGER.debug("HTTP Status: %s", response.status_code)
            if response is None:
                return None

            if (
                self._401_has_retried.get()
                and response.status_code
                != ErrorCode.AUTHENTICATION_PASSTHROUGH.http_error_code
            ):
                self._401_has_retried.set(False)

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
                        if hasattr(response, "_stream_lines"):
                            for line in response._stream_lines:
                                if not line:
                                    continue
                                if not line.startswith("data: "):
                                    raise ErrorCode.UNABLE_TO_DESERIALIZE.exception_with_parameters(
                                        line
                                    )
                                events.append(json.loads(line.split("data: ")[1]))
                    if text_response:
                        response_ = response.text
                    else:
                        response_ = (
                            events
                            if events
                            else AtlanResponse(
                                raw_json=response.json(), client=self
                            ).to_dict()
                        )
                    LOGGER.debug("response: %s", response_)
                    return response_
                except (json.decoder.JSONDecodeError,) as e:
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
                    error_code = (
                        error_info.get("errorCode", 0)
                        or error_info.get("code", 0)
                        or error_info.get("status")
                    )
                    error_message = error_info.get(
                        "errorMessage", ""
                    ) or error_info.get("message", "")
                    error_doc = (
                        error_info.get("doc")
                        or error_info.get("errorDoc")
                        or error_info.get("errorDocument")
                        or error_info.get("errorDocumentation")
                    )
                    error_cause = error_info.get("errorCause", [])
                    causes = error_info.get("causes", [])
                    backend_error_id = error_info.get("errorId")

                    error_cause_details = [
                        f"ErrorType: {cause.get('errorType', 'Unknown')}, "
                        f"Message: {cause.get('errorMessage', 'No additional information provided')}, "
                        f"Location: {cause.get('location', 'Unknown location')}"
                        for cause in causes
                    ]
                    error_cause_details_str = (
                        "\n".join(error_cause_details) if error_cause_details else ""
                    )

                    if (
                        (self._user_id or self._oauth_token_manager)
                        and not self._401_has_retried.get()
                        and response.status_code
                        == ErrorCode.AUTHENTICATION_PASSTHROUGH.http_error_code
                    ):
                        try:
                            LOGGER.debug("Starting 401 automatic token refresh.")
                            return self._handle_401_token_refresh(
                                api,
                                path,
                                params,
                                binary_data=binary_data,
                                download_file_path=download_file_path,
                                text_response=text_response,
                            )
                        except Exception as e:
                            LOGGER.debug(
                                "API call failed after a successful 401 token refresh. Error details: %s",
                                e,
                            )
                            raise

                    if error_code and error_message:
                        error = ERROR_CODE_FOR_HTTP_STATUS.get(
                            response.status_code, ErrorCode.ERROR_PASSTHROUGH
                        )
                        raise error.exception_with_parameters(
                            error_code,
                            error_message,
                            error_cause_details_str,
                            error_cause=error_cause,
                            backend_error_id=backend_error_id,
                            error_doc=error_doc,
                        )
                raise AtlanError(
                    SimpleNamespace(
                        http_error_code=response.status_code,
                        error_id=f"ATLAN-PYTHON-{response.status_code}-000",
                        error_message=response.text,
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
        LOGGER.debug("Client-Type  : %s", "SYNC")
        LOGGER.debug("Python-Version: %s", get_python_version())
        LOGGER.debug("User-Agent   : %s", f"Atlan-PythonSDK/{VERSION}")

    def _call_api(
        self,
        api,
        query_params=None,
        request_obj=None,
        text_response=False,
        extra_headers=None,
    ):
        path = self._create_path(api)
        params = self._create_params(api, query_params, request_obj)
        if extra_headers:
            params["headers"].update(extra_headers)
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return self._call_api_internal(api, path, params, text_response=text_response)

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
        params = self._create_params(api, query_params=None, request_obj=None)
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return self._call_api_internal(api, path, params, binary_data=post_data)

    def _s3_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        return self._call_api_internal(api, path, params, binary_data=upload_file)

    def _azure_blob_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        params["headers"]["x-ms-blob-type"] = "BlockBlob"
        return self._call_api_internal(api, path, params, binary_data=upload_file)

    def _gcs_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        return self._call_api_internal(api, path, params, binary_data=upload_file)

    def _presigned_url_file_download(self, api: API, file_path: str):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        return self._call_api_internal(api, path, params, download_file_path=file_path)

    def _create_params(self, api: API, query_params, request_obj):
        params = copy.deepcopy(self._request_params)
        if self._oauth_token_manager:
            token = self._oauth_token_manager.get_token()
            params["headers"]["authorization"] = f"Bearer {token}"
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        if query_params is not None:
            params["params"] = query_params
        if request_obj is not None:
            if api.consumes == APPLICATION_ENCODED_FORM:
                params["data"] = request_obj
            elif isinstance(request_obj, LegacyAtlanObject):
                # Use legacy serialization so request body matches legacy client exactly
                params["data"] = LegacyAtlanRequest(
                    instance=request_obj, client=self
                ).json()
            elif hasattr(request_obj, "json") and callable(request_obj.json):
                # Prefer json() method if available (handles nested serialization properly)
                params["data"] = request_obj.json(by_alias=True, exclude_none=True)
            elif hasattr(request_obj, "to_dict") and callable(request_obj.to_dict):
                params["data"] = json.dumps(request_obj.to_dict())
            elif isinstance(request_obj, (dict, list)):
                params["data"] = json.dumps(request_obj)
            elif isinstance(request_obj, msgspec.Struct):
                params["data"] = AtlanRequest(instance=request_obj, client=self).json()
            elif hasattr(request_obj, "to_json") and callable(request_obj.to_json):
                params["data"] = AtlanRequest(instance=request_obj, client=self).json()
            elif hasattr(request_obj, "dict") and callable(request_obj.dict):
                # Pydantic v1 models (old pyatlan models)
                params["data"] = json.dumps(
                    request_obj.dict(by_alias=True, exclude_none=True)
                )
            elif hasattr(request_obj, "model_dump") and callable(
                request_obj.model_dump
            ):
                # Pydantic v2 models
                params["data"] = json.dumps(
                    request_obj.model_dump(by_alias=True, exclude_none=True)
                )
            elif hasattr(request_obj, "__root__"):
                params["data"] = json.dumps(request_obj.__root__)
            else:
                params["data"] = json.dumps(request_obj)
        return params

    def _handle_401_token_refresh(
        self,
        api,
        path,
        params,
        binary_data=None,
        download_file_path=None,
        text_response=False,
    ):
        """Handle token refresh and retry the API request upon a 401 Unauthorized."""
        if self._oauth_token_manager:
            self._oauth_token_manager.invalidate_token()
            token = self._oauth_token_manager.get_token()
            params["headers"]["authorization"] = f"Bearer {token}"
            self._401_has_retried.set(True)
            LOGGER.debug("Successfully refreshed OAuth token after 401.")
            return self._call_api_internal(
                api,
                path,
                params,
                binary_data=binary_data,
                download_file_path=download_file_path,
                text_response=text_response,
            )

        try:
            new_token = self.impersonate.user(user_id=self._user_id)
        except Exception as e:
            LOGGER.debug(
                "Failed to impersonate user %s for 401 token refresh. Not retrying. Error: %s",
                self._user_id,
                e,
            )
            raise
        self.api_key = new_token
        self._401_has_retried.set(True)
        params["headers"]["authorization"] = f"Bearer {self.api_key}"
        self._request_params["headers"]["authorization"] = f"Bearer {self.api_key}"
        LOGGER.debug("Successfully completed 401 automatic token refresh.")

        import time

        retry_count = 1
        while retry_count <= self.retry.total:
            try:
                response = self.typedef.get(type_category=[AtlanTypeCategory.STRUCT])
                if response and response.struct_defs:
                    break
            except Exception as e:
                LOGGER.debug(
                    "Retrying to get typedefs (to ensure token is active) after token refresh failed: %s",
                    e,
                )
            time.sleep(retry_count)
            retry_count += 1

        return self._call_api_internal(
            api,
            path,
            params,
            binary_data=binary_data,
            download_file_path=download_file_path,
            text_response=text_response,
        )

    def upload_image(self, file, filename: str) -> AtlanImage:
        """
        Uploads an image from the provided local file.

        :param file: local file to upload
        :param filename: name of the file to be uploaded
        :returns: details of the uploaded image
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._upload_file(UPLOAD_IMAGE, file=file, filename=filename)
        return msgspec.convert(raw_json, AtlanImage, strict=False)

    def search(self, criteria):
        """Search assets. Delegates to asset.search()."""
        from warnings import warn

        warn(
            "This method is deprecated, please use 'asset.search' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.asset.search(criteria=criteria)

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
        )
        return msgspec.convert(raw_json, ParsedQuery, strict=False)

    def save(
        self,
        entity: Union["Asset", List["Asset"]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
        append_atlan_tags: bool = False,
    ) -> "AssetMutationResponse":
        """
        Convenience method that delegates to asset.save().
        If an asset with the same qualified_name exists, updates the existing asset. Otherwise, creates the asset.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :param append_atlan_tags: whether to add/update/remove AtlanTags during an update (True) or not (False)
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        """
        return self.asset.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
            append_atlan_tags=append_atlan_tags,
        )

    @contextlib.contextmanager
    def max_retries(
        self, max_retries: Retry = CONNECTION_RETRY
    ) -> _GeneratorContextManager[None]:
        """
        Creates a context manager that temporarily changes retry parameters.

        The original Retry information will be restored when the context is exited.
        """
        current_transport = self._session._transport

        transport_kwargs: Dict[str, Any] = {}
        if self.proxy:
            transport_kwargs["proxy"] = self.proxy
        if self.verify is not None:
            transport_kwargs["verify"] = self.verify

        new_transport = PyatlanSyncTransport(retry=max_retries, **transport_kwargs)
        self._session._transport = new_transport

        LOGGER.debug(
            "max_retries set to total: %s force_list: %s",
            max_retries.total,
            max_retries.status_forcelist,
        )
        try:
            LOGGER.debug("Entering max_retries")
            yield None  # type: ignore[misc]
            LOGGER.debug("Exiting max_retries")
        except httpx.TransportError as err:
            LOGGER.exception("Exception in max retries")
            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err
        finally:
            self._session._transport = current_transport
            LOGGER.debug("max_retries restored %s", self._session._transport.retry)  # type: ignore[attr-defined]


@contextlib.contextmanager
def client_connection(
    client: AtlanClient,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    connect_timeout: float = 30.0,
    read_timeout: float = 120.0,
    retry: Retry = DEFAULT_RETRY,
) -> Generator[AtlanClient, None, None]:
    """
    Creates a new client with the given base_url and/or api_key.

    :param client: existing client to clone settings from
    :param base_url: the base_url for the new connection (uses current if not specified)
    :param api_key: the api_key for the new connection (uses current if not specified)
    """
    tmp_client = AtlanClient(
        base_url=base_url or client.base_url,
        api_key=api_key or client.api_key,
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
        retry=retry,
    )
    yield tmp_client
