import pytest

from pyatlan.model.assets import ADLSContainer
from tests.unit.model.constants import (
    ADLS_ACCOUNT_QUALIFIED_NAME,
    ADLS_CONNECTION_QUALIFIED_NAME,
    ADLS_CONNECTOR_TYPE,
    ADLS_CONTAINER_NAME,
    ADLS_CONTAINER_QUALIFIED_NAME,
)


# Test cases for missing parameters
@pytest.mark.parametrize(
    "name, adls_account_qualified_name, message",
    [
        (None, "adls/account", "name is required"),
        (ADLS_CONTAINER_NAME, None, "adls_account_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, adls_account_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        ADLSContainer.create(
            name=name, adls_account_qualified_name=adls_account_qualified_name
        )


# Test case for creating an ADLSContainer
def test_create():
    sut = ADLSContainer.create(
        name=ADLS_CONTAINER_NAME,
        adls_account_qualified_name=ADLS_ACCOUNT_QUALIFIED_NAME,
    )

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.adls_account_qualified_name == ADLS_ACCOUNT_QUALIFIED_NAME
    assert sut.connection_qualified_name == ADLS_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == ADLS_CONNECTOR_TYPE
    assert sut.qualified_name == f"{ADLS_ACCOUNT_QUALIFIED_NAME}/{ADLS_CONTAINER_NAME}"


def test_overload_creator():
    sut = ADLSContainer.creator(
        name=ADLS_CONTAINER_NAME,
        adls_account_qualified_name=ADLS_ACCOUNT_QUALIFIED_NAME,
        connection_qualified_name=ADLS_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.adls_account_qualified_name == ADLS_ACCOUNT_QUALIFIED_NAME
    assert sut.connection_qualified_name == ADLS_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == ADLS_CONNECTOR_TYPE
    assert sut.qualified_name == f"{ADLS_ACCOUNT_QUALIFIED_NAME}/{ADLS_CONTAINER_NAME}"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ADLS_CONTAINER_NAME, "qualified_name is required"),
        (ADLS_CONTAINER_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        ADLSContainer.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = ADLSContainer.create_for_modification(
        qualified_name=ADLS_CONTAINER_QUALIFIED_NAME, name=ADLS_CONTAINER_NAME
    )

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.qualified_name == ADLS_CONTAINER_QUALIFIED_NAME


# Test case for trimming to required fields
def test_trim_to_required():
    sut = ADLSContainer.create_for_modification(
        qualified_name=ADLS_CONTAINER_QUALIFIED_NAME, name=ADLS_CONTAINER_NAME
    ).trim_to_required()

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.qualified_name == ADLS_CONTAINER_QUALIFIED_NAME
