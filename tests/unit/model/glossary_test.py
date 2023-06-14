import pytest

from pyatlan.model.assets import AtlasGlossary
from tests.unit.model.constants import GLOSSARY_NAME, GLOSSARY_QUALIFIED_NAME


def test_create_with_missing_parameters_raise_value_error():
    with pytest.raises(ValueError, match="name is required"):
        AtlasGlossary.create(name=None)


def test_create():
    sut = AtlasGlossary.create(name=GLOSSARY_NAME)

    assert sut.name == GLOSSARY_NAME
    assert sut.qualified_name


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, GLOSSARY_QUALIFIED_NAME, "qualified_name is required"),
        (GLOSSARY_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossary.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = AtlasGlossary.create_for_modification(
        qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
    )

    assert sut.qualified_name == GLOSSARY_QUALIFIED_NAME
    assert sut.name == GLOSSARY_NAME


def test_trim_to_required():
    sut = AtlasGlossary.create_for_modification(
        qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
    ).trim_to_required()

    assert sut.qualified_name == GLOSSARY_QUALIFIED_NAME
    assert sut.name == GLOSSARY_NAME
