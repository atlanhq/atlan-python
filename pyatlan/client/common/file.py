# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import os
from pathlib import Path
from typing import Any

# System directories that must never be read from.
_SENSITIVE_SYSTEM_PREFIXES = (
    "/etc/",
    "/proc/",
    "/sys/",
    "/dev/",
    "/root/",
    "/private/etc/",  # macOS: /etc is a symlink to /private/etc
    "/private/var/",  # macOS
)

# Hidden credential/config directories that must never be read from.
_SENSITIVE_DIR_NAMES = frozenset({".aws", ".ssh", ".gnupg"})

# File name prefixes for environment/secret files.
_SENSITIVE_FILE_PREFIXES = (".env",)


def _parse_env_list(env_var: str) -> list:
    val = os.environ.get(env_var, "")
    return [p.strip() for p in val.split(",") if p.strip()] if val else []

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
        :raises INVALID_UPLOAD_FILE_PATH_TRAVERSAL: if path traversal is detected
        :raises INVALID_UPLOAD_FILE_PATH_SENSITIVE: if path points to a sensitive location
        :raises INVALID_UPLOAD_FILE_PATH: if file not found
        """
        path = Path(file_path)

        # Block directory traversal via '..'
        if ".." in path.parts:
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH_TRAVERSAL.exception_with_parameters(
                file_path
            )

        resolved = path.resolve()
        resolved_str = str(resolved)

        # Block sensitive system directories (e.g. /etc/, /proc/, /dev/)
        if resolved_str.startswith(_SENSITIVE_SYSTEM_PREFIXES):
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH_SENSITIVE.exception_with_parameters(
                file_path
            )

        # Block credential/config hidden directories (e.g. .aws, .ssh, .gnupg)
        if any(part in _SENSITIVE_DIR_NAMES for part in resolved.parts):
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH_SENSITIVE.exception_with_parameters(
                file_path
            )

        # Block environment/secret files (e.g. .env, .env.local, .env.production)
        if resolved.name.startswith(_SENSITIVE_FILE_PREFIXES):
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH_SENSITIVE.exception_with_parameters(
                file_path
            )

        # Block user-defined paths via PYATLAN_UPLOAD_FILE_BLOCKED_PATHS (comma-separated).
        # Each entry is matched as a substring against the full resolved path, so it
        # can express system prefixes ("/vault/"), dir names (".vault"), or
        # file prefixes (".credentials").
        # e.g. PYATLAN_UPLOAD_FILE_BLOCKED_PATHS="/custom/secrets/,.vault,.credentials"
        user_blocked = _parse_env_list("PYATLAN_UPLOAD_FILE_BLOCKED_PATHS")
        if any(pattern in resolved_str for pattern in user_blocked):
            raise ErrorCode.INVALID_UPLOAD_FILE_PATH_SENSITIVE.exception_with_parameters(
                file_path
            )

        try:
            return open(resolved, "rb")
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
