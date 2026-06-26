# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import BigqueryMiner, BigqueryMinerInputs


def test_bigquery_miner_inputs_defaults():
    i = BigqueryMinerInputs()
    assert BigqueryMinerInputs._APP_ID == "bigquery-miner"
    assert BigqueryMinerInputs._ENTRYPOINT == "miner"
    assert i.miner_start_time_epoch == 0
    assert i.region_strategy == "default"
    assert i.region == "region-us"
    assert i.fetch_all_projects_query_history is False
    assert i.calculate_popularity == "true"
    assert i.pricing_model == "on-demand"
    assert i.popularity_window_days == 30
    assert i.popularity_exclude_user_config == []
    assert i.control_config_strategy == "default"
    assert i.control_config == "{}"


def test_bigquery_miner_builder_payload():
    out = (
        BigqueryMiner(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "bigquery"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "query_history"
    assert out["chunk_interval_hours"] == 0
    assert out["enable_continue_as_new"] is False
    assert out["max_concurrent_activities"] == 50
    assert out["max_activities_per_execution"] == 300
    assert out["schedule_to_start_timeout_secs"] == 10800
    assert out["sql_pandas_batch_size"] == 6000
