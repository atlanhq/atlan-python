import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import AtlasGlossary
from pyatlan.exceptions import AtlanServiceException

@pytest.fixture
def client():
    return EntityClient(AtlanClient())

def test_get_entity_by_guid_good_guid(client):
    glossary = client.get_entity_by_guid("76d54dd6-925b-499b-a455-6f756ae2d522", AtlasGlossary)
    assert isinstance(glossary, AtlasGlossary)


def test_get_entity_by_guid_bad_guid(client):
    with pytest.raises(AtlanServiceException) as ex_info:
        client.get_entity_by_guid("76d54dd6-925b-499b-a455-6", AtlasGlossary)
    assert 'Given instance guid 76d54dd6-925b-499b-a455-6 is invalid/not found' in  ex_info.value.args[0]

