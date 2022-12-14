import pytest

from pyatlan.cache import ClassificationCache
from pyatlan.model.typedef import ClassificationDef
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.typedef import TypeDefClient

CLS_NAME = "psdk-ClassificationTest"

@pytest.fixture
def client() -> TypeDefClient:
    return TypeDefClient(AtlanClient())

def test_classifications(client: TypeDefClient):
    cls = ClassificationDef(
        name=CLS_NAME,
        display_name=CLS_NAME,
        options={
            "color": "GREEN"
        }
    )
    response = client.create_typedef(cls)
    print(response)
    assert response
    assert response.classification_defs
    assert len(response.classification_defs) == 1

    # Now test retrieval from the cache
    cls_id = ClassificationCache.get_id_for_name(CLS_NAME)
    print("Found ID: ", cls_id)
    assert cls_id
    cls_name = ClassificationCache.get_name_for_id(cls_id)
    print("Found name: ", cls_name)
    assert cls_name
    assert cls_name == CLS_NAME

    # And finally delete what we created
    client.purge_typedef(cls_id)
