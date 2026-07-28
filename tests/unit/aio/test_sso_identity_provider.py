# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from json import load
from pathlib import Path
from unittest.mock import Mock

import pytest

from pyatlan.client.aio.sso import AsyncSSOClient
from pyatlan.client.common import AsyncApiCaller
from pyatlan.errors import NotFoundError

TEST_DATA_DIR = Path(__file__).parent.parent / "data"
SSO_RESPONSES_DIR = TEST_DATA_DIR / "sso_responses"

PEM_CERT = (
    "-----BEGIN CERTIFICATE-----\n"
    "TkVXQ0VS\nVA==\n"
    "-----END CERTIFICATE-----\n"
)  # body is base64("NEWCERT")


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def mock_api_caller():
    return Mock(spec=AsyncApiCaller)


@pytest.fixture()
def get_all_idps_json():
    with (SSO_RESPONSES_DIR / "get_all_identity_providers.json").open() as f:
        return load(f)


async def test_get_all(mock_api_caller, get_all_idps_json):
    mock_api_caller._call_api.return_value = get_all_idps_json
    client = AsyncSSOClient(mock_api_caller)
    providers = await client.get_all_identity_providers()
    assert len(providers) == 1 and providers[0].alias == "okta"


async def test_get_by_alias_not_found(mock_api_caller, get_all_idps_json):
    mock_api_caller._call_api.return_value = get_all_idps_json
    client = AsyncSSOClient(mock_api_caller)
    with pytest.raises(NotFoundError):
        await client.get_identity_provider("azure")


async def test_update_signing_certificate_round_trip(
    mock_api_caller, get_all_idps_json
):
    mock_api_caller._call_api.side_effect = [
        get_all_idps_json,
        None,
        get_all_idps_json,
    ]
    client = AsyncSSOClient(mock_api_caller)
    await client.update_signing_certificate(sso_alias="okta", certificate=PEM_CERT)
    update_call = mock_api_caller._call_api.call_args_list[1]
    sent = update_call.kwargs.get("request_obj") or update_call.args[1]
    assert sent.config["signingCertificate"] == "TkVXQ0VSVA=="
    assert sent.config["someFutureConfigKey"] == "also-must-survive"
