# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Connection model in pyatlan_v9."""

import json
from typing import List, Optional

import pytest
from msgspec import UNSET

from pyatlan.model.enums import AtlanConnectionCategory, AtlanConnectorType
from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model import Connection
from tests_v9.unit.model.constants import CONNECTION_NAME, CONNECTION_QUALIFIED_NAME


@pytest.fixture()
def client():
    """Create a test AtlanClient instance."""
    return AtlanClient(base_url="https://test.atlan.com", api_key="test-api-key")


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles, message",
    [
        (None, AtlanConnectorType.SNOWFLAKE, [], [], [], "name is required"),
        (CONNECTION_NAME, None, [], [], [], "connector_type is required"),
        (
            CONNECTION_NAME,
            AtlanConnectorType.SNOWFLAKE,
            [],
            [],
            [],
            "One of admin_user, admin_groups or admin_roles is required",
        ),
        (
            CONNECTION_NAME,
            AtlanConnectorType.SNOWFLAKE,
            ["bad"],
            [],
            [],
            "Provided username bad was not found in Atlan.",
        ),
        (
            CONNECTION_NAME,
            AtlanConnectorType.SNOWFLAKE,
            [],
            ["bad"],
            [],
            "Provided group name bad was not found in Atlan.",
        ),
        (
            CONNECTION_NAME,
            AtlanConnectorType.SNOWFLAKE,
            [],
            [],
            ["bad"],
            "Provided role ID bad was not found in Atlan.",
        ),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    client: AtlanClient,
    name: str,
    connector_type: AtlanConnectorType,
    admin_users: Optional[List[str]],
    admin_groups: Optional[List[str]],
    admin_roles: Optional[List[str]],
    message: str,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """Test that creator raises ValueError when required parameters are missing."""

    def role_side_effect(*args, **kwargs):
        if "idstrs" in kwargs:
            if "bad" in kwargs["idstrs"]:
                raise ValueError("Provided role ID bad was not found in Atlan.")

    def user_side_effect(*args, **kwargs):
        if "names" in kwargs:
            if "bad" in kwargs["names"]:
                raise ValueError("Provided username bad was not found in Atlan.")

    def group_side_effect(*args, **kwargs):
        if "aliases" in kwargs:
            if "bad" in kwargs["aliases"]:
                raise ValueError("Provided group name bad was not found in Atlan.")

    mock_role_cache.validate_idstrs.side_effect = role_side_effect
    mock_user_cache.validate_names.side_effect = user_side_effect
    mock_group_cache.validate_aliases.side_effect = group_side_effect

    with pytest.raises(ValueError, match=message):
        Connection.creator(
            client=client,
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )
    mock_role_cache.validate_idstrs.reset_mock()
    mock_user_cache.validate_names.reset_mock()
    mock_group_cache.validate_aliases.reset_mock()


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [
        (CONNECTION_NAME, AtlanConnectorType.SNOWFLAKE, ["ernest"], [], []),
        (CONNECTION_NAME, AtlanConnectorType.SNOWFLAKE, [], ["ernest"], []),
        (CONNECTION_NAME, AtlanConnectorType.SNOWFLAKE, [], [], ["ernest"]),
    ],
)
def test_creator(
    client: AtlanClient,
    name: str,
    connector_type: AtlanConnectorType,
    admin_users: List[str],
    admin_groups: List[str],
    admin_roles: List[str],
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """Test that creator properly initializes a Connection with all derived fields."""
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    sut = Connection.creator(
        client=client,
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )

    assert sut.name == name
    assert sut.qualified_name
    assert sut.qualified_name[:20] == connector_type.to_qualified_name()[:20]
    assert sut.connector_name == connector_type.value
    assert sut.admin_users == set(admin_users)
    assert sut.admin_groups == set(admin_groups)
    assert sut.admin_roles == set(admin_roles)

    mock_role_cache.validate_idstrs.reset_mock()
    mock_user_cache.validate_names.reset_mock()
    mock_group_cache.validate_aliases.reset_mock()


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [
        (
            CONNECTION_NAME,
            AtlanConnectorType.CREATE_CUSTOM(
                name="FOO", value="foo", category=AtlanConnectionCategory.BI
            ),
            ["ernest"],
            [],
            [],
        ),
        (
            CONNECTION_NAME,
            AtlanConnectorType.CREATE_CUSTOM(
                name="BAR", value="bar", category=AtlanConnectionCategory.API
            ),
            [],
            ["ernest"],
            [],
        ),
        (
            CONNECTION_NAME,
            AtlanConnectorType.CREATE_CUSTOM(
                name="BAZ", value="baz", category=AtlanConnectionCategory.WAREHOUSE
            ),
            [],
            [],
            ["ernest"],
        ),
    ],
)
def test_creator_with_custom_type(
    client: AtlanClient,
    name: str,
    connector_type: AtlanConnectorType,
    admin_users: List[str],
    admin_groups: List[str],
    admin_roles: List[str],
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """Test that creator works with custom connector types."""
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    sut = Connection.creator(
        client=client,
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )

    assert sut.name == name
    assert sut.qualified_name
    assert sut.qualified_name[:20] == connector_type.to_qualified_name()[:20]
    assert sut.connector_name == connector_type.value
    assert sut.admin_users == set(admin_users)
    assert sut.admin_groups == set(admin_groups)
    assert sut.admin_roles == set(admin_roles)

    mock_role_cache.validate_idstrs.reset_mock()
    mock_user_cache.validate_names.reset_mock()
    mock_group_cache.validate_aliases.reset_mock()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "qualified_name is required"),
        (CONNECTION_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Connection.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Connection instance for modification."""
    sut = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    )

    assert sut.qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.name == CONNECTION_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a Connection with only required fields."""
    sut = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    assert sut.qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.name == CONNECTION_NAME


def test_admin_users_when_set_to_good_name():
    """Test that admin_users can be set and retrieved as a set."""
    sut = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    sut.admin_users = {"ernest"}

    assert sut.admin_users == {"ernest"}


def test_admin_groups_when_set_to_good_name():
    """Test that admin_groups can be set and retrieved as a set."""
    sut = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    sut.admin_groups = {"ernest"}

    assert sut.admin_groups == {"ernest"}


def test_admin_roles_when_set_to_good_name():
    """Test that admin_roles can be set and retrieved as a set."""
    sut = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    sut.admin_roles = {"ernest"}

    assert sut.admin_roles == {"ernest"}


def test_validation_of_admin_not_done_when_constructed_from_json(serde):
    """Test that admin fields are preserved when deserializing from JSON."""
    data = {
        "typeName": "Connection",
        "attributes": {
            "adminGroups": ["bogus"],
            "adminUsers": ["bogus"],
            "name": "S3 Ernest",
            "connectorName": "s3",
            "adminRoles": ["bogus"],
        },
        "guid": "ee59f5b0-3b59-409f-a42d-d151e5ffba22",
        "isIncomplete": False,
        "status": "ACTIVE",
        "createdBy": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
        "updatedBy": "service-account-apikey-a1c7beae-a558-4994-adb4-16ee422b91d6",
        "createTime": 1695884860580,
        "updateTime": 1695884860580,
        "version": 0,
        "relationshipAttributes": {},
        "labels": [],
    }

    json_str = json.dumps(data)
    conn = Connection.from_json(json_str, serde=serde)

    assert conn.name == "S3 Ernest"
    assert conn.connector_name == "s3"
    assert conn.admin_users == {"bogus"}
    assert conn.admin_groups == {"bogus"}
    assert conn.admin_roles == {"bogus"}
    assert conn.guid == "ee59f5b0-3b59-409f-a42d-d151e5ffba22"
    assert conn.status == "ACTIVE"


def test_basic_construction():
    """Test basic Connection construction with minimal parameters."""
    conn = Connection(name=CONNECTION_NAME, qualified_name=CONNECTION_QUALIFIED_NAME)

    assert conn.name == CONNECTION_NAME
    assert conn.qualified_name == CONNECTION_QUALIFIED_NAME
    assert conn.type_name == "Connection"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    conn = Connection(name=CONNECTION_NAME, qualified_name=CONNECTION_QUALIFIED_NAME)

    assert conn.category is UNSET
    assert conn.sub_category is UNSET
    assert conn.host is UNSET
    assert conn.port is UNSET
    assert conn.admin_users is UNSET
    assert conn.admin_groups is UNSET
    assert conn.admin_roles is UNSET


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    conn = Connection(name=CONNECTION_NAME, qualified_name=CONNECTION_QUALIFIED_NAME)

    assert conn.host is UNSET
    conn.host = None
    assert conn.host is None
    assert conn.host is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    conn = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    )

    json_str = conn.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "Connection"
    assert "attributes" in data
    assert data["attributes"]["name"] == CONNECTION_NAME
    assert data["attributes"]["qualifiedName"] == CONNECTION_QUALIFIED_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = Connection.updater(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = Connection.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'Connection'."""
    conn = Connection(name=CONNECTION_NAME, qualified_name=CONNECTION_QUALIFIED_NAME)
    assert conn.type_name == "Connection"
