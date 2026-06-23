# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Unit tests for generated typed app-input classes (BLDX-1472)."""

from unittest.mock import Mock

from pyatlan.client.app import AppClient
from pyatlan.client.common import ApiCaller
from pyatlan.model.app_inputs import (
    AppInput,
    BigqueryCrawlerInputs,
    BigqueryMinerInputs,
)


def test_generated_classes_are_app_inputs():
    assert issubclass(BigqueryCrawlerInputs, AppInput)
    assert BigqueryCrawlerInputs._APP_ID == "bigquery-crawler"
    assert BigqueryCrawlerInputs._ENTRYPOINT == "crawler"
    assert BigqueryMinerInputs._APP_ID == "bigquery-miner"


def test_to_inputs_carries_defaults_and_overrides():
    i = BigqueryCrawlerInputs(
        connection={"typeName": "Connection", "attributes": {}},
        credential_guid="cred-1",
        enable_nested_columns=False,  # override a default (default is True)
    )
    out = i.to_inputs()
    assert out["connection"] == {"typeName": "Connection", "attributes": {}}
    assert out["credential_guid"] == "cred-1"
    assert out["enable_nested_columns"] is False  # override honored
    assert out["list_datasets_per_chunk"] == 50  # contract default carried


def test_create_accepts_generated_inputs():
    api = Mock(spec=ApiCaller)
    api._call_api.return_value = {"slug": "bq-1", "version": 1}
    client = AppClient(api)
    resp = client.create(
        app_id="bigquery-crawler",
        entrypoint="crawler",
        name="prod",
        inputs=BigqueryCrawlerInputs(connection={"a": 1}, filter_sharded_tables=False),
        run=False,
    )
    assert resp.slug == "bq-1"
    sent = api._call_api.call_args.kwargs["request_obj"].inputs
    assert sent["connection"] == {"a": 1}
    assert sent["filter_sharded_tables"] is False
    assert sent["enable_nested_columns"] is True  # default carried
