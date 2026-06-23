# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Unit tests for AppInputsBuilder (BLDX-1472).

Two layers, mirroring the old ``test_packages`` approach (assert the exact built
payload per app) but generically:
  1. Builder mechanics (helpers + contract validation + build).
  2. Per-app config assertions across connectors and both credential modes
     (direct/vaulted and agent/SDR), proving the generic builder produces the
     correct ``inputs`` for each app.
"""

import json

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.model.app import AppInputContract, AppInputsBuilder


def _contract(*fields: str, required=None) -> AppInputContract:
    """Fabricate an input contract with the given field names."""
    return AppInputContract.parse_obj(
        {
            "title": "AppInputContract",
            "type": "object",
            "properties": {f: {} for f in fields},
            "required": list(required or []),
        }
    )


def _connection(qn: str, connector: str):
    return {
        "typeName": "Connection",
        "attributes": {"qualifiedName": qn, "connectorName": connector},
    }


# --------------------------------------------------------------------------- #
# Builder mechanics
# --------------------------------------------------------------------------- #
def test_connection_helper_shape():
    out = (
        AppInputsBuilder()
        .connection(
            qualified_name="default/snowflake/1",
            connector_name="snowflake",
            name="prod",
            admin_users=["jane"],
            admin_roles=["r1"],
            admin_groups=["g1"],
            default_credential_guid="cred-1",
            allowQuery=True,
        )
        .build()
    )
    assert out["connection"] == {
        "typeName": "Connection",
        "attributes": {
            "qualifiedName": "default/snowflake/1",
            "connectorName": "snowflake",
            "name": "prod",
            "adminUsers": ["jane"],
            "adminRoles": ["r1"],
            "adminGroups": ["g1"],
            "defaultCredentialGuid": "cred-1",
            "allowQuery": True,
        },
    }


def test_direct_credential_guid_and_raw():
    out = AppInputsBuilder().direct_credential(guid="cred-123").build()
    assert out == {"credential_guid": "cred-123"}

    raw = {"authType": "basic", "name": "c", "extra": {"u": "x"}}
    out = AppInputsBuilder().direct_credential(credential=raw).build()
    assert out == {"credential": raw}


def test_agent_sdr_maps_to_hyphenated_keys():
    out = (
        AppInputsBuilder()
        .agent(
            agent_name="ora-agent",
            agent_type="sql",
            auth_type="basic",
            host="db.internal",
            port=1521,
            connect_by="SID",
            secret_manager="vault",
            secret_path="kv/ora",
            **{"oracle.user": "ref-user"},
        )
        .build()
    )
    assert out["agent_json"] == {
        "agent-name": "ora-agent",
        "agent-type": "sql",
        "auth-type": "basic",
        "connectBy": "SID",
        "secret-manager": "vault",
        "secret-path": "kv/ora",
        "host": "db.internal",
        "port": 1521,
        "oracle.user": "ref-user",
    }


def test_filters_accept_dict_and_str():
    out = AppInputsBuilder().filters(include={"SCHEMA": {}}, exclude="{}").build()
    assert out["include_filter"] == json.dumps({"SCHEMA": {}})
    assert out["exclude_filter"] == "{}"


def test_set_validates_unknown_field_with_suggestion():
    builder = AppInputsBuilder(_contract("system_schema_name"), app_id="oracle-crawler")
    with pytest.raises(InvalidRequestError) as exc:
        builder.set("system_schema_nam", "SYS")  # typo
    msg = str(exc.value)
    assert "system_schema_nam" in msg and "system_schema_name" in msg  # suggestion


def test_update_validates_all_keys():
    builder = AppInputsBuilder(_contract("a", "b"), app_id="x")
    builder.update({"a": 1, "b": 2})
    assert builder.build() == {"a": 1, "b": 2}
    with pytest.raises(InvalidRequestError):
        AppInputsBuilder(_contract("a"), app_id="x").update({"zzz": 1})


def test_build_enforces_required():
    builder = AppInputsBuilder(
        _contract("connection", required=["connection"]), app_id="x"
    )
    with pytest.raises(InvalidRequestError) as exc:
        builder.build()
    assert "connection" in str(exc.value)


def test_no_contract_skips_validation():
    out = AppInputsBuilder().set("anything", 1).set("else", 2).build()
    assert out == {"anything": 1, "else": 2}


# --------------------------------------------------------------------------- #
# Per-app config assertions (direct + SDR), mirroring test_packages
# --------------------------------------------------------------------------- #
def test_bigquery_crawler_direct():
    contract = _contract(
        "connection",
        "credential_guid",
        "include_filter",
        "exclude_filter",
        "enable_nested_columns",
        "filter_sharded_tables",
        required=["connection"],
    )
    out = (
        AppInputsBuilder(contract, app_id="bigquery-crawler", entrypoint="crawler")
        .connection(qualified_name="default/bigquery/1", connector_name="bigquery")
        .direct_credential(guid="cred-1")
        .filters(include={}, exclude={})
        .set("enable_nested_columns", True)
        .set("filter_sharded_tables", True)
        .build()
    )
    assert out == {
        "connection": _connection("default/bigquery/1", "bigquery"),
        "credential_guid": "cred-1",
        "include_filter": "{}",
        "exclude_filter": "{}",
        "enable_nested_columns": True,
        "filter_sharded_tables": True,
    }


def test_bigquery_miner_config():
    contract = _contract(
        "connection",
        "calculate_popularity",
        "pricing_model",
        "popularity_window_days",
    )
    out = (
        AppInputsBuilder(contract, app_id="bigquery-miner", entrypoint="miner")
        .connection(qualified_name="default/bigquery/1", connector_name="bigquery")
        .set("calculate_popularity", True)
        .set("pricing_model", "on_demand")
        .set("popularity_window_days", 30)
        .build()
    )
    assert out == {
        "connection": _connection("default/bigquery/1", "bigquery"),
        "calculate_popularity": True,
        "pricing_model": "on_demand",
        "popularity_window_days": 30,
    }


def test_oracle_crawler_sdr():
    """Oracle crawler via agent/SDR (no central credential)."""
    contract = _contract(
        "connection",
        "agent_json",
        "include_filter",
        "exclude_filter",
        "extraction_method",
        "system_schema_name",
        "preflight_check",
    )
    out = (
        AppInputsBuilder(contract, app_id="oracle-crawler", entrypoint="crawler")
        .connection(qualified_name="default/oracle/1", connector_name="oracle")
        .agent(agent_name="ora-agent", secret_manager="vault", secret_path="kv/ora")
        .filters(include={}, exclude={})
        .set("extraction_method", "direct")
        .set("system_schema_name", "SYS")
        .set("preflight_check", True)
        .build()
    )
    assert out == {
        "connection": _connection("default/oracle/1", "oracle"),
        "agent_json": {
            "agent-name": "ora-agent",
            "secret-manager": "vault",
            "secret-path": "kv/ora",
        },
        "include_filter": "{}",
        "exclude_filter": "{}",
        "extraction_method": "direct",
        "system_schema_name": "SYS",
        "preflight_check": True,
    }


def test_snowflake_crawler_direct():
    contract = _contract(
        "connection",
        "credential_guid",
        "include_filter",
        "exclude_filter",
        "extraction_method",
    )
    out = (
        AppInputsBuilder(contract, app_id="snowflake-crawler", entrypoint="crawler")
        .connection(qualified_name="default/snowflake/1", connector_name="snowflake")
        .direct_credential(guid="cred-sf")
        .filters(include={}, exclude={})
        .set("extraction_method", "direct")
        .build()
    )
    assert out == {
        "connection": _connection("default/snowflake/1", "snowflake"),
        "credential_guid": "cred-sf",
        "include_filter": "{}",
        "exclude_filter": "{}",
        "extraction_method": "direct",
    }


def test_postgres_crawler_config():
    contract = _contract(
        "connection",
        "credential_guid",
        "extraction_method",
        "use_jdbc_internal_methods",
        "use_source_schema_filtering",
    )
    out = (
        AppInputsBuilder(contract, app_id="postgres-crawler", entrypoint="crawler")
        .connection(qualified_name="default/postgres/1", connector_name="postgres")
        .direct_credential(guid="cred-pg")
        .set("extraction_method", "direct")
        .set("use_jdbc_internal_methods", True)
        .set("use_source_schema_filtering", False)
        .build()
    )
    assert out == {
        "connection": _connection("default/postgres/1", "postgres"),
        "credential_guid": "cred-pg",
        "extraction_method": "direct",
        "use_jdbc_internal_methods": True,
        "use_source_schema_filtering": False,
    }


def test_powerbi_crawler_config():
    contract = _contract(
        "connection",
        "credential_guid",
        "exclude_filter",
        "extraction_method",
        "incremental_extraction",
        "endorsement_attach_mode",
    )
    out = (
        AppInputsBuilder(contract, app_id="powerbi-crawler", entrypoint="crawler")
        .connection(qualified_name="default/powerbi/1", connector_name="powerbi")
        .direct_credential(guid="cred-pbi")
        .filters(exclude={})
        .set("extraction_method", "direct")
        .set("incremental_extraction", True)
        .set("endorsement_attach_mode", "metadata")
        .build()
    )
    assert out == {
        "connection": _connection("default/powerbi/1", "powerbi"),
        "credential_guid": "cred-pbi",
        "exclude_filter": "{}",
        "extraction_method": "direct",
        "incremental_extraction": True,
        "endorsement_attach_mode": "metadata",
    }


def test_mssql_crawler_direct():
    contract = _contract(
        "connection",
        "credential_guid",
        "extraction_method",
        "include_filter",
    )
    out = (
        AppInputsBuilder(contract, app_id="atlan-mssql", entrypoint="crawler")
        .connection(qualified_name="default/mssql/1", connector_name="mssql")
        .direct_credential(guid="cred-mssql")
        .filters(include={})
        .set("extraction_method", "direct")
        .build()
    )
    assert out == {
        "connection": _connection("default/mssql/1", "mssql"),
        "credential_guid": "cred-mssql",
        "extraction_method": "direct",
        "include_filter": "{}",
    }


def test_trino_crawler_sdr():
    contract = _contract(
        "connection",
        "agent_json",
        "include_filter",
        "exclude_filter",
        "extraction_method",
        "preflight_check",
    )
    out = (
        AppInputsBuilder(contract, app_id="atlan-trino", entrypoint="crawler")
        .connection(qualified_name="default/trino/1", connector_name="trino")
        .agent(
            agent_name="trino-agent",
            auth_type="basic",
            secret_manager="vault",
            secret_path="kv/trino",
        )
        .filters(include={}, exclude={})
        .set("extraction_method", "direct")
        .set("preflight_check", True)
        .build()
    )
    assert out == {
        "connection": _connection("default/trino/1", "trino"),
        "agent_json": {
            "agent-name": "trino-agent",
            "auth-type": "basic",
            "secret-manager": "vault",
            "secret-path": "kv/trino",
        },
        "include_filter": "{}",
        "exclude_filter": "{}",
        "extraction_method": "direct",
        "preflight_check": True,
    }
