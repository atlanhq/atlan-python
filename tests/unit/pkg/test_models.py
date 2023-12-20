from pyatlan.pkg.models import NamePathS3Tuple

LABEL = "Some label"
HELP = "some help"
PLACEHOLDER = "some placeholder"
TITLE = "some title"
DESCRIPTION = "some description"


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
