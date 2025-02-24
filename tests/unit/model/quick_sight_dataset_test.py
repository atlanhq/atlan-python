import pytest

from pyatlan.model.assets import QuickSightDataset
from pyatlan.model.enums import QuickSightDatasetImportMode
from tests.unit.model.constants import (
    QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    QUICK_SIGHT_CONNECTOR_TYPE,
    QUICK_SIGHT_FOLDER_SET,
    QUICK_SIGHT_ID,
    QUICK_SIGHT_NAME,
    QUICK_SIGHT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, quick_sight_id, message",
    [
        (
            None,
            QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
            QUICK_SIGHT_ID,
            "name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            None,
            QUICK_SIGHT_ID,
            "connection_qualified_name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
            None,
            "quick_sight_id is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, quick_sight_id: str, message: str
):
    with pytest.raises(ValueError, match=message):
        QuickSightDataset.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            quick_sight_id=quick_sight_id,
        )


def test_creator():
    sut = QuickSightDataset.creator(
        name=QUICK_SIGHT_NAME,
        connection_qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
        quick_sight_id=QUICK_SIGHT_ID,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.connection_qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.quick_sight_id == QUICK_SIGHT_ID
    assert sut.qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE


def test_overload_creator():
    sut = QuickSightDataset.creator(
        name=QUICK_SIGHT_NAME,
        connection_qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
        quick_sight_id=QUICK_SIGHT_ID,
        quick_sight_dataset_import_mode=QuickSightDatasetImportMode.DIRECT_QUERY,
        quick_sight_dataset_folders=QUICK_SIGHT_FOLDER_SET,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.connection_qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.quick_sight_id == QUICK_SIGHT_ID
    assert (
        sut.quick_sight_dataset_import_mode == QuickSightDatasetImportMode.DIRECT_QUERY
    )
    assert sut.qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE


def test_updater():
    sut = QuickSightDataset.updater(
        qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME, name=QUICK_SIGHT_NAME
    )

    assert sut.qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.name == QUICK_SIGHT_NAME


def test_trim_to_required():
    sut = QuickSightDataset.updater(
        name=QUICK_SIGHT_NAME, qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
