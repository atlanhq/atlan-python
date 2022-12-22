import json
from pathlib import Path

import pytest
from deepdiff import DeepDiff
from pydantic.error_wrappers import ValidationError

from pyatlan.model.assets import (
    AssetMutationResponse,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
)
from pyatlan.model.core import Announcement, AssetResponse
from pyatlan.model.enums import AnnouncementType

DATA_DIR = Path(__file__).parent / "data"
GLOSSARY_JSON = "glossary.json"
GLOSSARY_TERM_JSON = "glossary_term.json"
GLOSSARY_CATEGORY_JSON = "glossary_category.json"


def load_json(filename):
    with (DATA_DIR / filename).open() as input_file:
        return json.load(input_file)


@pytest.fixture()
def glossary_json():
    return load_json(GLOSSARY_JSON)


@pytest.fixture()
def glossary(glossary_json):
    return AtlasGlossary(**glossary_json)


@pytest.fixture()
def announcement():
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="Very important info",
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture()
def glossary_term_json():
    return load_json(GLOSSARY_TERM_JSON)


@pytest.fixture()
def glossary_category_json():
    return load_json(GLOSSARY_CATEGORY_JSON)


def test_wrong_json(glossary_json):
    with pytest.raises(ValidationError):
        AtlasGlossaryTerm(**glossary_json)


def test_asset_response(glossary_category_json):
    asset_response_json = {"referredEntities": {}, "entity": glossary_category_json}
    glossary_category = AssetResponse[AtlasGlossaryCategory](
        **asset_response_json
    ).entity
    assert glossary_category == AtlasGlossaryCategory(**glossary_category_json)


@pytest.fixture(scope="function")
def the_json(request):
    return load_json(request.param)


@pytest.mark.parametrize(
    "the_json, a_type",
    [
        ("glossary.json", AtlasGlossary),
        ("glossary_category.json", AtlasGlossaryCategory),
        ("glossary_term.json", AtlasGlossaryTerm),
        ("glossary_term2.json", AtlasGlossaryTerm),
        ("asset_mutated_response_empty.json", AssetMutationResponse),
        ("asset_mutated_response_update.json", AssetMutationResponse),
    ],
    indirect=["the_json"],
)
def test_constructor(the_json, a_type):
    asset = a_type(**the_json)
    assert not DeepDiff(
        the_json,
        json.loads(asset.json(by_alias=True, exclude_unset=True)),
        ignore_order=True,
    )


def test_has_announcement(glossary):
    assert glossary.has_announcement() == (
        bool(glossary.attributes.announcement_type)
        or bool(glossary.attributes.announcement_title)
    )


def test_set_announcement(glossary, announcement):
    glossary.set_announcement(announcement)
    assert glossary.has_announcement() is True
    assert announcement == glossary.get_announcment()


def test_create_glossary():
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name="Integration Test Glossary", user_description="This a test glossary"
        )
    )
    assert "AtlasGlossary" == glossary.type_name


def test_clear_announcement(glossary, announcement):
    glossary.set_announcement(announcement)
    glossary.clear_announcment()
    assert not glossary.has_announcement()
    assert glossary.attributes.announcement_title is None
    assert glossary.attributes.announcement_type is None
    assert glossary.attributes.announcement_message is None
