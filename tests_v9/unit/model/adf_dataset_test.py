# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for AdfDataset model in pyatlan_v9.

The parity test uses the exact qualifiedNames atlan-adf-app emits today
(``{connQN}/factory/{factory}/datasets/{name}``, FND-3838 census, and the
linked service reference built by ``_enrich_dataset``), so a creator change
that would re-key existing datasets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import AdfDataset

CONNECTION_QUALIFIED_NAME = "default/azure-data-factory/1700000000"
CONNECTOR_NAME = "azure-data-factory"
FACTORY_NAME = "adf-factory"
DATASET_NAME = "DelimitedText1"
DATASET_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/factory/{FACTORY_NAME}/datasets/{DATASET_NAME}"
)


def test_creator_matches_app_qualified_name():
    """Mirror atlan-adf-app's process_datasets and _enrich_dataset output."""
    sut = AdfDataset.creator(
        name="DelimitedText1",
        adf_factory_name="adf-factory",
        connection_qualified_name="default/azure-data-factory/1700000000",
        adf_linkedservice_name="AzureBlobStorage1",
    )

    assert sut.qualified_name == (
        "default/azure-data-factory/1700000000"
        "/factory/adf-factory/datasets/DelimitedText1"
    )
    assert sut.adf_dataset_linked_service == "AzureBlobStorage1"
    assert sut.adf_linkedservice.unique_attributes == {
        "qualifiedName": "default/azure-data-factory/1700000000"
        "/factory/adf-factory/linkedservices/AzureBlobStorage1"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, factory_name, connection_qualified_name, message",
    [
        (None, FACTORY_NAME, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", FACTORY_NAME, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (DATASET_NAME, None, CONNECTION_QUALIFIED_NAME, "adf_factory_name is required"),
        (
            DATASET_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            "adf_factory_name cannot be blank",
        ),
        (DATASET_NAME, FACTORY_NAME, None, "connection_qualified_name is required"),
        (
            DATASET_NAME,
            FACTORY_NAME,
            " ",
            "connection_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, factory_name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AdfDataset.creator(
            name=name,
            adf_factory_name=factory_name,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator without a linked service leaves the relationship unset."""
    sut = AdfDataset.creator(
        name=DATASET_NAME,
        adf_factory_name=FACTORY_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == DATASET_NAME
    assert sut.qualified_name == DATASET_QUALIFIED_NAME
    assert sut.adf_factory_name == FACTORY_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.adf_dataset_linked_service is UNSET
    assert sut.adf_linkedservice is UNSET
    sut.validate(for_creation=True)


def test_validate_rejects_other_qualified_name_shapes():
    """The generated pattern only accepts the app's dataset shape."""
    sut = AdfDataset.updater(
        qualified_name=f"{CONNECTION_QUALIFIED_NAME}/{DATASET_NAME}",
        name=DATASET_NAME,
    )

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATASET_NAME, "qualified_name is required"),
        (DATASET_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AdfDataset.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an AdfDataset for modification."""
    sut = AdfDataset.updater(qualified_name=DATASET_QUALIFIED_NAME, name=DATASET_NAME)

    assert sut.qualified_name == DATASET_QUALIFIED_NAME
    assert sut.name == DATASET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = AdfDataset.updater(
        qualified_name=DATASET_QUALIFIED_NAME, name=DATASET_NAME
    ).trim_to_required()

    assert sut.qualified_name == DATASET_QUALIFIED_NAME
    assert sut.name == DATASET_NAME
