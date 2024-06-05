import pytest

from pyatlan.model.assets import APIPath
from tests.unit.model.constants import (
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_PATH_NAME,
    API_PATH_QUALIFIED_NAME,
    API_PATH_RAW_URI,
    API_SPEC_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "path_raw_uri, spec_qualified_name, message",
    [
        (None, "api/spec", "path_raw_uri is required"),
        (API_PATH_RAW_URI, None, "spec_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    path_raw_uri: str,
    spec_qualified_name: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        APIPath.create(
            path_raw_uri=path_raw_uri,
            spec_qualified_name=spec_qualified_name,
        )


def test_create():
    sut = APIPath.create(
        path_raw_uri=API_PATH_RAW_URI,
        spec_qualified_name=API_SPEC_QUALIFIED_NAME,
    )

    assert sut.name == API_PATH_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_spec_qualified_name == API_SPEC_QUALIFIED_NAME
    assert sut.api_path_raw_u_r_i == API_PATH_RAW_URI


def test_overload_creator():
    sut = APIPath.creator(
        path_raw_uri=API_PATH_RAW_URI,
        spec_qualified_name=API_SPEC_QUALIFIED_NAME,
        connection_qualified_name=API_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == API_PATH_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_spec_qualified_name == API_SPEC_QUALIFIED_NAME
    assert sut.api_path_raw_u_r_i == API_PATH_RAW_URI


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, API_PATH_QUALIFIED_NAME, "qualified_name is required"),
        (API_PATH_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIPath.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = APIPath.create_for_modification(
        qualified_name=API_PATH_QUALIFIED_NAME, name=API_PATH_NAME
    )

    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
    assert sut.name == API_PATH_NAME


def test_trim_to_required():
    sut = APIPath.create_for_modification(
        name=API_PATH_NAME, qualified_name=API_PATH_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == API_PATH_NAME
    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
