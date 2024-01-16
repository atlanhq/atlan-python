import pytest

from pyatlan.pkg.ui import UIStep
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

LABEL = "Some label"
HELP = "some help"
PLACEHOLDER = "some placeholder"
TITLE = "some title"
DESCRIPTION = "some description"
POSSIBLE_VALUES = {"name": "Dave"}


@pytest.fixture()
def api_token_selector() -> APITokenSelector:
    return APITokenSelector(label=LABEL)


@pytest.fixture()
def boolean_input() -> BooleanInput:
    return BooleanInput(label=LABEL)


@pytest.fixture()
def connection_creator() -> ConnectionCreator:
    return ConnectionCreator(label=LABEL)


@pytest.fixture()
def connector_type_selector() -> ConnectorTypeSelector:
    return ConnectorTypeSelector(label=LABEL)


@pytest.fixture()
def date_input() -> DateInput:
    return DateInput(label=LABEL)


@pytest.fixture()
def drop_down() -> DropDown:
    return DropDown(label=LABEL, possible_values=POSSIBLE_VALUES)


@pytest.fixture()
def file_uploader() -> FileUploader:
    uploader = FileUploader(
        label=LABEL,
        file_types=["text/csv"],
        required=False,
        help=HELP,
        placeholder=PLACEHOLDER,
    )
    return uploader


@pytest.fixture()
def keygen_input() -> KeygenInput:
    return KeygenInput(label=LABEL)


@pytest.fixture()
def multiple_groups() -> MultipleGroups:
    return MultipleGroups(label=LABEL)


@pytest.fixture()
def multiple_users() -> MultipleUsers:
    return MultipleUsers(label=LABEL)


@pytest.fixture()
def numeric_input() -> NumericInput:
    return NumericInput(label=LABEL)


@pytest.fixture()
def password_input() -> PasswordInput:
    return PasswordInput(label=LABEL)


@pytest.fixture()
def radio() -> Radio:
    return Radio(label=LABEL, posssible_values=POSSIBLE_VALUES, default="one")


@pytest.fixture()
def single_group() -> SingleGroup:
    return SingleGroup(label=LABEL)


@pytest.fixture()
def single_user() -> SingleUser:
    return SingleUser(label=LABEL)


@pytest.fixture()
def text_input() -> TextInput:
    return TextInput(label="Qualified name prefix")


@pytest.fixture()
def an_input(
    request,
    api_token_selector,
    boolean_input,
    connection_creator,
    connector_type_selector,
    date_input,
    drop_down,
    file_uploader,
    keygen_input,
    multiple_groups,
    multiple_users,
    numeric_input,
    password_input,
    radio,
    single_group,
    single_user,
    text_input,
):
    if request.param == "APITokenSelector":
        return api_token_selector
    if request.param == "BooleanInput":
        return boolean_input
    if request.param == "TextInput":
        return text_input
    if request.param == "ConnectionCreator":
        return connection_creator
    if request.param == "ConnectionSelector":
        return connector_type_selector
    if request.param == "ConnectorTypeSelector":
        return connector_type_selector
    if request.param == "DateInput":
        return date_input
    if request.param == "DropDown":
        return drop_down
    if request.param == "FileUploader":
        return file_uploader
    if request.param == "KeygenInput":
        return keygen_input
    if request.param == "MultipleGroups":
        return multiple_groups
    if request.param == "MultipleUsers":
        return multiple_users
    if request.param == "NumericInput":
        return numeric_input
    if request.param == "PasswordInput":
        return password_input
    if request.param == "Radio":
        return radio
    if request.param == "SingleGroup":
        return single_group
    if request.param == "SingleUser":
        return single_user
    if request.param == "TextInput":
        return text_input
    return None


@pytest.fixture()
def ui_step(text_input) -> UIStep:
    return UIStep(title=TITLE, inputs={"key": text_input})
