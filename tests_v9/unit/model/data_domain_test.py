# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataDomain model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import DataDomain
from tests_v9.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(name: str, message: str):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        DataDomain.creator(name=name)


def test_creator_attributes_with_required_parameters():
    """Test that creator resolves parent-domain relationship from qualified name."""
    test_domain = DataDomain.creator(
        name=DATA_DOMAIN_NAME,
        parent_domain_qualified_name=DATA_DOMAIN_QUALIFIED_NAME,
    )
    assert test_domain.parent_domain.unique_attributes == {
        "qualifiedName": DATA_DOMAIN_QUALIFIED_NAME
    }


def test_creator():
    """Test that creator initializes root and sub-domain correctly."""
    test_domain = DataDomain.creator(name=DATA_DOMAIN_NAME)
    test_domain.qualified_name = DATA_DOMAIN_QUALIFIED_NAME
    _assert_domain(test_domain)

    test_sub_domain = DataDomain.creator(
        name=DATA_SUB_DOMAIN_NAME,
        parent_domain_qualified_name=test_domain.qualified_name,
    )
    assert test_sub_domain.name == DATA_SUB_DOMAIN_NAME
    assert test_sub_domain.qualified_name == DATA_SUB_DOMAIN_NAME
    assert test_sub_domain.parent_domain_qualified_name == test_domain.qualified_name


def test_updater():
    """Test updater creates a DataDomain with required fields."""
    test_domain = DataDomain.updater(
        name=DATA_DOMAIN_NAME, qualified_name=DATA_DOMAIN_QUALIFIED_NAME
    )
    _assert_domain(test_domain)


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    test_domain = DataDomain.updater(
        qualified_name=DATA_DOMAIN_QUALIFIED_NAME, name=DATA_DOMAIN_NAME
    ).trim_to_required()
    _assert_domain(test_domain)
