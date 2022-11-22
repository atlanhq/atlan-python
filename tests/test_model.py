from pathlib import Path
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm, AtlasGlossaryCategory
import pytest
import json

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

def test_glossary_term(glossary_term_json):
    AtlasGlossaryTerm(**glossary_term_json)

def test_glossary_category(glossary_category_json):
    AtlasGlossaryCategory(**glossary_category_json)