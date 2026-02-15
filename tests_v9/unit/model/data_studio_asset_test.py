# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataStudioAsset model in pyatlan_v9."""

import pytest

from pyatlan.model.enums import GoogleDatastudioAssetType
from pyatlan_v9.models import DataStudioAsset
from tests_v9.unit.model.constants import (
    CONNECTOR_NAME,
    DATASTUDIO_CONNECTION_QUALIFIED_NAME,
    QUALIFIED_NAME_REPORT,
    QUALIFIED_NAME_SOURCE,
    REPORT_NAME,
    SOURCE_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, data_studio_asset_type, message",
    [
        (
            None,
            DATASTUDIO_CONNECTION_QUALIFIED_NAME,
            GoogleDatastudioAssetType.REPORT,
            "name is required",
        ),
        (
            REPORT_NAME,
            None,
            GoogleDatastudioAssetType.REPORT,
            "connection_qualified_name is required",
        ),
        (
            REPORT_NAME,
            DATASTUDIO_CONNECTION_QUALIFIED_NAME,
            None,
            "data_studio_asset_type is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    connection_qualified_name: str,
    data_studio_asset_type: GoogleDatastudioAssetType,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DataStudioAsset.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            data_studio_asset_type=data_studio_asset_type,
        )


def test_creator_report():
    """Test creator for REPORT asset type."""
    sut = DataStudioAsset.creator(
        name=REPORT_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.REPORT,
    )

    assert sut.name == REPORT_NAME
    assert sut.connection_qualified_name == DATASTUDIO_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == QUALIFIED_NAME_REPORT
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.data_studio_asset_type == GoogleDatastudioAssetType.REPORT


def test_creator_data_source():
    """Test creator for DATA_SOURCE asset type."""
    sut = DataStudioAsset.creator(
        name=SOURCE_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.DATA_SOURCE,
    )

    assert sut.name == SOURCE_NAME
    assert sut.connection_qualified_name == DATASTUDIO_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == QUALIFIED_NAME_SOURCE
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.data_studio_asset_type == GoogleDatastudioAssetType.DATA_SOURCE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, QUALIFIED_NAME_REPORT, "qualified_name is required"),
        (REPORT_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DataStudioAsset.updater(qualified_name=qualified_name, name=name)


def test_updater_report():
    """Test updater for report asset qualified name."""
    sut = DataStudioAsset.updater(
        qualified_name=QUALIFIED_NAME_REPORT, name=REPORT_NAME
    )

    assert sut.qualified_name == QUALIFIED_NAME_REPORT
    assert sut.name == REPORT_NAME


def test_updater_data_source():
    """Test updater for data source asset qualified name."""
    sut = DataStudioAsset.updater(
        qualified_name=QUALIFIED_NAME_SOURCE, name=SOURCE_NAME
    )

    assert sut.qualified_name == QUALIFIED_NAME_SOURCE
    assert sut.name == SOURCE_NAME


def test_trim_to_required_report():
    """Test trim_to_required retains only required fields for report."""
    sut = DataStudioAsset.creator(
        name=REPORT_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.REPORT,
    ).trim_to_required()

    assert sut.name == REPORT_NAME
    assert sut.qualified_name == QUALIFIED_NAME_REPORT


def test_trim_to_required_data_source():
    """Test trim_to_required retains only required fields for data source."""
    sut = DataStudioAsset.creator(
        name=SOURCE_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.DATA_SOURCE,
    ).trim_to_required()

    assert sut.name == SOURCE_NAME
    assert sut.qualified_name == QUALIFIED_NAME_SOURCE
