# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the DbtSource creator in pyatlan_v9."""

import pytest

from pyatlan_v9.model import DbtSource
from tests_v9.unit.model import dbt_helpers as h

# The literal qualifiedName atlan-dbt-app emits.
APP_QUALIFIED_NAME = (
    "default/dbt/1712345678/account/70403103932498/project/70403104069713"
    "/source.jaffle_shop.raw.orders"
)
KWARGS = dict(**h.PROJECT_KWARGS, unique_id="source.jaffle_shop.raw.orders")
IDS = [p for p in KWARGS if p != "connection_qualified_name"]


def test_creator_emits_app_qualified_name():
    sut = DbtSource.creator(name=h.NAME, **KWARGS)

    h.assert_created(sut, APP_QUALIFIED_NAME)
    assert sut.asset_dbt_unique_id == KWARGS["unique_id"]


def test_create_alias():
    assert DbtSource.create(name=h.NAME, **KWARGS).qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *KWARGS])
def test_creator_rejects_missing_or_blank_inputs(param):
    h.assert_rejects_missing_or_blank(DbtSource, KWARGS, param)


@pytest.mark.parametrize("param", IDS)
def test_creator_rejects_ids_containing_a_slash(param):
    h.assert_rejects_slash(DbtSource, KWARGS, param)


def test_creator_rejects_malformed_connection_qualified_name():
    h.assert_rejects_malformed_connection(DbtSource, KWARGS)


def test_updater_and_trim_to_required():
    h.assert_updater(DbtSource, APP_QUALIFIED_NAME)
