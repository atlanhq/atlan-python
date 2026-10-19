# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the DbtTag creator in pyatlan_v9."""

import pytest

from pyatlan_v9.model import DbtTag
from tests_v9.unit.model import dbt_helpers as h

# The literal qualifiedName atlan-dbt-app emits.
APP_QUALIFIED_NAME = (
    "default/dbt/1712345678/account/70403103932498/project/70403104069713/tag/orders"
)
KWARGS = dict(**h.PROJECT_KWARGS)
IDS = ["account_id", "project_id"]


def test_creator_emits_app_qualified_name():
    h.assert_created(DbtTag.creator(name=h.NAME, **KWARGS), APP_QUALIFIED_NAME)


def test_create_alias():
    assert DbtTag.create(name=h.NAME, **KWARGS).qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *KWARGS])
def test_creator_rejects_missing_or_blank_inputs(param):
    h.assert_rejects_missing_or_blank(DbtTag, KWARGS, param)


@pytest.mark.parametrize("param", IDS)
def test_creator_rejects_ids_containing_a_slash(param):
    h.assert_rejects_slash(DbtTag, KWARGS, param)


def test_creator_rejects_malformed_connection_qualified_name():
    h.assert_rejects_malformed_connection(DbtTag, KWARGS)


def test_updater_and_trim_to_required():
    h.assert_updater(DbtTag, APP_QUALIFIED_NAME)
