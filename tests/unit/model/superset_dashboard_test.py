import pytest

from pyatlan.model.assets import SupersetDashboard
from tests.unit.model.constants import (
    SUPERSET_CONNECTION_QUALIFIED_NAME,
    SUPERSET_CONNECTOR_TYPE,
    SUPERSET_DASHBOARD_NAME,
    SUPERSET_DASHBOARD_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (SUPERSET_DASHBOARD_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        SupersetDashboard.create(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create():
    sut = SupersetDashboard.create(
        name=SUPERSET_DASHBOARD_NAME,
        connection_qualified_name=SUPERSET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == SUPERSET_DASHBOARD_NAME
    assert sut.connection_qualified_name == SUPERSET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{SUPERSET_CONNECTION_QUALIFIED_NAME}/{SUPERSET_DASHBOARD_NAME}"
    )
    assert sut.connector_name == SUPERSET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SUPERSET_DASHBOARD_QUALIFIED_NAME, "qualified_name is required"),
        (SUPERSET_DASHBOARD_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        SupersetDashboard.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification():
    sut = SupersetDashboard.create_for_modification(
        qualified_name=SUPERSET_DASHBOARD_QUALIFIED_NAME, name=SUPERSET_DASHBOARD_NAME
    )

    assert sut.qualified_name == SUPERSET_DASHBOARD_QUALIFIED_NAME
    assert sut.name == SUPERSET_DASHBOARD_NAME


def test_trim_to_required():
    sut = SupersetDashboard.create_for_modification(
        qualified_name=SUPERSET_DASHBOARD_QUALIFIED_NAME, name=SUPERSET_DASHBOARD_NAME
    ).trim_to_required()

    assert sut.qualified_name == SUPERSET_DASHBOARD_QUALIFIED_NAME
    assert sut.name == SUPERSET_DASHBOARD_NAME
