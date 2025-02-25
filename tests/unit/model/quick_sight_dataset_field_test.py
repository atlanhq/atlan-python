import pytest

from pyatlan.model.assets import QuickSightDatasetField
from pyatlan.model.enums import QuickSightDatasetFieldType
from tests.unit.model.constants import (
    QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    QUICK_SIGHT_CONNECTOR_TYPE,
    QUICK_SIGHT_DATASET_FIELD_QUALIFIED_NAME,
    QUICK_SIGHT_ID_DATASET_FEILD,
    QUICK_SIGHT_NAME,
    QUICK_SIGHT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, quick_sight_dataset_qualified_name, quick_sight_id, message",
    [
        (
            None,
            QUICK_SIGHT_QUALIFIED_NAME,
            QUICK_SIGHT_ID_DATASET_FEILD,
            "name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            None,
            QUICK_SIGHT_ID_DATASET_FEILD,
            "quick_sight_dataset_qualified_name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            QUICK_SIGHT_QUALIFIED_NAME,
            None,
            "quick_sight_id is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    quick_sight_dataset_qualified_name: str,
    quick_sight_id: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        QuickSightDatasetField.creator(
            name=name,
            quick_sight_dataset_qualified_name=quick_sight_dataset_qualified_name,
            quick_sight_id=quick_sight_id,
        )


def test_creator():
    sut = QuickSightDatasetField.creator(
        name=QUICK_SIGHT_NAME,
        quick_sight_dataset_qualified_name=QUICK_SIGHT_QUALIFIED_NAME,
        quick_sight_id=QUICK_SIGHT_ID_DATASET_FEILD,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.quick_sight_dataset_qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.quick_sight_id == QUICK_SIGHT_ID_DATASET_FEILD
    assert sut.qualified_name == QUICK_SIGHT_DATASET_FIELD_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE


def test_overload_creator():
    sut = QuickSightDatasetField.creator(
        name=QUICK_SIGHT_NAME,
        quick_sight_dataset_qualified_name=QUICK_SIGHT_QUALIFIED_NAME,
        quick_sight_id=QUICK_SIGHT_ID_DATASET_FEILD,
        quick_sight_dataset_field_type=QuickSightDatasetFieldType.STRING,
        connection_qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.quick_sight_dataset_qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.quick_sight_id == QUICK_SIGHT_ID_DATASET_FEILD
    assert sut.qualified_name == QUICK_SIGHT_DATASET_FIELD_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE
    assert sut.connection_qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.quick_sight_dataset_field_type == QuickSightDatasetFieldType.STRING


def test_updater():
    sut = QuickSightDatasetField.updater(
        qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME, name=QUICK_SIGHT_NAME
    )

    assert sut.qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.name == QUICK_SIGHT_NAME


def test_trim_to_required():
    sut = QuickSightDatasetField.updater(
        name=QUICK_SIGHT_NAME, qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
