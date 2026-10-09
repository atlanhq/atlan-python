# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for BIProcess model in pyatlan_v9."""

from typing import Any, List

import pytest

from pyatlan_v9.model import BIProcess, MetabaseDashboard, MetabaseQuestion
from tests_v9.unit.model.constants import (
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
    inputs: List[Any],
    outputs: List[Any],
    error_msg: str,
):
    """Test creator raises ValueError when required parameters are missing."""
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
        (None, BI_PROCESS_QUALIFIED_NAME_HASH),
    ],
)
def test_creator(process_id: str, qualified_name: str):
    """Test creator sets qualified name and relationship references."""
    test_bp = BIProcess.creator(
        name=BI_PROCESS_NAME,
        connection_qualified_name=BI_PROCESS_CONNECTION_QUALIFIED_NAME,
        inputs=[MetabaseQuestion()],
        outputs=[MetabaseDashboard(), MetabaseDashboard()],
        process_id=process_id,
    )
    assert test_bp.type_name == "BIProcess"
    assert test_bp.name == BI_PROCESS_NAME
    assert test_bp.qualified_name == qualified_name
    assert test_bp.connection_qualified_name == BI_PROCESS_CONNECTION_QUALIFIED_NAME
    assert test_bp.connector_name == "metabase"
    assert len(test_bp.inputs) == 1
    assert len(test_bp.outputs) == 2


def test_creator_references_relationships_by_qualified_name():
    """Test creator keeps qualifiedName references for assets it is not building."""
    question_qn = f"{BI_PROCESS_CONNECTION_QUALIFIED_NAME}/questions/42"
    test_bp = BIProcess.creator(
        name=BI_PROCESS_NAME,
        connection_qualified_name=BI_PROCESS_CONNECTION_QUALIFIED_NAME,
        inputs=[MetabaseQuestion(qualified_name=question_qn)],
        outputs=[MetabaseDashboard()],
        process_id=BI_PROCESS_ID,
    )
    assert test_bp.inputs[0].unique_attributes == {"qualifiedName": question_qn}


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, BI_PROCESS_NAME, "qualified_name is required"),
        (BI_PROCESS_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        BIProcess.updater(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    test_bp = BIProcess.updater(
        qualified_name=BI_PROCESS_QUALIFIED_NAME, name=BI_PROCESS_NAME
    ).trim_to_required()
    assert test_bp.name == BI_PROCESS_NAME
    assert test_bp.qualified_name == BI_PROCESS_QUALIFIED_NAME
