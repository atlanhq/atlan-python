# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from json import load
from pathlib import Path
from re import escape
from typing import List
from unittest.mock import Mock

import pytest
from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.client.sso import SSOClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper

TEST_DATA_DIR = Path(__file__).parent / "data"
SSO_GET_GROUP_MAPPING_JSON = "get_group_mapping.json"
SSO_GET_ALL_GROUP_MAPPING_JSON = "get_all_group_mapping.json"
SSO_CREATE_GROUP_MAPPING_JSON = "create_group_mapping.json"
SSO_UPDATE_GROUP_MAPPING_JSON = "update_group_mapping.json"
SSO_RESPONSES_DIR = TEST_DATA_DIR / "sso_responses"


def load_json(respones_dir, filename):
    with (respones_dir / filename).open() as input_file:
        return load(input_file)


def to_json(model):
    return model.json(by_alias=True, exclude_none=True)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def get_group_mapping_json():
    return load_json(SSO_RESPONSES_DIR, SSO_GET_GROUP_MAPPING_JSON)


@pytest.fixture()
def get_all_group_mapping_json():
    return load_json(SSO_RESPONSES_DIR, SSO_GET_ALL_GROUP_MAPPING_JSON)


@pytest.fixture()
def create_group_mapping_json():
    return load_json(SSO_RESPONSES_DIR, SSO_CREATE_GROUP_MAPPING_JSON)


@pytest.fixture()
def update_group_mapping_json():
    return load_json(SSO_RESPONSES_DIR, SSO_UPDATE_GROUP_MAPPING_JSON)


@pytest.mark.parametrize("test_api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(test_api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller",
    ):
        SSOClient(test_api_caller)


@pytest.mark.parametrize(
    "sso_alias, group_map_id, error_msg",
    [
        [None, "map-id", "none is not an allowed value"],
        ["auth0", None, "none is not an allowed value"],
        [[123], "map-id", "so_alias\n  str type expected"],
        ["azure", [123], "group_map_id\n  str type expected"],
    ],
)
def test_sso_get_group_mapping_wrong_params_raises_validation_error(
    sso_alias, group_map_id, error_msg
):
    with pytest.raises(ValidationError) as err:
        SSOClient.get_group_mapping(sso_alias=sso_alias, group_map_id=group_map_id)
    assert error_msg in str(err.value)


@pytest.mark.parametrize(
    "sso_alias, error_msg",
    [
        [None, "none is not an allowed value"],
        [[123], "so_alias\n  str type expected"],
    ],
)
def test_sso_get_all_group_mapping_wrong_params_raises_validation_error(
    sso_alias, error_msg
):
    with pytest.raises(ValidationError, match=error_msg):
        SSOClient.get_all_group_mappings(sso_alias=sso_alias)


@pytest.mark.parametrize(
    "sso_alias, atlan_group, sso_group_name, error_msg",
    [
        [None, "atlan-group", "sso-group", "none is not an allowed value"],
        ["auth0", None, "sso-group", "none is not an allowed value"],
        ["auth0", "atlan-group", None, "none is not an allowed value"],
        [[123], "atlan-group", "sso-group", "so_alias\n  str type expected"],
        ["auth0", [123], "sso-group", "atlan_group\n  value is not a valid dict"],
        ["auth0", AtlanGroup(), [123], "sso_group_name\n  str type expected"],
    ],
)
def test_sso_create_group_mapping_wrong_params_raises_validation_error(
    sso_alias, atlan_group, sso_group_name, error_msg
):
    with pytest.raises(ValidationError, match=error_msg):
        SSOClient.create_group_mapping(
            sso_alias=sso_alias, atlan_group=atlan_group, sso_group_name=sso_group_name
        )


@pytest.mark.parametrize(
    "sso_alias, atlan_group, group_map_id, sso_group_name, error_msg",
    [
        [None, "atlan-group", "map-id", "sso-group", "none is not an allowed value"],
        ["auth0", None, "map-id", "sso-group", "none is not an allowed value"],
        ["auth0", "atlan-group", None, "sso-group", "none is not an allowed value"],
        ["auth0", "atlan-group", "map-id", None, "none is not an allowed value"],
        ["auth0", "atlan-group", "map-id", None, "none is not an allowed value"],
        [[123], "atlan-group", "map-id", "sso-group", "sso_alias\n  str type expected"],
        [
            "auth0",
            [123],
            "map-id",
            "sso-group",
            "atlan_group\n  value is not a valid dict",
        ],
        [
            "auth0",
            "atlan-group",
            [123],
            "sso-group",
            "group_map_id\n  str type expected",
        ],
        [
            "auth0",
            "atlan-group",
            "map-id",
            [123],
            "sso_group_name\n  str type expected",
        ],
    ],
)
def test_sso_update_group_mapping_wrong_params_raises_validation_error(
    sso_alias, atlan_group, group_map_id, sso_group_name, error_msg
):
    with pytest.raises(ValidationError, match=error_msg):
        SSOClient.update_group_mapping(
            sso_alias=sso_alias,
            atlan_group=atlan_group,
            group_map_id=group_map_id,
            sso_group_name=sso_group_name,
        )


@pytest.mark.parametrize(
    "sso_alias, group_map_id, error_msg",
    [
        [None, "map-id", "none is not an allowed value"],
        ["auth0", None, "none is not an allowed value"],
        [[123], "map-id", "so_alias\n  str type expected"],
        ["azure", [123], "group_map_id\n  str type expected"],
    ],
)
def test_sso_delete_group_mapping_wrong_params_raises_validation_error(
    sso_alias, group_map_id, error_msg
):
    with pytest.raises(ValidationError, match=error_msg):
        SSOClient.delete_group_mapping(sso_alias=sso_alias, group_map_id=group_map_id)


def test_sso_get_group_mapping(
    mock_api_caller,
    get_group_mapping_json,
):
    mock_api_caller._call_api.side_effect = [get_group_mapping_json]
    client = SSOClient(client=mock_api_caller)
    response = client.get_group_mapping(sso_alias="auth0", group_map_id="1234")
    assert response == SSOMapper(**get_group_mapping_json)
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_sso_get_all_group_mapping(
    mock_api_caller,
    get_all_group_mapping_json,
):
    mock_api_caller._call_api.side_effect = [get_all_group_mapping_json]
    client = SSOClient(client=mock_api_caller)
    response = client.get_all_group_mappings(sso_alias="auth0")
    # Only returns group mapping
    assert response == parse_obj_as(List[SSOMapper], [get_all_group_mapping_json[2]])
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_sso_create_group_mapping_invalid_request_error(
    mock_api_caller, get_all_group_mapping_json, create_group_mapping_json
):
    mock_api_caller._call_api.side_effect = [
        get_all_group_mapping_json,
        create_group_mapping_json,
    ]
    existing_atlan_group = AtlanGroup()
    existing_atlan_group.alias = "existing_atlan_group"
    existing_atlan_group.id = "atlan-group-guid-1234"
    client = SSOClient(client=mock_api_caller)
    expected_error = escape(
        (
            f"ATLAN-PYTHON-400-058 SSO group mapping already exists between "
            f"{existing_atlan_group.alias} (Atlan group) <-> test-sso-group (SSO group)"
        )
    )
    with pytest.raises(InvalidRequestError, match=expected_error):
        client.create_group_mapping(
            sso_alias="auth0",
            atlan_group=existing_atlan_group,
            sso_group_name="sso-group",
        )
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_sso_create_group_mapping(
    mock_api_caller, get_all_group_mapping_json, create_group_mapping_json
):
    mock_api_caller._call_api.side_effect = [
        get_all_group_mapping_json,
        create_group_mapping_json,
    ]
    # Group that doesn't exist in sso group mappings
    atlan_group = AtlanGroup()
    atlan_group.id = "atlan-group-new-mapping-guid-1234"
    client = SSOClient(client=mock_api_caller)
    response = client.create_group_mapping(
        sso_alias="auth0",
        atlan_group=atlan_group,
        sso_group_name="sso-group",
    )
    assert response == SSOMapper(**create_group_mapping_json)
    assert mock_api_caller._call_api.call_count == 2
    mock_api_caller.reset_mock()


def test_sso_update_group_mapping(mock_api_caller, update_group_mapping_json):
    mock_api_caller._call_api.side_effect = [
        update_group_mapping_json,
    ]
    client = SSOClient(client=mock_api_caller)
    response = client.update_group_mapping(
        sso_alias="auth0",
        atlan_group=AtlanGroup(),
        group_map_id="group-map-id",
        sso_group_name="sso-group",
    )
    assert response == SSOMapper(**update_group_mapping_json)
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_sso_delete_group_mapping(mock_api_caller):
    mock_api_caller._call_api.side_effect = [None]
    client = SSOClient(client=mock_api_caller)
    response = client.delete_group_mapping(
        sso_alias="auth0",
        group_map_id="group-map-id",
    )
    assert response is None
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()
