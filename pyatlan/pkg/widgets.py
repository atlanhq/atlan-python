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


@dataclass
class BooleanInputWidget(Widget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        placeholder: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="boolean",
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
        )


@dataclass
class BooleanInput(UIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        widget = BooleanInputWidget(label=label, hidden=hidden, help=help, grid=grid)
        super().__init__(type="boolean", required=required, ui=widget)


@dataclass
class ConnectionCreatorWidget(Widget):
    def __init__(
        self, label: str, hidden: bool = False, help: str = "", placeholder: str = ""
    ):
        super().__init__(
            widget="connection",
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
        )


@dataclass
class ConnectionCreator(UIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        placeholder: StrictStr = "",
    ):
        widget = ConnectionCreatorWidget(
            label=label, hidden=hidden, help=help, placeholder=placeholder
        )
        super().__init__(type="string", required=required, ui=widget)


@dataclass
class ConnectionSelectorWidget(Widget):
    start: int = 1

    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        placeholder: str = "",
        grid: int = 4,
        start: int = 1,
    ):
        super().__init__(
            widget="connectionSelector",
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
        )
        self.start = start


@dataclass
class ConnectionSelector(UIElement):
    start: StrictInt = 1

    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        placeholder: StrictStr = "",
        grid: StrictInt = 4,
        start: StrictInt = 1,
    ):
        widget = ConnectionSelectorWidget(
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
            start=start,
        )
        super().__init__(type="string", required=required, ui=widget)
        self.start = start
