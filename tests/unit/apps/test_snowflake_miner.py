# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import SnowflakeMiner, SnowflakeMinerInputs


def test_snowflake_miner_inputs_defaults():
    i = SnowflakeMinerInputs()
    assert SnowflakeMinerInputs._APP_ID == "snowflake-miner"
    assert SnowflakeMinerInputs._ENTRYPOINT == "miner"
    assert i.snowflake_database == "default"
    assert i.database_name == "SNOWFLAKE"
    assert i.schema_name == "ACCOUNT_USAGE"
    assert i.miner_start_time_epoch == 0
    assert i.control_config_strategy == "default"
    assert i.control_config == ""
    assert i.preflight_check == ""
    assert i.calculate_popularity is True
    assert i.popularity_window_days == 30
    assert i.popularity_exclude_user_config == []


def test_snowflake_miner_builder_payload():
    out = (
        SnowflakeMiner(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "snowflake"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["extract_strategy"] == "miner"
    assert out["native_lineage_active"] is False
    assert out["indirect_lineage"] == "false"
    assert out["ignore_orphans"] == "false"
    assert out["enable_sharded"] == "false"
    assert out["enable_parent_job_scoping"] == "false"
    assert out["enable_fallback_match"] == "true"
    assert out["include_indirect_column_relations"] == "false"
    assert out["process_routines"] == "true"
