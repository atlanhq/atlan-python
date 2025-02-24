import pytest

from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid, message",
    [
        (None, None, None, "1234", "name is required"),
        (
            "Glossary",
            None,
            None,
            None,
            "One of the following parameters are required: anchor, glossary_qualified_name, glossary_guid",
        ),
        (
            "Glossary",
            AtlasGlossary(),
            "qname",
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name",
        ),
        (
            "Glossary",
            AtlasGlossary(),
            None,
            "123",
            "Only one of the following parameters are allowed: anchor, glossary_guid",
        ),
        (
            "Glossary",
            None,
            "qname",
            "123",
            "Only one of the following parameters are allowed: glossary_qualified_name, glossary_guid",
        ),
    ],
)
def test_create_atttributes_without_required_parameters_raises_value_error(
    name, anchor, glossary_qualified_name, glossary_guid, message
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryTerm.Attributes.create(
            name=name,
            anchor=anchor,
            glossary_qualified_name=glossary_qualified_name,
            glossary_guid=glossary_guid,
        )


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid",
    [
        ("Glossary", AtlasGlossary(), None, None),
        ("Glossary", None, "glossary/qualifiedName", None),
        ("Glossary", None, None, "123"),
    ],
)
def test_create_atttributes_with_required_parameters(
    name, anchor, glossary_qualified_name, glossary_guid
):
    sut = AtlasGlossaryTerm.Attributes.create(
        name=name,
        anchor=anchor,
        glossary_qualified_name=glossary_qualified_name,
        glossary_guid=glossary_guid,
    )

    if anchor:
        assert anchor == sut.anchor
    if glossary_qualified_name:
        assert sut.anchor.unique_attributes == {
            "qualifiedName": glossary_qualified_name
        }
    if glossary_guid:
        assert sut.anchor.guid == glossary_guid


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid, message",
    [
        (None, None, None, "1234", "name is required"),
        (
            "Glossary",
            None,
            None,
            None,
            "One of the following parameters are required: anchor, glossary_qualified_name, glossary_guid",
        ),
        (
            "Glossary",
            AtlasGlossary(),
            "qname",
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name",
        ),
        (
            "Glossary",
            AtlasGlossary(),
            None,
            "123",
            "Only one of the following parameters are allowed: anchor, glossary_guid",
        ),
        (
            "Glossary",
            None,
            "qname",
            "123",
            "Only one of the following parameters are allowed: glossary_qualified_name, glossary_guid",
        ),
    ],
)
def test_create_without_required_parameters_raises_value_error(
    name, anchor, glossary_qualified_name, glossary_guid, message
):
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryTerm.create(
            name=name,
            anchor=anchor,
            glossary_qualified_name=glossary_qualified_name,
            glossary_guid=glossary_guid,
        )


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid",
    [
        ("Glossary", AtlasGlossary(), None, None),
        ("Glossary", None, "glossary/qualifiedName", None),
        ("Glossary", None, None, "123"),
    ],
)
def test_create_with_required_parameters(
    name, anchor, glossary_qualified_name, glossary_guid
):
    sut = AtlasGlossaryTerm.create(
        name=name,
        anchor=anchor,
        glossary_qualified_name=glossary_qualified_name,
        glossary_guid=glossary_guid,
    )

    if anchor:
        assert anchor == sut.attributes.anchor
    if glossary_qualified_name:
        assert sut.attributes.anchor.unique_attributes == {
            "qualifiedName": glossary_qualified_name
        }
    if glossary_guid:
        assert sut.attributes.anchor.guid == glossary_guid
