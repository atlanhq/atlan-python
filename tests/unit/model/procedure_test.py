import pytest

from pyatlan.model.assets import Procedure
from tests.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    PROCEDURE_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
)

DEFINITION = """
BEGIN
insert into `atlanhq.testing_lineage.INSTACART_ALCOHOL_ORDER_TIME_copy`
select * from `atlanhq.testing_lineage.INSTACART_ALCOHOL_ORDER_TIME`;
END
"""


@pytest.mark.parametrize(
    "name, definition, schema_qualified_name, message",
    [
        (None, DEFINITION, SCHEMA_QUALIFIED_NAME, "name is required"),
        (PROCEDURE_NAME, None, SCHEMA_QUALIFIED_NAME, "definition is required"),
        (PROCEDURE_NAME, DEFINITION, None, "schema_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, definition: str, schema_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Procedure.create(
            name=name,
            definition=definition,
            schema_qualified_name=schema_qualified_name,
        )


def test_creator():
    sut = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert sut.name == PROCEDURE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert (
        sut.qualified_name == f"{SCHEMA_QUALIFIED_NAME}/_procedures_/{PROCEDURE_NAME}"
    )
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME


def test_overload_creator():
    sut = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PROCEDURE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert (
        sut.qualified_name == f"{SCHEMA_QUALIFIED_NAME}/_procedures_/{PROCEDURE_NAME}"
    )
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME
