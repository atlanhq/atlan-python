# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataProduct model in pyatlan_v9."""

from json import dumps, load, loads
from pathlib import Path

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import CertificateStatus, DataProductStatus
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import IndexSearchRequest
from pyatlan_v9.model import DataProduct
from pyatlan_v9.model.assets import AtlasGlossary
from tests_v9.unit.model.constants import (
    DATA_DOMAIN_QUALIFIED_NAME,
    DATA_PRODUCT_NAME,
    DATA_PRODUCT_QUALIFIED_NAME,
    DATA_PRODUCT_UNDER_SUB_DOMAIN_QUALIFIED_NAME,
    DATA_SUB_DOMAIN_QUALIFIED_NAME,
)

TEST_DATA_DIR = Path(__file__).resolve().parents[3] / "tests" / "unit" / "data"
DATA_PRODUCT_ASSETS_DSL_JSON = "data_product_assets_dsl.json"
DATA_MESH_DIR = TEST_DATA_DIR / "data_mesh_requests"
ASSETS_PLAYBOOK_FILTER = '{"condition":"AND","isGroupLocked":false,"rules":[]}'


def load_json(response_dir: Path, filename: str):
    """Load a JSON file from test data."""
    with (response_dir / filename).open() as input_file:
        return load(input_file)


@pytest.fixture()
def data_product_assets_dsl_json():
    """Return expected data-product assets DSL fixture JSON."""
    return load_json(DATA_MESH_DIR, DATA_PRODUCT_ASSETS_DSL_JSON)


@pytest.fixture()
def data_product_asset_selection():
    """Build a fluent-search request used to define DataProduct assets."""
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
        (None, "dummy", DATA_DOMAIN_QUALIFIED_NAME, "name is required"),
        (
            DATA_PRODUCT_NAME,
            None,
            DATA_DOMAIN_QUALIFIED_NAME,
            "asset_selection is required",
        ),
        (DATA_PRODUCT_NAME, "dummy", None, "domain_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    asset_selection: IndexSearchRequest,
    domain_qualified_name: str,
    message: str,
):
    """Test creator raises ValueError when required fields are missing."""
    with pytest.raises(ValueError, match=message):
        DataProduct.creator(
            name=name,
            asset_selection=asset_selection,
            domain_qualified_name=domain_qualified_name,
        )


def test_creator(
    data_product_asset_selection: IndexSearchRequest, data_product_assets_dsl_json
):
    """Test creator populates relationships and DSL payload for root domain."""
    test_product = DataProduct.creator(
        name=DATA_PRODUCT_NAME,
        asset_selection=data_product_asset_selection,
        domain_qualified_name=DATA_DOMAIN_QUALIFIED_NAME,
    )
    assert test_product.data_domain.unique_attributes == {
        "qualifiedName": DATA_DOMAIN_QUALIFIED_NAME
    }
    assert test_product.parent_domain_qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    assert test_product.super_domain_qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    test_asset_dsl = dumps(loads(test_product.data_product_assets_dsl), sort_keys=True)
    expected_asset_dsl = dumps(data_product_assets_dsl_json, sort_keys=True)
    assert test_asset_dsl == expected_asset_dsl
    assert test_product.data_product_assets_playbook_filter == ASSETS_PLAYBOOK_FILTER
    _assert_product(test_product)


def test_creator_under_sub_domain(
    data_product_asset_selection: IndexSearchRequest, data_product_assets_dsl_json
):
    """Test creator populates parent and super domain for sub-domain products."""
    test_product = DataProduct.creator(
        name=DATA_PRODUCT_NAME,
        asset_selection=data_product_asset_selection,
        domain_qualified_name=DATA_SUB_DOMAIN_QUALIFIED_NAME,
    )
    assert test_product.data_domain.unique_attributes == {
        "qualifiedName": DATA_SUB_DOMAIN_QUALIFIED_NAME
    }
    assert test_product.parent_domain_qualified_name == DATA_SUB_DOMAIN_QUALIFIED_NAME
    assert test_product.super_domain_qualified_name == DATA_DOMAIN_QUALIFIED_NAME
    test_asset_dsl = dumps(loads(test_product.data_product_assets_dsl), sort_keys=True)
    expected_asset_dsl = dumps(data_product_assets_dsl_json, sort_keys=True)
    assert test_asset_dsl == expected_asset_dsl
    assert test_product.data_product_assets_playbook_filter == ASSETS_PLAYBOOK_FILTER
    _assert_product(
        test_product, qualified_name=DATA_PRODUCT_UNDER_SUB_DOMAIN_QUALIFIED_NAME
    )
    assert test_product.daap_status == DataProductStatus.ACTIVE


def test_updater():
    """Test updater returns a minimal DataProduct for updates."""
    test_product = DataProduct.updater(
        name=DATA_PRODUCT_NAME,
        qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
    )
    _assert_product(test_product)


def test_get_assets_with_missing_dp_asset_dsl():
    """Test get_assets raises InvalidRequestError when DSL is missing."""
    data_product = DataProduct(
        name=DATA_PRODUCT_NAME,
        parent_domain_qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
        data_product_assets_dsl=None,
    )
    with pytest.raises(
        InvalidRequestError,
        match=(
            "Missing value for `data_product_assets_d_s_l`, "
            "which is required to retrieve DataProduct assets."
        ),
    ):
        data_product.get_assets(client=object())


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    test_product = DataProduct.updater(
        qualified_name=DATA_PRODUCT_QUALIFIED_NAME,
        name=DATA_PRODUCT_NAME,
    ).trim_to_required()
    _assert_product(test_product)
