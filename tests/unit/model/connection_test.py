from typing import List, Optional
from unittest.mock import patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.token import TokenClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectionCategory, AtlanConnectorType
from tests.unit.model.constants import CONNECTION_NAME, CONNECTION_QUALIFIED_NAME


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def client():
    return AtlanClient()


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
def test_create_with_missing_parameters_raise_value_error(
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
    monkeypatch,
):
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

    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    AtlanClient()
    with patch.object(TokenClient, "get_by_id", return_value=None):
        with pytest.raises(ValueError, match=message):
            Connection.create(
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
def test_create(
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
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    sut = Connection.create(
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
    mock_role_cache.validate_idstrs
    mock_user_cache.validate_names
    mock_group_cache.validate_aliases

    sut = Connection.create(
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
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Connection.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Connection.create_for_modification(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    )

    assert sut.qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.name == CONNECTION_NAME


def test_trim_to_required():
    sut = Connection.create_for_modification(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    assert sut.qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.name == CONNECTION_NAME


def test_admin_users_when_set_to_good_name(mock_user_cache):
    mock_user_cache.validate_names
    sut = Connection.create_for_modification(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    sut.admin_users = ["ernest"]

    assert sut.admin_users == {"ernest"}
    assert mock_user_cache.validate_names.call_count == 0


def test_admin_groups_when_set_to_good_name(mock_group_cache):
    mock_group_cache.validate_aliases
    sut = Connection.create_for_modification(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    sut.admin_groups = ["ernest"]

    assert sut.admin_groups == {"ernest"}
    assert mock_group_cache.validate_aliases.call_count == 0


def test_admin_roles_when_set_to_good_name(mock_role_cache):
    mock_role_cache.validate_idstrs
    sut = Connection.create_for_modification(
        qualified_name=CONNECTION_QUALIFIED_NAME, name=CONNECTION_NAME
    ).trim_to_required()

    sut.admin_roles = ["ernest"]

    assert sut.admin_roles == {"ernest"}
    assert mock_role_cache.validate_idstrs.call_count == 0


def test_validation_of_admin_not_done_when_constructed_from_json(
    mock_user_cache, mock_group_cache, mock_role_cache
):
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

    Connection(**data)

    mock_role_cache.validate_idstrs.assert_not_called()
    mock_group_cache.validate_aliases.assert_not_called()
    mock_user_cache.validate_names.assert_not_called()


# ---------------------------------------------------------------------------
# BLDX-1294 — connector-type value regex validation in Connection.creator
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_value",
    [
        "dev_cmdr",  # underscore — the original reported case
        "dev.cmdr",  # dot
        "dev cmdr",  # whitespace
        "dev/cmdr",  # slash
        "dev@cmdr",  # special char
        "dev_",  # trailing underscore
    ],
)
def test_creator_rejects_invalid_connector_type_value(
    client: AtlanClient,
    bad_value: str,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """BLDX-1294: Connection.creator() must reject custom connector_type values
    whose slug doesn't match the platform's [a-z0-9-]+ pattern. Without this,
    callers create Connections via pyatlan that the server-side asset-import
    path later rejects, leaving phantom Connection rows in Atlas."""
    custom = AtlanConnectorType.CREATE_CUSTOM(
        name=bad_value.upper().replace("-", "_") or "EMPTY",
        value=bad_value,
        category=AtlanConnectionCategory.CUSTOM,
    )

    with pytest.raises(InvalidRequestError) as exc_info:
        Connection.creator(
            client=client,
            name=CONNECTION_NAME,
            connector_type=custom,
            admin_users=["ernest"],
        )
    # Match the Java SDK convention — typed error with code
    # ATLAN-PYTHON-400-079 (INVALID_CONNECTION_QN) and the bad slug
    # surfaced in the message.
    assert "ATLAN-PYTHON-400-079" in str(exc_info.value)
    assert bad_value in str(exc_info.value)


@pytest.mark.parametrize(
    "good_value",
    [
        "dev-cmdr",  # hyphen — the recommended replacement
        "snowflake",  # built-in-like slug
        "amazon-msk",  # hyphenated multi-word
        "a",  # single-char
        "abc123",  # alphanumerics
        "123-abc-456",  # mixed digit + alpha + hyphen
    ],
)
def test_creator_accepts_valid_connector_type_value(
    client: AtlanClient,
    good_value: str,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """Valid lowercase-alphanumeric-and-hyphen slugs continue to work."""
    custom = AtlanConnectorType.CREATE_CUSTOM(
        name="CUSTOM",
        value=good_value,
        category=AtlanConnectionCategory.CUSTOM,
    )

    sut = Connection.creator(
        client=client,
        name=CONNECTION_NAME,
        connector_type=custom,
        admin_users=["ernest"],
    )
    assert sut.name == CONNECTION_NAME
    assert sut.qualified_name.startswith(f"default/{good_value}/")


def test_creator_accepts_builtin_connector_types(
    client: AtlanClient,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """Built-in AtlanConnectorType members have always-valid slugs.
    Regression pin — the new BLDX-1294 validator must not break them."""
    sut = Connection.creator(
        client=client,
        name=CONNECTION_NAME,
        connector_type=AtlanConnectorType.SNOWFLAKE,
        admin_users=["ernest"],
    )
    assert sut.qualified_name.startswith("default/snowflake/")


@pytest.mark.asyncio
async def test_creator_async_rejects_invalid_connector_type_value(
    client: AtlanClient,
    mock_role_cache,
    mock_user_cache,
    mock_group_cache,
):
    """Same validation must apply to the async creator path."""
    bad = AtlanConnectorType.CREATE_CUSTOM(
        name="DEV_CMDR",
        value="dev_cmdr",
        category=AtlanConnectionCategory.CUSTOM,
    )

    with pytest.raises(InvalidRequestError) as exc_info:
        await Connection.creator_async(
            client=client,
            name=CONNECTION_NAME,
            connector_type=bad,
            admin_users=["ernest"],
        )
    assert "ATLAN-PYTHON-400-079" in str(exc_info.value)
    assert "dev_cmdr" in str(exc_info.value)
