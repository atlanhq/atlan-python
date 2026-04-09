# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for BusinessPolicyException model in pyatlan_v9."""

from pyatlan_v9.model.assets.business_policy_exception import (
    BusinessPolicyException,
    BusinessPolicyExceptionAttributes,
)


def test_import():
    """BusinessPolicyException can be imported from pyatlan_v9."""
    assert BusinessPolicyException is not None
    assert BusinessPolicyExceptionAttributes is not None


def test_type_name():
    """BusinessPolicyException has correct type_name."""
    instance = BusinessPolicyException()
    assert instance.type_name == "BusinessPolicyException"


def test_attributes_struct():
    """BusinessPolicyExceptionAttributes has expected fields."""
    attrs = BusinessPolicyExceptionAttributes()
    assert hasattr(attrs, "business_policy_qualified_name")
    assert hasattr(attrs, "business_policy_exception_filter_dsl")
    assert hasattr(attrs, "business_policy_exception_users")
    assert hasattr(attrs, "business_policy_exception_groups")


def test_init_exports():
    """BusinessPolicyException is exported from the init module."""
    from pyatlan_v9.model.assets._init_business_policy import (
        BusinessPolicyException as Exported,
    )

    assert Exported is BusinessPolicyException
