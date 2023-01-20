import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import (
    AtlasGlossary,
    Connection,
    Database,
    MaterialisedView,
    Schema,
    Table,
    View,
)
from pyatlan.model.search import (
    DSL,
    Exists,
    IndexSearchRequest,
    SortItem,
    SortOrder,
    Term,
)


@pytest.fixture(scope="module")
def client() -> EntityClient:
    return EntityClient(AtlanClient())


@pytest.mark.parametrize(
    "query,  post_filter,attributes, sort_order, a_class",
    [
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="AtlasGlossary"),
            ["schemaName", "databaseName"],
            None,
            AtlasGlossary,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Connection")
            + Exists(field="category")
            + Term(field="adminUsers", value="ernest"),
            ["schemaName", "databaseName"],
            None,
            Connection,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Database"),
            ["schemaName", "databaseName"],
            None,
            Database,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Schema"),
            ["schemaName", "databaseName"],
            None,
            Schema,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Table"),
            ["schemaName", "databaseName"],
            [SortItem(field="__typeName.keyword", order=SortOrder.ASCENDING)],
            Table,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="View"),
            ["schemaName", "databaseName"],
            None,
            View,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="MaterialisedView"),
            ["schemaName", "databaseName"],
            None,
            MaterialisedView,
        ),
        (
            Term(field="__typeName.keyword", value="AtlasGlossary"),
            None,
            ["schemaName", "databaseName"],
            None,
            AtlasGlossary,
        ),
    ],
)
def test_search(
    client: EntityClient, query, post_filter, attributes, sort_order, a_class
):
    dsl = DSL(query=query, post_filter=post_filter, sort=sort_order)
    request = IndexSearchRequest(dsl=dsl, attributes=attributes)
    results = client.search(criteria=request)
    counter = 0
    for asset in results:
        assert isinstance(asset, a_class)
        counter += 1
        if counter > 3:
            break
    assert counter > 0


def test_search_next_page(client: EntityClient):
    size = 15
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.count > size
    assert len(results.current_page()) == size
    counter = 0
    while True:
        for _ in results.current_page():
            counter += 1
        if results.next_page() is not True:
            break
    assert counter == results.count


def test_search_iter(client: EntityClient):
    size = 15
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.count > size
    assert len([a for a in results]) == results.count


def test_search_next_when_start_changed_returns_remaining(client: EntityClient):
    size = 2
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.next_page(start=results.count - size) is True
    assert len(list(results)) == size
