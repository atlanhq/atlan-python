import pytest
from pydantic import ValidationError

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
)

LABEL: str = "Some label"
HELP: str = "Some help text"
PLACE_HOLDER: str = "something goes here"
IS_REQUIRED = True
IS_NOT_REQUIRED = False
IS_HIDDEN = True
IS_NOT_HIDDEN = False


class TestAPITokenSelector:
    def test_constructor_with_defaults(self):
        sut = APITokenSelector(LABEL)
        assert sut.type == "string"
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
        assert sut.type == "string"
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
        "label, required, hidden, help, grid, msg",
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
    def test_validation(self, label, required, hidden, help, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            APITokenSelector(
                label=label, required=required, hidden=hidden, help=help, grid=grid
            )


class TestBooleanInput:
    def test_constructor_with_defaults(self):
        sut = BooleanInput(label=LABEL)
        assert sut.type == "boolean"
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
        assert sut.type == "boolean"
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
        "label, required, hidden, help, grid, msg",
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
    def test_validation(self, label, required, hidden, help, grid, msg):
        with pytest.raises(ValidationError, match=msg):
            BooleanInput(
                label=label, required=required, hidden=hidden, help=help, grid=grid
            )


class TestConnectionCreator:
    def test_constructor_with_defaults(self):
        sut = ConnectionCreator(label=LABEL)
        assert sut.type == "string"
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
        assert sut.type == "string"
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
        "label, required, hidden, help, placeholder, msg",
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
    def test_validation(self, label, required, hidden, help, placeholder, msg):
        with pytest.raises(ValidationError, match=msg):
            ConnectionCreator(
                label=label,
                required=required,
                hidden=hidden,
                help=help,
                placeholder=placeholder,
            )


class TestConnectionSelector:
    def test_constructor_with_defaults(self):
        sut = ConnectionSelector(label=LABEL)
        assert sut.type == "string"
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
        assert sut.type == "string"
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
        "label, required, hidden, help, placeholder, grid, start, msg",
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
        self, label, required, hidden, help, placeholder, grid, start, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            ConnectionSelector(
                label=label,
                required=required,
                hidden=hidden,
                help=help,
                placeholder=placeholder,
                grid=grid,
                start=start,
            )


class TestConnectorTypeSelector:
    def test_constructor_with_defaults(self):
        sut = ConnectorTypeSelector(label=LABEL)
        assert sut.type == "string"
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
        assert sut.type == "string"
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
        "label, required, hidden, help, grid, start, msg",
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
    def test_validation(self, label, required, hidden, help, grid, start, msg):
        with pytest.raises(ValidationError, match=msg):
            ConnectorTypeSelector(
                label=label,
                required=required,
                hidden=hidden,
                help=help,
                grid=grid,
                start=start,
            )


class TestDateInput:
    def test_constructor_with_defaults(self):
        sut = DateInput(label=LABEL)
        assert sut.type == "number"
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
            min=(min := -2),
            max=(max := 3),
            default=(default := 1),
            start=(start := 10),
            grid=(grid := 2),
        )
        assert sut.type == "number"
        assert sut.required == IS_REQUIRED

        ui = sut.ui
        assert ui
        assert isinstance(ui, DateInputWidget)
        assert ui.widget == "date"
        assert ui.label == LABEL
        assert ui.hidden == IS_HIDDEN
        assert ui.help == HELP
        assert ui.min == min
        assert ui.max == max
        assert ui.default == default
        assert ui.start == start
        assert ui.grid == grid

    @pytest.mark.parametrize(
        "label, required, hidden, help, min, max, default, start, grid, msg",
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
        self, label, required, hidden, help, min, max, default, start, grid, msg
    ):
        with pytest.raises(ValidationError, match=msg):
            DateInput(
                label=label,
                required=required,
                hidden=hidden,
                help=help,
                min=min,
                max=max,
                default=default,
                start=start,
                grid=grid,
            )
