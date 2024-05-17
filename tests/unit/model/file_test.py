import pytest

from pyatlan.model.assets import File
from pyatlan.model.enums import AtlanConnectorType, FileType
from tests.unit.model.constants import (
    FILE_CONNECTION_QUALIFIED_NAME,
    FILE_NAME,
    FILE_QUALIFIED_NAME,
)

FILE_TYPE = FileType.PDF


@pytest.mark.parametrize(
    "name, connection_qualified_name, file_type, msg",
    [
        (None, FILE_CONNECTION_QUALIFIED_NAME, FILE_TYPE, "name is required"),
        (FILE_NAME, None, FILE_TYPE, "connection_qualified_name is required"),
        ("", FILE_CONNECTION_QUALIFIED_NAME, FILE_TYPE, "name cannot be blank"),
        (FILE_NAME, "", FILE_TYPE, "connection_qualified_name cannot be blank"),
        (FILE_NAME, FILE_CONNECTION_QUALIFIED_NAME, None, "file_type is required"),
        (FILE_NAME, FILE_CONNECTION_QUALIFIED_NAME, "", "file_type cannot be blank"),
    ],
)
def test__create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, file_type, msg
):
    with pytest.raises(ValueError, match=msg):
        File.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            file_type=file_type,
        )


def test_create_with_required_parameters():
    attributes = File.create(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )
    assert attributes.name == FILE_NAME
    assert attributes.connection_qualified_name == FILE_CONNECTION_QUALIFIED_NAME
    assert attributes.qualified_name == FILE_QUALIFIED_NAME
    assert attributes.connector_name == AtlanConnectorType.get_connector_name(
        FILE_CONNECTION_QUALIFIED_NAME
    )


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FILE_QUALIFIED_NAME, "qualified_name is required"),
        (FILE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        File.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = File.create_for_modification(
        qualified_name=FILE_QUALIFIED_NAME, name=FILE_NAME
    )

    assert sut.qualified_name == FILE_QUALIFIED_NAME
    assert sut.name == FILE_NAME


def test_trim_to_required():
    sut = File.create_for_modification(
        qualified_name=FILE_QUALIFIED_NAME, name=FILE_NAME
    ).trim_to_required()

    assert sut.qualified_name == FILE_QUALIFIED_NAME
    assert sut.name == FILE_NAME
