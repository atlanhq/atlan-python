# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from contextlib import _AsyncGeneratorContextManager, _GeneratorContextManager
from typing import Any, Protocol, runtime_checkable

from httpx_retries import Retry

HTTPS_PREFIX = "https://"
HTTP_PREFIX = "http://"
CONNECTION_RETRY = Retry(
    total=10,
    backoff_factor=1,
    status_forcelist=[403],
    allowed_methods=["GET"],
)


@runtime_checkable
class ApiCaller(Protocol):
    def _call_api(
        self,
        api,
        query_params=None,
        request_obj=None,
        exclude_unset: bool = True,
        text_response: bool = False,
    ):
        pass

    def max_retries(
        self, max_retries: Retry = CONNECTION_RETRY
    ) -> _GeneratorContextManager[None]:
        pass

    def _s3_presigned_url_file_upload(self, api, upload_file: Any):
        pass

    def _azure_blob_presigned_url_file_upload(self, api, upload_file: Any):
        pass

    def _gcs_presigned_url_file_upload(self, api, upload_file: Any):
        pass

    def _presigned_url_file_download(self, api, file_path: str):
        pass


@runtime_checkable
class AsyncApiCaller(Protocol):
    async def _call_api(
        self,
        api,
        query_params=None,
        request_obj=None,
        exclude_unset: bool = True,
        text_response: bool = False,
    ) -> Any:
        pass

    async def max_retries(
        self, max_retries: Retry = CONNECTION_RETRY
    ) -> _AsyncGeneratorContextManager[None]:
        pass

    async def _s3_presigned_url_file_upload(self, api, upload_file: Any):
        pass

    async def _azure_blob_presigned_url_file_upload(self, api, upload_file: Any):
        pass

    async def _gcs_presigned_url_file_upload(self, api, upload_file: Any):
        pass

    async def _presigned_url_file_download(self, api, file_path: str):
        pass
