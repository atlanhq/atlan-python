import pytest

from pyatlan.model.assets import MetabaseDashboard
from tests.unit.model.constants import (
    METABASE_CONNECTION_QUALIFIED_NAME,
    METABASE_CONNECTOR_TYPE,
    METABASE_DASHBOARD_NAME,
    METABASE_DASHBOARD_QUALIFIED_NAME,
    METABASE_ID,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, metabase_id, message",
    [
        (None, METABASE_CONNECTION_QUALIFIED_NAME, METABASE_ID, "name is required"),
        (
            METABASE_DASHBOARD_NAME,
            None,
            METABASE_ID,
            "connection_qualified_name is required",
        ),
        (
            METABASE_DASHBOARD_NAME,
            METABASE_CONNECTION_QUALIFIED_NAME,
            None,
            "metabase_id is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, metabase_id: str, message: str
):
    with pytest.raises(ValueError, match=message):
        MetabaseDashboard.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            metabase_id=metabase_id,
        )


def test_creator():
    sut = MetabaseDashboard.creator(
        name=METABASE_DASHBOARD_NAME,
        connection_qualified_name=METABASE_CONNECTION_QUALIFIED_NAME,
        metabase_id=METABASE_ID,
    )

    assert sut.name == METABASE_DASHBOARD_NAME
    assert sut.connection_qualified_name == METABASE_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == METABASE_DASHBOARD_QUALIFIED_NAME
    assert sut.connector_name == METABASE_CONNECTOR_TYPE


def test_overload_creator_deprecated_create():
    with pytest.warns(DeprecationWarning):
        sut = MetabaseDashboard.create(
            name=METABASE_DASHBOARD_NAME,
            connection_qualified_name=METABASE_CONNECTION_QUALIFIED_NAME,
            metabase_id=METABASE_ID,
        )

    assert sut.qualified_name == METABASE_DASHBOARD_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, METABASE_DASHBOARD_NAME, "qualified_name is required"),
        (METABASE_DASHBOARD_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        MetabaseDashboard.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_trim_to_required():
    sut = MetabaseDashboard.create_for_modification(
        qualified_name=METABASE_DASHBOARD_QUALIFIED_NAME,
        name=METABASE_DASHBOARD_NAME,
    ).trim_to_required()

    assert sut.qualified_name == METABASE_DASHBOARD_QUALIFIED_NAME
    assert sut.name == METABASE_DASHBOARD_NAME
