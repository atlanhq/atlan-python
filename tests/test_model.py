import json
from pathlib import Path

import pytest
from pydantic.error_wrappers import ValidationError

from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm, AtlasGlossaryCategory
from pyatlan.model.core import AssetResponse, AssetMutationResponse

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


def test_wrong_json(glossary_json):
    with pytest.raises(ValidationError):
        AtlasGlossaryTerm(**glossary_json)


def test_asset_response(glossary_category_json):
    asset_response_json = {"referredEntities": {}, "entity": glossary_category_json}
    glossary_category = AssetResponse[AtlasGlossaryCategory](**asset_response_json).entity
    assert glossary_category == AtlasGlossaryCategory(**glossary_category_json)


@pytest.fixture(scope="function")
def the_json(request):
    return load_json(request.param)


@pytest.mark.parametrize("the_json, a_type",
                         [('glossary.json', AtlasGlossary),
                          ("glossary_category.json", AtlasGlossaryCategory),
                          ("glossary_term.json", AtlasGlossaryTerm),
                          ("glossary_term2.json", AtlasGlossaryTerm),
                          ("asset_mutated_response_empty.json", AssetMutationResponse[AtlasGlossary]),
                          ("asset_mutated_response_update.json", AssetMutationResponse[AtlasGlossary])],
                         indirect=["the_json"])
def test_indirect(the_json, a_type):
    asset = a_type(**the_json)
    assert isinstance(asset, a_type)
