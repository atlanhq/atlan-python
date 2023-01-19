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
def test_index_search(
    client: EntityClient, query, post_filter, attributes, sort_order, a_class
):
    dsl = DSL(query=query, post_filter=post_filter, sort=sort_order)
    request = IndexSearchRequest(dsl=dsl, attributes=attributes)
    assets = client.index_search(criteria=request)
    counter = 0
    for asset in assets:
        # if asset.scrubbed:
        #     continue
        assert isinstance(asset, a_class)
        counter += 1
        if counter > 3:
            break
    assert counter > 0
