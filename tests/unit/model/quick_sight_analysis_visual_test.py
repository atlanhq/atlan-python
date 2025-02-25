import pytest

from pyatlan.model.assets import QuickSightAnalysisVisual
from tests.unit.model.constants import (
    QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
    QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    QUICK_SIGHT_CONNECTOR_TYPE,
    QUICK_SIGHT_ID_ANALYSIS_VISUAL,
    QUICK_SIGHT_NAME,
    QUICK_SIGHT_QUALIFIED_NAME,
    QUICK_SIGHT_SHEET_ID,
    QUICK_SIGHT_SHEET_NAME,
)


@pytest.mark.parametrize(
    "name, quick_sight_id, quick_sight_sheet_id, quick_sight_sheet_name, quick_sight_analysis_qualified_name, message",
    [
        (
            None,
            QUICK_SIGHT_ID_ANALYSIS_VISUAL,
            QUICK_SIGHT_SHEET_ID,
            QUICK_SIGHT_SHEET_NAME,
            QUICK_SIGHT_QUALIFIED_NAME,
            "name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            None,
            QUICK_SIGHT_SHEET_ID,
            QUICK_SIGHT_SHEET_NAME,
            QUICK_SIGHT_QUALIFIED_NAME,
            "quick_sight_id is required",
        ),
        (
            QUICK_SIGHT_NAME,
            QUICK_SIGHT_ID_ANALYSIS_VISUAL,
            None,
            QUICK_SIGHT_SHEET_NAME,
            QUICK_SIGHT_QUALIFIED_NAME,
            "quick_sight_sheet_id is required",
        ),
        (
            QUICK_SIGHT_NAME,
            QUICK_SIGHT_ID_ANALYSIS_VISUAL,
            QUICK_SIGHT_SHEET_ID,
            None,
            QUICK_SIGHT_QUALIFIED_NAME,
            "quick_sight_sheet_name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            QUICK_SIGHT_ID_ANALYSIS_VISUAL,
            QUICK_SIGHT_SHEET_ID,
            QUICK_SIGHT_SHEET_NAME,
            None,
            "quick_sight_analysis_qualified_name is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    quick_sight_id: str,
    quick_sight_sheet_id: str,
    quick_sight_sheet_name: str,
    quick_sight_analysis_qualified_name: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        QuickSightAnalysisVisual.creator(
            name=name,
            quick_sight_sheet_id=quick_sight_sheet_id,
            quick_sight_id=quick_sight_id,
            quick_sight_sheet_name=quick_sight_sheet_name,
            quick_sight_analysis_qualified_name=quick_sight_analysis_qualified_name,
        )


def test_creator():
    sut = QuickSightAnalysisVisual.creator(
        name=QUICK_SIGHT_NAME,
        quick_sight_id=QUICK_SIGHT_ID_ANALYSIS_VISUAL,
        quick_sight_sheet_id=QUICK_SIGHT_SHEET_ID,
        quick_sight_sheet_name=QUICK_SIGHT_SHEET_NAME,
        quick_sight_analysis_qualified_name=QUICK_SIGHT_QUALIFIED_NAME,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.quick_sight_analysis_qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.quick_sight_id == QUICK_SIGHT_ID_ANALYSIS_VISUAL
    assert sut.qualified_name == QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE
    assert sut.quick_sight_sheet_id == QUICK_SIGHT_SHEET_ID
    assert sut.quick_sight_sheet_name == QUICK_SIGHT_SHEET_NAME


def test_overload_creator():
    sut = QuickSightAnalysisVisual.creator(
        name=QUICK_SIGHT_NAME,
        quick_sight_id=QUICK_SIGHT_ID_ANALYSIS_VISUAL,
        quick_sight_sheet_id=QUICK_SIGHT_SHEET_ID,
        quick_sight_sheet_name=QUICK_SIGHT_SHEET_NAME,
        quick_sight_analysis_qualified_name=QUICK_SIGHT_QUALIFIED_NAME,
        connection_qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.quick_sight_analysis_qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.quick_sight_id == QUICK_SIGHT_ID_ANALYSIS_VISUAL
    assert sut.qualified_name == QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE
    assert sut.quick_sight_sheet_id == QUICK_SIGHT_SHEET_ID
    assert sut.quick_sight_sheet_name == QUICK_SIGHT_SHEET_NAME
    assert sut.connection_qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME


def test_updater():
    sut = QuickSightAnalysisVisual.updater(
        qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME, name=QUICK_SIGHT_NAME
    )

    assert sut.qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.name == QUICK_SIGHT_NAME


def test_trim_to_required():
    sut = QuickSightAnalysisVisual.updater(
        name=QUICK_SIGHT_NAME, qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
