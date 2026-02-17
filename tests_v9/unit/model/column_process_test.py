# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for ColumnProcess model in pyatlan_v9."""

from typing import List

import pytest

from pyatlan_v9.model import Column, ColumnProcess, Process
from tests_v9.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    connection_qualified_name: str,
    inputs: List[Column],
    outputs: List[Column],
    process: Process,
    error_msg: str,
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=error_msg):
        ColumnProcess.creator(
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
def test_creator(
    name: str,
    connection_qualified_name: str,
    inputs: List[Column],
    outputs: List[Column],
    process_id: str,
    parent: Process,
):
    """Test creator sets qualified name and relationship references."""
    test_cp = ColumnProcess.creator(
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
    else:
        assert test_cp.qualified_name == CP_QUALIFIED_NAME_HASH
    assert len(test_cp.inputs) == len(inputs)
    assert len(test_cp.outputs) == len(outputs)
    assert test_cp.process is not None


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CP_QUALIFIED_NAME, "qualified_name is required"),
        (CP_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        ColumnProcess.updater(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    test_cp = ColumnProcess.updater(
        qualified_name=CP_QUALIFIED_NAME, name=CP_NAME
    ).trim_to_required()
    assert test_cp.name == CP_NAME
    assert test_cp.qualified_name == CP_QUALIFIED_NAME
