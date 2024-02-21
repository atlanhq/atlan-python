from typing import List

import pytest

from pyatlan.model.assets import Column, ColumnProcess, Process
from tests.unit.model.constants import (
    CP_CONNECTION_QUALIFIED_NAME,
    CP_NAME,
    CP_PROCESS_ID,
    CP_QUALIFIED_NAME,
    CP_QUALIFIED_NAME_HASH,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, inputs, outputs, process, error_msg",
    [
        (
            None,
            CP_CONNECTION_QUALIFIED_NAME,
            [Column()],
            [Column()],
            Process(),
            "name is required",
        ),
        (
            CP_NAME,
            None,
            [Column()],
            [Column()],
            Process(),
            "connection_qualified_name is required",
        ),
        (
            CP_NAME,
            CP_CONNECTION_QUALIFIED_NAME,
            None,
            [Column()],
            Process(),
            "inputs is required",
        ),
        (
            CP_NAME,
            CP_CONNECTION_QUALIFIED_NAME,
            [Column()],
            None,
            Process(),
            "outputs is required",
        ),
        (
            CP_NAME,
            CP_CONNECTION_QUALIFIED_NAME,
            [Column()],
            [Column()],
            None,
            "parent is required",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    connection_qualified_name: str,
    inputs: List[Column],
    outputs: List[Column],
    process: Process,
    error_msg: str,
):
    with pytest.raises(ValueError, match=error_msg):
        ColumnProcess.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            inputs=inputs,
            outputs=outputs,
            parent=process,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, inputs, outputs, process_id, parent",
    [
        (
            CP_NAME,
            CP_CONNECTION_QUALIFIED_NAME,
            [Column()],
            [Column()],
            CP_PROCESS_ID,
            Process(),
        ),
        (
            CP_NAME,
            CP_CONNECTION_QUALIFIED_NAME,
            [Column()],
            [Column()],
            None,
            Process(),
        ),
    ],
)
def test_create(
    name: str,
    connection_qualified_name: str,
    inputs: List[Column],
    outputs: List[Column],
    process_id: str,
    parent: Process,
):
    test_cp = ColumnProcess.create(
        name=name,
        connection_qualified_name=connection_qualified_name,
        inputs=inputs,
        outputs=outputs,
        process_id=process_id,
        parent=parent,
    )
    assert test_cp
    assert test_cp.name == CP_NAME
    if process_id:
        assert test_cp.qualified_name == CP_QUALIFIED_NAME
    # Otherwise SDK will generate aunique ID (MD5 hash) based on the
    # unique combination of inputs and outputs for the process.
    else:
        assert test_cp.qualified_name == CP_QUALIFIED_NAME_HASH
    assert test_cp.inputs == inputs
    assert test_cp.outputs == outputs
    assert test_cp.process == parent


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CP_QUALIFIED_NAME, "qualified_name is required"),
        (CP_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        ColumnProcess.create_for_modification(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    test_cp = ColumnProcess.create_for_modification(
        qualified_name=CP_QUALIFIED_NAME, name=CP_NAME
    ).trim_to_required()
    assert test_cp.name == CP_NAME
    assert test_cp.qualified_name == CP_QUALIFIED_NAME
