# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for APIPath model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import APIPath
from tests_v9.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(
    path_raw_uri: str,
    spec_qualified_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        APIPath.creator(
            path_raw_uri=path_raw_uri,
            spec_qualified_name=spec_qualified_name,
        )


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = APIPath.creator(
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
    """Test creator accepts explicit connection qualified name."""
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
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        APIPath.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates APIPath for modification."""
    sut = APIPath.updater(qualified_name=API_PATH_QUALIFIED_NAME, name=API_PATH_NAME)

    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
    assert sut.name == API_PATH_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = APIPath.updater(
        name=API_PATH_NAME, qualified_name=API_PATH_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == API_PATH_NAME
    assert sut.qualified_name == API_PATH_QUALIFIED_NAME
