# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for GCPDataplexAspectType model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-dataplex-app emits today
(``aspect_type_qn``: ``{connectionQN}/aspect-type/{resourceName}``, FND-3838 census),
so a creator change that would re-key existing aspect types fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import GCPDataplexAspectType

CONNECTION_QUALIFIED_NAME = "default/dataplex/123456789"
CONNECTOR_NAME = "dataplex"
RESOURCE_NAME = "projects/my-project/locations/us-central1/aspectTypes/data-owner"
ASPECT_TYPE_NAME = "data-owner"
ASPECT_TYPE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/aspect-type/{RESOURCE_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-dataplex-app's extract_aspect_types inputs and output."""
    sut = GCPDataplexAspectType.creator(
        resource_name="projects/acme-prod/locations/global/aspectTypes/pii",
        connection_qualified_name="default/dataplex/1700000000",
    )

    assert (
        sut.qualified_name == "default/dataplex/1700000000/aspect-type/"
        "projects/acme-prod/locations/global/aspectTypes/pii"
    )
    assert sut.name == "pii"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "resource_name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "resource_name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "resource_name cannot be blank"),
        (RESOURCE_NAME, None, "connection_qualified_name is required"),
        (RESOURCE_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    resource_name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        GCPDataplexAspectType.creator(
            resource_name=resource_name,
            connection_qualified_name=connection_qualified_name,
        )


@pytest.mark.parametrize(
    "resource_name",
    [
        "data-owner",
        "projects/p/locations/l/entryTypes/data-owner",
        "projects/p/locations/ /aspectTypes/data-owner",
        "projects/p/locations/l/aspectTypes/data-owner/extra",
    ],
)
def test_creator_with_malformed_resource_name_raises_value_error(resource_name: str):
    """Test creator rejects a resource name that is not an aspect type resource."""
    with pytest.raises(ValueError, match="Invalid resource_name"):
        GCPDataplexAspectType.creator(
            resource_name=resource_name,
            connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        )


def test_creator():
    """Test creator sets the resource attributes and denormalised connection attributes."""
    sut = GCPDataplexAspectType.creator(
        resource_name=RESOURCE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "GCPDataplexAspectType"
    assert sut.name == ASPECT_TYPE_NAME
    assert sut.qualified_name == ASPECT_TYPE_QUALIFIED_NAME
    assert sut.gcp_dataplex_aspect_type_resource_name == RESOURCE_NAME
    assert sut.gcp_dataplex_aspect_type_project == "my-project"
    assert sut.gcp_dataplex_aspect_type_location == "us-central1"
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.guid
    sut.validate(for_creation=True)


def test_create_alias():
    """Test the deprecated create alias delegates to creator."""
    sut = GCPDataplexAspectType.create(
        resource_name=RESOURCE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == ASPECT_TYPE_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ASPECT_TYPE_NAME, "qualified_name is required"),
        (ASPECT_TYPE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        GCPDataplexAspectType.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a GCPDataplexAspectType for modification."""
    sut = GCPDataplexAspectType.updater(
        qualified_name=ASPECT_TYPE_QUALIFIED_NAME, name=ASPECT_TYPE_NAME
    )

    assert sut.qualified_name == ASPECT_TYPE_QUALIFIED_NAME
    assert sut.name == ASPECT_TYPE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = GCPDataplexAspectType.creator(
        resource_name=RESOURCE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == ASPECT_TYPE_QUALIFIED_NAME
    assert sut.name == ASPECT_TYPE_NAME
    assert sut.gcp_dataplex_aspect_type_resource_name is UNSET
