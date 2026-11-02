# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapAnalyticsCloudModel model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-sapanalyticscloud-app emits
(``app/processing/qualified_names.model_path``, golden ``tests/golden/sac-ref``):
an Import model is ``{parentFolder}/{resourceId}`` and a Live model, which is
never in a folder, is ``{connection}/{modelId}``.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapAnalyticsCloudModel

CONNECTION_QUALIFIED_NAME = "default/sapanalyticscloud/1700000000"
CONNECTOR_NAME = "sapanalyticscloud"
MODEL_NAME = "SAP__MANU_Employee_Info"
RESOURCE_ID = "C34jefz8ykzezs7nus8lkrtclc"
PARENT_FOLDER_QUALIFIED_NAME = (
    "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
    "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
)
MODEL_QUALIFIED_NAME = f"{PARENT_FOLDER_QUALIFIED_NAME}/{RESOURCE_ID}"


def test_creator_matches_app_qualified_name_for_import_model():
    """Mirror the app's Import model in a folder."""
    sut = SapAnalyticsCloudModel.creator(
        name="SAP__MANU_Employee_Info",
        resource_id="C34jefz8ykzezs7nus8lkrtclc",
        parent_folder_qualified_name=(
            "default/sapanalyticscloud/1700000000/PUBLIC"
            "/B9F8280354E43C4BBDF03A9A31710EFC/A5BA1AEB2E2B576DAF1DB51B809BEA6A"
            "/4FC97AEB76E79EBF42933EFF9496DFB9"
        ),
        parent_folder_name="SAP_BestRun_ Bikes_ Mobile",
    )

    assert sut.qualified_name == (
        "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
        "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
        "/C34jefz8ykzezs7nus8lkrtclc"
    )
    assert sut.sap_analytics_cloud_resource_id == "C34jefz8ykzezs7nus8lkrtclc"
    assert sut.sap_analytics_cloud_parent_folder_name == "SAP_BestRun_ Bikes_ Mobile"
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_for_live_model():
    """Mirror the app's Live model: no folder, keyed by modelId."""
    sut = SapAnalyticsCloudModel.creator(
        name="SAP_SMPL_FI_AM_FINTRANSACTIONS",
        model_id="t.4.Cl3o2n0lsc8gn9v8p8uh7qp7q22:Cl3o2n0lsc8gn9v8p8uh7qp7q22",
        connection_qualified_name="default/sapanalyticscloud/1700000000",
    )

    assert sut.qualified_name == (
        "default/sapanalyticscloud/1700000000"
        "/t.4.Cl3o2n0lsc8gn9v8p8uh7qp7q22:Cl3o2n0lsc8gn9v8p8uh7qp7q22"
    )
    assert (
        sut.sap_analytics_cloud_model_id
        == "t.4.Cl3o2n0lsc8gn9v8p8uh7qp7q22:Cl3o2n0lsc8gn9v8p8uh7qp7q22"
    )
    assert sut.sap_analytics_cloud_resource_id is UNSET
    assert sut.sap_analytics_cloud_folder is UNSET
    sut.validate(for_creation=True)


def test_creator_keys_import_model_on_resource_id_not_model_id():
    """When both ids are known, the qualifiedName uses resourceId, as the app does."""
    sut = SapAnalyticsCloudModel.creator(
        name=MODEL_NAME,
        resource_id=RESOURCE_ID,
        model_id="SomeOtherModelId",
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.qualified_name == MODEL_QUALIFIED_NAME
    assert sut.sap_analytics_cloud_resource_id == RESOURCE_ID
    assert sut.sap_analytics_cloud_model_id == "SomeOtherModelId"


@pytest.mark.parametrize(
    "name, resource_id, model_id, connection_qualified_name, parent_folder_qualified_name, message",
    [
        (None, RESOURCE_ID, None, CONNECTION_QUALIFIED_NAME, None, "name is required"),
        (
            " ",
            RESOURCE_ID,
            None,
            CONNECTION_QUALIFIED_NAME,
            None,
            "name cannot be blank",
        ),
        (
            MODEL_NAME,
            None,
            None,
            CONNECTION_QUALIFIED_NAME,
            None,
            "One of resource_id or model_id is required",
        ),
        (
            MODEL_NAME,
            RESOURCE_ID,
            None,
            None,
            None,
            "connection_qualified_name is required",
        ),
        (
            MODEL_NAME,
            RESOURCE_ID,
            None,
            None,
            CONNECTION_QUALIFIED_NAME,
            "parent_folder_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    resource_id: str,
    model_id: str,
    connection_qualified_name: str,
    parent_folder_qualified_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudModel.creator(
            name=name,
            resource_id=resource_id,
            model_id=model_id,
            connection_qualified_name=connection_qualified_name,
            parent_folder_qualified_name=parent_folder_qualified_name,
        )


def test_creator_derives_connection_from_parent_folder():
    """Test creator derives the connection and relates the folder."""
    sut = SapAnalyticsCloudModel.creator(
        name=MODEL_NAME,
        resource_id=RESOURCE_ID,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.name == MODEL_NAME
    assert sut.qualified_name == MODEL_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert (
        sut.sap_analytics_cloud_parent_folder_qualified_name
        == PARENT_FOLDER_QUALIFIED_NAME
    )
    assert sut.sap_analytics_cloud_folder.unique_attributes == {
        "qualifiedName": PARENT_FOLDER_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection():
    """Test an explicit connection qualified name is kept as given."""
    sut = SapAnalyticsCloudModel.creator(
        name=MODEL_NAME,
        resource_id=RESOURCE_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.qualified_name == MODEL_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, MODEL_NAME, "qualified_name is required"),
        (MODEL_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudModel.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a minimal instance for modification."""
    sut = SapAnalyticsCloudModel.updater(
        qualified_name=MODEL_QUALIFIED_NAME, name=MODEL_NAME
    )

    assert sut.qualified_name == MODEL_QUALIFIED_NAME
    assert sut.name == MODEL_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the fields needed for update."""
    sut = SapAnalyticsCloudModel.creator(
        name=MODEL_NAME,
        resource_id=RESOURCE_ID,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == MODEL_QUALIFIED_NAME
    assert sut.name == MODEL_NAME
