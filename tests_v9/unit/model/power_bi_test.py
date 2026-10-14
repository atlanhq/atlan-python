# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Power BI creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-powerbi-app emits today
(FND-3838 census), so a creator change that would re-key existing Power BI assets fails here.
"""

import pytest

from pyatlan_v9.model import (
    PowerBIApp,
    PowerBIColumn,
    PowerBIDashboard,
    PowerBIDataflow,
    PowerBIDataflowEntityColumn,
    PowerBIDataset,
    PowerBIDatasource,
    PowerBIMeasure,
    PowerBIPage,
    PowerBIReport,
    PowerBITable,
    PowerBIWorkspace,
)

CONN_QN = "default/powerbi/1712345678"
WS_ID = "0f1e2d3c-ws"
WS_QN = f"{CONN_QN}/{WS_ID}"
DS_QN = f"{WS_QN}/ds-123"
TABLE_QN = f"{DS_QN}/Sales"
REPORT_QN = f"{WS_QN}/rp-456"
DATAFLOW_QN = f"{WS_QN}/df-789"
NAME = "Quarterly Sales"


def _assert_common(sut, expected_qn, name=NAME):
    assert sut.qualified_name == expected_qn
    assert sut.name == name
    assert sut.connection_qualified_name == CONN_QN
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate()


# Types keyed directly off the connection: (type, id kwarg, expected qualifiedName)
CONNECTION_CHILDREN = [
    (PowerBIWorkspace, "workspace_id", f"{CONN_QN}/{WS_ID}"),
    (PowerBIDatasource, "datasource_id", f"{CONN_QN}/{WS_ID}"),
    (PowerBIApp, "app_id", f"{CONN_QN}/app/{WS_ID}"),
]

# Types nested under a workspace: (type, id kwarg)
WORKSPACE_CHILDREN = [
    (PowerBIDataset, "dataset_id"),
    (PowerBIReport, "report_id"),
    (PowerBIDashboard, "dashboard_id"),
    (PowerBIDataflow, "dataflow_id"),
]


@pytest.mark.parametrize("asset_type, id_kwarg, expected_qn", CONNECTION_CHILDREN)
def test_connection_child_creator(asset_type, id_kwarg, expected_qn):
    sut = asset_type.creator(
        name=NAME, connection_qualified_name=CONN_QN, **{id_kwarg: WS_ID}
    )

    _assert_common(sut, expected_qn)
    sut.validate(for_creation=asset_type is not PowerBIDatasource)


def test_app_creator_sets_app_id():
    sut = PowerBIApp.creator(
        name=NAME, connection_qualified_name=CONN_QN, app_id="app-1"
    )

    assert sut.qualified_name == f"{CONN_QN}/app/app-1"
    assert sut.power_bi_app_id == "app-1"


@pytest.mark.parametrize("asset_type, id_kwarg", WORKSPACE_CHILDREN)
def test_workspace_child_creator(asset_type, id_kwarg):
    sut = asset_type.creator(
        name=NAME, workspace_qualified_name=WS_QN, **{id_kwarg: "x-1"}
    )

    _assert_common(sut, f"{CONN_QN}/{WS_ID}/x-1")
    assert sut.workspace_qualified_name == WS_QN
    assert sut.workspace.unique_attributes == {"qualifiedName": WS_QN}
    sut.validate(for_creation=True)


def test_table_creator():
    sut = PowerBITable.creator(name="Sales", dataset_qualified_name=DS_QN)

    _assert_common(sut, f"{CONN_QN}/{WS_ID}/ds-123/Sales", name="Sales")
    assert sut.workspace_qualified_name == WS_QN
    assert sut.dataset_qualified_name == DS_QN
    assert sut.dataset.unique_attributes == {"qualifiedName": DS_QN}
    sut.validate(for_creation=True)


@pytest.mark.parametrize("asset_type", [PowerBIColumn, PowerBIMeasure])
def test_column_and_measure_creator(asset_type):
    sut = asset_type.creator(name="Revenue", power_bi_table_qualified_name=TABLE_QN)

    _assert_common(sut, f"{CONN_QN}/{WS_ID}/ds-123/Sales/Revenue", name="Revenue")
    assert sut.workspace_qualified_name == WS_QN
    assert sut.dataset_qualified_name == DS_QN
    assert sut.power_bi_table_qualified_name == TABLE_QN
    assert sut.table.unique_attributes == {"qualifiedName": TABLE_QN}
    sut.validate(for_creation=True)


@pytest.mark.parametrize("asset_type", [PowerBIColumn, PowerBIMeasure])
def test_column_and_measure_under_table_name_with_slash(asset_type):
    table_qn = f"{DS_QN}/Sales/2024"

    sut = asset_type.creator(name="Revenue", power_bi_table_qualified_name=table_qn)

    assert sut.qualified_name == f"{table_qn}/Revenue"
    assert sut.dataset_qualified_name == DS_QN
    assert sut.workspace_qualified_name == WS_QN


def test_column_and_measure_share_qualified_name():
    # The app emits one shape for both, so the creators must too (no re-keying).
    column = PowerBIColumn.creator(
        name="Revenue", power_bi_table_qualified_name=TABLE_QN
    )
    measure = PowerBIMeasure.creator(
        name="Revenue", power_bi_table_qualified_name=TABLE_QN
    )

    assert column.qualified_name == measure.qualified_name


def test_page_creator():
    sut = PowerBIPage.creator(
        name="Overview", report_qualified_name=REPORT_QN, page_id="ReportSection1"
    )

    _assert_common(sut, f"{CONN_QN}/{WS_ID}/rp-456/ReportSection1", name="Overview")
    assert sut.workspace_qualified_name == WS_QN
    assert sut.report_qualified_name == REPORT_QN
    assert sut.report.unique_attributes == {"qualifiedName": REPORT_QN}
    sut.validate(for_creation=True)


def test_dataflow_entity_column_creator():
    sut = PowerBIDataflowEntityColumn.creator(
        power_bi_dataflow_qualified_name=DATAFLOW_QN,
        entity_name="Customers",
        column_name="Region",
    )

    _assert_common(
        sut,
        f"{CONN_QN}/{WS_ID}/df-789/Customers/Region",
        name="Customers -> Region",
    )
    assert sut.power_bi_workspace_qualified_name == WS_QN
    assert sut.power_bi_dataflow_qualified_name == DATAFLOW_QN
    assert sut.power_bi_dataflow_entity_name == "Customers"
    assert sut.power_bi_dataflow.unique_attributes == {"qualifiedName": DATAFLOW_QN}
    sut.validate(for_creation=True)


def test_dataflow_entity_column_creator_with_explicit_name():
    sut = PowerBIDataflowEntityColumn.creator(
        name="Region",
        power_bi_dataflow_qualified_name=DATAFLOW_QN,
        entity_name="Customers",
        column_name="Region",
    )

    assert sut.name == "Region"


@pytest.mark.parametrize(
    "asset_type, kwargs, message",
    [
        (
            PowerBIWorkspace,
            {"name": NAME, "connection_qualified_name": CONN_QN, "workspace_id": None},
            "workspace_id is required",
        ),
        (
            PowerBIWorkspace,
            {"name": NAME, "connection_qualified_name": CONN_QN, "workspace_id": "  "},
            "workspace_id cannot be blank",
        ),
        (
            PowerBIDatasource,
            {"name": NAME, "connection_qualified_name": "", "datasource_id": "d"},
            "connection_qualified_name cannot be blank",
        ),
        (
            PowerBIApp,
            {"name": None, "connection_qualified_name": CONN_QN, "app_id": "a"},
            "name is required",
        ),
        (
            PowerBIDataset,
            {"name": NAME, "workspace_qualified_name": WS_QN, "dataset_id": ""},
            "dataset_id cannot be blank",
        ),
        (
            PowerBIDataset,
            {
                "name": NAME,
                "workspace_qualified_name": f"{CONN_QN}/",
                "dataset_id": "d",
            },
            "workspace_qualified_name is invalid",
        ),
        (
            PowerBIReport,
            {"name": NAME, "workspace_qualified_name": CONN_QN, "report_id": "r"},
            "workspace_qualified_name is invalid",
        ),
        (
            PowerBIDashboard,
            {"name": NAME, "workspace_qualified_name": None, "dashboard_id": "d"},
            "workspace_qualified_name is required",
        ),
        (
            PowerBIDataflow,
            {"name": NAME, "workspace_qualified_name": WS_QN, "dataflow_id": " "},
            "dataflow_id cannot be blank",
        ),
        (
            PowerBITable,
            {"name": " ", "dataset_qualified_name": DS_QN},
            "name cannot be blank",
        ),
        (
            PowerBITable,
            {"name": "Sales", "dataset_qualified_name": f"{CONN_QN}//ds-123"},
            "dataset_qualified_name is invalid",
        ),
        (
            PowerBIColumn,
            {"name": "", "power_bi_table_qualified_name": TABLE_QN},
            "name cannot be blank",
        ),
        (
            PowerBIColumn,
            {"name": "c", "power_bi_table_qualified_name": DS_QN},
            "power_bi_table_qualified_name is invalid",
        ),
        (
            PowerBIMeasure,
            {"name": "m", "power_bi_table_qualified_name": f"{WS_QN}//Sales"},
            "power_bi_table_qualified_name is invalid",
        ),
        (
            PowerBIPage,
            {"name": NAME, "report_qualified_name": REPORT_QN, "page_id": ""},
            "page_id cannot be blank",
        ),
        (
            PowerBIPage,
            {"name": NAME, "report_qualified_name": WS_QN, "page_id": "p"},
            "report_qualified_name is invalid",
        ),
        (
            PowerBIDataflowEntityColumn,
            {
                "power_bi_dataflow_qualified_name": DATAFLOW_QN,
                "entity_name": " ",
                "column_name": "c",
            },
            "entity_name cannot be blank",
        ),
        (
            PowerBIDataflowEntityColumn,
            {
                "power_bi_dataflow_qualified_name": DATAFLOW_QN,
                "entity_name": "e",
                "column_name": None,
            },
            "column_name is required",
        ),
        (
            PowerBIDataflowEntityColumn,
            {
                "power_bi_dataflow_qualified_name": WS_QN,
                "entity_name": "e",
                "column_name": "c",
            },
            "power_bi_dataflow_qualified_name is invalid",
        ),
    ],
)
def test_creator_rejects_missing_blank_or_malformed_inputs(asset_type, kwargs, message):
    with pytest.raises(ValueError, match=message):
        asset_type.creator(**kwargs)


@pytest.mark.parametrize("asset_type, id_kwarg", WORKSPACE_CHILDREN)
def test_create_alias(asset_type, id_kwarg):
    sut = asset_type.create(
        name=NAME, workspace_qualified_name=WS_QN, **{id_kwarg: "x-1"}
    )

    assert sut.qualified_name == f"{WS_QN}/x-1"
