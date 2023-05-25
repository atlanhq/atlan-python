# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import QueryParserSourceType
from pyatlan.model.query import QueryParserRequest


def test_parse_valid_query(client: AtlanClient):
    request = QueryParserRequest.create(
        sql="INSERT INTO orders (order_name, customer_id, product_id)"
        " VALUES(SELECT 'test_order', id, 21 FROM customers)",
        source=QueryParserSourceType.SNOWFLAKE,
    )
    request.default_database = "ORDERS"
    request.default_schema = "PRODUCTION"
    response = client.parse_query(request)
    assert response
    assert response.dbobjs
    assert response.relationships
    assert not response.errors


def test_parse_invalid_query(client: AtlanClient):
    request = QueryParserRequest.create(
        sql="INSERT INTO orders (order_name, customer_id, product_id)"
        " VALUES(SELECT 'test_order', id, 21 FROM customers)"
        " with some extra",
        source=QueryParserSourceType.SNOWFLAKE,
    )
    request.default_database = "ORDERS"
    request.default_schema = "PRODUCTION"
    response = client.parse_query(request)
    assert response
    assert not response.dbobjs
    assert not response.relationships
    assert response.errors
    assert len(response.errors) == 2
    assert response.errors[0].error_type == "SyntaxError"
