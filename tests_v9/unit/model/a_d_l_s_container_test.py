# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for ADLSContainer model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import ADLSContainer
from tests_v9.unit.model.constants import (
    ADLS_ACCOUNT_QUALIFIED_NAME,
    ADLS_CONNECTION_QUALIFIED_NAME,
    ADLS_CONNECTOR_TYPE,
    ADLS_CONTAINER_NAME,
    ADLS_CONTAINER_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, adls_account_qualified_name, message",
    [
        (None, "adls/account", "name is required"),
        (ADLS_CONTAINER_NAME, None, "adls_account_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, adls_account_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ADLSContainer.creator(
            name=name, adls_account_qualified_name=adls_account_qualified_name
        )


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = ADLSContainer.creator(
        name=ADLS_CONTAINER_NAME,
        adls_account_qualified_name=ADLS_ACCOUNT_QUALIFIED_NAME,
    )

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.adls_account_qualified_name == ADLS_ACCOUNT_QUALIFIED_NAME
    assert sut.connection_qualified_name == ADLS_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == ADLS_CONNECTOR_TYPE
    assert sut.qualified_name == f"{ADLS_ACCOUNT_QUALIFIED_NAME}/{ADLS_CONTAINER_NAME}"


def test_overload_creator():
    """Test creator accepts explicit connection qualified name."""
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
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ADLSContainer.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates ADLSContainer for modification."""
    sut = ADLSContainer.updater(
        qualified_name=ADLS_CONTAINER_QUALIFIED_NAME, name=ADLS_CONTAINER_NAME
    )

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.qualified_name == ADLS_CONTAINER_QUALIFIED_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ADLSContainer.updater(
        qualified_name=ADLS_CONTAINER_QUALIFIED_NAME, name=ADLS_CONTAINER_NAME
    ).trim_to_required()

    assert sut.name == ADLS_CONTAINER_NAME
    assert sut.qualified_name == ADLS_CONTAINER_QUALIFIED_NAME
