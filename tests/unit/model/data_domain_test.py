import pytest

from pyatlan.model.assets import DataDomain
from tests.unit.model.constants import (
    DATA_DOMAIN_NAME,
    DATA_DOMAIN_QUALIFIED_NAME,
    DATA_SUB_DOMAIN_NAME,
)


def _assert_domain(domain: DataDomain) -> None:
    assert domain.name == DATA_DOMAIN_NAME
    assert domain.qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    assert domain.parent_domain_qualified_name is None


@pytest.mark.parametrize(
    "name, message",
    [(None, "name is required")],
)
def test_create_with_missing_parameters_raise_value_error(name: str, message: str):
    with pytest.raises(ValueError, match=message):
        DataDomain.create(name=name)


def test_create_atttributes_with_required_parameters():
    test_domain = DataDomain.Attributes.create(
        name=DATA_DOMAIN_NAME,
        parent_domain_qualified_name=DATA_DOMAIN_QUALIFIED_NAME,
    )
    assert test_domain.parent_domain.unique_attributes == {
        "qualifiedName": DATA_DOMAIN_QUALIFIED_NAME
    }


def test_create():
    test_domain = DataDomain.create(name=DATA_DOMAIN_NAME)
    test_domain.qualified_name = DATA_DOMAIN_QUALIFIED_NAME
    _assert_domain(test_domain)

    test_sub_domain = DataDomain.create(
        name=DATA_SUB_DOMAIN_NAME,
        parent_domain_qualified_name=test_domain.qualified_name,
    )
    assert test_sub_domain.name == DATA_SUB_DOMAIN_NAME
    assert test_sub_domain.qualified_name == DATA_SUB_DOMAIN_NAME
    assert test_sub_domain.parent_domain_qualified_name == test_domain.qualified_name


def test_create_for_modification():
    test_domain = DataDomain.create_for_modification(
        name=DATA_DOMAIN_NAME, qualified_name=DATA_DOMAIN_QUALIFIED_NAME
    )
    _assert_domain(test_domain)


def test_trim_to_required():
    test_domain = DataDomain.create_for_modification(
        qualified_name=DATA_DOMAIN_QUALIFIED_NAME, name=DATA_DOMAIN_NAME
    ).trim_to_required()
    _assert_domain(test_domain)
