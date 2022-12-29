import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import AtlasGlossary
from pyatlan.model.search import DSL, IndexSearchRequest, Term


@pytest.fixture(scope="module")
def client() -> EntityClient:
    return EntityClient(AtlanClient())


def test_index_search(client: EntityClient):
    dsl = DSL(
        query=Term(field="__state", value="ACTIVE"),
        post_filter=Term(field="__typeName.keyword", value="AtlasGlossary"),
    )
    request = IndexSearchRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
    assets = client.index_search(criteria=request)
    assert len(list(assets)) > 0
    for asset in assets:
        assert isinstance(asset, AtlasGlossary)
