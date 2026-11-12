# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from json import load, loads
from pathlib import Path
from unittest.mock import Mock

import pytest

from pyatlan.client.common import ApiCaller, normalize_signing_certificate
from pyatlan.client.sso import SSOClient
from pyatlan.errors import InvalidRequestError, NotFoundError
from pyatlan.model.sso import SSOProvider

TEST_DATA_DIR = Path(__file__).parent / "data"
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


class TestNormalizeSigningCertificate:
    def test_pem_input_becomes_single_line(self):
        assert normalize_signing_certificate(PEM_CERT) == "TkVXQ0VSVA=="

    def test_raw_single_line_unchanged(self):
        assert normalize_signing_certificate("TkVXQ0VSVA==") == "TkVXQ0VSVA=="

    def test_crlf_and_blank_lines_stripped(self):
        cert = "\r\nTkVXQ0VS\r\nVA==\r\n\r\n"
        assert normalize_signing_certificate(cert) == "TkVXQ0VSVA=="

    def test_internal_whitespace_stripped(self):
        assert normalize_signing_certificate("TkVXQ0VS \tVA==") == "TkVXQ0VSVA=="

    def test_multi_cert_bundle_rejected(self):
        """IdP federation metadata often bundles the expiring cert AND its
        replacement; silently concatenating them would write an invalid
        certificate into the tenant's SSO config during an outage."""
        two = PEM_CERT + PEM_CERT
        with pytest.raises(
            InvalidRequestError, match="found 2 certificates, expected 1"
        ):
            normalize_signing_certificate(two)

    def test_non_base64_rejected(self):
        with pytest.raises(InvalidRequestError, match="not base64"):
            normalize_signing_certificate("not a certificate at all!!!")

    def test_empty_input_rejected(self):
        with pytest.raises(InvalidRequestError, match="no certificate content between"):
            normalize_signing_certificate(
                "-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----"
            )


class TestGetIdentityProviders:
    def test_get_all(self, mock_api_caller, get_all_idps_json):
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        providers = client.get_all_identity_providers()
        assert len(providers) == 1
        assert providers[0].alias == "okta"
        assert providers[0].provider_id == "saml"
        assert providers[0].config["signingCertificate"] == "MIIDOLDCERTAAAA"

    def test_get_all_empty(self, mock_api_caller):
        mock_api_caller._call_api.return_value = []
        client = SSOClient(mock_api_caller)
        assert client.get_all_identity_providers() == []

    def test_get_by_alias(self, mock_api_caller, get_all_idps_json):
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        provider = client.get_identity_provider("okta")
        assert provider.alias == "okta"

    def test_get_by_alias_not_found(self, mock_api_caller, get_all_idps_json):
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        with pytest.raises(NotFoundError):
            client.get_identity_provider("azure")


class TestUpdateIdentityProvider:
    def test_full_object_round_trip_preserves_all_fields(
        self, mock_api_caller, get_all_idps_json
    ):
        """Regression guard for the partial-update trap (SHA-497 / BLDX-634):
        every field returned by the API — including ones this SDK version
        does not know about — must be present in the update payload."""
        mock_api_caller._call_api.return_value = get_all_idps_json
        client = SSOClient(mock_api_caller)
        provider = client.get_identity_provider("okta")

        payload = loads(provider.json(by_alias=True, exclude_none=True))
        source = get_all_idps_json[0]
        for key in source["config"]:
            assert key in payload["config"], f"config key dropped: {key}"
        assert payload["config"]["someFutureConfigKey"] == "also-must-survive"
        # top-level unknown fields must also survive (Extra.allow), and the
        # internal extras holder must never leak into the payload
        assert payload["futureUnknownField"] == "must-survive-round-trip"
        assert "__atlan_extra__" not in payload

    def test_update_requires_alias(self, mock_api_caller):
        client = SSOClient(mock_api_caller)
        provider = SSOProvider(config={"signingCertificate": "MIIDOLDCERTAAAA"})
        with pytest.raises(InvalidRequestError):
            client.update_identity_provider(provider=provider)

    def test_update_posts_to_alias_path_and_refetches(
        self, mock_api_caller, get_all_idps_json
    ):
        # first call: GET (for get_identity_provider); second: POST update;
        # third: GET (re-read after update)
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
        endpoint = (
            update_call.args[0] if update_call.args else update_call.kwargs["api"]
        )
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
        # every other config key untouched
        assert sent.config["singleSignOnServiceUrl"] == (
            "https://example.okta.com/app/x/sso/saml"
        )
        assert sent.config["someFutureConfigKey"] == "also-must-survive"
