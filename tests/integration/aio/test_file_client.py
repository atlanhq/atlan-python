# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

import imghdr  # type: ignore[import-not-found]
import os
from pathlib import Path

import pytest
import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.file import PresignedURLRequest
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncFileClient")

URL_EXPIRY = "300s"  # 5 minutes instead of 10 seconds
FILE_NAME = "sdk.png"
DOWNLOAD_FILE_NAME = "sdk-download.png"
TENANT_S3_BUCKET_DIRECTORY = "presigned-url-sdk-integration-tests"
S3_UPLOAD_FILE_PATH = f"{TENANT_S3_BUCKET_DIRECTORY}/{FILE_NAME}"


TEST_DATA_DIR = Path(__file__).parent.parent / "data"
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
async def test_file_client_download_file_raises_invalid_request_error(
    client, file_path, expected_error
):
    with pytest.raises(InvalidRequestError, match=expected_error):
        await client.files.download_file(
            presigned_url="test-url",
            file_path=file_path,
        )


@pytest_asyncio.fixture(scope="module")
async def s3_put_presigned_url(client: AsyncAtlanClient) -> str:
    # Presigned URL for upload
    return await client.files.generate_presigned_url(
        request=PresignedURLRequest(
            key=S3_UPLOAD_FILE_PATH,
            expiry=URL_EXPIRY,
            method=PresignedURLRequest.Method.PUT,
        )
    )


@pytest_asyncio.fixture(scope="module")
async def s3_get_presigned_url(client: AsyncAtlanClient) -> str:
    # Presigned URL for download
    return await client.files.generate_presigned_url(
        request=PresignedURLRequest(
            key=S3_UPLOAD_FILE_PATH,
            expiry=URL_EXPIRY,
            method=PresignedURLRequest.Method.GET,
        )
    )


async def test_file_client_presigned_url_upload(
    client: AsyncAtlanClient, s3_put_presigned_url: str
):
    assert s3_put_presigned_url
    assert os.path.exists(UPLOAD_FILE_PATH)

    await client.files.upload_file(
        presigned_url=s3_put_presigned_url, file_path=UPLOAD_FILE_PATH
    )


async def test_file_client_presigned_url_download(
    client: AsyncAtlanClient, s3_get_presigned_url: str
):
    assert s3_get_presigned_url
    assert not os.path.exists(DOWNLOAD_FILE_PATH)

    await client.files.download_file(
        presigned_url=s3_get_presigned_url, file_path=DOWNLOAD_FILE_PATH
    )
    assert os.path.exists(DOWNLOAD_FILE_PATH)
    assert imghdr.what(DOWNLOAD_FILE_PATH) == "png"
    os.remove(DOWNLOAD_FILE_PATH)
