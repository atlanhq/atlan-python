import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import AtlasGlossary
from pyatlan.model.search import DSL, IndexSearchRequest


@pytest.fixture(scope="module")
def client() -> EntityClient:
    return EntityClient(AtlanClient())


def test_index_search(client: EntityClient):
    dsl = DSL(
        post_filter={
            "bool": {
                "filter": {
                    "bool": {
                        "filter": {"term": {"__typeName.keyword": "AtlasGlossary"}}
                    }
                }
            }
        },
        query={"bool": {"must": [{"term": {"__state": "ACTIVE"}}]}},
    )
    request = IndexSearchRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
    assets = client.index_search(criteria=request)
    assert len(list(assets)) > 0
    for asset in assets:
        assert isinstance(asset, AtlasGlossary)
