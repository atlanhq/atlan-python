# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
Unit tests for event models using v9 types for assertions.

Ported from tests/unit/test_events.py. The legacy AtlanEvent is used for
deserialization (Pydantic handles the discriminated union + Asset type), while
v9 event payload types are used for isinstance checks via _is_model_instance.
"""

from json import load, loads
from pathlib import Path

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.events.atlan_event_handler import is_validation_request, valid_signature
from pyatlan.validate import _is_model_instance

# Legacy AtlanEvent for deserialization (handles discriminated union)
from pyatlan.model.events import AtlanEvent

# v9 event payload types for type assertions
from pyatlan_v9.model.events import (
    AssetCreatePayload,
    AssetDeletePayload,
    AssetUpdatePayload,
    AtlanTagAddPayload,
    AtlanTagDeletePayload,
    CustomMetadataUpdatePayload,
)

# v9 asset type for asset isinstance check
from pyatlan_v9.model.assets import AtlasGlossaryTerm

ACTUAL_JSON = "actual.json"
VALIDATION_JSON = "validation.json"
ENTITY_CREATE_JSON = "entity_create.json"
ENTITY_UPDATE_JSON = "entity_update.json"
ENTITY_DELETE_JSON = "entity_delete.json"
CLASSIFICATION_ADD_JSON = "classification_add.json"
CLASSIFICATION_DELETE_JSON = "classification_delete.json"
BUSINESS_ATTRIBUTE_UPDATE_JSON = "business_attribute_update.json"
TEST_DATA_DIR = Path(__file__).parent.parent.parent / "tests" / "unit" / "data"
EVENT_RESPONSES_DIR = TEST_DATA_DIR / "event_responses"


def load_json(respones_dir, filename):
    with (respones_dir / filename).open() as input_file:
        return load(input_file)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def actual_json():
    return load_json(EVENT_RESPONSES_DIR, ACTUAL_JSON)


@pytest.fixture()
def validation_json():
    return load_json(EVENT_RESPONSES_DIR, VALIDATION_JSON)


@pytest.fixture()
def entity_create_json():
    return load_json(EVENT_RESPONSES_DIR, ENTITY_CREATE_JSON)


@pytest.fixture()
def entity_update_json():
    return load_json(EVENT_RESPONSES_DIR, ENTITY_UPDATE_JSON)


@pytest.fixture()
def entity_delete_json():
    return load_json(EVENT_RESPONSES_DIR, ENTITY_DELETE_JSON)


@pytest.fixture()
def custom_metadata_add_json():
    return load_json(EVENT_RESPONSES_DIR, BUSINESS_ATTRIBUTE_UPDATE_JSON)


@pytest.fixture()
def tag_add_json():
    return load_json(EVENT_RESPONSES_DIR, CLASSIFICATION_ADD_JSON)


@pytest.fixture()
def tag_delete_json():
    return load_json(EVENT_RESPONSES_DIR, CLASSIFICATION_DELETE_JSON)


def test_validation_payload(validation_json):
    body = validation_json.get("body")
    assert is_validation_request(body)


def test_no_signing_key(validation_json):
    assert not valid_signature("test-secret", validation_json.get("headers"))


def test_signing_key(actual_json):
    assert valid_signature("test-secret", actual_json.get("headers"))


def test_body(actual_json):
    body = loads(actual_json.get("body"))
    assert body
    atlan_event = AtlanEvent(**body)
    assert atlan_event
    assert atlan_event.payload
    assert _is_model_instance(atlan_event.payload.asset, AtlasGlossaryTerm)


def test_atlan_events_deserialization(
    client,
    mock_tag_cache,
    entity_create_json,
    entity_update_json,
    entity_delete_json,
    tag_add_json,
    tag_delete_json,
    custom_metadata_add_json,
):
    _EVENT_TYPES = {
        "entity_create_json": AssetCreatePayload,
        "entity_update_json": AssetUpdatePayload,
        "entity_delete_json": AssetDeletePayload,
        "tag_add_json": AtlanTagAddPayload,
        "tag_delete_json": AtlanTagDeletePayload,
        "custom_metadata_add_json": CustomMetadataUpdatePayload,
    }

    for key, payload_type in _EVENT_TYPES.items():
        data = locals()[key]
        event = AtlanEvent(**data)
        assert _is_model_instance(event.payload, payload_type)
