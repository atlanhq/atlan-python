import os
import random
import string

import pytest
import requests

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.exceptions import AtlanServiceException
from pyatlan.model.assets import AtlasGlossary
from pyatlan.model.core import Announcement
from pyatlan.model.enums import AnnouncementType


@pytest.fixture
def client() -> EntityClient:
    return EntityClient(AtlanClient())


@pytest.fixture()
def announcement() -> Announcement:
    return Announcement(announcement_title="Important Announcement",
                        announcement_message='A message'.join(random.choices(string.ascii_lowercase, k=20)),
                        announcement_type=AnnouncementType.ISSUE)


@pytest.fixture(scope='session')
def atlan_host() -> str:
    return get_environment_variable('ATLAN_HOST')


@pytest.fixture(scope='session')
def atlan_api_key() -> str:
    return get_environment_variable('ATLAN_API_KEY')


def get_environment_variable(name) -> str:
    ret_value = os.environ[name]
    assert ret_value
    return ret_value


@pytest.fixture()
def glossary_guid(atlan_host, atlan_api_key) -> str:
    url = f"{atlan_host}/api/meta/entity/bulk"

    payload = {
        "entities": [
            {
                "attributes": {
                    "userDescription": "Some glossary description",
                    "name": "Integration Test Glossary",
                    "qualifiedName": "",
                    "certificateStatus": "DRAFT",
                    "ownersUsers": [],
                    "ownerGroups": []
                },
                "typeName": "AtlasGlossary"
            }
        ]
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'authorization': f'Bearer {atlan_api_key}',
    }
    response = requests.request("POST", url, headers=headers, json=payload)

    return list(response.json()['guidAssignments'].values())[0]


@pytest.fixture(autouse=True)
def cleanup_glossaries(atlan_host, atlan_api_key):
    def delete_glossaries():
        url = f"{atlan_host}/api/meta/glossary"
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {atlan_api_key}'
        }

        response = requests.request("GET", url, headers=headers)

        for glossary in response.json():
            if glossary['name'].startswith("Integration Test"):
                url = f"https://mark.atlan.com/api/meta/entity/guid/{glossary['guid']}?deleteType=HARD"
                response = requests.delete(url, headers=headers)
                response.raise_for_status()

    delete_glossaries()
    yield
    delete_glossaries()


def test_get_glossary_by_guid_good_guid(glossary_guid: str, client: EntityClient):
    glossary = client.get_entity_by_guid(glossary_guid, AtlasGlossary)
    assert isinstance(glossary, AtlasGlossary)


def test_get_glossary_by_guid_bad_guid(client: EntityClient):
    with pytest.raises(AtlanServiceException) as ex_info:
        client.get_entity_by_guid("76d54dd6-925b-499b-a455-6", AtlasGlossary)
    assert 'Given instance guid 76d54dd6-925b-499b-a455-6 is invalid/not found' in ex_info.value.args[0]


def test_update_glossary_when_no_changes(client: EntityClient):
    glossary = client.get_entity_by_guid("76d54dd6-925b-499b-a455-6f756ae2d522", AtlasGlossary)
    response = client.update_entity(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities


def test_update_glossary_with_changes(glossary_guid: str, client: EntityClient, announcement):
    glossary = client.get_entity_by_guid(glossary_guid, AtlasGlossary)
    glossary.set_announcement(announcement)
    response = client.update_entity(glossary)
    assert not response.guid_assignments
    assert response.mutated_entities
    assert not response.mutated_entities.CREATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert response.mutated_entities.UPDATE[0]["attributes"]["announcementTitle"] == announcement.announcement_title
    glossary.clear_announcment()
    client.update_entity(glossary)


def test_purge_glossary(glossary_guid: str, client: EntityClient):
    response = client.purge_entity_by_guid(glossary_guid)
    assert len(response.mutated_entities.DELETE) == 1
    assert not response.mutated_entities.UPDATE
    assert not response.mutated_entities.CREATE


def test_create_glossary(client: EntityClient):
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(name="Integration Test Glossary", user_description="This a test glossary"))
    response = client.create_entity(glossary)
    assert not response.mutated_entities.UPDATE
    assert len(response.mutated_entities.CREATE) == 1
