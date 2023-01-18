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
from pyatlan.model.search import DSL, Exists, IndexSearchRequest, Term


@pytest.fixture(scope="module")
def client() -> EntityClient:
    return EntityClient(AtlanClient())


@pytest.mark.parametrize(
    "query,  post_filter, attributes, a_class",
    [
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="AtlasGlossary"),
            ["schemaName", "databaseName"],
            AtlasGlossary,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Connection")
            + Exists(field="category")
            + Term(field="adminUsers", value="ernest"),
            ["schemaName", "databaseName"],
            Connection,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Database"),
            ["schemaName", "databaseName"],
            Database,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Schema"),
            ["schemaName", "databaseName"],
            Schema,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="Table"),
            ["schemaName", "databaseName"],
            Table,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="View"),
            ["schemaName", "databaseName"],
            View,
        ),
        (
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="MaterialisedView"),
            ["schemaName", "databaseName"],
            MaterialisedView,
        ),
    ],
)
def test_index_search(client: EntityClient, query, post_filter, attributes, a_class):
    dsl = DSL(
        query=query,
        post_filter=post_filter,
    )
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
