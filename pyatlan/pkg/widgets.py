# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import abc
from dataclasses import dataclass, field

# from dataclasses import dataclass
from typing import Optional

from pydantic import StrictBool, StrictInt, StrictStr, validate_arguments

# from pydantic.dataclasses import dataclass


@dataclass
class Widget(abc.ABC):
    widget: str
    label: str
    hidden: bool = False
    help_: str = ""
    placeholder: str = ""
    grid: int = 8


@dataclass
class UIElement(abc.ABC):
    type_: str
    required: bool
    ui: Optional[Widget]


@dataclass
class UIElementWithEnum(UIElement):
    default: Optional[str]
    enum: list[str]
    enum_names: list[str]

    def __init__(
        self,
        type_: str,
        required: bool,
        possible_values: dict[str, str],
        ui: Optional[Widget] = None,
    ):
        super().__init__(type_=type_, required=required, ui=ui)
        self.enum = list(possible_values.keys())
        self.enum_names = list(possible_values.values())


@dataclass
class APITokenSelectorWidget(Widget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help_: str = "",
        grid: int = 4,
    ):
        super().__init__(
            widget="apiTokenSelect",
            label=label,
            hidden=hidden,
            help_=help_,
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
        help_: StrictStr = "",
        grid: StrictInt = 4,
    ):
        widget = APITokenSelectorWidget(
            label=label, hidden=hidden, help_=help_, grid=grid
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclass
class BooleanInputWidget(Widget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help_: str = "",
        placeholder: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="boolean",
            label=label,
            hidden=hidden,
            help_=help_,
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
        help_: StrictStr = "",
        grid: StrictInt = 8,
    ):
        widget = BooleanInputWidget(label=label, hidden=hidden, help_=help_, grid=grid)
        super().__init__(type_="boolean", required=required, ui=widget)


@dataclass
class ConnectionCreatorWidget(Widget):
    def __init__(
        self, label: str, hidden: bool = False, help_: str = "", placeholder: str = ""
    ):
        super().__init__(
            widget="connection",
            label=label,
            hidden=hidden,
            help_=help_,
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
        help_: StrictStr = "",
        placeholder: StrictStr = "",
    ):
        widget = ConnectionCreatorWidget(
            label=label, hidden=hidden, help_=help_, placeholder=placeholder
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclass
class ConnectionSelectorWidget(Widget):
    start: int = 1

    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help_: str = "",
        placeholder: str = "",
        grid: int = 4,
        start: int = 1,
    ):
        super().__init__(
            widget="connectionSelector",
            label=label,
            hidden=hidden,
            help_=help_,
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
        help_: StrictStr = "",
        placeholder: StrictStr = "",
        grid: StrictInt = 4,
        start: StrictInt = 1,
    ):
        widget = ConnectionSelectorWidget(
            label=label,
            hidden=hidden,
            help_=help_,
            placeholder=placeholder,
            grid=grid,
            start=start,
        )
        super().__init__(type_="string", required=required, ui=widget)
        self.start = start


@dataclass
class ConnectorTypeSelectorWidget(Widget):
    start: int = 1

    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help_: str = "",
        grid: int = 4,
        start: int = 1,
    ):
        super().__init__(
            widget="sourceConnectionSelector",
            label=label,
            hidden=hidden,
            help_=help_,
            grid=grid,
        )
        self.start = start


@dataclass
class ConnectorTypeSelector(UIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help_: StrictStr = "",
        grid: StrictInt = 4,
        start: StrictInt = 1,
    ):
        widget = ConnectorTypeSelectorWidget(
            label=label,
            hidden=hidden,
            help_=help_,
            grid=grid,
            start=start,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclass
class DateInputWidget(Widget):
    min_: int = -14
    max_: int = 0
    default: int = 0
    start: int = 1

    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help_: str = "",
        min_: int = -14,
        max_: int = 0,
        default: int = 0,
        start: int = 1,
        grid: int = 4,
    ):
        super().__init__(
            widget="date", label=label, hidden=hidden, help_=help_, grid=grid
        )
        self.start = start
        self.max_ = max_
        self.min_ = min_
        self.default = default


@dataclass
class DateInput(UIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help_: StrictStr = "",
        min_: StrictInt = -14,
        max_: StrictInt = 0,
        default: StrictInt = 0,
        start: StrictInt = 1,
        grid: StrictInt = 8,
    ):
        widget = DateInputWidget(
            label=label,
            hidden=hidden,
            help_=help_,
            min_=min_,
            max_=max_,
            default=default,
            start=start,
            grid=grid,
        )
        super().__init__(type_="number", required=required, ui=widget)


@dataclass
class DropDownWidget(Widget):
    mode: str = ""

    def __init__(
        self,
        label: str,
        mode: str,
        hidden: bool = False,
        help_: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="select",
            label=label,
            hidden=hidden,
            help_=help_,
            grid=grid,
        )
        self.mode = mode


@dataclass
class DropDown(UIElementWithEnum):
    possible_values: dict[str, str]

    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        possible_values: dict[str, str],
        required: StrictBool = False,
        hidden: StrictBool = False,
        help_: StrictStr = "",
        multi_select: StrictBool = False,
        grid: StrictInt = 8,
    ):
        widget = DropDownWidget(
            label=label,
            mode="multiple" if multi_select else "",
            hidden=hidden,
            help_=help_,
            grid=grid,
        )
        super().__init__(
            type_="string",
            required=required,
            possible_values=possible_values,
            ui=widget,
        )
        self.possible_values = possible_values


@dataclass
class FileUploaderWidget(Widget):
    file_types: list[str] = field(default_factory=list)

    def __init__(
        self,
        label: str,
        file_types: list[str],
        hidden: bool = False,
        help_: str = "",
        placeholder: str = "",
    ):
        super().__init__(
            widget="fileUpload",
            label=label,
            hidden=hidden,
            help_=help_,
            placeholder=placeholder,
        )
        self.file_types = file_types


@dataclass
class FileUploader(UIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        file_types: list[str],
        required: StrictBool = False,
        hidden: StrictBool = False,
        help_: StrictStr = "",
        placeholder: StrictStr = "",
    ):
        widget = FileUploaderWidget(
            label=label,
            file_types=file_types,
            hidden=hidden,
            help_=help_,
            placeholder=placeholder,
        )
        super().__init__(type_="string", required=required, ui=widget)
