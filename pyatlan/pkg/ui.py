import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from pydantic.v1 import Extra, StrictStr, validate_arguments
from pydantic.v1.json import pydantic_encoder

from pyatlan.pkg.widgets import (
    APITokenSelector,
    BooleanInput,
    ConnectionCreator,
    ConnectionSelector,
    ConnectorTypeSelector,
    Credential,
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
    ConnectionSelector,
    ConnectorTypeSelector,
    Credential,
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

TUIStep = TypeVar("TUIStep", bound="UIStep")


@dataclass()
class UIStep:
    title: str
    inputs: Dict[str, UIElement]
    description: str = ""
    id: str = ""
    properties: List[str] = field(default_factory=list)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        title: StrictStr,
        inputs: Dict[StrictStr, UIElement],
        description: StrictStr = "",
    ):
        self.title = title
        self.inputs = inputs
        self.description = description
        self.id = title.replace(" ", "_").lower()
        self.properties = list(self.inputs.keys())

    def to_json(self: TUIStep) -> str:
        @dataclass()
        class Inner:
            title: str
            description: str = ""
            id: str = ""
            properties: List[str] = field(default_factory=list)

        inner = Inner(
            title=self.title,
            description=self.description,
            id=self.id,
            properties=self.properties,
        )
        return json.dumps(inner, indent=2, default=pydantic_encoder)


TUIRule = TypeVar("TUIRule", bound="UIRule")


@dataclass()
class UIRule:
    when_inputs: Dict[str, str]
    required: List[str]
    properties: Dict[str, Dict[str, str]] = field(default_factory=dict)

    @validate_arguments()
    def __init__(
        self, when_inputs: Dict[StrictStr, StrictStr], required: List[StrictStr]
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

    def to_json(self: TUIRule) -> str:
        return json.dumps(
            {"properties": self.properties, "required": self.required},
            indent=2,
            default=pydantic_encoder,
        )


@dataclass()
class UIConfig:
    steps: List[UIStep]
    rules: List[Any] = field(default_factory=list)
    properties: Dict[str, UIElement] = field(default_factory=dict)

    @validate_arguments()
    def __init__(self, steps: List[UIStep], rules: Optional[List[Any]] = None):
        if rules is None:
            rules = []
        self.steps = steps
        self.rules = rules
        self.properties = {}
        for step in steps:
            for key, value in step.inputs.items():
                if key in self.properties:
                    LOGGER.warning("Duplicate key found across steps: %s", key)
                self.properties[key] = value

    @property
    def credentials(self) -> Optional[Tuple[str, UIElement]]:
        for step in self.steps:
            for key, value in step.inputs.items():
                if isinstance(value, Credential):
                    return (key, value)
        return None

    class Config:
        extra = Extra.forbid
