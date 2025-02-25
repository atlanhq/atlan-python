# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

import imghdr  # type: ignore[import-not-found]
import os
from pathlib import Path

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.file import PresignedURLRequest
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("TaskClient")

URL_EXPIRY = "10s"
FILE_NAME = "sdk.png"
DOWNLOAD_FILE_NAME = "sdk-download.png"
TENANT_S3_BUCKET_DIRECTORY = "presigned-url-sdk-integration-tests"
S3_UPLOAD_FILE_PATH = f"{TENANT_S3_BUCKET_DIRECTORY}/{FILE_NAME}"


TEST_DATA_DIR = Path(__file__).parent / "data"
UPLOAD_FILE_PATH = str(TEST_DATA_DIR / "file_requests" / FILE_NAME)
DOWNLOAD_FILE_PATH = str(TEST_DATA_DIR / "file_requests" / DOWNLOAD_FILE_NAME)


@pytest.mark.parametrize(
    "file_path, expected_error",
    [
        [
            "some/invalid/file_path.png",
            (
                "ATLAN-PYTHON-400-060 Unable to download file, "
                "Error: No such file or directory, Path: some/invalid/file_path.png"
            ),
        ],
    ],
)
def test_file_client_download_file_raises_invalid_request_error(
    client, file_path, expected_error
):
    with pytest.raises(InvalidRequestError, match=expected_error):
        client.files.download_file(
            presigned_url="test-url",
            file_path=file_path,
        )


@pytest.fixture(scope="module")
def s3_put_presigned_url(client: AtlanClient) -> str:
    # Presigned URL for upload
    return client.files.generate_presigned_url(
        request=PresignedURLRequest(
            key=S3_UPLOAD_FILE_PATH,
            expiry=URL_EXPIRY,
            method=PresignedURLRequest.Method.PUT,
        )
    )


@pytest.fixture(scope="module")
def s3_get_presigned_url(client: AtlanClient) -> str:
    # Presigned URL for download
    return client.files.generate_presigned_url(
        request=PresignedURLRequest(
            key=S3_UPLOAD_FILE_PATH,
            expiry=URL_EXPIRY,
            method=PresignedURLRequest.Method.GET,
        )
    )


def test_file_client_presigned_url_upload(
    client: AtlanClient, s3_put_presigned_url: str
):
    assert s3_put_presigned_url
    assert os.path.exists(UPLOAD_FILE_PATH)

    client.files.upload_file(
        presigned_url=s3_put_presigned_url, file_path=UPLOAD_FILE_PATH
    )


def test_file_client_presigned_url_download(
    client: AtlanClient, s3_get_presigned_url: str
):
    assert s3_get_presigned_url
    assert not os.path.exists(DOWNLOAD_FILE_PATH)

    client.files.download_file(
        presigned_url=s3_get_presigned_url, file_path=DOWNLOAD_FILE_PATH
    )
    assert os.path.exists(DOWNLOAD_FILE_PATH)
    assert imghdr.what(DOWNLOAD_FILE_PATH) == "png"
    os.remove(DOWNLOAD_FILE_PATH)
