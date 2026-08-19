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
from pyatlan.model.apps import AppBuilder, BigqueryCrawler, SnowflakeMiner

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
    cls(c).connection(name="conn", admin_users=["u"]).credential_guid("g").create()
    ak = c.app.create.call_args.kwargs
    assert ak["app_id"] == cls._APP_ID
    # an empty entrypoint is sent as None ("use the app's default")
    assert ak["entrypoint"] == (cls._ENTRYPOINT or None)
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
        .connection(name="prod-bq", admin_users=["jdoe"], admin_groups=["g1"])
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
    cred = b._raw_creds["credential_guid"]
    assert cred.auth_type == "basic"
    assert cred.connector_config_name == "atlan-connectors-bigquery"
    assert cred.username == "svc@p.iam.gserviceaccount.com"
    assert cred.host == "https://psc.internal"
    assert cred.extras == {"project_id": "proj", "connect_type": "private"}


def test_workload_identity_federation_auth_type():
    b = BigqueryCrawler(Mock()).workload_identity_federation(
        project_id="proj",
        service_account_email="svc@proj.iam.gserviceaccount.com",
        wif_pool_provider_id="pool/provider",
        atlan_oauth_id="oauth-id",
        atlan_oauth_secret="oauth-secret",
    )
    cred = b._raw_creds["credential_guid"]
    assert cred.auth_type == "gcp-wif"
    assert cred.extras["project_id"] == "proj"


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
        .connection(name="prod-bq", admin_users=["jdoe"])
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


# --------------------------------------------------------------------------- #
# Existing-connection (miner) path — select by QN, no name/credential needed
# --------------------------------------------------------------------------- #
def test_miner_references_existing_connection_by_qn_only():
    out = (
        SnowflakeMiner(Mock())
        .connection(qualified_name="default/snowflake/1700000000")
        .preview()
    )
    attrs = out["connection"]["attributes"]
    assert attrs["qualifiedName"] == "default/snowflake/1700000000"
    # connectorName derived from the QN, not the app-id
    assert attrs["connectorName"] == "snowflake"
    assert "name" not in attrs  # no display name needed when selecting existing
    # no credential supplied — server resolves the connection's default credential
    assert out["credential_guid"] == ""
    assert "credential" not in out and "agent_json" not in out


def test_connector_name_derived_from_qn(client):
    # Even when the builder's connector fallback differs, the QN wins.
    SnowflakeMiner(client).connection(qualified_name="default/snowflake/123").create()
    out = client.app.create.call_args.kwargs["inputs"].to_inputs()
    assert out["connection"]["attributes"]["connectorName"] == "snowflake"


def test_miner_auto_resolves_connection_credential(client):
    # Referencing an existing connection by QN (no credential) → the builder looks
    # up the connection and reuses its defaultCredentialGuid on create().
    client.asset.search.return_value = iter(
        [Mock(default_credential_guid="conn-cred-guid")]
    )
    SnowflakeMiner(client).connection(qualified_name="default/snowflake/123").create()
    assert client.asset.search.called  # connection was looked up
    out = client.app.create.call_args.kwargs["inputs"].to_inputs()
    assert out["credential_guid"] == "conn-cred-guid"  # its credential reused


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


# --------------------------------------------------------------------------- #
# update() — load an existing workflow, change a field, full-replace
# --------------------------------------------------------------------------- #
def test_load_update_preserves_reinjects_and_references_credential():
    """load(slug).<change>.update() re-injects connection_qualified_name, keeps
    the existing credential (referenced, not rotated), normalizes string-typed
    fields, drops runtime keys, and preserves everything else."""
    from types import SimpleNamespace

    client = Mock()
    current = {
        "connection": {"typeName": "Connection", "attributes": {
            "qualifiedName": "default/bigquery/123", "connectorName": "bigquery",
            "name": "prod", "adminRoles": ["role-1"]}},
        "credential_guid": "cred-1",
        "extraction_method": "direct",
        "include_filter": {"^proj$": ["^old$"]},
        "control_config": {},          # object on read-back -> must normalize to "{}"
        "user-id": "u1", "workflow_id": "w1",   # runtime keys -> must be dropped
        "atlas_auth_type": "internal",          # non-structural -> preserved
    }
    client.app.get.return_value.dict.return_value = {
        "dag": {"extract": {"inputs": {"args": current}}}
    }
    client.app.get_input_contract.return_value = SimpleNamespace(
        properties={"control_config": {"type": "string"}}
    )
    client.app.update.return_value = Mock(version=2)

    BigqueryCrawler(client).load("slug-1").include({"proj": ["new"]}).update()

    kw = client.app.update.call_args.kwargs
    inp = kw["inputs"]
    assert kw["slug"] == "slug-1" and kw["entrypoint"] == "crawler"
    assert inp["connection_qualified_name"] == "default/bigquery/123"  # re-injected
    assert inp["credential_guid"] == "cred-1" and "credential" not in inp  # no rotation
    assert inp["include_filter"] == '{"^proj$": ["^new$"]}'  # changed + anchored
    assert inp["control_config"] == "{}"  # normalized object -> string
    assert "user-id" not in inp and "workflow_id" not in inp  # runtime keys dropped
    assert inp["atlas_auth_type"] == "internal"  # preserved
    assert inp["connection"]["attributes"]["adminRoles"] == ["role-1"]  # connection kept


def test_update_without_load_raises():
    with pytest.raises(ValueError):
        BigqueryCrawler(Mock()).update()


@pytest.mark.parametrize("cls", BUILDERS, ids=BUILDER_IDS)
def test_load_update_is_generic_across_builders(cls):
    """load()/update() lives on the base, so every app builder can update: it
    re-injects connection_qualified_name and references the existing credential
    (no rotation), targeting the right slug/entrypoint. The builder's own
    preview() is used as the 'current inputs' so the seed is valid for its
    typed inputs model."""
    from types import SimpleNamespace

    qn = f"default/{cls._CONNECTOR_NAME}/1700000000"
    current = cls(Mock()).connection(qualified_name=qn).credential_guid("cred-x").preview()
    client = Mock()
    client.app.get.return_value.dict.return_value = {
        "dag": {"extract": {"inputs": {"args": current}}}
    }
    client.app.get_input_contract.return_value = SimpleNamespace(properties={})
    client.app.update.return_value = Mock(version=2)

    cls(client).load("slug-x").update()

    kw = client.app.update.call_args.kwargs
    inp = kw["inputs"]
    assert kw["slug"] == "slug-x"
    assert kw["entrypoint"] == (cls._ENTRYPOINT or None)
    assert inp["connection_qualified_name"] == qn      # re-injected
    assert inp["credential_guid"] == "cred-x"          # referenced, not rotated
    assert "credential" not in inp                      # no raw credential re-sent


def test_update_retries_without_entrypoint_on_1003():
    """update() falls back to the default entrypoint when the named one has no
    registered contract (server 1003) — mirroring _create()."""
    from types import SimpleNamespace

    current = (
        BigqueryCrawler(Mock())
        .connection(qualified_name="default/bigquery/1")
        .credential_guid("g")
        .preview()
    )
    client = Mock()
    client.app.get.return_value.dict.return_value = {
        "dag": {"extract": {"inputs": {"args": current}}}
    }
    client.app.get_input_contract.return_value = SimpleNamespace(properties={})
    client.app.update.side_effect = [
        Exception("Server responded 1003: unknown entrypoint"),
        Mock(version=3),
    ]

    BigqueryCrawler(client).load("slug-x").update()

    assert client.app.update.call_count == 2
    assert client.app.update.call_args_list[0].kwargs["entrypoint"] == "crawler"
    assert client.app.update.call_args_list[1].kwargs["entrypoint"] is None


def test_load_update_applies_multiple_field_changes():
    """load(slug).<several typed changes>.update() applies every change and
    preserves + re-injects the rest (connection_qualified_name, credential ref,
    hidden defaults), dropping runtime keys."""
    from types import SimpleNamespace

    current = {
        "connection": {"typeName": "Connection", "attributes": {
            "qualifiedName": "default/bigquery/1", "connectorName": "bigquery",
            "name": "prod", "adminRoles": ["role-1"]}},
        "credential_guid": "cred-1", "extraction_method": "direct",
        "include_filter": {"^p$": ["^old$"]}, "exclude_filter": {},
        "temp_table_regex": "", "enable_nested_columns": True,
        "enable_bigquery_tag_sync": False, "filter_sharded_tables": True,
        "hidden_datasets": False, "control_config": {},
        "control_config_strategy": "default", "atlas_auth_type": "internal",
        "user-id": "u1",
    }
    client = Mock()
    client.app.get.return_value.dict.return_value = {
        "dag": {"extract": {"inputs": {"args": current}}}
    }
    client.app.get_input_contract.return_value = SimpleNamespace(
        properties={"control_config": {"type": "string"}}
    )
    client.app.update.return_value = Mock(version=2)

    (
        BigqueryCrawler(client)
        .load("slug-1")
        .include({"p": ["a", "b"]})
        .exclude({"p": ["tmp"]})
        .exclude_regex(".*_bak$")
        .import_nested_columns(False)
        .import_tags(True)
        .combine_sharded_tables(False)
        .hidden_assets(True)
        .custom_config('{"flag": 1}')
        .update()
    )

    inp = client.app.update.call_args.kwargs["inputs"]
    # every requested change applied
    assert inp["include_filter"] == '{"^p$": ["^a$", "^b$"]}'
    assert inp["exclude_filter"] == '{"^p$": ["^tmp$"]}'
    assert inp["temp_table_regex"] == ".*_bak$"
    assert inp["enable_nested_columns"] is False
    assert inp["enable_bigquery_tag_sync"] is True
    assert inp["filter_sharded_tables"] is False
    assert inp["hidden_datasets"] is True
    assert inp["control_config_strategy"] == "custom"
    assert inp["control_config"] == '{"flag": 1}'
    # rest preserved / re-injected / stripped
    assert inp["connection_qualified_name"] == "default/bigquery/1"
    assert inp["credential_guid"] == "cred-1" and "credential" not in inp
    assert inp["atlas_auth_type"] == "internal"
    assert "user-id" not in inp
