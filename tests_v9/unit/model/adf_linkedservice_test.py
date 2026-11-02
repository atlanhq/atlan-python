# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for AdfLinkedservice model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-adf-app emits today
(``{connQN}/factory/{factory}/linkedservices/{name}``, FND-3838 census), so a
creator change that would re-key existing linked services fails here.
"""

import pytest

from pyatlan_v9.model import AdfLinkedservice

CONNECTION_QUALIFIED_NAME = "default/azure-data-factory/1700000000"
CONNECTOR_NAME = "azure-data-factory"
FACTORY_NAME = "adf-factory"
LINKEDSERVICE_NAME = "AzureBlobStorage1"
LINKEDSERVICE_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/factory/{FACTORY_NAME}"
    f"/linkedservices/{LINKEDSERVICE_NAME}"
)


def test_creator_matches_app_qualified_name():
    """Mirror atlan-adf-app's process_linked_services inputs and output."""
    sut = AdfLinkedservice.creator(
        name="AzureBlobStorage1",
        adf_factory_name="adf-factory",
        connection_qualified_name="default/azure-data-factory/1700000000",
    )

    assert sut.qualified_name == (
        "default/azure-data-factory/1700000000"
        "/factory/adf-factory/linkedservices/AzureBlobStorage1"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, factory_name, connection_qualified_name, message",
    [
        (None, FACTORY_NAME, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", FACTORY_NAME, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (
            LINKEDSERVICE_NAME,
            None,
            CONNECTION_QUALIFIED_NAME,
            "adf_factory_name is required",
        ),
        (
            LINKEDSERVICE_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            "adf_factory_name cannot be blank",
        ),
        (
            LINKEDSERVICE_NAME,
            FACTORY_NAME,
            None,
            "connection_qualified_name is required",
        ),
        (
            LINKEDSERVICE_NAME,
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
        AdfLinkedservice.creator(
            name=name,
            adf_factory_name=factory_name,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the factory and connection attributes."""
    sut = AdfLinkedservice.creator(
        name=LINKEDSERVICE_NAME,
        adf_factory_name=FACTORY_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == LINKEDSERVICE_NAME
    assert sut.qualified_name == LINKEDSERVICE_QUALIFIED_NAME
    assert sut.adf_factory_name == FACTORY_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    sut.validate(for_creation=True)


def test_validate_rejects_other_qualified_name_shapes():
    """The generated pattern only accepts the app's linked service shape."""
    sut = AdfLinkedservice.updater(
        qualified_name=f"{CONNECTION_QUALIFIED_NAME}/{LINKEDSERVICE_NAME}",
        name=LINKEDSERVICE_NAME,
    )

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, LINKEDSERVICE_NAME, "qualified_name is required"),
        (LINKEDSERVICE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AdfLinkedservice.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an AdfLinkedservice for modification."""
    sut = AdfLinkedservice.updater(
        qualified_name=LINKEDSERVICE_QUALIFIED_NAME, name=LINKEDSERVICE_NAME
    )

    assert sut.qualified_name == LINKEDSERVICE_QUALIFIED_NAME
    assert sut.name == LINKEDSERVICE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = AdfLinkedservice.updater(
        qualified_name=LINKEDSERVICE_QUALIFIED_NAME, name=LINKEDSERVICE_NAME
    ).trim_to_required()

    assert sut.qualified_name == LINKEDSERVICE_QUALIFIED_NAME
    assert sut.name == LINKEDSERVICE_NAME
