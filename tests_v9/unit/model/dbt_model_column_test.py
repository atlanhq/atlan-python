# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the DbtModelColumn creator in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import DbtModelColumn
from tests_v9.unit.model import dbt_helpers as h

# The literal qualifiedNames atlan-dbt-app emits.
APP_MODEL_COLUMN_QUALIFIED_NAME = (
    "default/dbt/1712345678/account/70403103932498/project/70403104069713"
    "/env/70403103991524/model.jaffle_shop.orders/orders"
)
APP_SEED_COLUMN_QUALIFIED_NAME = (
    "default/dbt/1712345678/account/70403103932498/project/70403104069713"
    "/env/70403103991524/seed.jaffle_shop.raw_customers/customer_id"
)


def test_creator_emits_app_qualified_name_for_model_column():
    sut = DbtModelColumn.creator(name=h.NAME, model_qualified_name=h.MODEL_QN)

    h.assert_created(sut, APP_MODEL_COLUMN_QUALIFIED_NAME)
    assert sut.asset_dbt_unique_id == f"{h.MODEL_UID}/{h.NAME}"
    assert sut.dbt_model_qualified_name == h.MODEL_QN
    assert sut.dbt_model.qualified_name == h.MODEL_QN
    assert sut.dbt_seed is UNSET


def test_creator_emits_app_qualified_name_for_seed_column():
    sut = DbtModelColumn.creator(name="customer_id", seed_qualified_name=h.SEED_QN)

    h.assert_created(sut, APP_SEED_COLUMN_QUALIFIED_NAME, name="customer_id")
    assert sut.asset_dbt_unique_id == f"{h.SEED_UID}/customer_id"
    # atlan-dbt-app sets dbtModelQualifiedName to the seed qn for seed columns
    assert sut.dbt_model_qualified_name == h.SEED_QN
    assert sut.dbt_seed.qualified_name == h.SEED_QN
    assert sut.dbt_model is UNSET


def test_create_alias():
    sut = DbtModelColumn.create(name=h.NAME, model_qualified_name=h.MODEL_QN)

    assert sut.qualified_name == APP_MODEL_COLUMN_QUALIFIED_NAME


@pytest.mark.parametrize(
    "parents",
    [{}, {"model_qualified_name": h.MODEL_QN, "seed_qualified_name": h.SEED_QN}],
    ids=["neither", "both"],
)
def test_creator_requires_exactly_one_parent(parents):
    with pytest.raises(ValueError, match="Exactly one of"):
        DbtModelColumn.creator(name=h.NAME, **parents)


@pytest.mark.parametrize("param", ["model_qualified_name", "seed_qualified_name"])
def test_creator_rejects_blank_inputs(param):
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        DbtModelColumn.creator(name=h.NAME, **{param: "  "})
    with pytest.raises(ValueError, match="name is required"):
        DbtModelColumn.creator(name=None, **{param: h.MODEL_QN})
    with pytest.raises(ValueError, match="name cannot be blank"):
        DbtModelColumn.creator(name="  ", **{param: h.MODEL_QN})


@pytest.mark.parametrize("param", ["model_qualified_name", "seed_qualified_name"])
@h.MALFORMED_PARENT_QNS
def test_creator_rejects_malformed_parent_qualified_name(param, bad_parent_qn):
    with pytest.raises(ValueError, match=f"Invalid {param}"):
        DbtModelColumn.creator(name=h.NAME, **{param: bad_parent_qn})


def test_updater_and_trim_to_required():
    h.assert_updater(DbtModelColumn, APP_MODEL_COLUMN_QUALIFIED_NAME)
