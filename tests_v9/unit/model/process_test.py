# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Process model in pyatlan_v9."""

from hashlib import md5

import pytest

from pyatlan_v9.model import Catalog, Process

PROCESS_QUALIFIED_NAME = "default/s3/1678379436102"
PROCESS_NAME = "DoIt"


@pytest.mark.parametrize(
    "name, connection_qualified_name, process_id, inputs,outputs, parent, message",
    [
        (None, "133/s3", None, [Catalog()], [Catalog()], None, "name is required"),
        (
            "bob",
            None,
            None,
            [Catalog()],
            [Catalog()],
            None,
            "connection_qualified_name is required",
        ),
        ("bob", "133/s3", None, None, [Catalog()], None, "inputs is required"),
        (
            "bob",
            "133/s3",
            None,
            [],
            [Catalog()],
            None,
            "inputs cannot be an empty list",
        ),
        ("bob", "133/s3", None, [Catalog()], None, None, "outputs is required"),
        (
            "bob",
            "133/s3",
            None,
            [Catalog()],
            [],
            None,
            "outputs cannot be an empty list",
        ),
    ],
)
def test_creator_without_required_parameter_raises_value_error(
    name, connection_qualified_name, process_id, inputs, outputs, parent, message
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Process.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            process_id=process_id,
            inputs=inputs,
            outputs=outputs,
            parent=parent,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, process_id, inputs,outputs, parent, expected_value",
    [
        (
            "doit",
            PROCESS_QUALIFIED_NAME,
            "123",
            [Catalog()],
            [Catalog()],
            None,
            "default/s3/1678379436102/123",
        ),
        (
            "doit",
            PROCESS_QUALIFIED_NAME,
            None,
            [Catalog(guid="123")],
            [Catalog(guid="456")],
            None,
            "doitdefault/s3/1678379436102123456",
        ),
        (
            "doit",
            PROCESS_QUALIFIED_NAME,
            None,
            [Catalog(guid="456")],
            [Catalog(guid="789")],
            Catalog(guid="123"),
            "doitdefault/s3/1678379436102123456789",
        ),
    ],
)
def test_creator(
    name, connection_qualified_name, process_id, inputs, outputs, parent, expected_value
):
    """Test creator builds expected qualified name and relationships."""
    expected_value = (
        expected_value
        if process_id
        # deepcode ignore InsecureHash/test: this is not used for generating security keys
        else f"{connection_qualified_name}/{md5(expected_value.encode()).hexdigest()}"
    )

    process = Process.creator(
        name=name,
        connection_qualified_name=connection_qualified_name,
        process_id=process_id,
        inputs=inputs,
        outputs=outputs,
        parent=parent,
    )
    assert process.name == name
    assert process.connection_qualified_name == connection_qualified_name
    assert process.qualified_name == expected_value
    assert process_id == process_id
    assert len(process.inputs) == len(inputs)
    assert len(process.outputs) == len(outputs)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PROCESS_QUALIFIED_NAME, "qualified_name is required"),
        (PROCESS_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Process.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates process with required fields for update operations."""
    sut = Process.updater(qualified_name=PROCESS_QUALIFIED_NAME, name=PROCESS_NAME)

    assert sut.qualified_name == PROCESS_QUALIFIED_NAME
    assert sut.name == PROCESS_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only required update fields."""
    sut = Process.updater(
        qualified_name=PROCESS_QUALIFIED_NAME, name=PROCESS_NAME
    ).trim_to_required()

    assert sut.qualified_name == PROCESS_QUALIFIED_NAME
    assert sut.name == PROCESS_NAME


@pytest.mark.parametrize(
    "name, connection_qualified_name, process_id, inputs,outputs, parent, message",
    [
        (None, "133/s3", None, [Catalog()], [Catalog()], None, "name is required"),
        (
            "bob",
            None,
            None,
            [Catalog()],
            [Catalog()],
            None,
            "connection_qualified_name is required",
        ),
        ("bob", "133/s3", None, None, [Catalog()], None, "inputs is required"),
        (
            "bob",
            "133/s3",
            None,
            [],
            [Catalog()],
            None,
            "inputs cannot be an empty list",
        ),
        ("bob", "133/s3", None, [Catalog()], None, None, "outputs is required"),
        (
            "bob",
            "133/s3",
            None,
            [Catalog()],
            [],
            None,
            "outputs cannot be an empty list",
        ),
    ],
)
def test_process_attributes_generate_qualified_name_without_required_parameter_raises_value_error(
    name, connection_qualified_name, process_id, inputs, outputs, parent, message
):
    """Test ProcessAttributes.generate_qualified_name validates required inputs."""
    with pytest.raises(ValueError, match=message):
        Process.Attributes.generate_qualified_name(
            name=name,
            connection_qualified_name=connection_qualified_name,
            process_id=process_id,
            inputs=inputs,
            outputs=outputs,
            parent=parent,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, process_id, inputs,outputs, parent, expected_value",
    [
        (
            "doit",
            "default/s3/1678379436102",
            "123",
            [Catalog()],
            [Catalog()],
            None,
            "default/s3/1678379436102/123",
        ),
        (
            "doit",
            "default/s3/1678379436102",
            None,
            [Catalog(guid="123")],
            [Catalog(guid="456")],
            None,
            "doitdefault/s3/1678379436102123456",
        ),
        (
            "doit",
            "default/s3/1678379436102",
            None,
            [Catalog(guid="456")],
            [Catalog(guid="789")],
            Catalog(guid="123"),
            "doitdefault/s3/1678379436102123456789",
        ),
    ],
)
def test_process_attributes_generate_qualified_name(
    name, connection_qualified_name, process_id, inputs, outputs, parent, expected_value
):
    """Test ProcessAttributes.generate_qualified_name returns expected values."""
    expected_value = (
        expected_value
        if process_id
        # deepcode ignore InsecureHash/test: this is not used for generating security keys
        else f"{connection_qualified_name}/{md5(expected_value.encode()).hexdigest()}"
    )

    assert (
        Process.Attributes.generate_qualified_name(
            name=name,
            connection_qualified_name=connection_qualified_name,
            process_id=process_id,
            inputs=inputs,
            outputs=outputs,
            parent=parent,
        )
        == expected_value
    )
