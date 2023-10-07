import pytest

from pyatlan.model.assets import APIPath
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
    API_PATH_NAME,
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_PATH_RAW_URI,
    API_SPEC_QUALIFIED_NAME,
    API_PATH_QUALIFIED_NAME,
)

@pytest.mark.parametrize(
    "name, connection_qualified_name, apiPathRawURI, apiSpecQualifiedName, message",
    [
        (None, "connection/name", API_PATH_RAW_URI, API_SPEC_QUALIFIED_NAME, "name is required"),
        (API_PATH_NAME, None, API_PATH_RAW_URI, API_SPEC_QUALIFIED_NAME, "connection_qualified_name is required"),
        (API_PATH_NAME, "connection/name", None, API_SPEC_QUALIFIED_NAME, "apiPathRawURI is required"),
        (API_PATH_NAME, "connection/name", API_PATH_RAW_URI, None, "apiSpecQualifiedName is required")
    ],
)

def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, apiPathRawURI: str, apiSpecQualifiedName: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIPath.create(
            name=name, connection_qualified_name=connection_qualified_name, apiPathRawURI=apiPathRawURI, apiSpecQualifiedName=apiSpecQualifiedName
        )

def test_create():
    sut = APIPath.create(
        name=API_PATH_NAME, connection_qualified_name=API_CONNECTION_QUALIFIED_NAME, apiPathRawURI=API_PATH_RAW_URI, apiSpecQualifiedName=API_SPEC_QUALIFIED_NAME
    )

    assert sut.name == API_PATH_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE

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




