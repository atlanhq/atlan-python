import pytest

from pyatlan.model.assets import Readme, Table
from tests.unit.model.constants import SCHEMA_QUALIFIED_NAME, TABLE_NAME

README_NAME = f"{TABLE_NAME}/readme"
README_QUALIFIED_NAME = "2f8d68d2-8cd7-41e0-9d3b-cf27cd30f7ef/readme"


@pytest.mark.parametrize(
    "asset, content, asset_name, error, message",
    [
        (None, "stuff", None, ValueError, "asset is required"),
        (
            Table.create(
                name=TABLE_NAME,
                schema_qualified_name=SCHEMA_QUALIFIED_NAME,
            ),
            None,
            None,
            ValueError,
            "content is required",
        ),
        (
            Table(),
            "stuff",
            None,
            ValueError,
            "asset_name is required when name is not available from asset",
        ),
    ],
)
def test_create_readme_without_required_parameters_raises_exception(
    asset, content, asset_name, error, message
):
    with pytest.raises(error, match=message):
        Readme.create(asset=asset, content=content, asset_name=asset_name)


@pytest.mark.parametrize(
    "asset, content, asset_name, expected_name",
    [
        (
            Table.create(
                name=TABLE_NAME,
                schema_qualified_name=SCHEMA_QUALIFIED_NAME,
            ),
            "<h1>stuff</h1>",
            None,
            TABLE_NAME,
        ),
        (
            Table(attributes=Table.Attributes()),
            "<h1>stuff</h1>",
            TABLE_NAME,
            TABLE_NAME,
        ),
    ],
)
def test_create_readme(asset, content, asset_name, expected_name):
    readme = Readme.create(asset=asset, content=content, asset_name=asset_name)
    assert readme.qualified_name == f"{asset.guid}/readme"
    assert readme.name == f"{expected_name} Readme"
    assert readme.attributes.asset == asset
    assert readme.description == content


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, README_QUALIFIED_NAME, "qualified_name is required"),
        (README_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Readme.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Readme.create_for_modification(
        qualified_name=README_QUALIFIED_NAME, name=README_NAME
    )

    assert sut.qualified_name == README_QUALIFIED_NAME
    assert sut.name == README_NAME


def test_trim_to_required():
    sut = Readme.create_for_modification(
        qualified_name=README_QUALIFIED_NAME, name=README_NAME
    ).trim_to_required()

    assert sut.qualified_name == README_QUALIFIED_NAME
    assert sut.name == README_NAME
