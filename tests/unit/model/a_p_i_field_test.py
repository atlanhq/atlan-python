import pytest

from pyatlan.model.assets import APIField
from pyatlan.model.enums import APIQueryParamTypeEnum
from tests.unit.model.constants import (
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_FIELD_NAME,
    API_FIELD_PARENT_OBJECT_QUALIFIED_NAME,
    API_FIELD_PARENT_QUERY_QUALIFIED_NAME,
    API_FIELD_REFERENCE_OBJECT_QN,
)


@pytest.mark.parametrize(
    "name, parent_api_object_qualified_name, parent_api_query_qualified_name, message",
    [
        (None, "connection/name", "connection/name", "name is required"),
        (
            API_FIELD_NAME,
            None,
            None,
            "Either parent_api_object_qualified_name or parent_api_query_qualified_name requires a valid value",
        ),
        (
            API_FIELD_NAME,
            API_FIELD_PARENT_OBJECT_QUALIFIED_NAME,
            API_FIELD_PARENT_QUERY_QUALIFIED_NAME,
            "Both parent_api_object_qualified_name and parent_api_query_qualified_name cannot be valid",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    parent_api_object_qualified_name: str,
    parent_api_query_qualified_name: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        APIField.creator(
            name=name,
            parent_api_object_qualified_name=parent_api_object_qualified_name,
            parent_api_query_qualified_name=parent_api_query_qualified_name,
        )


def test_create_parent_object():
    sut = APIField.creator(
        name=API_FIELD_NAME,
        parent_api_object_qualified_name=API_FIELD_PARENT_OBJECT_QUALIFIED_NAME,
        parent_api_query_qualified_name=None,
    )

    assert sut.name == API_FIELD_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}"
    )
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_object.qualified_name == API_FIELD_PARENT_OBJECT_QUALIFIED_NAME


def test_create_parent_query():
    sut = APIField.creator(
        name=API_FIELD_NAME,
        parent_api_object_qualified_name=None,
        parent_api_query_qualified_name=API_FIELD_PARENT_QUERY_QUALIFIED_NAME,
    )

    assert sut.name == API_FIELD_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{API_FIELD_PARENT_QUERY_QUALIFIED_NAME}/{API_FIELD_NAME}"
    )
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_query.qualified_name == API_FIELD_PARENT_QUERY_QUALIFIED_NAME


def test_overload_creator_parent_object():
    sut = APIField.creator(
        name=API_FIELD_NAME,
        parent_api_object_qualified_name=API_FIELD_PARENT_OBJECT_QUALIFIED_NAME,
        parent_api_query_qualified_name=None,
        connection_qualified_name=API_CONNECTION_QUALIFIED_NAME,
        api_field_type="api-object-ref",
        api_field_type_secondary="Object",
        is_api_object_reference=True,
        reference_api_object_qualified_name=API_FIELD_REFERENCE_OBJECT_QN,
        api_query_param_type=None,
    )

    assert sut.name == API_FIELD_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}"
    )
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_field_type == "api-object-ref"
    assert sut.api_field_type_secondary == "Object"
    assert sut.api_is_object_reference
    assert sut.api_object_qualified_name == API_FIELD_REFERENCE_OBJECT_QN
    assert sut.api_object.qualified_name == API_FIELD_PARENT_OBJECT_QUALIFIED_NAME


def test_overload_creator_parent_query():
    sut = APIField.creator(
        name=API_FIELD_NAME,
        parent_api_object_qualified_name=None,
        parent_api_query_qualified_name=API_FIELD_PARENT_QUERY_QUALIFIED_NAME,
        connection_qualified_name=API_CONNECTION_QUALIFIED_NAME,
        api_field_type="api-object-ref",
        api_field_type_secondary="Object",
        is_api_object_reference=True,
        reference_api_object_qualified_name=API_FIELD_REFERENCE_OBJECT_QN,
        api_query_param_type=APIQueryParamTypeEnum.INPUT,
    )

    assert sut.name == API_FIELD_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{API_FIELD_PARENT_QUERY_QUALIFIED_NAME}/{API_FIELD_NAME}"
    )
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_field_type == "api-object-ref"
    assert sut.api_field_type_secondary == "Object"
    assert sut.api_is_object_reference
    assert sut.api_object_qualified_name == API_FIELD_REFERENCE_OBJECT_QN
    assert sut.api_query.qualified_name == API_FIELD_PARENT_QUERY_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (
            None,
            f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}",
            "qualified_name is required",
        ),
        (API_FIELD_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIField.updater(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = APIField.updater(
        qualified_name=f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}",
        name=API_FIELD_NAME,
    )

    assert (
        sut.qualified_name
        == f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}"
    )
    assert sut.name == API_FIELD_NAME


def test_trim_to_required():
    sut = APIField.updater(
        name=API_FIELD_NAME,
        qualified_name=f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}",
    ).trim_to_required()

    assert sut.name == API_FIELD_NAME
    assert (
        sut.qualified_name
        == f"{API_FIELD_PARENT_OBJECT_QUALIFIED_NAME}/{API_FIELD_NAME}"
    )
