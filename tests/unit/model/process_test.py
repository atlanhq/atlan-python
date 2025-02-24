from hashlib import md5

import pytest

from pyatlan.model.assets import Catalog, Process

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
def test_create_without_required_parameter_raises_value_error(
    name, connection_qualified_name, process_id, inputs, outputs, parent, message
):
    with pytest.raises(ValueError, match=message):
        Process.create(
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
def test__create(
    name, connection_qualified_name, process_id, inputs, outputs, parent, expected_value
):
    expected_value = (
        expected_value
        if process_id
        else f"{connection_qualified_name}/{md5(expected_value.encode()).hexdigest()}"
    )

    process = Process.create(
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
    assert process.inputs == inputs
    assert process.outputs == outputs


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PROCESS_QUALIFIED_NAME, "qualified_name is required"),
        (PROCESS_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Process.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Process.create_for_modification(
        qualified_name=PROCESS_QUALIFIED_NAME, name=PROCESS_NAME
    )

    assert sut.qualified_name == PROCESS_QUALIFIED_NAME
    assert sut.name == PROCESS_NAME


def test_trim_to_required():
    sut = Process.create_for_modification(
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
    expected_value = (
        expected_value
        if process_id
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
