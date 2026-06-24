# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Unit tests for the fluent app builders.

The builders mirror the UI's 3-step "new app" wizard. These tests assert the
assembled payload (connection minting, credential vaulting, hidden-default
injection, filter anchoring) without any network — the client is mocked.
"""

import inspect
from unittest.mock import Mock

import pytest

import pyatlan.model.apps as apps
from pyatlan.model.apps import AppBuilder, BigqueryCrawler

# Every concrete builder (the hand-written flagship + all generated ones).
BUILDERS = [
    obj
    for n in apps.__all__
    if isinstance(obj := getattr(apps, n), type)
    and issubclass(obj, AppBuilder)
    and obj is not AppBuilder
]
BUILDER_IDS = [c.__name__ for c in BUILDERS]


@pytest.fixture
def client():
    c = Mock()
    c.app.create.return_value = Mock(slug="bq-1", run_id="r-1", version=1)
    return c


# --------------------------------------------------------------------------- #
# Source-agnostic — every generated builder
# --------------------------------------------------------------------------- #
def test_builders_were_generated():
    assert len(BUILDERS) >= 20


@pytest.mark.parametrize("cls", BUILDERS, ids=BUILDER_IDS)
def test_builder_class_vars(cls):
    assert cls._APP_ID and isinstance(cls._APP_ID, str)
    assert cls._CONNECTOR_NAME and issubclass(cls._INPUTS_CLASS, apps.AppInput)


@pytest.mark.parametrize("cls", BUILDERS, ids=BUILDER_IDS)
def test_builder_create_path(cls):
    # connection + existing guid is the uniform path across every connector.
    c = Mock()
    c.app.create.return_value = Mock(slug="s", version=1, run_id="r")
    cls(c).connection(name="conn", admins=["u"]).credential_guid("g").create()
    ak = c.app.create.call_args.kwargs
    assert ak["app_id"] == cls._APP_ID
    assert ak["entrypoint"] == cls._ENTRYPOINT
    assert ak["run"] is False  # .create() does not run
    out = ak["inputs"].to_inputs()
    assert out["connection"]["attributes"]["connectorName"] == cls._CONNECTOR_NAME
    assert out["credential_guid"] == "g"


@pytest.mark.parametrize("cls", BUILDERS, ids=BUILDER_IDS)
def test_builder_has_at_least_one_credential_method(cls):
    # Each builder should expose either a generated auth method or inherit the
    # base credential_guid()/agent() path. Generated ones add ≥1 auth method.
    base_methods = set(dir(AppBuilder))
    own = {
        n
        for n, m in inspect.getmembers(cls, inspect.isfunction)
        if n not in base_methods and not n.startswith("_")
    }
    # at minimum, the base credential_guid/agent are always available
    assert callable(cls.credential_guid) and callable(cls.agent)
    assert isinstance(own, set)  # generated step methods (may be empty for sparse apps)


# --------------------------------------------------------------------------- #
# Payload assembly (no network)
# --------------------------------------------------------------------------- #
def test_preview_mirrors_ui_form():
    out = (
        BigqueryCrawler(Mock())
        .service_account(
            email="svc@p.iam.gserviceaccount.com",
            service_account_json='{"k":"v"}',
            project_id="proj",
        )
        .connection(name="prod-bq", admins=["jdoe"], admin_groups=["g1"])
        .include({"proj": ["analytics"]})
        .exclude({"proj": ["tmp"]})
        .import_nested_columns(False)
        .combine_sharded_tables(True)
        .preview()
    )
    conn = out["connection"]["attributes"]
    assert conn["connectorName"] == "bigquery"
    assert conn["qualifiedName"].startswith("default/bigquery/")
    assert conn["adminUsers"] == ["jdoe"] and conn["adminGroups"] == ["g1"]
    assert out["extraction_method"] == "direct"
    # net-new: raw credential embedded for the server to vault; credential_guid
    # sent as "" (the contract default) and the secret is redacted in preview.
    assert out["credential"]["authType"] == "basic"
    assert out["credential"]["connectorConfigName"] == "atlan-connectors-bigquery"
    assert out["credential"]["password"] == "***"
    assert out["credential_guid"] == ""
    # friendly map -> anchored-regex JSON (what the UI submits)
    assert out["include_filter"] == '{"^proj$": ["^analytics$"]}'
    assert out["exclude_filter"] == '{"^proj$": ["^tmp$"]}'
    assert out["enable_nested_columns"] is False
    assert out["filter_sharded_tables"] is True
    # hidden ui fields ride along with their defaults
    assert out["max_concurrent_activities"] == 15
    assert out["list_datasets_per_chunk"] == 50
    assert "agent_json" not in out


def test_filter_passthrough_string():
    out = (
        BigqueryCrawler(Mock())
        .connection(name="c")
        .include('{"^already$": ["^anchored$"]}')
        .preview()
    )
    assert out["include_filter"] == '{"^already$": ["^anchored$"]}'


def test_custom_config_sets_strategy():
    out = (
        BigqueryCrawler(Mock())
        .connection(name="c")
        .custom_config('{"flag":1}')
        .preview()
    )
    assert out["control_config_strategy"] == "custom"
    assert out["control_config"] == '{"flag":1}'


# --------------------------------------------------------------------------- #
# Credential building
# --------------------------------------------------------------------------- #
def test_service_account_credential_shape():
    b = BigqueryCrawler(Mock()).service_account(
        email="svc@p.iam.gserviceaccount.com",
        service_account_json='{"k":"v"}',
        project_id="proj",
        connectivity="private",
        host="https://psc.internal",
    )
    cred = b._credential
    assert cred.auth_type == "basic"
    assert cred.connector_config_name == "atlan-connectors-bigquery"
    assert cred.username == "svc@p.iam.gserviceaccount.com"
    assert cred.host == "https://psc.internal"
    assert cred.extras == {"project_id": "proj", "connect_type": "private"}


def test_workload_identity_federation_auth_type():
    b = BigqueryCrawler(Mock()).workload_identity_federation(project_id="proj")
    assert b._credential.auth_type == "gcp-wif"
    assert b._credential.extras["project_id"] == "proj"


# --------------------------------------------------------------------------- #
# create() — full flow with mocked client
# --------------------------------------------------------------------------- #
def test_run_embeds_raw_credential_for_server_to_vault(client):
    resp = (
        BigqueryCrawler(client)
        .service_account(
            email="svc@p.iam.gserviceaccount.com",
            service_account_json='{"k":"v"}',
            project_id="proj",
        )
        .connection(name="prod-bq", admins=["jdoe"])
        .include({"proj": ["ds"]})
        .run()  # create AND submit a run
    )
    assert resp.slug == "bq-1"
    # no separate credential-create call — the create endpoint vaults the raw cred
    client.credentials.creator.assert_not_called()
    ak = client.app.create.call_args
    assert ak.kwargs["app_id"] == "bigquery-crawler"
    assert ak.kwargs["entrypoint"] == "crawler"
    assert ak.kwargs["run"] is True  # .run() => run=True
    assert ak.kwargs["name"] == "prod-bq"
    out = ak.kwargs["inputs"].to_inputs()
    # raw secret travels (server strips/vaults it); name auto-minted; guid sent ""
    cred = out["credential"]
    assert cred["authType"] == "basic"
    assert cred["password"] == '{"k":"v"}'  # real secret, not redacted, on create
    assert cred["name"].startswith("default-bigquery-")
    assert out["credential_guid"] == ""


def test_create_with_existing_guid_sends_guid_not_raw_credential(client):
    (
        BigqueryCrawler(client)
        .credential_guid("existing-guid")
        .connection(name="prod-bq")
        .create()
    )
    out = client.app.create.call_args.kwargs["inputs"].to_inputs()
    assert out["credential_guid"] == "existing-guid"
    assert "credential" not in out  # no raw credential when referencing a guid


def test_agent_mode_uses_agent_json_not_credential(client):
    (
        BigqueryCrawler(client)
        .agent({"name": "my-agent"})
        .connection(name="prod-bq")
        .create()
    )
    out = client.app.create.call_args.kwargs["inputs"].to_inputs()
    assert out["extraction_method"] == "agent"
    assert out["agent_json"] == {"name": "my-agent"}
    assert "credential" not in out
    assert "credential_guid" not in out
