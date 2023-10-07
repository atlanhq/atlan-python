import pytest

from pyatlan.model.assets import APISpec
from tests.unit.model.constants import (
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_QUALIFIED_NAME,
    API_SPEC_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (API_SPEC_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APISpec.create(name=name, connection_qualified_name=connection_qualified_name)


def test_create():
    sut = APISpec.create(
        name=API_SPEC_NAME, connection_qualified_name=API_CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == API_SPEC_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, API_QUALIFIED_NAME, "qualified_name is required"),
        (API_SPEC_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APISpec.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = APISpec.create_for_modification(
        qualified_name=API_QUALIFIED_NAME, name=API_SPEC_NAME
    )

    assert sut.qualified_name == API_QUALIFIED_NAME
    assert sut.name == API_SPEC_NAME


def test_trim_to_required():
    sut = APISpec.create_for_modification(
        name=API_SPEC_NAME, qualified_name=API_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == API_SPEC_NAME
    assert sut.qualified_name == API_QUALIFIED_NAME
