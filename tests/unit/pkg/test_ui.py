from typing import Dict

import pytest
from pydantic.v1 import ValidationError

from pyatlan.pkg.ui import UIConfig, UIRule, UIStep
from pyatlan.pkg.widgets import AbstractUIElement, TextInput

WHEN_INPUTS_VALUE = "advanced"

WHEN_INPUTS_KEY = "control_config_strategy"

REQUIRED = ["asset_types"]

WHEN_INPUTS = {WHEN_INPUTS_KEY: WHEN_INPUTS_VALUE}

TITLE = "Some Title"
DESCRIPTION = "Some description"
HELP = "some help"
PLACEHOLDER = "some placeholder"
LABEL = "Some label"


@pytest.fixture()
def text_input() -> TextInput:
    return TextInput(label="Qualified name prefix")


@pytest.fixture()
def inputs(text_input: TextInput) -> Dict[str, AbstractUIElement]:
    return {"qn_prefix": text_input}


@pytest.fixture()
def ui_step(inputs) -> UIStep:
    return UIStep(title=TITLE, inputs=inputs)


@pytest.fixture()
def ui_rule() -> UIRule:
    return UIRule(when_inputs=WHEN_INPUTS, required=REQUIRED)


@pytest.fixture()
def good_or_bad_step(request, ui_step):
    if request.param == "good":
        return [ui_step]
    else:
        return None


@pytest.fixture()
def good_or_bad_rule(request, ui_rule):
    if request.param == "good":
        return [ui_rule]
    else:
        return 1


class TestUIConfig:
    def test_constructor(self, ui_step, ui_rule):
        sut = UIConfig(steps=[ui_step], rules=[ui_rule])
        assert sut.rules == [ui_rule]
        assert sut.steps == [ui_step]
        for key, value in ui_step.inputs.items():
            assert key in sut.properties
            assert sut.properties[key] == value

    @pytest.mark.parametrize(
        "good_or_bad_step, good_or_bad_rule, msg",
        [
            (
                "good",
                "bad",
                r"1 validation error for Init\nrules\n  value is not a valid list",
            ),
            (
                "bad",
                "good",
                r"1 validation error for Init\nsteps\n  none is not an allowed value",
            ),
        ],
        indirect=["good_or_bad_step", "good_or_bad_rule"],
    )
    def test_validation(self, good_or_bad_step, good_or_bad_rule, msg):
        with pytest.raises(ValidationError, match=msg):
            UIConfig(steps=good_or_bad_step, rules=good_or_bad_rule)


class TestUIRule:
    def test_constructor(self, text_input, inputs):
        sut = UIRule(when_inputs=WHEN_INPUTS, required=REQUIRED)
        assert sut.properties == {WHEN_INPUTS_KEY: {"const": WHEN_INPUTS_VALUE}}
        assert sut.required == REQUIRED
        assert sut.when_inputs == WHEN_INPUTS

    @pytest.mark.parametrize(
        "when_inputs, required, msg",
        [
            (
                {1: "kjk"},
                REQUIRED,
                r"1 validation error for Init\nwhen_inputs -> __key__\n  str type expected",
            ),
            (
                WHEN_INPUTS,
                [1],
                r"1 validation error for Init\nrequired -> 0\n  str type expected",
            ),
        ],
    )
    def test_validation(self, when_inputs, required, msg):
        with pytest.raises(ValidationError, match=msg):
            UIRule(when_inputs=when_inputs, required=required)


class TestUIStep:
    @pytest.mark.parametrize(
        "an_input",
        [
            "APITokenSelector",
            "BooleanInput",
            "ConnectionCreator",
            "ConnectionSelector",
            "ConnectorTypeSelector",
            "DateInput",
            "DropDown",
            "FileUploader",
            "KeygenInput",
            "MultipleGroups",
            "MultipleUsers",
            "NumericInput",
            "PasswordInput",
            "Radio",
            "SingleGroup",
            "SingleUser",
            "TextInput",
        ],
        indirect=True,
    )
    def test_contstructor(self, an_input):
        UIStep(title=TITLE, inputs={"an_input": an_input})

    def test_constructor_with_defaults(self, text_input, inputs):
        sut = UIStep(title=TITLE, inputs=inputs)

        assert sut.title == TITLE
        assert sut.inputs == inputs
        assert sut.description == ""
        assert sut.id == TITLE.replace(" ", "_").lower()
        assert sut.properties == list(inputs.keys())

    def test_constructor_with_overrides(self, text_input, inputs):
        sut = UIStep(title=TITLE, inputs=inputs, description=DESCRIPTION)

        assert sut.title == TITLE
        assert sut.inputs == inputs
        assert sut.description == DESCRIPTION
        assert sut.id == TITLE.replace(" ", "_").lower()
        assert sut.properties == list(inputs.keys())

    @pytest.mark.parametrize(
        "title, input, description, msg",
        [
            (
                None,
                {"qn_prefix": TextInput(label="Qualified name prefix")},
                "",
                r"1 validation error for Init\ntitle\n  none is not an allowed value",
            ),
            (
                1,
                {"qn_prefix": TextInput(label="Qualified name prefix")},
                "",
                r"1 validation error for Init\ntitle\n  str type expected",
            ),
            (
                TITLE,
                {"qn_prefix": "oioi"},
                "",
                r"18 validation errors for Init\ninputs -> qn_prefix\n  instance of APITokenSelector, tuple or dict "
                r"expected",
            ),
            (
                TITLE,
                {"qn_prefix": TextInput(label="Qualified name prefix")},
                None,
                r"1 validation error for Init\ndescription\n  none is not an allowed value",
            ),
            (
                TITLE,
                {"qn_prefix": TextInput(label="Qualified name prefix")},
                1,
                r"1 validation error for Init\ndescription\n  str type expected",
            ),
        ],
    )
    def test_validation(self, title, input, description, msg):
        with pytest.raises(ValidationError, match=msg):
            UIStep(title=title, inputs=input, description=description)
