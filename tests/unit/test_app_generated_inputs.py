# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Unit tests for the generated typed app-input classes (BLDX-1472).

Source-agnostic: auto-discovers every generated ``*Inputs`` class from
``pyatlan.model.app_inputs`` and exercises the contract they all must honour, so
the suite stays valid as the generated set (and its source) changes. A few
per-app spot checks anchor known contract defaults.
"""

import inspect
from unittest.mock import Mock

import pytest

import pyatlan.model.app_inputs as app_inputs
from pyatlan.client.app import AppClient
from pyatlan.client.common import ApiCaller
from pyatlan.model.app_inputs import (
    AppInput,
    BigqueryCrawlerInputs,
    DatabricksCrawlerInputs,
    OracleCrawlerInputs,
    PostgresCrawlerInputs,
)

GENERATED = [getattr(app_inputs, n) for n in app_inputs.__all__ if n != "AppInput"]
IDS = [c.__name__ for c in GENERATED]

# Internal/infra fields the generator denylists — must NOT leak into any class.
_INTERNALS = {
    "output_dir",
    "checkpoint_dir",
    "output_prefix",
    "output_path",
    "load_to_atlan",
    "publish_dry_run",
    "atlas_auth_type",
    "max_concurrent_activities",
    "max_activities_per_execution",
    "user-id",
    "user_id",
    "workflow_id",
    "correlation_id",
}


# --------------------------------------------------------------------------- #
# Structural integrity — every generated class
# --------------------------------------------------------------------------- #
def test_some_classes_were_generated():
    assert len(GENERATED) >= 10


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_is_app_input_subclass(cls):
    assert issubclass(cls, AppInput) and cls is not AppInput


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_has_app_id_classvar(cls):
    assert isinstance(cls._APP_ID, str) and cls._APP_ID
    assert cls._ENTRYPOINT is None or isinstance(cls._ENTRYPOINT, str)


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_instantiates_with_defaults_and_serializes(cls):
    # Every field is optional or defaulted, so no-arg construction must work.
    assert isinstance(cls().to_inputs(), dict)


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_no_internal_fields_leak(cls):
    leaked = _INTERNALS & set(cls.__fields__)
    assert not leaked, f"{cls.__name__} leaks internal fields: {leaked}"


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_module_is_marked_generated(cls):
    assert "AUTO-GENERATED" in inspect.getsource(inspect.getmodule(cls))


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_extra_fields_tolerated(cls):
    # Forward-compatible: a field newer than the snapshot must not raise.
    assert cls(some_brand_new_field_xyz=123).to_inputs()["some_brand_new_field_xyz"] == 123


@pytest.mark.parametrize("cls", GENERATED, ids=IDS)
def test_create_accepts_generated_inputs(cls):
    api = Mock(spec=ApiCaller)
    api._call_api.return_value = {"slug": "s-1", "version": 1}
    resp = AppClient(api).create(
        app_id=cls._APP_ID, entrypoint=cls._ENTRYPOINT, name="prod", inputs=cls(), run=False
    )
    assert resp.slug == "s-1"
    assert isinstance(api._call_api.call_args.kwargs["request_obj"].inputs, dict)


# --------------------------------------------------------------------------- #
# Serialization semantics
# --------------------------------------------------------------------------- #
def test_override_default_and_drop_none():
    out = BigqueryCrawlerInputs(
        connection={"typeName": "Connection", "attributes": {}},
        enable_nested_columns=False,  # override (default True)
    ).to_inputs()
    assert out["enable_nested_columns"] is False  # override honored
    assert out["list_datasets_per_chunk"] == 50  # untouched default carried
    assert "agent_json" not in out  # unset optional dropped


# --------------------------------------------------------------------------- #
# Per-app default spot checks
# --------------------------------------------------------------------------- #
def test_bigquery_crawler_defaults():
    i = BigqueryCrawlerInputs()
    assert i.enable_nested_columns is True
    assert i.filter_sharded_tables is True
    assert i.list_datasets_per_chunk == 50
    assert BigqueryCrawlerInputs._APP_ID == "bigquery-crawler"
    assert BigqueryCrawlerInputs._ENTRYPOINT == "crawler"


def test_databricks_crawler_defaults():
    assert DatabricksCrawlerInputs().extract_strategy == "system-tables"
    assert DatabricksCrawlerInputs._APP_ID == "databricks-crawler"


def test_oracle_and_postgres_app_ids():
    assert OracleCrawlerInputs._APP_ID == "oracle-crawler"
    assert PostgresCrawlerInputs._APP_ID == "postgres-crawler"
