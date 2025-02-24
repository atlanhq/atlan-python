import pytest

from pyatlan.model.assets import APIQuery
from tests.unit.model.constants import (
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_QUERY_NAME,
    API_QUERY_QUALIFIED_NAME,
    API_QUERY_REFERENCE_OBJECT_QN,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (API_QUERY_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIQuery.creator(name=name, connection_qualified_name=connection_qualified_name)


def test_create():
    sut = APIQuery.creator(
        name=API_QUERY_NAME, connection_qualified_name=API_CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == API_QUERY_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_QUERY_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE


def test_overload_creator():
    sut = APIQuery.creator(
        name=API_QUERY_NAME,
        connection_qualified_name=API_CONNECTION_QUALIFIED_NAME,
        api_input_field_count=1,
        api_query_output_type="api-object-ref",
        api_query_output_type_secondary="Object",
        is_object_reference=True,
        reference_api_object_qualified_name=API_QUERY_REFERENCE_OBJECT_QN,
    )

    assert sut.name == API_QUERY_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_QUERY_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_input_field_count == 1
    assert sut.api_query_output_type == "api-object-ref"
    assert sut.api_query_output_type_secondary == "Object"
    assert sut.api_is_object_reference
    assert sut.api_object_qualified_name == API_QUERY_REFERENCE_OBJECT_QN


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, API_QUERY_QUALIFIED_NAME, "qualified_name is required"),
        (API_QUERY_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIQuery.updater(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = APIQuery.updater(qualified_name=API_QUERY_QUALIFIED_NAME, name=API_QUERY_NAME)

    assert sut.qualified_name == API_QUERY_QUALIFIED_NAME
    assert sut.name == API_QUERY_NAME


def test_trim_to_required():
    sut = APIQuery.updater(
        name=API_QUERY_NAME, qualified_name=API_QUERY_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == API_QUERY_NAME
    assert sut.qualified_name == API_QUERY_QUALIFIED_NAME
