# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Any

from pyatlan.client.constants import (
    API,
    PRESIGNED_URL,
    PRESIGNED_URL_DOWNLOAD,
    PRESIGNED_URL_UPLOAD_AZURE_BLOB,
    PRESIGNED_URL_UPLOAD_GCS,
    PRESIGNED_URL_UPLOAD_S3,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.file import CloudStorageIdentifier, PresignedURLRequest


class FilePresignedUrl:
    """
    Shared business logic for generating presigned URLs.
    """

    @staticmethod
    def prepare_request(
        request: PresignedURLRequest,
    ) -> tuple[API, PresignedURLRequest]:
        """
        Prepare the API request for generating a presigned URL.

        :param request: presigned URL request details
        :returns: tuple of (endpoint, request_obj)
        """
        return PRESIGNED_URL, request

    @staticmethod
    def process_response(raw_json: Any) -> str:
        """
        Process the response from presigned URL generation.

        :param raw_json: raw API response
        :returns: presigned URL string
        """
        return raw_json and raw_json.get("url", "")


class FileUpload:
    """
    Shared business logic for file upload operations.
    """

    @staticmethod
    def validate_file_path(file_path: str) -> Any:
        """
        Validate and open the file for upload.

        :param file_path: path to the file to upload
        :returns: opened file object
        :raises INVALID_UPLOAD_FILE_PATH: if file not found
        """
        try:
            return open(file_path, "rb")
        except FileNotFoundError as err:
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH.exception_with_parameters(
                str(err.strerror), file_path
            )

    @staticmethod
    def identify_cloud_provider(presigned_url: str) -> str:
        """
        Identify the cloud provider from the presigned URL.

        :param presigned_url: the presigned URL to analyze
        :returns: cloud provider identifier
        :raises UNSUPPORTED_PRESIGNED_URL: if provider not supported
        """
        if CloudStorageIdentifier.S3 in presigned_url:
            return "s3"
        elif CloudStorageIdentifier.AZURE_BLOB in presigned_url:
            return "azure_blob"
        elif CloudStorageIdentifier.GCS in presigned_url:
            return "gcs"
        else:
            raise ErrorCode.UNSUPPORTED_PRESIGNED_URL.exception_with_parameters()

    @staticmethod
    def prepare_s3_request(presigned_url: str) -> str:
        """
        Prepare S3 upload request.

        :param presigned_url: S3 presigned URL
        :returns: formatted API endpoint
        """
        return PRESIGNED_URL_UPLOAD_S3.format_path({"presigned_url_put": presigned_url})

    @staticmethod
    def prepare_azure_request(presigned_url: str) -> str:
        """
        Prepare Azure Blob upload request.

        :param presigned_url: Azure Blob presigned URL
        :returns: formatted API endpoint
        """
        return PRESIGNED_URL_UPLOAD_AZURE_BLOB.format_path(
            {"presigned_url_put": presigned_url}
        )

    @staticmethod
    def prepare_gcs_request(presigned_url: str) -> str:
        """
        Prepare GCS upload request.

        :param presigned_url: GCS presigned URL
        :returns: formatted API endpoint
        """
        return PRESIGNED_URL_UPLOAD_GCS.format_path(
            {"presigned_url_put": presigned_url}
        )


class FileDownload:
    """
    Shared business logic for file download operations.
    """

    @staticmethod
    def prepare_request(presigned_url: str) -> str:
        """
        Prepare the API request for downloading a file.

        :param presigned_url: presigned URL for download
        :returns: formatted API endpoint
        """
        return PRESIGNED_URL_DOWNLOAD.format_path({"presigned_url_get": presigned_url})
