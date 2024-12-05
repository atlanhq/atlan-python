from json import dumps, load, loads
from pathlib import Path

import pytest

from pyatlan.model.assets import AtlasGlossary, DataProduct
from pyatlan.model.enums import CertificateStatus, DataProductStatus
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import IndexSearchRequest
from tests.unit.model.constants import (
    DATA_DOMAIN_QUALIFIED_NAME,
    DATA_PRODUCT_NAME,
    DATA_PRODUCT_QUALIFIED_NAME,
    DATA_PRODUCT_UNDER_SUB_DOMAIN_QUALIFIED_NAME,
    DATA_SUB_DOMAIN_QUALIFIED_NAME,
)

TEST_DATA_DIR = Path(__file__).parent.parent / "data"
DATA_PRODUCT_ASSETS_DSL_JSON = "data_product_assets_dsl.json"
DATA_MESH_DIR = TEST_DATA_DIR / "data_mesh_requests"
ASSETS_PLAYBOOK_FILTER = '{"condition":"AND","isGroupLocked":false,"rules":[]}'


def load_json(respones_dir, filename):
    with (respones_dir / filename).open() as input_file:
        return load(input_file)


def to_json(model):
    return model.json(by_alias=True, exclude_none=True)


@pytest.fixture()
def data_product_assets_dsl_json():
    return load_json(DATA_MESH_DIR, DATA_PRODUCT_ASSETS_DSL_JSON)


@pytest.fixture()
def data_product_asset_selection():
    return (
        FluentSearch()
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossary))
        .where(AtlasGlossary.CERTIFICATE_STATUS.eq(CertificateStatus.VERIFIED.value))
    ).to_request()


def _assert_product(
    product: DataProduct, qualified_name: str = DATA_PRODUCT_QUALIFIED_NAME
) -> None:
    assert product.name == DATA_PRODUCT_NAME
    assert product.qualified_name == qualified_name


@pytest.mark.parametrize(
    "name, asset_selection, domain_qualified_name, message",
    [
        (
            None,
            data_product_asset_selection,
            DATA_DOMAIN_QUALIFIED_NAME,
            "name is required",
        ),
        (
            DATA_PRODUCT_NAME,
            None,
            DATA_DOMAIN_QUALIFIED_NAME,
            "asset_selection is required",
        ),
        (
            DATA_PRODUCT_NAME,
            data_product_asset_selection,
            None,
            "domain_qualified_name is required",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str,
    asset_selection: IndexSearchRequest,
    domain_qualified_name: str,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        DataProduct.create(
            name=name,
            asset_selection=asset_selection,
            domain_qualified_name=domain_qualified_name,
        )


def test_create(
    data_product_asset_selection: IndexSearchRequest, data_product_assets_dsl_json
):
    test_product = DataProduct.create(
        name=DATA_PRODUCT_NAME,
        asset_selection=data_product_asset_selection,
        domain_qualified_name=DATA_DOMAIN_QUALIFIED_NAME,
    )
    assert test_product.data_domain.unique_attributes == {
        "qualifiedName": DATA_DOMAIN_QUALIFIED_NAME
    }
    assert test_product.parent_domain_qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    assert test_product.super_domain_qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    test_asset_dsl = dumps(
        loads(test_product.data_product_assets_d_s_l), sort_keys=True
    )
    expected_asset_dsl = dumps(data_product_assets_dsl_json, sort_keys=True)
    assert test_asset_dsl == expected_asset_dsl
    assert test_product.data_product_assets_playbook_filter == ASSETS_PLAYBOOK_FILTER
    _assert_product(test_product)


def test_create_under_sub_domain(
    data_product_asset_selection: IndexSearchRequest, data_product_assets_dsl_json
):
    test_product = DataProduct.create(
        name=DATA_PRODUCT_NAME,
        asset_selection=data_product_asset_selection,
        domain_qualified_name=DATA_SUB_DOMAIN_QUALIFIED_NAME,
    )
    assert test_product.data_domain.unique_attributes == {
        "qualifiedName": DATA_SUB_DOMAIN_QUALIFIED_NAME
    }
    assert test_product.parent_domain_qualified_name == DATA_SUB_DOMAIN_QUALIFIED_NAME
    assert test_product.super_domain_qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    test_asset_dsl = dumps(
        loads(test_product.data_product_assets_d_s_l), sort_keys=True
    )
    expected_asset_dsl = dumps(data_product_assets_dsl_json, sort_keys=True)
    assert test_asset_dsl == expected_asset_dsl
    assert test_product.data_product_assets_playbook_filter == ASSETS_PLAYBOOK_FILTER
    _assert_product(
        test_product, qualified_name=DATA_PRODUCT_UNDER_SUB_DOMAIN_QUALIFIED_NAME
    )
    assert test_product.daap_status == DataProductStatus.ACTIVE


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
