# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
import os
from json import load
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.common import ApiCaller
from pyatlan.client.file import FileClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.file import PresignedURLRequest
from tests.unit.constants import TEST_FILE_CLIENT_METHODS

TEST_DATA_DIR = Path(__file__).parent / "data"
UPLOAD_FILE_PATH = str(TEST_DATA_DIR / "file_requests/upload.txt")
DOWNLOAD_FILE_PATH = str(TEST_DATA_DIR / "file_requests/download.txt")


def load_json(respones_dir, filename):
    with (respones_dir / filename).open() as input_file:
        return load(input_file)


def to_json(model):
    return model.json(by_alias=True, exclude_none=True)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture(scope="module")
def s3_presigned_url():
    return (
        "https://test-vcluster.amazonaws.com/some-directory/test.png"
        "?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240425T09240"
    )


@pytest.fixture()
def mock_session():
    with patch.object(AtlanClient, "_session") as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raw = open(UPLOAD_FILE_PATH, "rb")
        mock_session.request.return_value = mock_response
        yield mock_session
    assert os.path.exists(DOWNLOAD_FILE_PATH)
    os.remove(DOWNLOAD_FILE_PATH)


@pytest.fixture()
def mock_session_invalid():
    with patch.object(AtlanClient, "_session") as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raw = "not a bytes-like object"
        mock_session.request.return_value = mock_response
        yield mock_session
    assert os.path.exists(DOWNLOAD_FILE_PATH)
    os.remove(DOWNLOAD_FILE_PATH)


@pytest.mark.parametrize("method, params", TEST_FILE_CLIENT_METHODS.items())
def test_file_client_methods_validation_error(client, method, params):
    client_method = getattr(client.files, method)
    for param_values, error_msg in params:
        with pytest.raises(ValidationError, match=error_msg):
            client_method(*param_values)


@pytest.mark.parametrize(
    "file_path, expected_error",
    [
        [
            UPLOAD_FILE_PATH,
            (
                "ATLAN-PYTHON-400-061 Provided presigned URL's cloud provider "
                "storage is currently not supported for file uploads."
            ),
        ],
        [
            "some/invalid/file_path.png",
            (
                "ATLAN-PYTHON-400-059 Unable to upload file, "
                "Error: No such file or directory, Path: some/invalid/file_path.png"
            ),
        ],
    ],
)
def test_file_client_upload_file_raises_invalid_request_error(
    mock_api_caller, s3_presigned_url, file_path, expected_error
):
    client = FileClient(client=mock_api_caller)

    with pytest.raises(InvalidRequestError, match=expected_error):
        client.upload_file(
            presigned_url="test-url",
            file_path=file_path,
        )


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


def test_file_client_download_file_invalid_format_raises_invalid_request_error(
    client, s3_presigned_url, mock_session_invalid
):
    expected_error = (
        "ATLAN-PYTHON-400-060 Unable to download file, "
        f"Error: 'str' object has no attribute 'read', Path: {DOWNLOAD_FILE_PATH}"
    )
    with pytest.raises(InvalidRequestError, match=expected_error):
        client.files.download_file(
            presigned_url=s3_presigned_url, file_path=DOWNLOAD_FILE_PATH
        )


def test_file_client_get_presigned_url(mock_api_caller, s3_presigned_url):
    mock_api_caller._call_api.side_effect = [{"url": s3_presigned_url}]
    client = FileClient(mock_api_caller)
    response = client.generate_presigned_url(
        request=PresignedURLRequest(
            key="some-directory/test.png",
            expiry="60s",
            method=PresignedURLRequest.Method.GET,
        )
    )
    assert mock_api_caller._call_api.call_count == 1
    assert response == s3_presigned_url
    mock_api_caller.reset_mock()


@patch.object(AtlanClient, "_call_api_internal", return_value=None)
def test_file_client_upload_file(mock_call_api_internal, client, s3_presigned_url):
    client = FileClient(client=client)
    client.upload_file(presigned_url=s3_presigned_url, file_path=UPLOAD_FILE_PATH)

    assert mock_call_api_internal.call_count == 1
    mock_call_api_internal.reset_mock()


def test_file_client_download_file(client, s3_presigned_url, mock_session):
    # Make sure the download file doesn't exist before downloading
    assert not os.path.exists(DOWNLOAD_FILE_PATH)
    response = client.files.download_file(
        presigned_url=s3_presigned_url, file_path=DOWNLOAD_FILE_PATH
    )
    assert response == DOWNLOAD_FILE_PATH
    assert mock_session.request.call_count == 1
    # The file should exist after calling the method
    assert os.path.exists(DOWNLOAD_FILE_PATH)
    assert open(DOWNLOAD_FILE_PATH, "r").read() == "test data 12345.\n"
