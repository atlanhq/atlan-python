import pytest

from pyatlan.model.assets import DataDomain
from tests.unit.model.constants import DATA_MESH_SLUG, DATA_MESH_ABBREVIATION, DATA_DOMAIN_NAME, DATA_SUB_DOMAIN_NAME, DATA_DOMAIN_QUALIFIED_NAME


def _assert_domain(domain: DataDomain) -> None:
    assert domain.name == DATA_DOMAIN_NAME
    assert domain.mesh_slug == DATA_MESH_SLUG
    assert domain.mesh_abbreviation == DATA_MESH_ABBREVIATION
    assert domain.qualified_name == DATA_DOMAIN_QUALIFIED_NAME

@pytest.mark.parametrize(
    "name, message",
    [
        (None, "name is required")
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataDomain.create(name=name)

def test_create():
    test_domain = DataDomain.create(name=DATA_DOMAIN_NAME)
    test_domain.guid = "parent-domain-guid-1-2-3" 
    _assert_domain(test_domain)

    test_sub_domain = DataDomain.create(name=DATA_SUB_DOMAIN_NAME, parent_domain_guid=test_domain.guid)
    assert test_sub_domain.name == DATA_SUB_DOMAIN_NAME
    assert test_sub_domain.parent_domain.guid == test_domain.guid

@pytest.mark.parametrize(
    "name, parent_domain, parent_domain_guid",
    [
        ("DataDomain", None, None),
        ("DataDomain", DataDomain(), None),
        ("DataDomain", None, "parent-domain-guid-1-2-3"),
    ],
)
def test_create_atttributes_with_required_parameters(
    name, parent_domain, parent_domain_guid
):
    test_domain = DataDomain.Attributes.create(
        name=name,
        parent_domain=parent_domain,
        parent_domain_guid=parent_domain_guid,
    )

    if parent_domain:
        assert parent_domain == test_domain.parent_domain
    if parent_domain_guid:
        assert parent_domain_guid == test_domain.parent_domain.guid

def test_create_for_modification():
    test_domain = DataDomain.create_for_modification(name=DATA_DOMAIN_NAME, qualified_name=DATA_DOMAIN_QUALIFIED_NAME)
    _assert_domain(test_domain)


def test_trim_to_required():
    test_domain = DataDomain.create_for_modification(qualified_name=DATA_DOMAIN_QUALIFIED_NAME, name=DATA_DOMAIN_NAME).trim_to_required()
    _assert_domain(test_domain)
