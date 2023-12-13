# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import abc
from dataclasses import dataclass

# from dataclasses import dataclass
from typing import Optional

from pydantic import StrictBool, StrictInt, StrictStr, validate_arguments

# from pydantic.dataclasses import dataclass


@dataclass
class Widget(abc.ABC):
    widget: str
    label: str
    hidden: bool = False
    help: str = ""
    placeholder: str = ""
    grid: int = 8


@dataclass
class UIElement(abc.ABC):
    type: str
    required: bool
    ui: Optional[Widget]


@dataclass
class UIElementWithEnum(UIElement):
    default: Optional[str]
    enum: list[str]
    enum_names: list[str]

    def __init__(
        self,
        type: str,
        required: bool,
        possible_values: dict[str, str],
        ui: Optional[Widget] = None,
    ):
        super().__init__(type=type, required=required, ui=ui)
        self.enum = list(possible_values.keys())
        self.enum_names = list(possible_values.values())


@dataclass
class APITokenSelectorWidget(Widget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        grid: int = 4,
    ):
        super().__init__(
            widget="apiTokenSelect",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )


@dataclass
class APITokenSelector(UIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 4,
    ):
        widget = APITokenSelectorWidget(
            label=label, hidden=hidden, help=help, grid=grid
        )
        super().__init__(type="string", required=required, ui=widget)
