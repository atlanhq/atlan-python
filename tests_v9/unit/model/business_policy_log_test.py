# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for BusinessPolicyLog model in pyatlan_v9."""

from pyatlan_v9.model.assets.business_policy_log import (
    BusinessPolicyLog,
    BusinessPolicyLogAttributes,
)


def test_import():
    """BusinessPolicyLog can be imported from pyatlan_v9."""
    assert BusinessPolicyLog is not None
    assert BusinessPolicyLogAttributes is not None


def test_type_name():
    """BusinessPolicyLog has correct type_name."""
    instance = BusinessPolicyLog()
    assert instance.type_name == "BusinessPolicyLog"


def test_attributes_struct():
    """BusinessPolicyLogAttributes has expected fields."""
    attrs = BusinessPolicyLogAttributes()
    assert hasattr(attrs, "business_policy_id")
    assert hasattr(attrs, "business_policy_log_policy_type")
    assert hasattr(attrs, "governed_assets_count")
    assert hasattr(attrs, "non_governed_assets_count")
    assert hasattr(attrs, "compliant_assets_count")
    assert hasattr(attrs, "non_compliant_assets_count")


def test_init_exports():
    """BusinessPolicyLog is exported from the init module."""
    from pyatlan_v9.model.assets._init_business_policy import (
        BusinessPolicyLog as Exported,
    )

    assert Exported is BusinessPolicyLog
