import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.model.assets import AtlasGlossary
from pyatlan.model.core import Announcement
from pyatlan.model.enums import AnnouncementType
from pyatlan.exceptions import AtlanServiceException
import random
import string

@pytest.fixture
def client()->EntityClient:
    return EntityClient(AtlanClient())

@pytest.fixture()
def announcement():
    return Announcement(announcement_title="Important Announcement",
                        announcement_message='A message'.join(random.choices(string.ascii_lowercase, k=20)),
                        announcement_type=AnnouncementType.ISSUE)


def test_get_entity_by_guid_good_guid(client:EntityClient):
    glossary = client.get_entity_by_guid("76d54dd6-925b-499b-a455-6f756ae2d522", AtlasGlossary)
    assert isinstance(glossary, AtlasGlossary)


def test_get_entity_by_guid_bad_guid(client:EntityClient):
    with pytest.raises(AtlanServiceException) as ex_info:
        client.get_entity_by_guid("76d54dd6-925b-499b-a455-6", AtlasGlossary)
    assert 'Given instance guid 76d54dd6-925b-499b-a455-6 is invalid/not found' in  ex_info.value.args[0]

def test_update_entity_when_no_changes(client:EntityClient):
    glossary = client.get_entity_by_guid("76d54dd6-925b-499b-a455-6f756ae2d522", AtlasGlossary)
    response = client.update_entity(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities

def test_update_entity_with_changes(client:EntityClient, announcement):
    glossary = client.get_entity_by_guid("76d54dd6-925b-499b-a455-6f756ae2d522", AtlasGlossary)
    glossary.set_announcement(announcement)
    response = client.update_entity(glossary)
    assert not response.guid_assignments
    assert response.mutated_entities
    assert not response.mutated_entities.CREATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert response.mutated_entities.UPDATE[0]["attributes"]["announcementTitle"] == announcement.announcement_title
    glossary.clear_announcment()
    client.update_entity(glossary)
