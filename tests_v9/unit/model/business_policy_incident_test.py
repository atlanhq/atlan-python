# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for BusinessPolicyIncident model in pyatlan_v9."""

from pyatlan_v9.model.assets.business_policy_incident import (
    BusinessPolicyIncident,
    BusinessPolicyIncidentAttributes,
)


def test_import():
    """BusinessPolicyIncident can be imported from pyatlan_v9."""
    assert BusinessPolicyIncident is not None
    assert BusinessPolicyIncidentAttributes is not None


def test_type_name():
    """BusinessPolicyIncident has correct type_name."""
    instance = BusinessPolicyIncident()
    assert instance.type_name == "BusinessPolicyIncident"


def test_attributes_struct():
    """BusinessPolicyIncidentAttributes has expected fields."""
    attrs = BusinessPolicyIncidentAttributes()
    assert hasattr(attrs, "business_policy_incident_noncompliant_count")
    assert hasattr(attrs, "business_policy_incident_related_policy_guids")
    assert hasattr(attrs, "business_policy_incident_filter_dsl")


def test_init_exports():
    """BusinessPolicyIncident is exported from the init module."""
    from pyatlan_v9.model.assets._init_business_policy import (
        BusinessPolicyIncident as Exported,
    )

    assert Exported is BusinessPolicyIncident
