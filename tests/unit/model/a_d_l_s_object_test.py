import pytest

from pyatlan.model.assets import ADLSObject
from pyatlan.utils import get_parent_qualified_name
from tests.unit.model.constants import (
    ADLS_CONNECTION_QUALIFIED_NAME,
    ADLS_CONNECTOR_TYPE,
    ADLS_CONTAINER_QUALIFIED_NAME,
    ADLS_OBJECT_NAME,
    ADLS_OBJECT_QUALIFIED_NAME,
)


# Test cases for missing parameters
@pytest.mark.parametrize(
    "name, adls_container_qualified_name, message",
    [
        (None, "adls/container", "name is required"),
        (ADLS_OBJECT_NAME, None, "adls_container_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    adls_container_qualified_name: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        ADLSObject.create(
            name=name,
            adls_container_qualified_name=adls_container_qualified_name,
        )


# Test case for creating an ADLSObject
def test_create():
    sut = ADLSObject.create(
        name=ADLS_OBJECT_NAME,
        adls_container_qualified_name=ADLS_CONTAINER_QUALIFIED_NAME,
    )

    assert sut.name == ADLS_OBJECT_NAME
    assert sut.adls_container_qualified_name == ADLS_CONTAINER_QUALIFIED_NAME
    assert sut.qualified_name == f"{ADLS_CONTAINER_QUALIFIED_NAME}/{ADLS_OBJECT_NAME}"
    assert sut.connection_qualified_name == ADLS_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == ADLS_CONNECTOR_TYPE
    assert sut.adls_account_qualified_name == get_parent_qualified_name(
        ADLS_CONTAINER_QUALIFIED_NAME
    )


def test_overload_creator():
    sut = ADLSObject.creator(
        name=ADLS_OBJECT_NAME,
        adls_container_qualified_name=ADLS_CONTAINER_QUALIFIED_NAME,
        adls_account_qualified_name=get_parent_qualified_name(
            ADLS_CONTAINER_QUALIFIED_NAME
        ),
        connection_qualified_name=ADLS_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == ADLS_OBJECT_NAME
    assert sut.adls_container_qualified_name == ADLS_CONTAINER_QUALIFIED_NAME
    assert sut.qualified_name == f"{ADLS_CONTAINER_QUALIFIED_NAME}/{ADLS_OBJECT_NAME}"
    assert sut.connection_qualified_name == ADLS_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == ADLS_CONNECTOR_TYPE
    assert sut.adls_account_qualified_name == get_parent_qualified_name(
        ADLS_CONTAINER_QUALIFIED_NAME
    )


# Test cases for creating ADLSObject for modification
@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ADLS_OBJECT_NAME, "qualified_name is required"),
        (ADLS_OBJECT_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        ADLSObject.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = ADLSObject.create_for_modification(
        qualified_name=ADLS_OBJECT_QUALIFIED_NAME, name=ADLS_OBJECT_NAME
    )

    assert sut.name == ADLS_OBJECT_NAME
    assert sut.qualified_name == ADLS_OBJECT_QUALIFIED_NAME


# Test case for trimming to required fields
def test_trim_to_required():
    sut = ADLSObject.create_for_modification(
        qualified_name=ADLS_OBJECT_QUALIFIED_NAME, name=ADLS_OBJECT_NAME
    ).trim_to_required()

    assert sut.name == ADLS_OBJECT_NAME
    assert sut.qualified_name == ADLS_OBJECT_QUALIFIED_NAME
