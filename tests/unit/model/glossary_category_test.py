import pytest

from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory
from tests.unit.model.constants import (
    GLOSSARY_CATEGORY_NAME,
    GLOSSARY_CATEGORY_QUALIFIED_NAME,
    GLOSSARY_NAME,
    GLOSSARY_QUALIFIED_NAME,
)

ANCHOR = AtlasGlossary.create_for_modification(
    qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
)
GLOSSARY_GUID = "123"
PARENT_CATEGORY = AtlasGlossaryCategory.create_for_modification(
    qualified_name="123", name="Category", glossary_guid=GLOSSARY_GUID
)


@pytest.mark.parametrize(
    "name, anchor, parent_category, message",
    [
        (
            None,
            ANCHOR,
            None,
            "name is required",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    anchor: AtlasGlossary,
    parent_category: AtlasGlossaryCategory,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryCategory.create(
            name=name,
            anchor=anchor,
            parent_category=parent_category,
        )


@pytest.mark.parametrize(
    "anchor, parent_category",
    [
        (ANCHOR, None),
        (ANCHOR, PARENT_CATEGORY),
    ],
)
def test_create(
    anchor: AtlasGlossary,
    parent_category: AtlasGlossaryCategory,
):
    sut = AtlasGlossaryCategory.create(
        name=GLOSSARY_CATEGORY_NAME,
        anchor=anchor,
        parent_category=parent_category,
    )

    assert sut.name == GLOSSARY_CATEGORY_NAME
    assert sut.qualified_name
    assert sut.parent_category == parent_category
    assert sut.anchor == anchor


@pytest.mark.parametrize(
    "name, qualified_name, glossary_guid, message",
    [
        (None, GLOSSARY_CATEGORY_QUALIFIED_NAME, GLOSSARY_GUID, "name is required"),
        (GLOSSARY_CATEGORY_NAME, None, GLOSSARY_GUID, "qualified_name is required"),
        (
            GLOSSARY_CATEGORY_NAME,
            GLOSSARY_CATEGORY_QUALIFIED_NAME,
            None,
            "glossary_guid is required",
        ),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    name: str, qualified_name: str, glossary_guid: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryCategory.create_for_modification(
            qualified_name=qualified_name, name=name, glossary_guid=glossary_guid
        )


def test_create_for_modification():
    sut = AtlasGlossaryCategory.create_for_modification(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    )

    assert sut.name == GLOSSARY_CATEGORY_NAME
    assert sut.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


def test_update_when_parent_category_is_removed():
    category = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    )
    assert category.parent_category is None
    assert category.relationship_attributes is None
    assert category.anchor.guid == GLOSSARY_GUID
    assert category.name == GLOSSARY_CATEGORY_NAME
    assert category.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME

    category.parent_category = None
    assert category.parent_category is None
    assert category.relationship_attributes == {"parentCategory": None}


def test_trim_to_required():
    sut = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    ).trim_to_required()

    assert sut.name == GLOSSARY_CATEGORY_NAME
    assert sut.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


@pytest.mark.parametrize(
    "anchor",
    [(None), (AtlasGlossary())],
)
def test_trim_to_required_raises_value_error_when_anchor_is_none(anchor):
    sut = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    )
    sut.anchor = anchor

    with pytest.raises(ValueError, match="anchor.guid must be available"):
        sut.trim_to_required()
