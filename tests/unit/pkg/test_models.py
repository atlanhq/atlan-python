from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic.v1 import ValidationError

from pyatlan.pkg.models import CustomPackage, PackageConfig, PackageWriter, generate
from pyatlan.pkg.ui import UIConfig, UIStep
from pyatlan.pkg.widgets import TextInput

LABEL = "Some label"
HELP = "some help"
PLACEHOLDER = "some placeholder"
TITLE = "some title"
DESCRIPTION = "some description"


@pytest.fixture()
def labels():
    return {"first": "one"}


@pytest.fixture()
def annotations():
    return {"first": "one"}


@pytest.fixture()
def good_or_bad_labels(request, labels):
    if request.param == "good":
        return labels
    else:
        return {1: 1}


@pytest.fixture()
def good_or_bad_annotations(request, annotations):
    if request.param == "good":
        return annotations
    else:
        return {1: 1}


@pytest.fixture()
def mock_package_writer():
    with patch("pyatlan.pkg.models.PackageWriter") as package_writer:
        yield package_writer.return_value


@pytest.fixture()
def custom_package():
    text_input = TextInput(
        label="Qualified name prefix",
        help="Provide the starting name for schemas from which to propagate ownership",
        required=False,
        placeholder="default/snowflake/1234567890",
        grid=4,
    )
    ui_step = UIStep(
        title="Configuration",
        description="Owner propagation configuration",
        inputs={"qn_prefix": text_input},
    )
    return CustomPackage(
        package_id="@csa/owner-propagator",
        package_name="Owner Propagator",
        description="Propagate owners from schema downwards.",
        docs_url="https://solutions.atlan.com/",
        icon_url="https://assets.atlan.com/assets/ph-user-switch-light.svg",
        container_image="ghcr.io/atlanhq/csa-owner-propagator:1",
        container_command=["doit"],
        ui_config=UIConfig(steps=[ui_step]),
    )


@pytest.fixture()
def good_or_bad_custom_package(request, custom_package):
    if request.param == "good":
        return custom_package
    else:
        return None


class TestPackageConfig:
    @pytest.mark.parametrize(
        "good_or_bad_labels, good_or_bad_annotations, msg",
        [
            (
                "good",
                "bad",
                r"1 validation error for PackageConfig\nannotations -> __key__\n  str type expected",
            ),
            (
                "bad",
                "good",
                r"1 validation error for PackageConfig\nlabels -> __key__\n  str type expected",
            ),
        ],
        indirect=["good_or_bad_labels", "good_or_bad_annotations"],
    )
    def test_validation(self, good_or_bad_labels, good_or_bad_annotations, msg):
        with pytest.raises(ValidationError, match=msg):
            PackageConfig(
                labels=good_or_bad_labels, annotations=good_or_bad_annotations
            )

    def test_constructor(self, labels, annotations):
        sut = PackageConfig(labels=labels, annotations=annotations)
        assert sut.labels == labels
        assert sut.annotations == annotations


class TestPackageWriter:
    def test_constructor(self, custom_package, tmp_path):
        sut = PackageWriter(pkg=custom_package, path=tmp_path)

        assert sut.path == tmp_path
        assert sut.pkg == custom_package

    def test_create_package(self, custom_package, tmp_path: Path):
        sut = PackageWriter(pkg=custom_package, path=tmp_path)

        sut.create_package()
        root_dir = tmp_path / custom_package.name
        assert root_dir.exists()
        assert (root_dir / "index.js").exists()
        assert (root_dir / "package.json").exists()
        configmaps = root_dir / "configmaps"
        assert configmaps.exists()
        assert (configmaps / "default.yaml").exists()
        assert (root_dir / "templates").exists()


@pytest.mark.parametrize(
    "good_or_bad_custom_package, path, operation, msg",
    [
        (
            "bad",
            ".",
            "package",
            r"1 validation error for Generate\npkg\n  none is not an allowed value",
        ),
        (
            "good",
            1,
            "config",
            r"1 validation error for Generate\npath\n  value is not a valid path",
        ),
        (
            "good",
            ".",
            "bad",
            r"1 validation error for Generate\noperation\n  unexpected value; permitted: 'package', 'config'",
        ),
    ],
    indirect=["good_or_bad_custom_package"],
)
def test_generate_parameter_validation(
    good_or_bad_custom_package, path, operation, msg
):
    with pytest.raises(ValidationError, match=msg):
        generate(pkg=good_or_bad_custom_package, path=path, operation=operation)


def test_generate_with_operation_package(mock_package_writer, custom_package):
    generate(pkg=custom_package, path="..", operation="package")

    mock_package_writer.create_package.assert_called()


def test_generate_with_operation_config(mock_package_writer, custom_package):
    generate(pkg=custom_package, path="..", operation="config")

    mock_package_writer.create_config.assert_called()
