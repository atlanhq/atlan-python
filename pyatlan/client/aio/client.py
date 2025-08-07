"""
Async Atlan Client
==================

Main async client that provides the same API as AtlanClient but with async/await support.
"""

from __future__ import annotations

import json
from typing import Optional

import httpx
from pydantic.v1 import PrivateAttr

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
from pyatlan.client.aio.admin import AsyncAdminClient
from pyatlan.client.aio.asset import AsyncAssetClient
from pyatlan.client.aio.audit import AsyncAuditClient
from pyatlan.client.aio.contract import AsyncContractClient
from pyatlan.client.aio.credential import AsyncCredentialClient
from pyatlan.client.aio.file import AsyncFileClient
from pyatlan.client.aio.group import AsyncGroupClient
from pyatlan.client.aio.impersonate import AsyncImpersonationClient
from pyatlan.client.aio.open_lineage import AsyncOpenLineageClient
from pyatlan.client.aio.query import AsyncQueryClient
from pyatlan.client.aio.role import AsyncRoleClient
from pyatlan.client.aio.search_log import AsyncSearchLogClient
from pyatlan.client.aio.sso import AsyncSSOClient
from pyatlan.client.aio.task import AsyncTaskClient
from pyatlan.client.aio.token import AsyncTokenClient
from pyatlan.client.aio.typedef import AsyncTypeDefClient
from pyatlan.client.aio.user import AsyncUserClient
from pyatlan.client.aio.workflow import AsyncWorkflowClient
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.constants import EVENT_STREAM
from pyatlan.errors import ErrorCode


class AsyncAtlanClient(AtlanClient):
    """
    Async Atlan client with the same API as sync AtlanClient.

    This client reuses all existing sync business logic while providing
    async/await support for all operations.

    Usage:
        # Same API as sync, just add await
        async_client = AsyncAtlanClient()
        results = await async_client.asset.search(criteria)  # vs sync: client.asset.search(criteria)

        # Or with context manager
        async with AsyncAtlanClient() as client:
            results = await client.asset.search(criteria)
    """

    _async_session: Optional[httpx.AsyncClient] = PrivateAttr(default=None)
    _async_admin_client: Optional[AsyncAdminClient] = PrivateAttr(default=None)
    _async_asset_client: Optional[AsyncAssetClient] = PrivateAttr(default=None)
    _async_audit_client: Optional[AsyncAuditClient] = PrivateAttr(default=None)
    _async_contract_client: Optional[AsyncContractClient] = PrivateAttr(default=None)
    _async_credential_client: Optional[AsyncCredentialClient] = PrivateAttr(
        default=None
    )
    _async_file_client: Optional[AsyncFileClient] = PrivateAttr(default=None)
    _async_group_client: Optional[AsyncGroupClient] = PrivateAttr(default=None)
    _async_impersonate_client: Optional[AsyncImpersonationClient] = PrivateAttr(
        default=None
    )
    _async_open_lineage_client: Optional[AsyncOpenLineageClient] = PrivateAttr(
        default=None
    )
    _async_query_client: Optional[AsyncQueryClient] = PrivateAttr(default=None)
    _async_role_client: Optional[AsyncRoleClient] = PrivateAttr(default=None)
    _async_search_log_client: Optional[AsyncSearchLogClient] = PrivateAttr(default=None)
    _async_sso_client: Optional[AsyncSSOClient] = PrivateAttr(default=None)
    _async_task_client: Optional[AsyncTaskClient] = PrivateAttr(default=None)
    _async_token_client: Optional[AsyncTokenClient] = PrivateAttr(default=None)
    _async_typedef_client: Optional[AsyncTypeDefClient] = PrivateAttr(default=None)
    _async_user_client: Optional[AsyncUserClient] = PrivateAttr(default=None)
    _async_workflow_client: Optional[AsyncWorkflowClient] = PrivateAttr(default=None)

    # Async cache instances
    _async_atlan_tag_cache: Optional[AsyncAtlanTagCache] = PrivateAttr(default=None)
    _async_connection_cache: Optional[AsyncConnectionCache] = PrivateAttr(default=None)
    _async_custom_metadata_cache: Optional[AsyncCustomMetadataCache] = PrivateAttr(
        default=None
    )
    _async_dq_template_config_cache: Optional[AsyncDQTemplateConfigCache] = PrivateAttr(
        default=None
    )
    _async_enum_cache: Optional[AsyncEnumCache] = PrivateAttr(default=None)
    _async_group_cache: Optional[AsyncGroupCache] = PrivateAttr(default=None)
    _async_role_cache: Optional[AsyncRoleCache] = PrivateAttr(default=None)
    _async_source_tag_cache: Optional[AsyncSourceTagCache] = PrivateAttr(default=None)
    _async_user_cache: Optional[AsyncUserCache] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        # Initialize sync client (handles all validation, env vars, etc.)
        super().__init__(**kwargs)

    @property
    def admin(self) -> AsyncAdminClient:
        """Get async admin client with same API as sync"""
        if self._async_admin_client is None:
            self._async_admin_client = AsyncAdminClient(self)
        return self._async_admin_client

    @property
    def asset(self) -> AsyncAssetClient:
        """Get async asset client with same API as sync"""
        if self._async_asset_client is None:
            self._async_asset_client = AsyncAssetClient(self)
        return self._async_asset_client

    @property
    def audit(self) -> AsyncAuditClient:
        """Get async audit client with same API as sync"""
        if self._async_audit_client is None:
            self._async_audit_client = AsyncAuditClient(self)
        return self._async_audit_client

    @property
    def contracts(self) -> AsyncContractClient:
        """Get async contract client with same API as sync"""
        if self._async_contract_client is None:
            self._async_contract_client = AsyncContractClient(self)
        return self._async_contract_client

    @property
    def credentials(self) -> AsyncCredentialClient:
        """Get async credential client with same API as sync"""
        if self._async_credential_client is None:
            self._async_credential_client = AsyncCredentialClient(self)
        return self._async_credential_client

    @property
    def files(self) -> AsyncFileClient:
        """Get async file client with same API as sync"""
        if self._async_file_client is None:
            self._async_file_client = AsyncFileClient(self)
        return self._async_file_client

    @property
    def group(self) -> AsyncGroupClient:
        """Get async group client with same API as sync"""
        if self._async_group_client is None:
            self._async_group_client = AsyncGroupClient(self)
        return self._async_group_client

    @property
    def impersonate(self) -> AsyncImpersonationClient:
        """Get async impersonate client with same API as sync"""
        if self._async_impersonate_client is None:
            self._async_impersonate_client = AsyncImpersonationClient(self)
        return self._async_impersonate_client

    @property
    def open_lineage(self) -> AsyncOpenLineageClient:
        """Get async open lineage client with same API as sync"""
        if self._async_open_lineage_client is None:
            self._async_open_lineage_client = AsyncOpenLineageClient(self)
        return self._async_open_lineage_client

    @property
    def queries(self) -> AsyncQueryClient:
        """Get async query client with same API as sync"""
        if self._async_query_client is None:
            self._async_query_client = AsyncQueryClient(self)
        return self._async_query_client

    @property
    def role(self) -> AsyncRoleClient:
        """Get async role client with same API as sync"""
        if self._async_role_client is None:
            self._async_role_client = AsyncRoleClient(self)
        return self._async_role_client

    @property
    def search_log(self) -> AsyncSearchLogClient:
        """Get async search log client with same API as sync"""
        if self._async_search_log_client is None:
            self._async_search_log_client = AsyncSearchLogClient(self)
        return self._async_search_log_client

    @property
    def sso(self) -> AsyncSSOClient:
        """Get async SSO client with same API as sync"""
        if self._async_sso_client is None:
            self._async_sso_client = AsyncSSOClient(self)
        return self._async_sso_client

    @property
    def tasks(self) -> AsyncTaskClient:
        """Get the task client."""
        if self._async_task_client is None:
            self._async_task_client = AsyncTaskClient(client=self)
        return self._async_task_client

    @property
    def token(self) -> AsyncTokenClient:
        """Get async token client with same API as sync"""
        if self._async_token_client is None:
            self._async_token_client = AsyncTokenClient(self)
        return self._async_token_client

    @property
    def typedef(self) -> AsyncTypeDefClient:
        """Get async typedef client with same API as sync"""
        if self._async_typedef_client is None:
            self._async_typedef_client = AsyncTypeDefClient(self)
        return self._async_typedef_client

    @property
    def user(self) -> AsyncUserClient:
        """Get async user client with same API as sync"""
        if self._async_user_client is None:
            self._async_user_client = AsyncUserClient(self)
        return self._async_user_client

    @property
    def workflow(self) -> AsyncWorkflowClient:
        """Get async workflow client with same API as sync"""
        if self._async_workflow_client is None:
            self._async_workflow_client = AsyncWorkflowClient(self)
        return self._async_workflow_client

    @property
    def atlan_tag_cache(self) -> AsyncAtlanTagCache:
        """Get async Atlan tag cache with same API as sync"""
        if self._async_atlan_tag_cache is None:
            self._async_atlan_tag_cache = AsyncAtlanTagCache(client=self)
        return self._async_atlan_tag_cache

    @property
    def connection_cache(self) -> AsyncConnectionCache:
        """Get async connection cache with same API as sync"""
        if self._async_connection_cache is None:
            self._async_connection_cache = AsyncConnectionCache(client=self)
        return self._async_connection_cache

    @property
    def custom_metadata_cache(self) -> AsyncCustomMetadataCache:
        """Get async custom metadata cache with same API as sync"""
        if self._async_custom_metadata_cache is None:
            self._async_custom_metadata_cache = AsyncCustomMetadataCache(client=self)
        return self._async_custom_metadata_cache

    @property
    def dq_template_config_cache(self) -> AsyncDQTemplateConfigCache:
        """Get async DQ template config cache with same API as sync"""
        if self._async_dq_template_config_cache is None:
            self._async_dq_template_config_cache = AsyncDQTemplateConfigCache(
                client=self
            )
        return self._async_dq_template_config_cache

    @property
    def enum_cache(self) -> AsyncEnumCache:
        """Get async enum cache with same API as sync"""
        if self._async_enum_cache is None:
            self._async_enum_cache = AsyncEnumCache(client=self)
        return self._async_enum_cache

    @property
    def group_cache(self) -> AsyncGroupCache:
        """Get async group cache with same API as sync"""
        if self._async_group_cache is None:
            self._async_group_cache = AsyncGroupCache(client=self)
        return self._async_group_cache

    @property
    def role_cache(self) -> AsyncRoleCache:
        """Get async role cache with same API as sync"""
        if self._async_role_cache is None:
            self._async_role_cache = AsyncRoleCache(client=self)
        return self._async_role_cache

    @property
    def source_tag_cache(self) -> AsyncSourceTagCache:
        """Get async source tag cache with same API as sync"""
        if self._async_source_tag_cache is None:
            self._async_source_tag_cache = AsyncSourceTagCache(client=self)
        return self._async_source_tag_cache

    @property
    def user_cache(self) -> AsyncUserCache:
        """Get async user cache with same API as sync"""
        if self._async_user_cache is None:
            self._async_user_cache = AsyncUserCache(client=self)
        return self._async_user_cache

    def _get_async_session(self) -> httpx.AsyncClient:
        """Get or create async HTTP session"""
        if self._async_session is None:
            self._async_session = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers={"authorization": f"Bearer {self.api_key}"},
                base_url=str(self.base_url),
            )
        return self._async_session

    async def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset=True
    ):
        """
        Async version of _call_api that reuses sync client's logic.

        Pattern for reuse:
        1. Use sync client to prepare request (same validation, serialization)
        2. Make async HTTP call (streaming for EVENT_STREAM APIs)
        3. Return processed response for sync client's response processing
        """
        # Step 1: Reuse sync client's request preparation
        path = self._create_path(api)
        params = self._create_params(api, query_params, request_obj, exclude_unset)

        # Step 2: Make async HTTP call
        session = self._get_async_session()

        # Handle EVENT_STREAM APIs differently (like streaming queries)
        if api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
            return await self._call_event_stream_api(session, api, path, params)
        else:
            # Standard API call
            response = await session.request(
                api.method.value,
                path,
                **{k: v for k, v in params.items() if k != "headers"},
                headers={**session.headers, **params.get("headers", {})},
                timeout=httpx.Timeout(self.read_timeout),
            )
            response.raise_for_status()

            # Step 3: Return JSON for sync client's response processing
            return response.json()

    async def _call_event_stream_api(self, session, api, path, params):
        """
        Handle EVENT_STREAM APIs with async streaming.

        :param session: async HTTP session
        :param api: API definition with EVENT_STREAM consumes/produces
        :param path: API path
        :param params: request parameters
        :returns: list of parsed events from the stream
        """
        async with session.stream(
            api.method.value,
            path,
            **{k: v for k, v in params.items() if k != "headers"},
            headers={**session.headers, **params.get("headers", {})},
            timeout=httpx.Timeout(self.read_timeout),
        ) as response:
            response.raise_for_status()

            # Read stream content and parse event lines
            content = await response.aread()
            text = content.decode("utf-8") if content else ""
            lines = text.splitlines() if text else []

            # Process event stream lines (similar to sync client)
            events = []
            for line in lines:
                if not line:
                    continue
                if not line.startswith("data: "):
                    raise ErrorCode.UNABLE_TO_DESERIALIZE.exception_with_parameters(
                        line
                    )
                events.append(json.loads(line.split("data: ")[1]))

            return events

    async def _s3_presigned_url_file_upload(self, api, upload_file):
        """Async version of S3 presigned URL file upload"""
        # For presigned URLs, we make direct HTTP calls (not through Atlan)
        async with httpx.AsyncClient() as client:
            response = await client.put(
                api,  # api is the formatted presigned URL string
                data=upload_file,
                timeout=httpx.Timeout(self.read_timeout),
            )
            response.raise_for_status()
            return response

    async def _azure_blob_presigned_url_file_upload(self, api, upload_file):
        """Async version of Azure Blob presigned URL file upload"""
        # For presigned URLs, we make direct HTTP calls (not through Atlan)
        headers = {"x-ms-blob-type": "BlockBlob"}
        async with httpx.AsyncClient() as client:
            response = await client.put(
                api,  # api is the formatted presigned URL string
                data=upload_file,
                headers=headers,
                timeout=httpx.Timeout(self.read_timeout),
            )
            response.raise_for_status()
            return response

    async def _gcs_presigned_url_file_upload(self, api, upload_file):
        """Async version of GCS presigned URL file upload"""
        # For presigned URLs, we make direct HTTP calls (not through Atlan)
        async with httpx.AsyncClient() as client:
            response = await client.put(
                api,  # api is the formatted presigned URL string
                data=upload_file,
                timeout=httpx.Timeout(self.read_timeout),
            )
            response.raise_for_status()
            return response

    async def _presigned_url_file_download(self, api, file_path: str):
        """Async version of presigned URL file download"""
        # For presigned URLs, we make direct HTTP calls (not through Atlan)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                api,  # api is the formatted presigned URL string
                timeout=httpx.Timeout(self.read_timeout),
            )
            response.raise_for_status()

            # Handle file download async
            try:
                with open(file_path, "wb") as download_file:
                    async for chunk in response.aiter_bytes():
                        download_file.write(chunk)
            except Exception as err:
                raise ErrorCode.UNABLE_TO_DOWNLOAD_FILE.exception_with_parameters(
                    str((hasattr(err, "strerror") and err.strerror) or err), file_path
                )
            return file_path

    async def aclose(self):
        """Close async resources"""
        if self._async_session:
            await self._async_session.aclose()
            self._async_session = None
        if self._async_asset_client:
            self._async_asset_client = None
        if self._async_file_client:
            self._async_file_client = None
        if self._async_group_client:
            self._async_group_client = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
