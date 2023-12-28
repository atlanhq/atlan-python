import pytest

from pyatlan.model.assets import DataDomain, DataProduct
from pyatlan.model.search import DSL, IndexSearchRequest, Term
from tests.unit.model.constants import (
    DATA_DOMAIN_QUALIFIED_NAME,
    DATA_PRODUCT_NAME,
    DATA_PRODUCT_QUALIFIED_NAME,
)

dsl = DSL(
    query=Term(field="__typeName.keyword", value="Schema"),
    post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
)
assets = IndexSearchRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
assets_dsl = assets.get_dsl_str()


def _assert_product(product: DataProduct) -> None:
    assert product.name == DATA_PRODUCT_NAME
    assert product.qualified_name == DATA_PRODUCT_QUALIFIED_NAME


@pytest.mark.parametrize(
    "name, assets, domain, domain_qualified_name, message",
    [
        (None, assets, None, DATA_DOMAIN_QUALIFIED_NAME, "name is required"),
        (
            DATA_PRODUCT_NAME,
            None,
            None,
            DATA_DOMAIN_QUALIFIED_NAME,
            "assets is required",
        ),
        (
            DATA_PRODUCT_NAME,
            assets,
            None,
            None,
            "One of the following parameters are required: domain, domain_qualified_name",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    assets: IndexSearchRequest,
    domain: DataDomain,
    domain_qualified_name: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        DataProduct.create(
            name=name,
            assets=assets,
            domain=domain,
            domain_qualified_name=domain_qualified_name,
        )


@pytest.mark.parametrize(
    "name, assets, domain, domain_qualified_name",
    [
        (DATA_PRODUCT_NAME, assets, DataDomain(), None),
        (DATA_PRODUCT_NAME, assets, None, DATA_DOMAIN_QUALIFIED_NAME),
    ],
)
def test_create(
    name: str,
    assets: IndexSearchRequest,
    domain: DataDomain,
    domain_qualified_name: str,
):
    test_product = DataProduct.create(
        name=name,
        assets=assets,
        domain=domain,
        domain_qualified_name=domain_qualified_name,
    )
    if domain:
        assert domain == test_product.data_domain
    if domain_qualified_name:
        assert test_product.data_domain.unique_attributes == {
            "qualifiedName": domain_qualified_name
        }
    assert test_product.data_product_assets_d_s_l == assets_dsl
    _assert_product(test_product)


def test_create_for_modification():
    test_product = DataProduct.create_for_modification(
        name=DATA_PRODUCT_NAME,
        qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
    )
    _assert_product(test_product)


def test_trim_to_required():
    test_product = DataProduct.create_for_modification(
        qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
        name=DATA_PRODUCT_NAME,
    ).trim_to_required()
    _assert_product(test_product)
