import pytest
from pydantic.v1 import ValidationError

from pyatlan.pkg.widgets import (
    APITokenSelector,
    APITokenSelectorWidget,
    BooleanInput,
    BooleanInputWidget,
    ConnectionCreator,
    ConnectionCreatorWidget,
    ConnectionSelector,
    ConnectionSelectorWidget,
    ConnectorTypeSelector,
    ConnectorTypeSelectorWidget,
    DateInput,
    DateInputWidget,
    DropDown,
    DropDownWidget,
    FileUploader,
    FileUploaderWidget,
    KeygenInput,
    KeygenInputWidget,
    MultipleGroups,
    MultipleGroupsWidget,
    MultipleUsers,
    MultipleUsersWidget,
    NumericInput,
    NumericInputWidget,
    PasswordInput,
    PasswordInputWidget,
    Radio,
    RadioWidget,
    SingleGroup,
    SingleGroupWidget,
    SingleUser,
    SingleUserWidget,
    TextInput,
    TextInputWidget,
)

LABEL: str = "Some label"
HELP: str = "Some help_ text"
PLACE_HOLDER: str = "something goes here"
IS_REQUIRED = True
IS_NOT_REQUIRED = False
IS_HIDDEN = True
IS_NOT_HIDDEN = False
POSSIBLE_VALUES = {"name": "Dave"}
FILE_TYPES = ["txt"]


class TestAPITokenSelector:
    def test_constructor_with_defaults(self):
        sut = APITokenSelector(LABEL)
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert ui.widget == "apiTokenSelect"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 4

    def test_constructor_with_overrides(self):
        sut = APITokenSelector(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 1),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, APITokenSelectorWidget)
        assert ui.widget == "apiTokenSelect"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                1,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                1,
                True,
                True,
                HELP,
                1,
                r"1 validation error for Init\nlabel\n  str type expected",
            ),
            (
                LABEL,
                1,
                True,
                HELP,
                1,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                1,
                HELP,
                1,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                1,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1.0,
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            APITokenSelector(
                label=label, required=required, hidden=hidden, help=help_, grid=grid
            )


class TestBooleanInput:
    def test_constructor_with_defaults(self):
        sut = BooleanInput(label=LABEL)
        assert sut.type_ == "boolean"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, BooleanInputWidget)
        assert ui.widget == "boolean"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = BooleanInput(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "boolean"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, BooleanInputWidget)
        assert ui.widget == "boolean"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                1,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                1,
                True,
                True,
                HELP,
                1,
                r"1 validation error for Init\nlabel\n  str type expected",
            ),
            (
                LABEL,
                1,
                True,
                HELP,
                1,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                1,
                HELP,
                1,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                1,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1.0,
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            BooleanInput(
                label=label, required=required, hidden=hidden, help=help_, grid=grid
            )


class TestConnectionCreator:
    def test_constructor_with_defaults(self):
        sut = ConnectionCreator(label=LABEL)
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, ConnectionCreatorWidget)
        assert ui.widget == "connection"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.placeholder == ""

    def test_constructor_with_overrides(self):
        sut = ConnectionCreator(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            placeholder=PLACE_HOLDER,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, ConnectionCreatorWidget)
        assert ui.widget == "connection"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.placeholder == PLACE_HOLDER

    @pytest.mark.parametrize(
        "label, required, hidden, help_, placeholder, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                1,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nlabel\n  str type expected",
            ),
            (
                LABEL,
                1,
                True,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                1,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                PLACE_HOLDER,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1.0,
                r"1 validation error for Init\nplaceholder\n  str type expected",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, placeholder, msg):
        with pytest.raises(ValidationError, match=msg):
            ConnectionCreator(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                placeholder=placeholder,
            )


class TestConnectionSelector:
    def test_constructor_with_defaults(self):
        sut = ConnectionSelector(label=LABEL)
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, ConnectionSelectorWidget)
        assert ui.widget == "connectionSelector"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.placeholder == ""
        assert ui.grid == 4
        assert ui.start == 1

    def test_constructor_with_overrides(self):
        sut = ConnectionSelector(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            placeholder=PLACE_HOLDER,
            grid=(grid := 2),
            start=(start := 10),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, ConnectionSelectorWidget)
        assert ui.widget == "connectionSelector"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.placeholder == PLACE_HOLDER
        assert ui.grid == grid
        assert ui.start == start

    @pytest.mark.parametrize(
        "label, required, hidden, help_, placeholder, grid, start, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                1,
                2,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                1,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                1,
                2,
                r"1 validation error for Init\nlabel\n  str type expected",
            ),
            (
                LABEL,
                1,
                True,
                HELP,
                PLACE_HOLDER,
                1,
                2,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                1,
                HELP,
                PLACE_HOLDER,
                1,
                2,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                PLACE_HOLDER,
                1,
                2,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1.0,
                1,
                2,
                r"1 validation error for Init\nplaceholder\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                1.0,
                2,
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                1,
                2.0,
                r"1 validation error for Init\nstart\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(
        self, label, required, hidden, help_, placeholder, grid, start, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            ConnectionSelector(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                placeholder=placeholder,
                grid=grid,
                start=start,
            )


class TestConnectorTypeSelector:
    def test_constructor_with_defaults(self):
        sut = ConnectorTypeSelector(label=LABEL)
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, ConnectorTypeSelectorWidget)
        assert ui.widget == "sourceConnectionSelector"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 4
        assert ui.start == 1

    def test_constructor_with_overrides(self):
        sut = ConnectorTypeSelector(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 2),
            start=(start := 10),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, ConnectorTypeSelectorWidget)
        assert ui.widget == "sourceConnectionSelector"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid
        assert ui.start == start

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, start, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                1,
                2,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                1,
                True,
                True,
                HELP,
                1,
                2,
                r"1 validation error for Init\nlabel\n  str type expected",
            ),
            (
                LABEL,
                1,
                True,
                HELP,
                1,
                2,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                1,
                HELP,
                1,
                2,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                1,
                2,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1.0,
                2,
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1,
                2.0,
                r"1 validation error for Init\nstart\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, start, msg):
        with pytest.raises(ValidationError, match=msg):
            ConnectorTypeSelector(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
                start=start,
            )


class TestDateInput:
    def test_constructor_with_defaults(self):
        sut = DateInput(label=LABEL)
        assert sut.type_ == "number"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, DateInputWidget)
        assert ui.widget == "date"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.min == -14
        assert ui.max == 0
        assert ui.default == 0
        assert ui.start == 1
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = DateInput(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            min=(min_ := -2),
            max=(max_ := 3),
            default=(default := 1),
            start=(start := 10),
            grid=(grid := 2),
        )
        assert sut.type_ == "number"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, DateInputWidget)
        assert ui.widget == "date"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.min == min_
        assert ui.max == max_
        assert ui.default == default
        assert ui.start == start
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, min, max, default, start, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                -5,
                3,
                1,
                0,
                4,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                1,
                True,
                HELP,
                -5,
                3,
                1,
                0,
                4,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                1,
                HELP,
                -5,
                3,
                1,
                0,
                4,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                -5,
                3,
                1,
                0,
                4,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "a",
                3,
                1,
                0,
                4,
                r"1 validation error for Init\nmin\n  value is not a valid integer",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                -5,
                "a",
                1,
                0,
                4,
                r"1 validation error for Init\nmax\n  value is not a valid integer",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                -5,
                3,
                "a",
                0,
                4,
                r"1 validation error for Init\ndefault\n  value is not a valid integer",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                -5,
                3,
                1,
                "a",
                4,
                r"1 validation error for Init\nstart\n  value is not a valid integer",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                -5,
                3,
                1,
                0,
                "4",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(
        self, label, required, hidden, help_, min, max, default, start, grid, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            DateInput(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                min=min,
                max=max,
                default=default,
                start=start,
                grid=grid,
            )


class TestDropDown:
    def test_constructor_with_defaults(self):
        sut = DropDown(label=LABEL, possible_values=POSSIBLE_VALUES)
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED
        assert sut.possible_values == POSSIBLE_VALUES

        ui = sut.ui
        assert ui
        assert isinstance(ui, DropDownWidget)
        assert ui.widget == "select"
        assert ui.label == LABEL
        assert ui.mode == ""
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = DropDown(
            label=LABEL,
            possible_values=POSSIBLE_VALUES,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            multi_select=True,
            grid=(grid := 2),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED
        assert sut.possible_values == POSSIBLE_VALUES

        ui = sut.ui
        assert ui
        assert isinstance(ui, DropDownWidget)
        assert ui.widget == "select"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.mode == "multiple"
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, possible_values, required, hidden, help_, multi_select, grid, msg",
        [
            (
                None,
                POSSIBLE_VALUES,
                True,
                True,
                HELP,
                False,
                4,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                None,
                True,
                True,
                HELP,
                False,
                4,
                r"1 validation error for Init\npossible_values\n  none is not an allowed value",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                1,
                True,
                HELP,
                False,
                4,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                True,
                1,
                HELP,
                False,
                4,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                True,
                True,
                1,
                False,
                4,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                True,
                True,
                HELP,
                1,
                4,
                r"1 validation error for Init\nmulti_select\n  value is not a valid boolean",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                True,
                True,
                HELP,
                False,
                "1",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(
        self, label, possible_values, required, hidden, help_, multi_select, grid, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            DropDown(
                label=label,
                possible_values=possible_values,
                required=required,
                hidden=hidden,
                help=help_,
                multi_select=multi_select,
                grid=grid,
            )


class TestFileUploader:
    def test_constructor_with_defaults(self):
        sut = FileUploader(label=LABEL, file_types=FILE_TYPES)
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, FileUploaderWidget)
        assert ui.widget == "fileUpload"
        assert ui.label == LABEL
        assert ui.accept == FILE_TYPES
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.placeholder == ""

    def test_constructor_with_overrides(self):
        sut = FileUploader(
            label=LABEL,
            file_types=FILE_TYPES,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            placeholder=PLACE_HOLDER,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, FileUploaderWidget)
        assert ui.widget == "fileUpload"
        assert ui.label == LABEL
        assert ui.accept == FILE_TYPES
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.placeholder == PLACE_HOLDER

    @pytest.mark.parametrize(
        "label, file_types, required, hidden, help_, placeholder, msg",
        [
            (
                None,
                FILE_TYPES,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                None,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nfile_types\n  none is not an allowed value",
            ),
            (
                LABEL,
                FILE_TYPES,
                1,
                True,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                FILE_TYPES,
                True,
                0,
                HELP,
                PLACE_HOLDER,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                FILE_TYPES,
                True,
                True,
                1,
                PLACE_HOLDER,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                FILE_TYPES,
                True,
                True,
                HELP,
                1,
                r"1 validation error for Init\nplaceholder\n  str type expected",
            ),
        ],
    )
    def test_validation(
        self, label, file_types, required, hidden, help_, placeholder, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            FileUploader(
                label=label,
                file_types=file_types,
                required=required,
                hidden=hidden,
                help=help_,
                placeholder=placeholder,
            )


class TestKeygenInput:
    def test_constructor_with_defaults(self):
        sut = KeygenInput(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, KeygenInputWidget)
        assert ui.widget == "keygen"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = KeygenInput(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, KeygenInputWidget)
        assert ui.widget == "keygen"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            KeygenInput(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
            )


class TestMultipleGroups:
    def test_constructor_with_defaults(self):
        sut = MultipleGroups(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, MultipleGroupsWidget)
        assert ui.widget == "groupMultiple"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = MultipleGroups(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, MultipleGroupsWidget)
        assert ui.widget == "groupMultiple"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            MultipleGroups(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
            )


class TestMultipleUsers:
    def test_constructor_with_defaults(self):
        sut = MultipleUsers(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, MultipleUsersWidget)
        assert ui.widget == "userMultiple"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = MultipleUsers(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, MultipleUsersWidget)
        assert ui.widget == "userMultiple"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            MultipleUsers(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
            )


class TestNumericInput:
    def test_constructor_with_defaults(self):
        sut = NumericInput(
            label=LABEL,
        )
        assert sut.type_ == "number"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, NumericInputWidget)
        assert ui.widget == "inputNumber"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.placeholder == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = NumericInput(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            placeholder=PLACE_HOLDER,
            grid=(grid := 3),
        )
        assert sut.type_ == "number"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, NumericInputWidget)
        assert ui.widget == "inputNumber"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.placeholder == PLACE_HOLDER
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, placeholder, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1,
                3,
                r"1 validation error for Init\nplaceholder\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, placeholder, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            NumericInput(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                placeholder=placeholder,
                grid=grid,
            )


class TestPasswordInput:
    def test_constructor_with_defaults(self):
        sut = PasswordInput(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, PasswordInputWidget)
        assert ui.widget == "password"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = PasswordInput(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, PasswordInputWidget)
        assert ui.widget == "password"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            PasswordInput(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
            )


class TestRadio:
    def test_constructor_with_defaults(self):
        sut = Radio(
            label=LABEL, posssible_values=POSSIBLE_VALUES, default=(default := "a")
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED
        # assert sut.possible_values == POSSIBLE_VALUES
        assert sut.default == default

        ui = sut.ui
        assert ui
        assert isinstance(ui, RadioWidget)
        assert ui.widget == "radio"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""

    def test_constructor_with_overrides(self):
        sut = Radio(
            label=LABEL,
            posssible_values=POSSIBLE_VALUES,
            default=(default := "a"),
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED
        # assert sut.possible_values == POSSIBLE_VALUES
        assert sut.default == default

        ui = sut.ui
        assert ui
        assert isinstance(ui, RadioWidget)
        assert ui.widget == "radio"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP

    @pytest.mark.parametrize(
        "label, possible_values, default, required, hidden, help_, msg",
        [
            (
                None,
                POSSIBLE_VALUES,
                "a",
                True,
                True,
                HELP,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                None,
                "a",
                True,
                True,
                HELP,
                r"1 validation error for Init\nposssible_values\n  none is not an allowed value",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                None,
                True,
                True,
                HELP,
                r"1 validation error for Init\ndefault\n  none is not an allowed value",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                "a",
                1,
                True,
                HELP,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                "a",
                True,
                1,
                HELP,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                POSSIBLE_VALUES,
                "a",
                True,
                True,
                1,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
        ],
    )
    def test_validation(
        self, label, possible_values, default, required, hidden, help_, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            Radio(
                label=label,
                posssible_values=possible_values,
                default=default,
                required=required,
                hidden=hidden,
                help=help_,
            )


class TestSingleGroup:
    def test_constructor_with_defaults(self):
        sut = SingleGroup(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, SingleGroupWidget)
        assert ui.widget == "groups"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = SingleGroup(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, SingleGroupWidget)
        assert ui.widget == "groups"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            SingleGroup(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
            )


class TestSingleUser:
    def test_constructor_with_defaults(self):
        sut = SingleUser(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, SingleUserWidget)
        assert ui.widget == "users"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = SingleUser(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, SingleUserWidget)
        assert ui.widget == "users"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            SingleUser(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                grid=grid,
            )


class TestTextInput:
    def test_constructor_with_defaults(self):
        sut = TextInput(
            label=LABEL,
        )
        assert sut.type_ == "string"
        assert sut.required == IS_NOT_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, TextInputWidget)
        assert ui.widget == "input"
        assert ui.label == LABEL
        assert ui.hidden == IS_NOT_HIDDEN
        assert ui.help == ""
        assert ui.placeholder == ""
        assert ui.grid == 8

    def test_constructor_with_overrides(self):
        sut = TextInput(
            label=LABEL,
            required=IS_REQUIRED,
            hidden=IS_HIDDEN,
            help=HELP,
            placeholder=PLACE_HOLDER,
            grid=(grid := 3),
        )
        assert sut.type_ == "string"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, TextInputWidget)
        assert ui.widget == "input"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.placeholder == PLACE_HOLDER
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help_, placeholder, grid, msg",
        [
            (
                None,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nlabel\n  none is not an allowed value",
            ),
            (
                LABEL,
                0,
                True,
                HELP,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nrequired\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                0,
                HELP,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nhidden\n  value is not a valid boolean",
            ),
            (
                LABEL,
                True,
                True,
                1,
                PLACE_HOLDER,
                3,
                r"1 validation error for Init\nhelp\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                1,
                3,
                r"1 validation error for Init\nplaceholder\n  str type expected",
            ),
            (
                LABEL,
                True,
                True,
                HELP,
                PLACE_HOLDER,
                "3",
                r"1 validation error for Init\ngrid\n  value is not a valid integer",
            ),
        ],
    )
    def test_validation(self, label, required, hidden, help_, placeholder, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            TextInput(
                label=label,
                required=required,
                hidden=hidden,
                help=help_,
                placeholder=placeholder,
                grid=grid,
            )
