import pytest

from pyatlan.model.assets import DataStudioAsset
from pyatlan.model.enums import GoogleDatastudioAssetType
from tests.unit.model.constants import (
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
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    connection_qualified_name: str,
    data_studio_asset_type: GoogleDatastudioAssetType,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        DataStudioAsset.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            data_studio_asset_type=data_studio_asset_type,
        )


# Test create method for data studio asset type report
def test_create_report():
    sut = DataStudioAsset.create(
        name=REPORT_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.REPORT,
    )

    assert sut.name == REPORT_NAME
    assert sut.connection_qualified_name == DATASTUDIO_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.data_studio_asset_type == GoogleDatastudioAssetType.REPORT


# Test create method for data studio asset type source
def test_create_data_source():
    sut = DataStudioAsset.create(
        name=SOURCE_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.DATA_SOURCE,
    )

    assert sut.name == SOURCE_NAME
    assert sut.connection_qualified_name == DATASTUDIO_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.data_studio_asset_type == GoogleDatastudioAssetType.DATA_SOURCE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, QUALIFIED_NAME_REPORT, "qualified_name is required"),
        (REPORT_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataStudioAsset.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification_report():
    sut = DataStudioAsset.create_for_modification(
        qualified_name=QUALIFIED_NAME_REPORT, name=REPORT_NAME
    )

    assert sut.qualified_name == QUALIFIED_NAME_REPORT
    assert sut.name == REPORT_NAME


def test_create_for_modification_data_source():
    sut = DataStudioAsset.create_for_modification(
        qualified_name=QUALIFIED_NAME_SOURCE, name=SOURCE_NAME
    )

    assert sut.qualified_name == QUALIFIED_NAME_SOURCE
    assert sut.name == SOURCE_NAME


def test_trim_to_required_report():
    sut = DataStudioAsset.create(
        name=REPORT_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.REPORT,
    ).trim_to_required()

    assert sut.name == REPORT_NAME
    assert sut.qualified_name


def test_trim_to_required_data_source():
    sut = DataStudioAsset.create(
        name=SOURCE_NAME,
        connection_qualified_name=DATASTUDIO_CONNECTION_QUALIFIED_NAME,
        data_studio_asset_type=GoogleDatastudioAssetType.DATA_SOURCE,
    ).trim_to_required()

    assert sut.name == SOURCE_NAME
    assert sut.qualified_name
