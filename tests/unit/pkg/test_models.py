import pytest
from pydantic import ValidationError

from pyatlan.pkg.models import NamePathS3Tuple, PackageConfig

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


class TestNamePathS3Tuple:
    def test_constructor(self):
        sut = NamePathS3Tuple(input_name="something")

        assert sut.name == "something_s3"
        assert sut.path == "/tmp/something/{{inputs.parameters.something}}"
        assert sut.s3 == {"key": "{{inputs.parameters.something}}"}


class TestWorkflowInputs:
    def test_constructor(self, ui_step):
        pass
        # config = UIConfig(steps=[
        #     UIStep(title="Configuration",
        #            description="Owner propagation configuration",
        #            inputs={"assets_file": file_uploader})
        # ])
        # sut = WorkflowInputs(config=config, pkg_name="bob")bob
