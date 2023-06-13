from typing import Optional

import pytest

from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType

IT = Connection.create_for_modification(qualified_name="abc/def", name="connection")


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles, message",
    [
        (None, AtlanConnectorType.SNOWFLAKE, [], [], [], "name cannot be blank"),
        ("Connection", None, [], [], [], "connector_type is required"),
        (
            "Connection",
            AtlanConnectorType.SNOWFLAKE,
            [],
            [],
            [],
            "One of admin_user, admin_groups or admin_roles is required",
        ),
        (
            "Connection",
            AtlanConnectorType.SNOWFLAKE,
            ["bad"],
            [],
            [],
            "Provided username bad was not found in Atlan.",
        ),
        (
            "Connection",
            AtlanConnectorType.SNOWFLAKE,
            [],
            ["bad"],
            [],
            "Provided group name bad was not found in Atlan.",
        ),
        (
            "Connection",
            AtlanConnectorType.SNOWFLAKE,
            [],
            [],
            ["bad"],
            "Provided role ID bad was not found in Atlan.",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    connector_type: AtlanConnectorType,
    admin_users: Optional[list[str]],
    admin_groups: Optional[list[str]],
    admin_roles: Optional[list[str]],
    message: str,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    def side_effect(*args, **kwargs):
        if args and args[0] == "bad":
            return None
        return "123"

    mock_role_cache.get_name_for_id.side_effect = side_effect
    mock_user_cache.get_id_for_name.side_effect = side_effect
    mock_group_cache.get_id_for_alias.side_effect = side_effect

    with pytest.raises(ValueError, match=message):
        Connection.create(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )


@pytest.mark.parametrize(
    "name, connector_type, admin_users, admin_groups, admin_roles",
    [
        ("MyConnection", AtlanConnectorType.SNOWFLAKE, ["ernest"], [], []),
        ("MyConnection", AtlanConnectorType.SNOWFLAKE, [], ["ernest"], []),
        ("MyConnection", AtlanConnectorType.SNOWFLAKE, [], [], ["ernest"]),
    ],
)
def test_create(
    name: str,
    connector_type: AtlanConnectorType,
    admin_users: list[str],
    admin_groups: list[str],
    admin_roles: list[str],
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    mock_role_cache.get_name_for_id.return_value = "123"
    mock_user_cache.get_id_for_name.return_value = "456"
    mock_group_cache.get_id_for_alias.return_value = "789"

    sut = Connection.create(
        name=name,
        connector_type=connector_type,
        admin_users=admin_users,
        admin_groups=admin_groups,
        admin_roles=admin_roles,
    )

    assert sut.name == name
    assert sut.qualified_name[:20] == connector_type.to_qualified_name()[:20]
    assert sut.connector_name == connector_type.value
    assert sut.admin_users == set(admin_users)
    assert sut.admin_groups == set(admin_groups)
    assert sut.admin_roles == set(admin_roles)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, "abc/def", "qualified_name is required"),
        ("MyConnection", None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Connection.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    name = "MyConnection"
    qualified_name = "abc/def"

    sut = Connection.create_for_modification(qualified_name=qualified_name, name=name)

    assert sut.qualified_name == qualified_name
    assert sut.name == name


def test_trim_to_required():
    name = "MyConnection"
    qualified_name = "abc/def"

    sut = Connection.create_for_modification(
        qualified_name=qualified_name, name=name
    ).trim_to_required()

    assert sut.qualified_name == qualified_name
    assert sut.name == name
