# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from pyatlan.client.common import ApiCaller, FileDownload, FilePresignedUrl, FileUpload
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.file import PresignedURLRequest
from pyatlan_v9.validate import validate_arguments


class V9FileClient:
    """
    A client for operating on Atlan's tenant object storage.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def generate_presigned_url(self, request: PresignedURLRequest) -> str:
        """
        Generates a presigned URL based on Atlan's tenant object store.

        :param request: instance containing object key,
        expiry, and method (PUT: upload, GET: download).
        :raises AtlanError: on any error during API invocation.
        :returns: a response object containing a presigned URL with its cloud provider.
        """
        endpoint, request_obj = FilePresignedUrl.prepare_request(request)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return FilePresignedUrl.process_response(raw_json)

    @validate_arguments
    def upload_file(self, presigned_url: str, file_path: str) -> None:
        """
        Uploads a file to Atlan's object storage.

        :param presigned_url: any valid presigned URL.
        :param file_path: path to the file to be uploaded.
        :raises AtlanError: on any error during API invocation.
        :raises InvalidRequestException: if the upload file path is invalid,
        or when the presigned URL cloud provider is unsupported.
        """
        upload_file = FileUpload.validate_file_path(file_path)
        provider = FileUpload.identify_cloud_provider(presigned_url)
        if provider == "s3":
            endpoint = FileUpload.prepare_s3_request(presigned_url)
            return self._client._s3_presigned_url_file_upload(
                upload_file=upload_file, api=endpoint
            )
        elif provider == "azure_blob":
            endpoint = FileUpload.prepare_azure_request(presigned_url)
            return self._client._azure_blob_presigned_url_file_upload(
                upload_file=upload_file, api=endpoint
            )
        elif provider == "gcs":
            endpoint = FileUpload.prepare_gcs_request(presigned_url)
            return self._client._gcs_presigned_url_file_upload(
                upload_file=upload_file, api=endpoint
            )

    @validate_arguments
    def download_file(
        self,
        presigned_url: str,
        file_path: str,
    ) -> str:
        """
        Downloads a file from Atlan's tenant object storage.

        :param presigned_url: any valid presigned URL.
        :param file_path: path to the file where you want to download the file.
        :raises InvalidRequestException: if unable to download the file.
        :raises AtlanError: on any error during API invocation.
        :returns: full path to the downloaded file.
        """
        endpoint = FileDownload.prepare_request(presigned_url)
        return self._client._presigned_url_file_download(
            file_path=file_path, api=endpoint
        )
