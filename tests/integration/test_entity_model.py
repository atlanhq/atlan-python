import os
import random
import string

import pytest
import requests

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.entity import EntityClient
from pyatlan.exceptions import AtlanServiceException
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from pyatlan.model.core import Announcement
from pyatlan.model.enums import AnnouncementType


@pytest.fixture(scope="module")
def client() -> EntityClient:
    return EntityClient(AtlanClient())


@pytest.fixture()
def announcement() -> Announcement:
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="A message".join(
            random.choices(string.ascii_lowercase, k=20)  # nosec
        ),
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture(scope="session")
def atlan_host() -> str:
    return get_environment_variable("ATLAN_HOST")


@pytest.fixture(scope="session")
def atlan_api_key() -> str:
    return get_environment_variable("ATLAN_API_KEY")


@pytest.fixture(scope="session")
def headers(atlan_api_key):
    return {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "authorization": f"Bearer {atlan_api_key}",
    }


def get_environment_variable(name) -> str:
    ret_value = os.environ[name]
    assert ret_value
    return ret_value


@pytest.fixture()
def increment_counter():
    i = random.randint(0, 1000)

    def increment():
        nonlocal i
        i += 1
        return i

    return increment


@pytest.fixture()
def glossary_guids(atlan_host, headers):
    return get_guids(atlan_host, headers, "AtlasGlossary")


@pytest.fixture()
def create_glossary(atlan_host, headers, increment_counter):
    def create_it():
        suffix = increment_counter()
        url = f"{atlan_host}/api/meta/entity/bulk"
        payload = {
            "entities": [
                {
                    "attributes": {
                        "userDescription": f"Integration Test Glossary {suffix}",
                        "name": f"Integration Test Glossary {suffix}",
                        "qualifiedName": "",
                        "certificateStatus": "DRAFT",
                        "ownersUsers": [],
                        "ownerGroups": [],
                    },
                    "typeName": "AtlasGlossary",
                }
            ]
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        guid = list(data["guidAssignments"].values())[0]
        return guid

    return create_it


def get_guids(atlan_host, headers, type_name):
    url = f"{atlan_host}/api/meta/search/indexsearch"

    payload = {
        "dsl": {
            "from": 0,
            "size": 100,
            "query": {
                "bool": {
                    "must": [
                        {"term": {"__state": "ACTIVE"}},
                        {"prefix": {"name.keyword": {"value": "Integration"}}},
                    ]
                }
            },
            "post_filter": {
                "bool": {"filter": {"term": {"__typeName.keyword": type_name}}}
            },
        },
        "attributes": ["connectorName"],
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    if "entities" in data:
        return [entity["guid"] for entity in data["entities"]]
    else:
        return []


def delete_asset(atlan_host, headers, guid):
    url = f"{atlan_host}/api/meta/entity/guid/{guid}?deleteType=HARD"
    response = requests.delete(url, headers=headers)
    response.raise_for_status()


def delete_assets(atlan_host, headers, type_name):
    for guid in get_guids(atlan_host, headers, type_name):
        delete_asset(atlan_host, headers, guid)


@pytest.fixture(autouse=True, scope="module")
def cleanup_terms(atlan_host, headers, atlan_api_key):
    delete_assets(atlan_host, headers, "AtlasGlossaryTerm")
    yield
    delete_assets(atlan_host, headers, "AtlasGlossaryTerm")


@pytest.fixture(autouse=True, scope="module")
def cleanup_categories(atlan_host, headers, atlan_api_key):
    delete_assets(atlan_host, headers, "AtlasGlossaryCategory")
    yield
    delete_assets(atlan_host, headers, "AtlasGlossaryCategory")


@pytest.fixture(autouse=True, scope="module")
def cleanup_glossaries(atlan_host, headers, atlan_api_key):
    delete_assets(atlan_host, headers, "AtlasGlossary")
    yield
    delete_assets(atlan_host, headers, "AtlasGlossary")


def test_get_glossary_by_guid_good_guid(create_glossary, client: EntityClient):
    glossary = client.get_entity_by_guid(create_glossary(), AtlasGlossary)
    assert isinstance(glossary, AtlasGlossary)


def test_get_glossary_by_guid_bad_guid(client: EntityClient):
    with pytest.raises(AtlanServiceException) as ex_info:
        client.get_entity_by_guid("76d54dd6-925b-499b-a455-6", AtlasGlossary)
    assert (
        "Given instance guid 76d54dd6-925b-499b-a455-6 is invalid/not found"
        in ex_info.value.args[0]
    )


def test_update_glossary_when_no_changes(create_glossary, client: EntityClient):
    glossary = client.get_entity_by_guid(create_glossary(), AtlasGlossary)
    response = client.upsert(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities


def test_update_glossary_with_changes(
    create_glossary, client: EntityClient, announcement
):
    glossary = client.get_entity_by_guid(create_glossary(), AtlasGlossary)
    glossary.set_announcement(announcement)
    response = client.upsert(glossary)
    assert not response.guid_assignments
    assert response.mutated_entities
    assert not response.mutated_entities.CREATE
    assert not response.mutated_entities.DELETE
    assert len(response.mutated_entities.UPDATE) == 1
    glossary = response.mutated_entities.UPDATE[0]
    assert glossary.attributes.announcement_title == announcement.announcement_title


def test_purge_glossary(create_glossary, client: EntityClient):
    response = client.purge_entity_by_guid(create_glossary())
    assert len(response.mutated_entities.DELETE) == 1
    assert not response.mutated_entities.UPDATE
    assert not response.mutated_entities.CREATE


def test_create_glossary(client: EntityClient, increment_counter):
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {increment_counter()}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    assert not response.mutated_entities.UPDATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[glossary.guid]
    glossary = response.mutated_entities.CREATE[0]
    assert glossary.guid == guid


def test_create_multiple_glossaries_one_at_time(
    client: EntityClient, increment_counter
):
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {increment_counter()}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    assert not response.mutated_entities.UPDATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[glossary.guid]
    glossary = response.mutated_entities.CREATE[0]
    assert glossary.guid == guid
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {increment_counter()}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    assert not response.mutated_entities.UPDATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[glossary.guid]
    glossary = response.mutated_entities.CREATE[0]
    assert glossary.guid == guid


def test_create_multiple_glossaries(client: EntityClient, increment_counter):
    entities = []
    count = 2
    for i in range(count):
        entities.append(
            AtlasGlossary(
                attributes=AtlasGlossary.Attributes(
                    name=f"Integration Test Glossary {increment_counter() + i}",
                    user_description="This a test glossary",
                )
            )
        )
    response = client.upsert(entities)
    assert response.mutated_entities
    assert not response.mutated_entities.UPDATE
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == count
    for i in range(count):
        guid = response.guid_assignments[entities[i].guid]
        glossary = response.mutated_entities.CREATE[i]
        assert glossary.guid == guid


def test_create_glossary_category(client: EntityClient, increment_counter):
    suffix = increment_counter()
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {suffix}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    glossary = response.mutated_entities.CREATE[0]
    category = AtlasGlossaryCategory(
        attributes=AtlasGlossaryCategory.Attributes(
            name=f"Integration Test Glossary Category {suffix}",
            user_description="This is a test glossary category",
            anchor=glossary,
        )
    )
    response = client.upsert(category)
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[category.guid]
    category = response.mutated_entities.CREATE[0]
    assert isinstance(category, AtlasGlossaryCategory)
    assert guid == category.guid


def test_create_glossary_term(client: EntityClient, increment_counter):
    suffix = increment_counter()
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {suffix}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    glossary = response.mutated_entities.CREATE[0]
    term = AtlasGlossaryTerm(
        attributes=AtlasGlossaryTerm.Attributes(
            name=f"Integration Test Glossary Term {suffix}",
            user_description="This is a test glossary term",
            anchor=glossary,
        )
    )
    response = client.upsert(term)
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[term.guid]
    term = response.mutated_entities.CREATE[0]
    assert isinstance(term, AtlasGlossaryTerm)
    assert guid == term.guid


def test_create_hierarchy(client: EntityClient, increment_counter):
    suffix = increment_counter()
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {suffix}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    glossary = response.mutated_entities.CREATE[0]
    category_1 = AtlasGlossaryCategory(
        attributes=AtlasGlossaryCategory.Attributes(
            name=f"Integration Test Glossary Category {suffix}",
            user_description="This is a test glossary category",
            anchor=glossary,
        )
    )
    response = client.upsert(category_1)
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[category_1.guid]
    category_1 = response.mutated_entities.CREATE[0]
    assert isinstance(category_1, AtlasGlossaryCategory)
    assert guid == category_1.guid

    category_2 = AtlasGlossaryCategory(
        attributes=AtlasGlossaryCategory.Attributes(
            name=f"Integration Test Glossary Category {suffix}",
            user_description="This is a test glossary category",
            anchor=glossary,
            parent_category=category_1,
        )
    )
    response = client.upsert(category_2)
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 2
    if isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary):
        assert isinstance(response.mutated_entities.UPDATE[1], AtlasGlossaryCategory)
    else:
        assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossaryCategory)
        assert isinstance(response.mutated_entities.UPDATE[1], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[category_2.guid]
    category_2 = response.mutated_entities.CREATE[0]
    assert isinstance(category_2, AtlasGlossaryCategory)
    assert guid == category_2.guid

    term = AtlasGlossaryTerm(
        attributes=AtlasGlossaryTerm.Attributes(
            name=f"Integration Test term {suffix}",
            anchor=glossary,
            categories=[category_2],
        )
    )
    response = client.upsert(term)
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 2
    if isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary):
        assert isinstance(response.mutated_entities.UPDATE[1], AtlasGlossaryCategory)
    else:
        assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossaryCategory)
        assert isinstance(response.mutated_entities.UPDATE[1], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[term.guid]
    term = response.mutated_entities.CREATE[0]
    assert isinstance(term, AtlasGlossaryTerm)
    assert guid == term.guid
