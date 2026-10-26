# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""
Unit tests for v9 SSO identity provider methods — ported from
tests/unit/test_sso_identity_provider.py.
"""

from json import load
from pathlib import Path
from unittest.mock import Mock

import pytest

from pyatlan.client.common import ApiCaller
from pyatlan.errors import InvalidRequestError, NotFoundError
from pyatlan_v9.client.sso import V9SSOClient as SSOClient
from pyatlan_v9.model.sso import SSOProvider

TEST_DATA_DIR = Path(__file__).parent.parent.parent / "tests" / "unit" / "data"
SSO_RESPONSES_DIR = TEST_DATA_DIR / "sso_responses"
GET_ALL_IDPS_JSON = "get_all_identity_providers.json"

PEM_CERT = (
    "-----BEGIN CERTIFICATE-----\n"
    "TkVXQ0VS\nVA==\n"
    "-----END CERTIFICATE-----\n"
)  # body is base64("NEWCERT")


def load_json(filename):
    with (SSO_RESPONSES_DIR / filename).open() as input_file:
        return load(input_file)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def get_all_idps_json():
    return load_json(GET_ALL_IDPS_JSON)


class TestGetIdentityProviders:
    def test_get_all(self, mock_api_caller, get_all_idps_json):
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        providers = client.get_all_identity_providers()
        assert len(providers) == 1
        assert isinstance(providers[0], SSOProvider)
        assert providers[0].alias == "okta"
        assert providers[0].provider_id == "saml"
        assert providers[0].config["signingCertificate"] == "MIIDOLDCERTAAAA"

    def test_get_all_empty(self, mock_api_caller):
        mock_api_caller._call_api.return_value = []
        client = SSOClient(mock_api_caller)
        assert client.get_all_identity_providers() == []

    def test_get_by_alias_not_found(self, mock_api_caller, get_all_idps_json):
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        with pytest.raises(NotFoundError):
            client.get_identity_provider("azure")


class TestUpdateIdentityProvider:
    def test_config_keys_survive_round_trip(self, mock_api_caller, get_all_idps_json):
        """Regression guard (SHA-497 / BLDX-634): every `config` key returned
        by the API — including keys this SDK version does not know about —
        must be present in the serialized update payload.

        Note: msgspec drops unknown TOP-LEVEL fields (unlike the pydantic
        model, which uses Extra.allow); this is a known limitation pinned
        in the model docstring."""
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        provider = client.get_identity_provider("okta")
        payload = provider.to_dict()
        source = get_all_idps_json[0]
        for key in source["config"]:
            assert key in payload["config"], f"config key dropped: {key}"
        assert payload["config"]["someFutureConfigKey"] == "also-must-survive"

    def test_update_requires_alias(self, mock_api_caller):
        client = SSOClient(mock_api_caller)
        provider = SSOProvider(config={"signingCertificate": "MIIDOLDCERTAAAA"})
        with pytest.raises(InvalidRequestError):
            client.update_identity_provider(provider=provider)

    def test_update_posts_to_alias_path_and_refetches(
        self, mock_api_caller, get_all_idps_json
    ):
        mock_api_caller._call_api.side_effect = [
            get_all_idps_json,
            None,
            get_all_idps_json,
        ]
        client = SSOClient(mock_api_caller)
        provider = client.get_identity_provider("okta")
        result = client.update_identity_provider(provider=provider)
        assert result.alias == "okta"
        update_call = mock_api_caller._call_api.call_args_list[1]
        endpoint = update_call.args[0]
        assert "idp/okta" in endpoint.path

    def test_update_signing_certificate_normalizes_and_preserves_config(
        self, mock_api_caller, get_all_idps_json
    ):
        mock_api_caller._call_api.side_effect = [
            get_all_idps_json,
            None,
            get_all_idps_json,
        ]
        client = SSOClient(mock_api_caller)
        client.update_signing_certificate(sso_alias="okta", certificate=PEM_CERT)
        update_call = mock_api_caller._call_api.call_args_list[1]
        sent = update_call.kwargs.get("request_obj") or update_call.args[1]
        assert sent.config["signingCertificate"] == "TkVXQ0VSVA=="
        assert sent.config["someFutureConfigKey"] == "also-must-survive"
