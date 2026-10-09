from typing import List

import pytest

from pyatlan.model.assets import BIProcess, Catalog, MetabaseDashboard, MetabaseQuestion
from tests.unit.model.constants import (
    BI_PROCESS_CONNECTION_QUALIFIED_NAME,
    BI_PROCESS_ID,
    BI_PROCESS_NAME,
    BI_PROCESS_QUALIFIED_NAME,
    BI_PROCESS_QUALIFIED_NAME_HASH,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, inputs, outputs, error_msg",
    [
        (
            None,
            BI_PROCESS_CONNECTION_QUALIFIED_NAME,
            [MetabaseQuestion()],
            [MetabaseDashboard()],
            "name is required",
        ),
        (
            BI_PROCESS_NAME,
            None,
            [MetabaseQuestion()],
            [MetabaseDashboard()],
            "connection_qualified_name is required",
        ),
        (
            BI_PROCESS_NAME,
            BI_PROCESS_CONNECTION_QUALIFIED_NAME,
            None,
            [MetabaseDashboard()],
            "inputs is required",
        ),
        (
            BI_PROCESS_NAME,
            BI_PROCESS_CONNECTION_QUALIFIED_NAME,
            [MetabaseQuestion()],
            None,
            "outputs is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    connection_qualified_name: str,
    inputs: List[Catalog],
    outputs: List[Catalog],
    error_msg: str,
):
    with pytest.raises(ValueError, match=error_msg):
        BIProcess.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            inputs=inputs,
            outputs=outputs,
        )


@pytest.mark.parametrize(
    "process_id, qualified_name",
    [
        (BI_PROCESS_ID, BI_PROCESS_QUALIFIED_NAME),
        # Otherwise SDK will generate a unique ID (MD5 hash) based on the
        # unique combination of inputs and outputs for the process.
        (None, BI_PROCESS_QUALIFIED_NAME_HASH),
    ],
)
def test_creator(process_id: str, qualified_name: str):
    inputs = [MetabaseQuestion()]
    outputs = [MetabaseDashboard()]
    test_bp = BIProcess.creator(
        name=BI_PROCESS_NAME,
        connection_qualified_name=BI_PROCESS_CONNECTION_QUALIFIED_NAME,
        inputs=inputs,
        outputs=outputs,
        process_id=process_id,
    )
    assert isinstance(test_bp, BIProcess)
    assert test_bp.type_name == "BIProcess"
    assert test_bp.name == BI_PROCESS_NAME
    assert test_bp.qualified_name == qualified_name
    assert test_bp.connection_qualified_name == BI_PROCESS_CONNECTION_QUALIFIED_NAME
    assert test_bp.connector_name == "metabase"
    assert test_bp.inputs == inputs
    assert test_bp.outputs == outputs


def test_create_is_deprecated_alias_of_creator():
    with pytest.warns(DeprecationWarning):
        test_bp = BIProcess.create(
            name=BI_PROCESS_NAME,
            connection_qualified_name=BI_PROCESS_CONNECTION_QUALIFIED_NAME,
            inputs=[MetabaseQuestion()],
            outputs=[MetabaseDashboard()],
            process_id=BI_PROCESS_ID,
        )
    assert isinstance(test_bp, BIProcess)
    assert test_bp.qualified_name == BI_PROCESS_QUALIFIED_NAME


def test_trim_to_required():
    test_bp = BIProcess.updater(
        qualified_name=BI_PROCESS_QUALIFIED_NAME, name=BI_PROCESS_NAME
    ).trim_to_required()
    assert isinstance(test_bp, BIProcess)
    assert test_bp.name == BI_PROCESS_NAME
    assert test_bp.qualified_name == BI_PROCESS_QUALIFIED_NAME
