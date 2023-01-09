import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import AtlasGlossary, Connection, Database
from pyatlan.model.search import DSL, IndexSearchRequest, Term


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
            Term(field="connectorName", value="snowflake"),
            Term(field="__typeName.keyword", value="Connection"),
            ["schemaName", "databaseName"],
            Connection,
        ),
        (
            Term(field="connectorName", value="snowflake"),
            Term(field="__typeName.keyword", value="Database"),
            ["schemaName", "databaseName"],
            Database,
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
    assert len(list(assets)) > 0
    for asset in assets:
        assert isinstance(asset, a_class)
