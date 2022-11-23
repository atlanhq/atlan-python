import json
from pathlib import Path

import pytest
from pydantic.error_wrappers import ValidationError

from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm, AtlasGlossaryCategory
from pyatlan.model.core import AssetResponse

PARENT_DIR = Path(__file__).parent
GLOSSARY_JSON = 'glossary.json'
GLOSSARY_TERM_JSON = "glossary_term.json"
GLOSSARY_CATEGORY_JSON = "glossary_category.json"


def load_json(filename):
    with (PARENT_DIR / filename).open() as input_file:
        return json.load(input_file)


@pytest.fixture()
def glossary_json():
    return load_json(GLOSSARY_JSON)


@pytest.fixture()
def glossary_term_json():
    return load_json(GLOSSARY_TERM_JSON)


@pytest.fixture()
def glossary_category_json():
    return load_json(GLOSSARY_CATEGORY_JSON)


def test_glossary(glossary_json):
    AtlasGlossary(**glossary_json)


def test_wrong_json(glossary_json):
    with pytest.raises(ValidationError):
        AtlasGlossaryTerm(**glossary_json)


def test_glossary_term(glossary_term_json):
    AtlasGlossaryTerm(**glossary_term_json)


def test_glossary_category(glossary_category_json):
    AtlasGlossaryCategory(**glossary_category_json)


def test_asset_response(glossary_category_json):
    asset_response_json = {"referredEntities": {}, "entity": glossary_category_json}
    glossary_category = AssetResponse[AtlasGlossaryCategory](**asset_response_json).entity
    assert glossary_category == AtlasGlossaryCategory(**glossary_category_json)
