import logging
from dataclasses import dataclass, field
from typing import Any, Union

from pydantic import StrictStr, validate_arguments

from pyatlan.pkg.widgets import (
    APITokenSelector,
    BooleanInput,
    ConnectionCreator,
    ConnectorTypeSelector,
    DateInput,
    DropDown,
    FileUploader,
    KeygenInput,
    MultipleGroups,
    MultipleUsers,
    NumericInput,
    PasswordInput,
    Radio,
    SingleGroup,
    SingleUser,
    TextInput,
)

LOGGER = logging.getLogger(__name__)

UIElement = Union[
    APITokenSelector,
    BooleanInput,
    ConnectionCreator,
    ConnectorTypeSelector,
    DateInput,
    DropDown,
    FileUploader,
    KeygenInput,
    MultipleGroups,
    MultipleUsers,
    NumericInput,
    PasswordInput,
    Radio,
    SingleGroup,
    SingleUser,
    TextInput,
]


@dataclass()
class UIStep:
    title: str
    inputs: dict[str, UIElement]
    description: str = ""
    id: str = ""
    properties: list[str] = field(default_factory=list)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        title: StrictStr,
        inputs: dict[StrictStr, UIElement],
        description: StrictStr = "",
    ):
        self.title = title
        self.inputs = inputs
        self.description = description
        self.id = title.replace(" ", "_").lower()
        self.properties = list(self.inputs.keys())


@dataclass()
class UIRule:
    when_inputs: dict[str, str]
    required: list[str]
    properties: dict[str, dict[str, str]] = field(default_factory=dict)

    @validate_arguments()
    def __init__(
        self, when_inputs: dict[StrictStr, StrictStr], required: list[StrictStr]
    ):
        """
        Configure basic UI rules that when the specified inputs have specified values, certain other fields become
        required.

        :param when_inputs: mapping from input ID to value for the step
        :param required: list of input IDs that should become required when the inputs all match

        """
        self.when_inputs = when_inputs
        self.required = required
        self.properties = {key: {"const": value} for key, value in when_inputs.items()}


@dataclass()
class UIConfig:
    steps: list[UIStep]
    rules: list[Any]
    properties: dict[str, UIElement] = field(default_factory=dict)

    @validate_arguments()
    def __init__(self, steps: list[UIStep], rules: list[Any]):
        self.steps = steps
        self.rules = rules
        self.properties = {}
        for step in steps:
            for key, value in step.inputs.items():
                if key in self.properties:
                    LOGGER.warning("Duplicate key found accross steps: %s", key)
                self.properties[key] = value
