import pytest

from pyatlan.model.assets import DynamoDBTable


def test_creator_raises_not_implemented_error():
    with pytest.raises(NotImplementedError):
        DynamoDBTable.creator(
            name="test",
            schema_qualified_name="default/dynamodb/1234/test_db/test_schema",
        )
