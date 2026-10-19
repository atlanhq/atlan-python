# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the DbtMeasure creator in pyatlan_v9."""

import pytest

from pyatlan_v9.model import DbtMeasure
from tests_v9.unit.model import dbt_helpers as h

# The literal qualifiedName atlan-dbt-app emits.
APP_QUALIFIED_NAME = (
    "default/dbt/1712345678/account/70403103932498/project/70403104069713"
    "/env/70403103991524/semantic_model.jaffle_shop.orders/measure/orders"
)
KWARGS = dict(semantic_model_qualified_name=h.SEMANTIC_MODEL_QN)


def test_creator_emits_app_qualified_name():
    sut = DbtMeasure.creator(name=h.NAME, **KWARGS)

    h.assert_created(sut, APP_QUALIFIED_NAME)
    # the app's field uniqueId is {semantic_model_unique_id}/measure/{name}
    assert sut.asset_dbt_unique_id == f"{h.SEMANTIC_MODEL_UID}/measure/{h.NAME}"
    assert sut.dbt_semantic_model_qualified_name == h.SEMANTIC_MODEL_QN
    assert sut.semantic_model.qualified_name == h.SEMANTIC_MODEL_QN
    assert sut.semantic_model.type_name == "DbtSemanticModel"


def test_create_alias():
    assert DbtMeasure.create(name=h.NAME, **KWARGS).qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *KWARGS])
def test_creator_rejects_missing_or_blank_inputs(param):
    h.assert_rejects_missing_or_blank(DbtMeasure, KWARGS, param)


@h.MALFORMED_PARENT_QNS
def test_creator_rejects_malformed_semantic_model_qualified_name(bad_parent_qn):
    with pytest.raises(ValueError, match="Invalid semantic_model_qualified_name"):
        DbtMeasure.creator(name=h.NAME, semantic_model_qualified_name=bad_parent_qn)


def test_updater_and_trim_to_required():
    h.assert_updater(DbtMeasure, APP_QUALIFIED_NAME)
