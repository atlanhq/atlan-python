# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for ADLSAccount model in pyatlan_v9."""

import pytest

from pyatlan_v9.models import ADLSAccount
from tests_v9.unit.model.constants import (
    ADLS_ACCOUNT_NAME,
    ADLS_CONNECTION_QUALIFIED_NAME,
    ADLS_CONNECTOR_TYPE,
    ADLS_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (ADLS_ACCOUNT_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ADLSAccount.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = ADLSAccount.creator(
        name=ADLS_ACCOUNT_NAME, connection_qualified_name=ADLS_CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == ADLS_ACCOUNT_NAME
    assert sut.connection_qualified_name == ADLS_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == ADLS_QUALIFIED_NAME
    assert sut.connector_name == ADLS_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ADLS_QUALIFIED_NAME, "qualified_name is required"),
        (ADLS_ACCOUNT_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ADLSAccount.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates ADLSAccount for modification."""
    sut = ADLSAccount.updater(
        qualified_name=ADLS_QUALIFIED_NAME, name=ADLS_ACCOUNT_NAME
    )

    assert sut.qualified_name == ADLS_QUALIFIED_NAME
    assert sut.name == ADLS_ACCOUNT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ADLSAccount.updater(
        qualified_name=ADLS_QUALIFIED_NAME, name=ADLS_ACCOUNT_NAME
    ).trim_to_required()

    assert sut.qualified_name == ADLS_QUALIFIED_NAME
    assert sut.name == ADLS_ACCOUNT_NAME
