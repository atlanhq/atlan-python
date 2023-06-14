import pytest

from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from tests.unit.model.constants import (
    GLOSSARY_NAME,
    GLOSSARY_QUALIFIED_NAME,
    GLOSSARY_TERM_NAME,
    GLOSSARY_TERM_QUALIFIED_NAME,
)

ANCHOR = AtlasGlossary.create_for_modification(
    qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
)
GLOSSARY_GUID = "123"


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid, categories, message",
    [
        (
            None,
            ANCHOR,
            GLOSSARY_QUALIFIED_NAME,
            GLOSSARY_GUID,
            None,
            "name is required",
        ),
        (
            GLOSSARY_TERM_NAME,
            ANCHOR,
            GLOSSARY_QUALIFIED_NAME,
            GLOSSARY_GUID,
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name, glossary_guid",
        ),
        (
            GLOSSARY_TERM_NAME,
            ANCHOR,
            GLOSSARY_QUALIFIED_NAME,
            None,
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name",
        ),
        (
            GLOSSARY_TERM_NAME,
            ANCHOR,
            None,
            GLOSSARY_GUID,
            None,
            "Only one of the following parameters are allowed: anchor, glossary_guid",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            GLOSSARY_QUALIFIED_NAME,
            GLOSSARY_GUID,
            None,
            "Only one of the following parameters are allowed: glossary_qualified_name, glossary_guid",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            None,
            None,
            None,
            "One of the following parameters are required: anchor, glossary_qualified_name, glossary_guid",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    anchor: AtlasGlossary,
    glossary_qualified_name: str,
    glossary_guid: str,
    categories: list[AtlasGlossaryCategory],
    message: str,
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryTerm.create(
            name=name,
            anchor=anchor,
            glossary_qualified_name=glossary_qualified_name,
            glossary_guid=glossary_guid,
            categories=categories,
        )


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid, categories",
    [
        (ANCHOR, None, None, None),
        (None, GLOSSARY_QUALIFIED_NAME, None, None),
        (
            None,
            None,
            GLOSSARY_GUID,
            [
                AtlasGlossaryCategory.create_for_modification(
                    qualified_name="123", name="Category"
                )
            ],
        ),
    ],
)
def create(
    anchor: AtlasGlossary,
    glossary_qualified_name: str,
    glossary_guid: str,
    categories: list[AtlasGlossaryCategory],
):
    sut = AtlasGlossaryTerm.create(
        name=GLOSSARY_TERM_NAME,
        anchor=anchor,
        glossary_qualified_name=glossary_qualified_name,
        glossary_guid=glossary_guid,
        categories=categories,
    )

    assert sut.name == GLOSSARY_TERM_NAME
    assert sut.qualified_name
    assert sut.categories == categories
    if anchor:
        assert sut.anchor == anchor
    if glossary_qualified_name:
        assert sut.anchor.qualified_name == glossary_qualified_name
    if glossary_guid:
        assert sut.anchor.guid == glossary_guid


@pytest.mark.parametrize(
    "name, qualified_name, glossary_guid, message",
    [
        (None, GLOSSARY_TERM_QUALIFIED_NAME, GLOSSARY_GUID, "name is required"),
        (GLOSSARY_TERM_NAME, None, GLOSSARY_GUID, "qualified_name is required"),
        (
            GLOSSARY_TERM_NAME,
            GLOSSARY_TERM_QUALIFIED_NAME,
            None,
            "glossary_guid is required",
        ),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    name: str, qualified_name: str, glossary_guid: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryTerm.create_for_modification(
            qualified_name=qualified_name, name=name, glossary_guid=glossary_guid
        )


def test_create_for_modification():
    sut = AtlasGlossaryTerm.create_for_modification(
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        name=GLOSSARY_TERM_NAME,
        glossary_guid=GLOSSARY_GUID,
    )

    assert sut.name == GLOSSARY_TERM_NAME
    assert sut.qualified_name == GLOSSARY_TERM_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


def test_trim_to_required():
    sut = AtlasGlossaryTerm.create_for_modification(
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        name=GLOSSARY_TERM_NAME,
        glossary_guid=GLOSSARY_GUID,
    ).trim_to_required()

    assert sut.name == GLOSSARY_TERM_NAME
    assert sut.qualified_name == GLOSSARY_TERM_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID
