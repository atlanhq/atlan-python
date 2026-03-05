# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""
Unit tests for ALLOYDB_POSTGRES connector type support (REQ-589).

Verifies that AtlanConnectorType.ALLOYDB_POSTGRES and WorkflowPackage.ALLOYDB_POSTGRES
are properly defined, enabling programmatic metadata policy creation for AlloyDB assets.
"""

import pytest

from pyatlan.model.assets import Persona
from pyatlan.model.enums import (
    AtlanConnectionCategory,
    AtlanConnectorType,
    AuthPolicyType,
    PersonaMetadataAction,
    WorkflowPackage,
)

ALLOYDB_POSTGRES_CONNECTION_QN = "default/alloydb-postgres/1686532494"
PERSONA_GUID = "test-persona-guid-1234"


class TestAtlanConnectorTypeAlloydbPostgres:
    def test_enum_member_exists(self):
        assert hasattr(AtlanConnectorType, "ALLOYDB_POSTGRES")

    def test_enum_value(self):
        assert AtlanConnectorType.ALLOYDB_POSTGRES.value == "alloydb-postgres"

    def test_enum_category(self):
        assert (
            AtlanConnectorType.ALLOYDB_POSTGRES.category
            == AtlanConnectionCategory.DATABASE
        )

    def test_lookup_by_value(self):
        connector = AtlanConnectorType("alloydb-postgres")
        assert connector == AtlanConnectorType.ALLOYDB_POSTGRES

    def test_resolve_from_qualified_name(self):
        connector = AtlanConnectorType._get_connector_type_from_qualified_name(
            ALLOYDB_POSTGRES_CONNECTION_QN
        )
        assert connector == AtlanConnectorType.ALLOYDB_POSTGRES
        assert connector.value == "alloydb-postgres"

    def test_to_qualified_name_format(self):
        qn = AtlanConnectorType.ALLOYDB_POSTGRES.to_qualified_name()
        parts = qn.split("/")
        assert parts[0] == "default"
        assert parts[1] == "alloydb-postgres"


class TestWorkflowPackageAlloydbPostgres:
    def test_enum_member_exists(self):
        assert hasattr(WorkflowPackage, "ALLOYDB_POSTGRES")

    def test_enum_value(self):
        assert WorkflowPackage.ALLOYDB_POSTGRES.value == "atlan-alloydb-postgres"

    def test_lookup_by_value(self):
        pkg = WorkflowPackage("atlan-alloydb-postgres")
        assert pkg == WorkflowPackage.ALLOYDB_POSTGRES


class TestPersonaMetadataPolicyAlloydbPostgres:
    """
    Reproduces the CME use case: programmatically creating metadata policies
    for AlloyDB Postgres connections (REQ-589).
    """

    def test_create_metadata_policy_for_alloydb_postgres(self):
        policy = Persona.create_metadata_policy(
            name="AlloyDB read access",
            persona_id=PERSONA_GUID,
            policy_type=AuthPolicyType.ALLOW,
            actions={PersonaMetadataAction.READ},
            connection_qualified_name=ALLOYDB_POSTGRES_CONNECTION_QN,
            resources={f"entity:{ALLOYDB_POSTGRES_CONNECTION_QN}"},
        )

        assert policy is not None
        assert policy.policy_sub_category == "metadata"
        assert policy.connection_qualified_name == ALLOYDB_POSTGRES_CONNECTION_QN
        assert f"entity:{ALLOYDB_POSTGRES_CONNECTION_QN}" in policy.policy_resources
        assert PersonaMetadataAction.READ.value in policy.policy_actions
        assert policy.policy_type == AuthPolicyType.ALLOW

    def test_create_metadata_policy_with_table_resource(self):
        table_resource = (
            f"entity:{ALLOYDB_POSTGRES_CONNECTION_QN}/mydb/myschema/mytable"
        )
        policy = Persona.create_metadata_policy(
            name="AlloyDB table access",
            persona_id=PERSONA_GUID,
            policy_type=AuthPolicyType.ALLOW,
            actions={PersonaMetadataAction.READ, PersonaMetadataAction.UPDATE},
            connection_qualified_name=ALLOYDB_POSTGRES_CONNECTION_QN,
            resources={table_resource},
        )

        assert policy is not None
        assert table_resource in policy.policy_resources
        assert len(policy.policy_actions) == 2
