# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the CalculationView creator in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-saphana-app emits today
(FND-3838 census), so a creator change that would re-key existing SAP HANA
calculation views fails here. The app builds the same qualifiedName at three
sites; they agree whenever the package is set, which is why the creator
requires one.
"""

import json

import pytest

from pyatlan_v9.model import CalculationView

CONN = "default/sap-hana/1712345678"
CATALOG = "DEFAULT"
SCHEMA = "_SYS_BIC"
SCHEMA_QN = f"{CONN}/{CATALOG}/{SCHEMA}"
PACKAGE = "sales.reporting"
VIEW = "CV_REVENUE"


# --- the app's qualifiedName grammar, copied from atlan-saphana-app ----------
def _app_entity_qn(table_cat, table_schem, package_id, table_name):
    # app/transformers/query/sql_query_templates/extras-calc-view.yaml
    return f"{CONN}/{table_cat}/{table_schem}/{package_id or ''}/{table_name}"


def _app_lineage_target_qn(table_cat, table_schem, package_id, view_name):
    # app/activities/metadata_extraction/process/calc_view_lineage_processor.py
    package_prefix = f"{package_id}/" if package_id is not None else ""
    return f"{CONN}/{table_cat}/{table_schem}/{package_prefix}{view_name}"


def _app_column_parent_qn(schema, package_id, view_name):
    # app/activities/metadata_extraction/process/process_calculation_view.py
    # (the column-lineage output qualifiedName, minus its column segment)
    if package_id:
        return f"{CONN}/DEFAULT/{schema}/{package_id}/{view_name}"
    return f"{CONN}/DEFAULT/{schema}/{view_name}"


def test_creator_matches_app_qualified_names():
    sut = CalculationView.creator(
        name=VIEW, package_id=PACKAGE, schema_qualified_name=SCHEMA_QN
    )

    expected = "default/sap-hana/1712345678/DEFAULT/_SYS_BIC/sales.reporting/CV_REVENUE"
    assert sut.qualified_name == expected
    assert sut.qualified_name == _app_entity_qn(CATALOG, SCHEMA, PACKAGE, VIEW)
    assert sut.qualified_name == _app_lineage_target_qn(CATALOG, SCHEMA, PACKAGE, VIEW)
    assert sut.qualified_name == _app_column_parent_qn(SCHEMA, PACKAGE, VIEW)
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)


def test_creator_matches_app_system_schema_default():
    # extract_calc_view.sql falls back to SYSTEM when the view has no schema.
    schema_qn = f"{CONN}/{CATALOG}/SYSTEM"
    sut = CalculationView.creator(
        name=VIEW, package_id=PACKAGE, schema_qualified_name=schema_qn
    )

    assert sut.qualified_name == _app_entity_qn(CATALOG, "SYSTEM", PACKAGE, VIEW)
    assert sut.schema_name == "SYSTEM"


def test_app_sites_disagree_without_a_package():
    # Why the creator requires package_id: with no package the three app sites
    # build three different qualifiedNames for the same view.
    qns = {
        _app_entity_qn(CATALOG, SCHEMA, None, VIEW),
        _app_lineage_target_qn(CATALOG, SCHEMA, None, VIEW),
        _app_lineage_target_qn(CATALOG, SCHEMA, "", VIEW),
        _app_column_parent_qn(SCHEMA, None, VIEW),
    }
    assert len(qns) > 1


def test_creator_attributes():
    sut = CalculationView.creator(
        name=VIEW, package_id=PACKAGE, schema_qualified_name=SCHEMA_QN
    )

    # Every attribute extras-calc-view.yaml sets from its inputs.
    assert sut.type_name == "CalculationView"
    assert sut.name == VIEW
    assert sut.connector_name == "sap-hana"
    assert sut.connection_qualified_name == CONN
    assert sut.database_name == CATALOG
    assert sut.database_qualified_name == f"{CONN}/{CATALOG}"
    assert sut.schema_name == SCHEMA
    assert sut.schema_qualified_name == SCHEMA_QN
    assert sut.calculation_view_package_id == PACKAGE
    assert sut.atlan_schema.qualified_name == SCHEMA_QN
    assert sut.atlan_schema.type_name == "Schema"
    assert sut.guid
    sut.validate(for_creation=True)


def test_create_alias():
    sut = CalculationView.create(
        name=VIEW, package_id=PACKAGE, schema_qualified_name=SCHEMA_QN
    )

    assert sut.qualified_name == _app_entity_qn(CATALOG, SCHEMA, PACKAGE, VIEW)


def test_creator_serialises_parent_relationship():
    sut = CalculationView.creator(
        name=VIEW, package_id=PACKAGE, schema_qualified_name=SCHEMA_QN
    )

    payload = json.loads(sut.to_json())
    attributes = payload["attributes"]
    assert payload["typeName"] == "CalculationView"
    assert attributes["qualifiedName"] == sut.qualified_name
    assert attributes["calculationViewPackageId"] == PACKAGE
    schema = payload["relationshipAttributes"]["atlanSchema"]
    assert schema["typeName"] == "Schema"
    assert schema["uniqueAttributes"]["qualifiedName"] == SCHEMA_QN


@pytest.mark.parametrize(
    "name, package_id, schema_qualified_name, message",
    [
        (None, PACKAGE, SCHEMA_QN, "name is required"),
        ("  ", PACKAGE, SCHEMA_QN, "name cannot be blank"),
        (VIEW, None, SCHEMA_QN, "package_id is required"),
        (VIEW, "", SCHEMA_QN, "package_id cannot be blank"),
        (VIEW, "sales/reporting", SCHEMA_QN, "Invalid package_id"),
        (VIEW, PACKAGE, None, "schema_qualified_name is required"),
        (VIEW, PACKAGE, "", "schema_qualified_name cannot be blank"),
        (VIEW, PACKAGE, f"{CONN}/{CATALOG}", "Invalid schema_qualified_name"),
        (VIEW, PACKAGE, f"{SCHEMA_QN}/extra", "Invalid schema_qualified_name"),
    ],
)
def test_creator_rejects_bad_inputs(name, package_id, schema_qualified_name, message):
    with pytest.raises(ValueError, match=message):
        CalculationView.creator(
            name=name,
            package_id=package_id,
            schema_qualified_name=schema_qualified_name,
        )
