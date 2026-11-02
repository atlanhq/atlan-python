# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapAnalyticsCloudColumn model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-sapanalyticscloud-app emits
(``app/processing/qualified_names.column_path``, golden ``tests/golden/sac-ref``):
a measure or dimension is ``{model}/{name}``, and a dimension's attribute or
hierarchy level is ``{model}/{parentColumnName}/{name}``.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapAnalyticsCloudColumn

CONNECTION_QUALIFIED_NAME = "default/sapanalyticscloud/1700000000"
CONNECTOR_NAME = "sapanalyticscloud"
COLUMN_NAME = "ID"
MODEL_NAME = "SAP__MANU_COM_Inventory"
MODEL_QUALIFIED_NAME = (
    "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
    "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
    "/C3UWZED3DGCQJRAVLV9PE832M8"
)
PARENT_COLUMN_NAME = "Account"
PARENT_COLUMN_QUALIFIED_NAME = f"{MODEL_QUALIFIED_NAME}/{PARENT_COLUMN_NAME}"
COLUMN_QUALIFIED_NAME = f"{PARENT_COLUMN_QUALIFIED_NAME}/{COLUMN_NAME}"


def test_creator_matches_app_qualified_name_at_depth_1():
    """Mirror the app's measure: directly under its model."""
    sut = SapAnalyticsCloudColumn.creator(
        name="SignedData",
        sap_analytics_cloud_model_qualified_name=(
            "default/sapanalyticscloud/1700000000/PUBLIC"
            "/B9F8280354E43C4BBDF03A9A31710EFC/A5BA1AEB2E2B576DAF1DB51B809BEA6A"
            "/4FC97AEB76E79EBF42933EFF9496DFB9/C3UWZED3DGCQJRAVLV9PE832M8"
        ),
        sap_analytics_cloud_model_name="SAP__MANU_COM_Inventory",
        order=1,
    )

    assert sut.qualified_name == (
        "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
        "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
        "/C3UWZED3DGCQJRAVLV9PE832M8/SignedData"
    )
    assert sut.column_depth_level == 1
    assert sut.parent_column is UNSET
    assert sut.parent_column_name is UNSET
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_at_depth_2():
    """Mirror the app's dimension attribute: under the model and its dimension."""
    sut = SapAnalyticsCloudColumn.creator(
        name="ID",
        sap_analytics_cloud_model_qualified_name=(
            "default/sapanalyticscloud/1700000000/PUBLIC"
            "/B9F8280354E43C4BBDF03A9A31710EFC/A5BA1AEB2E2B576DAF1DB51B809BEA6A"
            "/4FC97AEB76E79EBF42933EFF9496DFB9/C3UWZED3DGCQJRAVLV9PE832M8"
        ),
        sap_analytics_cloud_model_name="SAP__MANU_COM_Inventory",
        order=3,
        parent_column_name="Account",
    )

    assert sut.qualified_name == (
        "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
        "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
        "/C3UWZED3DGCQJRAVLV9PE832M8/Account/ID"
    )
    assert sut.parent_column_qualified_name == (
        "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
        "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
        "/C3UWZED3DGCQJRAVLV9PE832M8/Account"
    )
    assert sut.column_depth_level == 2
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, model_qualified_name, model_name, order, message",
    [
        (None, MODEL_QUALIFIED_NAME, MODEL_NAME, 1, "name is required"),
        (" ", MODEL_QUALIFIED_NAME, MODEL_NAME, 1, "name cannot be blank"),
        (
            COLUMN_NAME,
            None,
            MODEL_NAME,
            1,
            "sap_analytics_cloud_model_qualified_name is required",
        ),
        (
            COLUMN_NAME,
            MODEL_QUALIFIED_NAME,
            None,
            1,
            "sap_analytics_cloud_model_name is required",
        ),
        (
            COLUMN_NAME,
            MODEL_QUALIFIED_NAME,
            " ",
            1,
            "sap_analytics_cloud_model_name cannot be blank",
        ),
        (COLUMN_NAME, MODEL_QUALIFIED_NAME, MODEL_NAME, None, "order is required"),
        (
            COLUMN_NAME,
            CONNECTION_QUALIFIED_NAME,
            MODEL_NAME,
            1,
            "sap_analytics_cloud_model_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, model_qualified_name: str, model_name: str, order: int, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudColumn.creator(
            name=name,
            sap_analytics_cloud_model_qualified_name=model_qualified_name,
            sap_analytics_cloud_model_name=model_name,
            order=order,
        )


def test_creator():
    """Test creator derives the connection and relates the model and parent column."""
    sut = SapAnalyticsCloudColumn.creator(
        name=COLUMN_NAME,
        sap_analytics_cloud_model_qualified_name=MODEL_QUALIFIED_NAME,
        sap_analytics_cloud_model_name=MODEL_NAME,
        order=3,
        parent_column_name=PARENT_COLUMN_NAME,
    )

    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.order == 3
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.sap_analytics_cloud_model_qualified_name == MODEL_QUALIFIED_NAME
    assert sut.sap_analytics_cloud_model_name == MODEL_NAME
    assert sut.sap_analytics_cloud_model.unique_attributes == {
        "qualifiedName": MODEL_QUALIFIED_NAME
    }
    assert sut.parent_column_name == PARENT_COLUMN_NAME
    assert sut.parent_column_qualified_name == PARENT_COLUMN_QUALIFIED_NAME
    assert sut.parent_column.type_name == "SapAnalyticsCloudColumn"
    assert sut.parent_column.unique_attributes == {
        "qualifiedName": PARENT_COLUMN_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection():
    """Test an explicit connection qualified name is kept as given."""
    sut = SapAnalyticsCloudColumn.creator(
        name=COLUMN_NAME,
        sap_analytics_cloud_model_qualified_name=MODEL_QUALIFIED_NAME,
        sap_analytics_cloud_model_name=MODEL_NAME,
        order=1,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == f"{MODEL_QUALIFIED_NAME}/{COLUMN_NAME}"
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, COLUMN_NAME, "qualified_name is required"),
        (COLUMN_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudColumn.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a minimal instance for modification."""
    sut = SapAnalyticsCloudColumn.updater(
        qualified_name=COLUMN_QUALIFIED_NAME, name=COLUMN_NAME
    )

    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the fields needed for update."""
    sut = SapAnalyticsCloudColumn.creator(
        name=COLUMN_NAME,
        sap_analytics_cloud_model_qualified_name=MODEL_QUALIFIED_NAME,
        sap_analytics_cloud_model_name=MODEL_NAME,
        order=3,
        parent_column_name=PARENT_COLUMN_NAME,
    ).trim_to_required()

    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME
