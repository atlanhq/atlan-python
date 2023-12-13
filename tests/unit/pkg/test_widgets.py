import pytest
from pydantic import ValidationError

from pyatlan.pkg.widgets import APITokenSelector

LABEL: str = "Some label"
HELP: str = "Some help text"
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
