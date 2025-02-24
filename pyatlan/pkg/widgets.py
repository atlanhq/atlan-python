# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import abc
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from pydantic.v1 import (
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    dataclasses,
    validate_arguments,
)
from pydantic.v1.json import pydantic_encoder

Widget = Union[
    "APITokenSelectorWidget",
    "BooleanInputWidget",
    "ConnectionCreatorWidget",
    "ConnectionSelectorWidget",
    "ConnectorTypeSelectorWidget",
    "CredentialWidget",
    "DateInputWidget",
    "DropDownWidget",
    "FileUploaderWidget",
    "KeygenInputWidget",
    "MultipleGroupsWidget",
    "MultipleUsersWidget",
    "NumericInputWidget",
    "PasswordInputWidget",
    "RadioWidget",
    "SingleGroupWidget",
    "SingleUserWidget",
    "TextInputWidget",
]


@dataclasses.dataclass
class AbstractWidget(abc.ABC):
    widget: str
    label: str
    hidden: bool = False
    help: str = Field(default="")
    placeholder: str = ""
    grid: int = 8

    def to_json(self):
        return json.dumps(self, indent=2, default=pydantic_encoder)

    def to_nested(self, name: str) -> str:
        return f"{{{{=toJson(inputs.parameters.{name})}}}}"

    def to_env(self, name: str) -> str:
        return f"{{{{inputs.parameters.{name}}}}}"

    @property
    def parameter_value(self) -> str:
        return '""'

    @property
    def s3_artifact(self) -> bool:
        return False

    def get_validator(self, name: str):
        return f"{name}: str\n"


@dataclass
class AbstractUIElement(abc.ABC):
    type_: str
    required: bool
    ui: Optional[Widget]


@dataclass
class UIElementWithEnum(AbstractUIElement):
    enum: List[str]
    enum_names: List[str]
    default: Optional[str] = None
    possible_values: Dict[str, str] = field(default_factory=dict)

    def __init__(
        self,
        type_: str,
        required: bool,
        possible_values: Dict[str, str],
        ui: Optional[Widget] = None,
    ):
        super().__init__(type_=type_, required=required, ui=ui)
        self.enum = list(possible_values.keys())
        self.enum_names = list(possible_values.values())
        self.possible_values = possible_values


@dataclasses.dataclass
class APITokenSelectorWidget(AbstractWidget):
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
class APITokenSelector(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 4,
    ):
        """
        Widget that allows you to select an existing API token from a drop-down list, and returns the GUID of the
        selected API token.
        Note: currently only API tokens that were created by the user configuring the workflow will appear in the
        drop-down list.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = APITokenSelectorWidget(
            label=label, hidden=hidden, help=help, grid=grid
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class BooleanInputWidget(AbstractWidget):
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

    def to_nested(self, name: str) -> str:
        return f"{{{{inputs.parameters.{name}}}}}"

    @property
    def parameter_value(self) -> str:
        return "false"

    def get_validator(self, name: str):
        return f"{name}: bool = None\n"


@dataclass
class BooleanInput(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to choose either "Yes" or "No", and returns the value that was selected.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = BooleanInputWidget(label=label, hidden=hidden, help=help, grid=grid)
        super().__init__(type_="boolean", required=required, ui=widget)


@dataclasses.dataclass
class ConnectionCreatorWidget(AbstractWidget):
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

    def get_validator(self, name: str):
        return f"""{name}: Optional[Connection] = None
    _validate_{name} = validator(
    "{name}", pre=True, allow_reuse=True
    )(validate_connection)"""


@dataclass
class ConnectionCreator(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        placeholder: StrictStr = "",
    ):
        """
        Widget that allows you to create a new connection by providing a name and list of admins, and returns a string
        representation of the connection object that should be created.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param placeholder: example text to place within the widget to exemplify its use
        """
        widget = ConnectionCreatorWidget(
            label=label, hidden=hidden, help=help, placeholder=placeholder
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class ConnectionSelectorWidget(AbstractWidget):
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
class ConnectionSelector(AbstractUIElement):
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
        """
        Widget that allows you to select an existing connection from a drop-down list, and returns the qualified name
        of the selected connection.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param placeholder: example text to place within the widget to exemplify its use
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        :param start: TBC
        """
        widget = ConnectionSelectorWidget(
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
            start=start,
        )
        super().__init__(type_="string", required=required, ui=widget)
        self.start = start


@dataclasses.dataclass
class ConnectorTypeSelectorWidget(AbstractWidget):
    start: int = 1

    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        grid: int = 4,
        start: int = 1,
    ):
        super().__init__(
            widget="sourceConnectionSelector",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        self.start = start

    def get_validator(self, name: str):
        return f"""{name}: Optional[ConnectorAndConnection] = None
    _validate_{name} = validator(
    "{name}", pre=True, allow_reuse=True
    )(validate_connector_and_connection)"""


@dataclass
class ConnectorTypeSelector(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 4,
        start: StrictInt = 1,
    ):
        """
        Widget that allows you to select from the types of connectors that exist in the tenant
        (for example "Snowflake"), without needing to select a specific instance of a connection
        (for example, the "production" connection for Snowflake). Will return a string-encoded object giving the
        connection type that was selected and a list of all connections in the tenant that have that type.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        :aram start: TBC
        """
        widget = ConnectorTypeSelectorWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
            start=start,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class CredentialWidget(AbstractWidget):
    credential_type: str = ""

    def __init__(self, label: str, credential_type: str):
        super().__init__(
            widget="credential",
            label=label,
        )
        self.credential_type = credential_type

    def to_json(self):
        ret_val = super().to_json()
        return ret_val.replace("credential_type", "credentialType")


@dataclass
class Credential(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        credential_type: str,
    ):
        """
        Widget that allows you to embed the UI to obtain credentials for a connector defined in the repo
        marketplace-packages/packages/atlan/connectors

        :param label: name to show in the UI for the widget
        :param credential_type" a string containing the id of the desired connector for exaample
        csa-connectors-databricks or csa-connectors-s3
        """
        widget = CredentialWidget(
            label=label,
            credential_type=credential_type,
        )
        super().__init__(type_="string", required=True, ui=widget)


@dataclasses.dataclass
class DateInputWidget(AbstractWidget):
    min: int = -14
    max: int = 0
    default: int = 0
    start: int = 1

    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        min: int = -14,
        max: int = 0,
        default: int = 0,
        start: int = 1,
        grid: int = 4,
    ):
        super().__init__(
            widget="date", label=label, hidden=hidden, help=help, grid=grid
        )
        self.start = start
        self.max = max
        self.min = min
        self.default = default

    def to_nested(self, name: str) -> str:
        return f"{{{{inputs.parameters.{name}}}}}"

    @property
    def parameter_value(self) -> str:
        return "-1"

    def get_validator(self, name: str):
        return f"{name}: Optional[datetime] = None\n"


@dataclass
class DateInput(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        min: StrictInt = -14,
        max: StrictInt = 0,
        default: StrictInt = 0,
        start: StrictInt = 1,
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to enter or select a date (not including time) from a calendar, and returns the
        epoch-based number representing that selected date in seconds.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param min: an offset from today (0) that indicates how far back in the calendar can be selected
        (-1 is yesterday, 1 is tomorrow, and so on)
        :param max: an offset from today (0) that indicates how far forward in the calendar can be selected
        (-1 is yesterday, 1 is tomorrow, and so on)
         :param default: an offset from today that indicates the default date that should be selected in the calendar
         (0 is today, -1 is yesterday, 1 is tomorrow, and so on)
         :param start: TBC
         :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = DateInputWidget(
            label=label,
            hidden=hidden,
            help=help,
            min=min,
            max=max,
            default=default,
            start=start,
            grid=grid,
        )
        super().__init__(type_="number", required=required, ui=widget)


@dataclasses.dataclass
class DropDownWidget(AbstractWidget):
    mode: str = ""

    def __init__(
        self,
        label: str,
        mode: str,
        hidden: bool = False,
        help: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="select",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        self.mode = mode

    def get_validator(self, name: str):
        return f"""{name}: Optional[List[str]] = Field(default_factory=list)
    _validate_{name} = validator(
    "{name}", pre=True, allow_reuse=True
    )(validate_multiselect)"""


@dataclass
class DropDown(UIElementWithEnum):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        possible_values: Dict[str, str],
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        multi_select: StrictBool = False,
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to select from a drop-down of provided options.

        :param label: name to show in the UI for the widget
        :param possible_values: map of option keys to the value that will be display for each option in the drop-down
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param multi_select: whether multiple options can be selected (true) or only a single option (false)
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = DropDownWidget(
            label=label,
            mode="multiple" if multi_select else "",
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(
            type_="string",
            required=required,
            possible_values=possible_values,
            ui=widget,
        )


@dataclasses.dataclass
class FileUploaderWidget(AbstractWidget):
    accept: List[str] = field(default_factory=list)

    def __init__(
        self,
        label: str,
        accept: List[str],
        hidden: bool = False,
        help: str = "",
        placeholder: str = "",
    ):
        super().__init__(
            widget="fileUpload",
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
        )
        self.accept = accept

    def to_nested(self, name: str) -> str:
        return f'"/tmp/{name}/{{{{inputs.parameters.{name}}}}}"'  # noqa: S108

    @property
    def parameter_value(self) -> str:
        return '"argo-artifacts/atlan-update/last-run-timestamp.txt"'

    def to_env(self, name: str) -> str:
        return f"/tmp/{name}/{{{{inputs.parameters.{name}}}}}"  # noqa: S108

    @property
    def s3_artifact(self) -> bool:
        return True


@dataclass
class FileUploader(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        file_types: List[str],
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        placeholder: StrictStr = "",
    ):
        """
        Widget that allows you to upload a file, and returns the GUID-based name of the file (as it is renamed after
        upload).

        :param label: name to show in the UI for the widget
        :param file_types: list of the mime-types of files that should be accepted
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param placeholder: placeholder example text to place within the widget to exemplify its use
        """
        widget = FileUploaderWidget(
            label=label,
            accept=file_types,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
        )
        super().__init__(type_="string", required=required, ui=widget)

    @property
    def parameter_value(self) -> str:
        return ""


@dataclasses.dataclass
class KeygenInputWidget(AbstractWidget):
    def __init__(self, label: str, hidden: bool = False, help: str = "", grid: int = 8):
        super().__init__(
            widget="keygen",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )


@dataclass
class KeygenInput(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to generate a unique key that could be used for securing an exchange or other unique
        identification purposes, and provides buttons to regenerate the key or copy its text. Will return the generated
        key as clear text.

        :param label: name to show in the UI for the widge
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = KeygenInputWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class MultipleGroupsWidget(AbstractWidget):
    def __init__(self, label: str, hidden: bool = False, help: str = "", grid: int = 8):
        super().__init__(
            widget="groupMultiple",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )

    def get_validator(self, name: str):
        return f"""{name}: Optional[List[str]] = Field(default_factory=list)
    _validate_{name} = validator(
    "{name}", pre=True, allow_reuse=True
    )(validate_multiselect)"""


@dataclass
class MultipleGroups(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to choose multiple groups, and returns an array of group names that were selected.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = MultipleGroupsWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class MultipleUsersWidget(AbstractWidget):
    def __init__(self, label: str, hidden: bool = False, help: str = "", grid: int = 8):
        super().__init__(
            widget="userMultiple",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )


@dataclass
class MultipleUsers(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to choose multiple users, and returns an array of usernames that were selected.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = MultipleUsersWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class NumericInputWidget(AbstractWidget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        placeholder: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="inputNumber",
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
        )

    def to_nested(self, name: str) -> str:
        return f"{{{{inputs.parameters.{name}}}}}"

    @property
    def parameter_value(self) -> str:
        return "-1"

    def get_validator(self, name: str):
        return f"{name}: Optional[Union[int,float]] = None\n"


@dataclass
class NumericInput(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        placeholder: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to enter an arbitrary number into a single-line text input field, and returns the value
        of the number that was entered.

        :param label name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param placeholder: example text to place within the widget to exemplify its use
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = NumericInputWidget(
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
        )
        super().__init__(type_="number", required=required, ui=widget)


@dataclasses.dataclass
class PasswordInputWidget(AbstractWidget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="password",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )


@dataclass
class PasswordInput(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to enter arbitrary text, but the text will be shown as dots when entered rather than
        being displayed in clear text. Will return the entered text in clear text.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = PasswordInputWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class RadioWidget(AbstractWidget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
    ):
        super().__init__(
            widget="radio",
            label=label,
            hidden=hidden,
            help=help,
        )


@dataclass
class Radio(UIElementWithEnum):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        posssible_values: Dict[str, str],
        default: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
    ):
        """
        Widget that allows you to select just one option from a set of options, and returns the key of the selected
        option. Typically, this is used to control mutually exclusive options in the UI.

        :param label: name to show in the UI for the widget
        :param possible_values: map of option keys to the value that will be display for each option in the UI
        :param default: the default value to select in the UI, given as the string key of the option
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input

        """
        widget = RadioWidget(
            label=label,
            hidden=hidden,
            help=help,
        )
        super().__init__(
            type_="string",
            required=required,
            ui=widget,
            possible_values=posssible_values,
        )
        self.default = default


@dataclasses.dataclass
class SingleGroupWidget(AbstractWidget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="groups",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )


@dataclass
class SingleGroup(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to select a single group, and returns the group name of the selected group.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = SingleGroupWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class SingleUserWidget(AbstractWidget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="users",
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )


@dataclass
class SingleUser(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to select a single user, and returns the username of the selected user.

        :param label: name to show in the UI for the widget
        :param required: whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)
        """
        widget = SingleUserWidget(
            label=label,
            hidden=hidden,
            help=help,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)


@dataclasses.dataclass
class TextInputWidget(AbstractWidget):
    def __init__(
        self,
        label: str,
        hidden: bool = False,
        help: str = "",
        placeholder: str = "",
        grid: int = 8,
    ):
        super().__init__(
            widget="input",
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
        )


@dataclass
class TextInput(AbstractUIElement):
    @validate_arguments()
    def __init__(
        self,
        label: StrictStr,
        required: StrictBool = False,
        hidden: StrictBool = False,
        help: StrictStr = "",
        placeholder: StrictStr = "",
        grid: StrictInt = 8,
    ):
        """
        Widget that allows you to enter arbitrary text into a single-line text input field, and returns the value of the
        text that was entered.

        :param label: name to show in the UI for the widget
        :param required" whether a value must be selected to proceed with the UI setup
        :param hidden: whether the widget will be shown in the UI (false) or not (true)
        :param help: informational text to place in a hover-over to describe the use of the input
        :param placeholder: example text to place within the widget to exemplify its use
        :param grid: sizing of the input on the UI (8 is full-width, 4 is half-width)

        """
        widget = TextInputWidget(
            label=label,
            hidden=hidden,
            help=help,
            placeholder=placeholder,
            grid=grid,
        )
        super().__init__(type_="string", required=required, ui=widget)
