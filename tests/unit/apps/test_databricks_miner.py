# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import DatabricksMiner, DatabricksMinerInputs


def test_databricks_miner_inputs_defaults():
    i = DatabricksMinerInputs()
    assert DatabricksMinerInputs._APP_ID == "databricks-miner"
    assert DatabricksMinerInputs._ENTRYPOINT == "miner"
    assert i.extract_strategy == "system-table"
    assert i.extraction_catalog_type_lineage == "system-table"
    assert i.cloned_catalog_name_lineage == "system"
    assert i.cloned_schema_name_lineage == "access"
    assert i.sql_warehouse == ""
    assert i.path_level_lineage == "false"
    assert i.calculate_popularity == "false"
    assert i.extraction_catalog_type_popularity == "system-table"
    assert i.cloned_catalog_name_popularity == "system"
    assert i.cloned_schema_name_popularity == "query"
    assert i.popularity_window_days == 30
    assert i.popularity_exclude_user_config == []
    assert i.miner_start_time_epoch == 0
    assert i.sql_warehouse_popularity == ""


def test_databricks_miner_builder_payload():
    out = (
        DatabricksMiner(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "databricks"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["miner_lookback_days"] == 30
    assert out["miner_chunk_interval_hours"] == 0
    assert out["miner_max_concurrent_activities"] == 20
    assert out["miner_wave_size"] == 50
    assert out["miner_wave_concurrency"] == 10
    assert out["preflight_context"] == "miner"
