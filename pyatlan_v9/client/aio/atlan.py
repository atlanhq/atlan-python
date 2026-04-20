# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
import contextlib
import copy
import json
import logging
import os
import uuid
from contextlib import _AsyncGeneratorContextManager
from contextvars import ContextVar
from http import HTTPStatus
from importlib.resources import read_text
from types import SimpleNamespace
from typing import Any, AsyncGenerator, Dict, Optional, Union
from urllib.parse import urljoin

import httpx
import msgspec
from httpx_retries import Retry
from msgspec import UNSET, UnsetType

from pyatlan.cache.aio import (
    AsyncAtlanTagCache,
    AsyncConnectionCache,
    AsyncCustomMetadataCache,
    AsyncDQTemplateConfigCache,
    AsyncEnumCache,
    AsyncGroupCache,
    AsyncRoleCache,
    AsyncSourceTagCache,
    AsyncUserCache,
)
from pyatlan.client.aio.oauth import AsyncOAuthTokenManager
from pyatlan.client.common import CONNECTION_RETRY
from pyatlan.client.constants import EVENT_STREAM, PARSE_QUERY, UPLOAD_IMAGE
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
from pyatlan_v9.client.aio.admin import V9AsyncAdminClient
from pyatlan_v9.client.aio.asset import V9AsyncAssetClient
from pyatlan_v9.client.aio.audit import V9AsyncAuditClient
from pyatlan_v9.client.aio.contract import V9AsyncContractClient
from pyatlan_v9.client.aio.credential import V9AsyncCredentialClient
from pyatlan_v9.client.aio.file import V9AsyncFileClient
from pyatlan_v9.client.aio.group import V9AsyncGroupClient
from pyatlan_v9.client.aio.impersonate import V9AsyncImpersonationClient
from pyatlan_v9.client.aio.oauth_client import V9AsyncOAuthClient
from pyatlan_v9.client.aio.open_lineage import V9AsyncOpenLineageClient
from pyatlan_v9.client.aio.query import V9AsyncQueryClient
from pyatlan_v9.client.aio.role import V9AsyncRoleClient
from pyatlan_v9.client.aio.search_log import V9AsyncSearchLogClient
from pyatlan_v9.client.aio.sso import V9AsyncSSOClient
from pyatlan_v9.client.aio.task import V9AsyncTaskClient
from pyatlan_v9.client.aio.token import V9AsyncTokenClient
from pyatlan_v9.client.aio.typedef import V9AsyncTypeDefClient
from pyatlan_v9.client.aio.user import V9AsyncUserClient
from pyatlan_v9.client.aio.workflow import V9AsyncWorkflowClient
from pyatlan_v9.client.transport import PyatlanAsyncTransport
from pyatlan_v9.model.aio.core import AsyncAtlanRequest, AsyncAtlanResponse
from pyatlan_v9.model.atlan_image import AtlanImage
from pyatlan_v9.model.enums import AtlanTypeCategory
from pyatlan_v9.model.query import ParsedQuery, QueryParserRequest

request_id_var = ContextVar("request_id", default=None)


def _get_adapter() -> logging.LoggerAdapter:
    logger = logging.getLogger(__name__)
    logger.addFilter(AuthorizationFilter())
    return RequestIdAdapter(logger=logger, contextvar=request_id_var)


LOGGER = _get_adapter()

DEFAULT_RETRY = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[302, 403, 429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    respect_retry_after_header=True,
)

VERSION = read_text("pyatlan", "version.txt").strip()


async def _log_response(response, *args, **kwargs):
    LOGGER.debug("HTTP Status: %s", response.status_code)
    LOGGER.debug("URL: %s", response.request.url)


class AsyncAtlanClient(msgspec.Struct, kw_only=True):
    """
    Standalone async client for the Atlan v9 API.

    Mirrors the sync V9 ``AtlanClient`` structure but with async/await support.
    Does **not** inherit from or delegate to any legacy client.

    Environment variables (with ATLAN_ prefix):
        ATLAN_BASE_URL: Base URL for the Atlan service
        ATLAN_API_KEY: API key for authentication
        ATLAN_OAUTH_CLIENT_ID: OAuth client ID
        ATLAN_OAUTH_CLIENT_SECRET: OAuth client secret

    Example::

        async with AsyncAtlanClient(
            base_url="https://myinstance.atlan.com",
            api_key="my-api-key",
        ) as client:
            results = await client.asset.search(criteria)
    """

    # --- Configuration fields ---
    base_url: Union[str, None] = None
    api_key: Union[str, None] = None
    oauth_client_id: Union[str, None] = None
    oauth_client_secret: Union[str, None] = None
    connect_timeout: float = 30.0
    read_timeout: float = 900.0
    retry: Any = None
    proxy: Any = None
    verify: Union[Any, UnsetType] = UNSET

    # --- Internal state ---
    _async_session: Any = None
    _request_params: Any = None
    _401_has_retried: Any = None
    _user_id: Union[str, None] = None
    _async_oauth_token_manager: Any = None
    _clients: Any = None
    _caches: Any = None

    def __post_init__(self):
        if self.retry is None:
            self.retry = DEFAULT_RETRY

        _verify_explicit = self.verify is not UNSET
        if not _verify_explicit:
            self.verify = True

        if self.base_url is None:
            self.base_url = os.environ.get("ATLAN_BASE_URL", "INTERNAL")
        if self.api_key is None:
            self.api_key = os.environ.get("ATLAN_API_KEY")
        if self.oauth_client_id is None:
            self.oauth_client_id = os.environ.get("ATLAN_OAUTH_CLIENT_ID")
        if self.oauth_client_secret is None:
            self.oauth_client_secret = os.environ.get("ATLAN_OAUTH_CLIENT_SECRET")

        self._401_has_retried = ContextVar("_401_has_retried", default=False)
        self._clients = {}
        self._caches = {}

        if self.oauth_client_id and self.oauth_client_secret and self.api_key is None:
            LOGGER.debug(
                "API KEY not provided. Using async OAuth flow for authentication"
            )
            self._async_oauth_token_manager = AsyncOAuthTokenManager(
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

        if self.proxy is None:
            env_proxy = (
                os.environ.get("HTTPS_PROXY")
                or os.environ.get("https_proxy")
                or os.environ.get("HTTP_PROXY")
                or os.environ.get("http_proxy")
            )
            if env_proxy:
                self.proxy = env_proxy

        if not _verify_explicit:
            ssl_cert_file = os.environ.get("SSL_CERT_FILE") or os.environ.get(
                "REQUESTS_CA_BUNDLE"
            )
            if ssl_cert_file:
                self.verify = ssl_cert_file

        transport_kwargs: Dict[str, Any] = {}
        if self.proxy is not None:
            transport_kwargs["proxy"] = self.proxy
        if _verify_explicit or self.verify is not True:
            transport_kwargs["verify"] = self.verify

        self._async_session = httpx.AsyncClient(
            transport=PyatlanAsyncTransport(retry=self.retry, **transport_kwargs),
            headers={
                "x-atlan-agent": "sdk",
                "x-atlan-agent-id": "python",
                "x-atlan-client-origin": "product_sdk",
                "x-atlan-python-version": get_python_version(),
                "x-atlan-client-type": "async",
                "User-Agent": f"Atlan-PythonSDK/{VERSION}",
            },
            event_hooks={"response": [_log_response]},
        )
        self._401_has_retried.set(False)

    # ------------------------------------------------------------------
    # Sub-client properties
    # ------------------------------------------------------------------

    def _get_client(self, key: str, factory):
        if key not in self._clients:
            self._clients[key] = factory(client=self)
        return self._clients[key]

    def _get_cache(self, key: str, factory):
        if key not in self._caches:
            self._caches[key] = factory(client=self)
        return self._caches[key]

    @property
    def admin(self) -> V9AsyncAdminClient:
        return self._get_client("admin", V9AsyncAdminClient)

    @property
    def asset(self) -> V9AsyncAssetClient:
        return self._get_client("asset", V9AsyncAssetClient)

    @property
    def audit(self) -> V9AsyncAuditClient:
        return self._get_client("audit", V9AsyncAuditClient)

    @property
    def contracts(self) -> V9AsyncContractClient:
        return self._get_client("contracts", V9AsyncContractClient)

    @property
    def credentials(self) -> V9AsyncCredentialClient:
        return self._get_client("credentials", V9AsyncCredentialClient)

    @property
    def files(self) -> V9AsyncFileClient:
        return self._get_client("files", V9AsyncFileClient)

    @property
    def group(self) -> V9AsyncGroupClient:
        return self._get_client("group", V9AsyncGroupClient)

    @property
    def impersonate(self) -> V9AsyncImpersonationClient:
        return self._get_client("impersonate", V9AsyncImpersonationClient)

    @property
    def oauth_client(self) -> V9AsyncOAuthClient:
        return self._get_client("oauth_client", V9AsyncOAuthClient)

    @property
    def open_lineage(self) -> V9AsyncOpenLineageClient:
        return self._get_client("open_lineage", V9AsyncOpenLineageClient)

    @property
    def queries(self) -> V9AsyncQueryClient:
        return self._get_client("queries", V9AsyncQueryClient)

    @property
    def role(self) -> V9AsyncRoleClient:
        return self._get_client("role", V9AsyncRoleClient)

    @property
    def search_log(self) -> V9AsyncSearchLogClient:
        return self._get_client("search_log", V9AsyncSearchLogClient)

    @property
    def sso(self) -> V9AsyncSSOClient:
        return self._get_client("sso", V9AsyncSSOClient)

    @property
    def tasks(self) -> V9AsyncTaskClient:
        return self._get_client("tasks", V9AsyncTaskClient)

    @property
    def token(self) -> V9AsyncTokenClient:
        return self._get_client("token", V9AsyncTokenClient)

    @property
    def typedef(self) -> V9AsyncTypeDefClient:
        return self._get_client("typedef", V9AsyncTypeDefClient)

    @property
    def user(self) -> V9AsyncUserClient:
        return self._get_client("user", V9AsyncUserClient)

    @property
    def workflow(self) -> V9AsyncWorkflowClient:
        return self._get_client("workflow", V9AsyncWorkflowClient)

    # ------------------------------------------------------------------
    # Cache properties (async caches)
    # ------------------------------------------------------------------

    @property
    def atlan_tag_cache(self) -> AsyncAtlanTagCache:
        return self._get_cache("atlan_tag", AsyncAtlanTagCache)

    @property
    def enum_cache(self) -> AsyncEnumCache:
        return self._get_cache("enum", AsyncEnumCache)

    @property
    def group_cache(self) -> AsyncGroupCache:
        return self._get_cache("group", AsyncGroupCache)

    @property
    def role_cache(self) -> AsyncRoleCache:
        return self._get_cache("role", AsyncRoleCache)

    @property
    def user_cache(self) -> AsyncUserCache:
        return self._get_cache("user", AsyncUserCache)

    @property
    def custom_metadata_cache(self) -> AsyncCustomMetadataCache:
        return self._get_cache("custom_metadata", AsyncCustomMetadataCache)

    @property
    def connection_cache(self) -> AsyncConnectionCache:
        return self._get_cache("connection", AsyncConnectionCache)

    @property
    def source_tag_cache(self) -> AsyncSourceTagCache:
        return self._get_cache("source_tag", AsyncSourceTagCache)

    @property
    def dq_template_config_cache(self) -> AsyncDQTemplateConfigCache:
        return self._get_cache("dq_template_config", AsyncDQTemplateConfigCache)

    # ------------------------------------------------------------------
    # Core API methods
    # ------------------------------------------------------------------

    def update_headers(self, header: Dict[str, str]):
        self._async_session.headers.update(header)

    def _create_path(self, api: API) -> str:
        if self.base_url == "INTERNAL":
            return urljoin(api.endpoint.service, api.path)
        return urljoin(urljoin(self.base_url, api.endpoint.prefix), api.path)

    async def _create_params(
        self, api: API, query_params, request_obj
    ) -> Dict[str, Any]:
        params = copy.deepcopy(self._request_params)
        if self._async_oauth_token_manager:
            token = await self._async_oauth_token_manager.get_token()
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
            elif hasattr(request_obj, "to_dict") and callable(request_obj.to_dict):
                params["data"] = json.dumps(request_obj.to_dict())
            elif isinstance(request_obj, (dict, list)):
                params["data"] = json.dumps(request_obj)
            elif isinstance(request_obj, msgspec.Struct):
                async_request = AsyncAtlanRequest(
                    instance=request_obj,
                    client=self,  # type: ignore[arg-type]
                )
                params["data"] = await async_request.json()
            elif hasattr(request_obj, "to_json") and callable(request_obj.to_json):
                async_request = AsyncAtlanRequest(
                    instance=request_obj,
                    client=self,  # type: ignore[arg-type]
                )
                params["data"] = await async_request.json()
            elif hasattr(request_obj, "__root__"):
                params["data"] = json.dumps(request_obj.__root__)
            elif hasattr(request_obj, "json") and hasattr(request_obj, "__fields__"):
                params["data"] = request_obj.json(by_alias=True, exclude_none=True)
            else:
                params["data"] = json.dumps(request_obj)
        return params

    def _api_logger(self, api: API, path: str):
        LOGGER.debug("------------------------------------------------------")
        LOGGER.debug("Call         : %s %s", api.method, path)
        LOGGER.debug("Content-type_ : %s", api.consumes)
        LOGGER.debug("Accept       : %s", api.produces)
        LOGGER.debug("Client-Type  : %s", "ASYNC")
        LOGGER.debug("Python-Version: %s", get_python_version())
        LOGGER.debug("User-Agent   : %s", f"Atlan-PythonSDK/{VERSION}")

    async def _call_api(
        self,
        api,
        query_params=None,
        request_obj=None,
        text_response=False,
        extra_headers=None,
    ):
        path = self._create_path(api)
        params = await self._create_params(api, query_params, request_obj)
        if extra_headers:
            params["headers"].update(extra_headers)
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return await self._call_api_internal(
            api, path, params, text_response=text_response
        )

    async def _handle_file_download(self, raw_response: Any, file_path: str) -> str:
        try:
            with open(file_path, "wb") as download_file:
                async for chunk in raw_response.aiter_raw():
                    download_file.write(chunk)
        except Exception as err:
            raise ErrorCode.UNABLE_TO_DOWNLOAD_FILE.exception_with_parameters(
                str((hasattr(err, "strerror") and err.strerror) or err), file_path
            )
        return file_path

    async def _call_api_internal(
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
                response = await self._async_session.request(
                    api.method.value,
                    path,
                    data=binary_data,
                    **params,
                    timeout=timeout,
                )
            elif api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                async with self._async_session.stream(
                    api.method.value,
                    path,
                    **params,
                    timeout=timeout,
                ) as stream_response:
                    if download_file_path:
                        return await self._handle_file_download(
                            stream_response, download_file_path
                        )

                    content = await stream_response.aread()
                    text = content.decode("utf-8") if content else ""
                    lines = []

                    if stream_response.status_code == api.expected_status:
                        lines = text.splitlines() if text else []

                    response = SimpleNamespace(
                        status_code=stream_response.status_code,
                        headers=stream_response.headers,
                        text=text,
                        content=content,
                        _stream_lines=lines,
                        json=lambda: json.loads(text) if text else {},
                    )
            else:
                response = await self._async_session.request(
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
                            else await AsyncAtlanResponse(
                                raw_json=response.json(),
                                client=self,  # type: ignore[arg-type]
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
                        (self._user_id or self._async_oauth_token_manager)
                        and not self._401_has_retried.get()
                        and response.status_code
                        == ErrorCode.AUTHENTICATION_PASSTHROUGH.http_error_code
                    ):
                        try:
                            LOGGER.debug("Starting async 401 automatic token refresh.")
                            return await self._handle_401_token_refresh(
                                api,
                                path,
                                params,
                                binary_data=binary_data,
                                download_file_path=download_file_path,
                                text_response=text_response,
                            )
                        except Exception as e:
                            LOGGER.debug(
                                "Async API call failed after a successful 401 "
                                "token refresh. Error details: %s",
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

    async def _handle_401_token_refresh(
        self,
        api,
        path,
        params,
        binary_data=None,
        download_file_path=None,
        text_response=False,
    ):
        if self._async_oauth_token_manager:
            await self._async_oauth_token_manager.invalidate_token()
            token = await self._async_oauth_token_manager.get_token()
            params["headers"]["authorization"] = f"Bearer {token}"
            self._401_has_retried.set(True)
            LOGGER.debug("Successfully refreshed async OAuth token after 401.")
            return await self._call_api_internal(
                api,
                path,
                params,
                binary_data=binary_data,
                download_file_path=download_file_path,
                text_response=text_response,
            )

        try:
            new_token = await self.impersonate.user(user_id=self._user_id)
        except Exception as e:
            LOGGER.debug(
                "Failed to impersonate user %s for async 401 token refresh. "
                "Not retrying. Error: %s",
                self._user_id,
                e,
            )
            raise
        self.api_key = new_token
        self._401_has_retried.set(True)
        params["headers"]["authorization"] = f"Bearer {self.api_key}"
        self._request_params["headers"]["authorization"] = f"Bearer {self.api_key}"
        LOGGER.debug("Successfully completed async 401 automatic token refresh.")

        retry_count = 1
        while retry_count <= self.retry.total:
            try:
                response = await self.typedef.get(
                    type_category=[AtlanTypeCategory.STRUCT]
                )
                if response and response.struct_defs:
                    break
            except Exception as e:
                LOGGER.debug(
                    "Retrying async to get typedefs (to ensure token is active) "
                    "after token refresh failed: %s",
                    e,
                )
            await asyncio.sleep(retry_count)
            retry_count += 1

        return await self._call_api_internal(
            api,
            path,
            params,
            binary_data=binary_data,
            download_file_path=download_file_path,
            text_response=text_response,
        )

    # ------------------------------------------------------------------
    # File upload / download helpers
    # ------------------------------------------------------------------

    async def _upload_file(self, api, file=None, filename=None):
        generator = MultipartDataGenerator()
        generator.add_file(file=file, filename=filename)
        post_data = generator.get_post_data()
        api.produces = f"multipart/form-data; boundary={generator.boundary}"
        path = self._create_path(api)
        params = await self._create_params(api, query_params=None, request_obj=None)
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return await self._call_api_internal(api, path, params, binary_data=post_data)

    async def _s3_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _azure_blob_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        params["headers"]["x-ms-blob-type"] = "BlockBlob"
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _gcs_presigned_url_file_upload(self, api: API, upload_file: Any):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _presigned_url_file_download(self, api: API, file_path: str):
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(
            api, path, params, download_file_path=file_path
        )

    # ------------------------------------------------------------------
    # High-level convenience methods
    # ------------------------------------------------------------------

    async def upload_image(self, file, filename: str) -> AtlanImage:
        """
        Uploads an image from the provided local file.

        :param file: local file to upload
        :param filename: name of the file to be uploaded
        :returns: details of the uploaded image
        :raises AtlanError: on any API communication issue
        """
        raw_json = await self._upload_file(UPLOAD_IMAGE, file=file, filename=filename)
        return msgspec.convert(raw_json, AtlanImage, strict=False)

    async def search(self, criteria):
        """Search assets. Delegates to asset.search()."""
        from warnings import warn

        warn(
            "This method is deprecated, please use 'asset.search' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.asset.search(criteria=criteria)

    async def parse_query(self, query: QueryParserRequest) -> Optional[ParsedQuery]:
        """
        Parses the provided query to describe its component parts.

        :param query: query to parse and configuration options
        :returns: parsed explanation of the query
        :raises AtlanError: on any API communication issue
        """
        raw_json = await self._call_api(
            PARSE_QUERY,
            request_obj=query,
        )
        return msgspec.convert(raw_json, ParsedQuery, strict=False)

    # ------------------------------------------------------------------
    # Retry context manager
    # ------------------------------------------------------------------

    @contextlib.asynccontextmanager  # type: ignore[arg-type]
    async def max_retries(
        self, max_retries: Retry = CONNECTION_RETRY
    ) -> _AsyncGeneratorContextManager[None]:  # type: ignore[misc]
        """
        Async context manager that temporarily changes retry parameters.

        The original Retry configuration is restored when the context exits.
        """
        current_transport = self._async_session._transport

        transport_kwargs: Dict[str, Any] = {}
        if self.proxy:
            transport_kwargs["proxy"] = self.proxy
        if self.verify is not None:
            transport_kwargs["verify"] = self.verify

        new_transport = PyatlanAsyncTransport(retry=max_retries, **transport_kwargs)
        self._async_session._transport = new_transport

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
            self._async_session._transport = current_transport
            LOGGER.debug(
                "max_retries restored %s",
                self._async_session._transport.retry,  # type: ignore[attr-defined]
            )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def aclose(self):
        """Close the async HTTP session and clean up resources."""
        if self._async_session:
            await self._async_session.aclose()
            self._async_session = None
        if self._async_oauth_token_manager:
            await self._async_oauth_token_manager.aclose()
            self._async_oauth_token_manager = None
        self._clients = {}
        self._caches = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()


@contextlib.asynccontextmanager
async def client_connection(
    client: AsyncAtlanClient,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    connect_timeout: float = 30.0,
    read_timeout: float = 120.0,
    retry: Retry = DEFAULT_RETRY,
) -> AsyncGenerator[AsyncAtlanClient, None]:
    """
    Creates a temporary async client with the given base_url and/or api_key.

    :param client: existing client to clone settings from
    :param base_url: the base_url for the new connection (uses current if not specified)
    :param api_key: the api_key for the new connection (uses current if not specified)
    """
    tmp_client = AsyncAtlanClient(
        base_url=base_url or client.base_url,
        api_key=api_key or client.api_key,
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
        retry=retry,
    )
    try:
        yield tmp_client
    finally:
        await tmp_client.aclose()
