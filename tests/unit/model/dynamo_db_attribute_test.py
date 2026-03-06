import pytest

from pyatlan.model.assets import DynamoDBAttribute

DYNAMODB_CONNECTOR_TYPE = "dynamodb"
DYNAMODB_CONNECTION_QUALIFIED_NAME = "default/dynamodb/1709471234"
DYNAMODB_TABLE_NAME = "UserSessions"
DYNAMODB_TABLE_QUALIFIED_NAME = (
    f"{DYNAMODB_CONNECTION_QUALIFIED_NAME}/{DYNAMODB_TABLE_NAME}"
)
DYNAMODB_ATTRIBUTE_NAME = "orderId"
DYNAMODB_ATTRIBUTE_QUALIFIED_NAME = (
    f"{DYNAMODB_TABLE_QUALIFIED_NAME}/{DYNAMODB_ATTRIBUTE_NAME}"
)


@pytest.mark.parametrize(
    "name, parent_qualified_name, order, message",
    [
        (None, DYNAMODB_TABLE_QUALIFIED_NAME, 1, "name is required"),
        (DYNAMODB_ATTRIBUTE_NAME, None, 1, "parent_qualified_name is required"),
        (
            DYNAMODB_ATTRIBUTE_NAME,
            DYNAMODB_TABLE_QUALIFIED_NAME,
            None,
            "order is required",
        ),
        (
            DYNAMODB_ATTRIBUTE_NAME,
            DYNAMODB_CONNECTION_QUALIFIED_NAME,
            1,
            "Invalid parent_qualified_name",
        ),
        (
            DYNAMODB_ATTRIBUTE_NAME,
            DYNAMODB_ATTRIBUTE_QUALIFIED_NAME,
            1,
            "Invalid parent_qualified_name",
        ),
        (
            DYNAMODB_ATTRIBUTE_NAME,
            DYNAMODB_TABLE_QUALIFIED_NAME,
            -1,
            "Order must be be a positive integer",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name, parent_qualified_name, order, message
):
    with pytest.raises(ValueError, match=message):
        DynamoDBAttribute.creator(
            name=name,
            parent_qualified_name=parent_qualified_name,
            order=order,
        )


def test_creator():
    sut = DynamoDBAttribute.creator(
        name=DYNAMODB_ATTRIBUTE_NAME,
        parent_qualified_name=DYNAMODB_TABLE_QUALIFIED_NAME,
        order=1,
    )

    assert sut.name == DYNAMODB_ATTRIBUTE_NAME
    assert sut.type_name == "DynamoDBAttribute"
    assert sut.qualified_name == DYNAMODB_ATTRIBUTE_QUALIFIED_NAME
    assert sut.connector_name == DYNAMODB_CONNECTOR_TYPE
    assert sut.connection_qualified_name == DYNAMODB_CONNECTION_QUALIFIED_NAME
    assert sut.order == 1
    assert sut.table_name == DYNAMODB_TABLE_NAME
    assert sut.table_qualified_name == DYNAMODB_TABLE_QUALIFIED_NAME
    assert sut.dynamo_dbtable.qualified_name == DYNAMODB_TABLE_QUALIFIED_NAME


def test_creator_with_explicit_parent_name():
    custom_parent_name = "CustomTableName"
    sut = DynamoDBAttribute.creator(
        name=DYNAMODB_ATTRIBUTE_NAME,
        parent_qualified_name=DYNAMODB_TABLE_QUALIFIED_NAME,
        order=2,
        parent_name=custom_parent_name,
    )

    assert sut.name == DYNAMODB_ATTRIBUTE_NAME
    assert sut.qualified_name == DYNAMODB_ATTRIBUTE_QUALIFIED_NAME
    assert sut.connector_name == DYNAMODB_CONNECTOR_TYPE
    assert sut.connection_qualified_name == DYNAMODB_CONNECTION_QUALIFIED_NAME
    assert sut.order == 2
    assert sut.table_name == custom_parent_name
    assert sut.table_qualified_name == DYNAMODB_TABLE_QUALIFIED_NAME
    assert sut.dynamo_dbtable.qualified_name == DYNAMODB_TABLE_QUALIFIED_NAME


def test_creator_with_explicit_connection_qualified_name():
    sut = DynamoDBAttribute.creator(
        name=DYNAMODB_ATTRIBUTE_NAME,
        parent_qualified_name=DYNAMODB_TABLE_QUALIFIED_NAME,
        order=0,
        connection_qualified_name=DYNAMODB_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == DYNAMODB_ATTRIBUTE_NAME
    assert sut.qualified_name == DYNAMODB_ATTRIBUTE_QUALIFIED_NAME
    assert sut.connector_name == DYNAMODB_CONNECTOR_TYPE
    assert sut.connection_qualified_name == DYNAMODB_CONNECTION_QUALIFIED_NAME
    assert sut.order == 0


@pytest.mark.parametrize(
    "parent_qualified_name",
    [
        DYNAMODB_CONNECTION_QUALIFIED_NAME,
        DYNAMODB_ATTRIBUTE_QUALIFIED_NAME,
    ],
)
def test_creator_with_connection_qn_and_invalid_parent_raises_value_error(
    parent_qualified_name,
):
    with pytest.raises(ValueError, match="Invalid parent_qualified_name"):
        DynamoDBAttribute.creator(
            name=DYNAMODB_ATTRIBUTE_NAME,
            parent_qualified_name=parent_qualified_name,
            order=1,
            connection_qualified_name=DYNAMODB_CONNECTION_QUALIFIED_NAME,
        )


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DYNAMODB_ATTRIBUTE_QUALIFIED_NAME, "qualified_name is required"),
        (DYNAMODB_ATTRIBUTE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name, name, message
):
    with pytest.raises(ValueError, match=message):
        DynamoDBAttribute.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification():
    sut = DynamoDBAttribute.create_for_modification(
        qualified_name=DYNAMODB_ATTRIBUTE_QUALIFIED_NAME,
        name=DYNAMODB_ATTRIBUTE_NAME,
    )

    assert sut.qualified_name == DYNAMODB_ATTRIBUTE_QUALIFIED_NAME
    assert sut.name == DYNAMODB_ATTRIBUTE_NAME


def test_trim_to_required():
    sut = DynamoDBAttribute.create_for_modification(
        qualified_name=DYNAMODB_ATTRIBUTE_QUALIFIED_NAME,
        name=DYNAMODB_ATTRIBUTE_NAME,
    ).trim_to_required()

    assert sut.qualified_name == DYNAMODB_ATTRIBUTE_QUALIFIED_NAME
    assert sut.name == DYNAMODB_ATTRIBUTE_NAME
