import pytest

from pyatlan.model.assets import DataDomain, DataProduct
from tests.unit.model.constants import (
    DATA_PRODUCT_MESH_ABBREVIATION,
    DATA_PRODUCT_MESH_SLUG,
    DATA_PRODUCT_NAME,
    DATA_PRODUCT_QUALIFIED_NAME,
)


def _assert_product(product: DataProduct) -> None:
    assert product.name == DATA_PRODUCT_NAME
    assert product.mesh_slug == DATA_PRODUCT_MESH_SLUG
    assert product.mesh_abbreviation == DATA_PRODUCT_MESH_ABBREVIATION
    assert product.qualified_name == DATA_PRODUCT_QUALIFIED_NAME


@pytest.mark.parametrize(
    "name, assets_dsl, domain, domain_guid, message",
    [
        (None, "test_dsl", None, "domain-guid-1-2-3", "name is required"),
        (DATA_PRODUCT_NAME, None, None, "domain-guid-1-2-3", "assets_dsl is required"),
        (
            DATA_PRODUCT_NAME,
            "test_dsl",
            None,
            None,
            "One of the following parameters are required: domain, domain_guid",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, assets_dsl: str, domain: DataDomain, domain_guid: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataProduct.create(
            name=name, assets_dsl=assets_dsl, domain=domain, domain_guid=domain_guid
        )


@pytest.mark.parametrize(
    "name, assets_dsl, domain, domain_guid",
    [
        (DATA_PRODUCT_NAME, "test_dsl", None, "domain-guid-1-2-3"),
        (DATA_PRODUCT_NAME, "test_dsl", DataDomain(), None),
    ],
)
def test_create_atttributes_with_required_parameters(
    name: str, assets_dsl: str, domain: DataDomain, domain_guid: str
):
    test_product = DataProduct.Attributes.create(
        name=name, assets_dsl=assets_dsl, domain=domain, domain_guid=domain_guid
    )
    if domain:
        assert domain == test_product.data_domain
    if domain_guid:
        assert domain_guid == test_product.data_domain.guid
    assert test_product.data_product_assets_d_s_l == assets_dsl
    _assert_product(test_product)


def test_create_for_modification():
    test_product = DataProduct.create_for_modification(
        name=DATA_PRODUCT_NAME,
        qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
        domain_guid="domain-guid-1-2-3",
    )
    _assert_product(test_product)


def test_trim_to_required():
    test_product = DataProduct.create_for_modification(
        qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
        name=DATA_PRODUCT_NAME,
        domain_guid="domain-guid-1-2-3",
    ).trim_to_required()
    _assert_product(test_product)
