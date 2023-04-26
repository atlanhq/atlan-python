# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Table
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef

CM_NAME = "psdk-CustomMetadataTest"
CM_ATTR_LICENSE = "License"
CM_ATTR_VERSION = "Version"
CM_ATTR_MANDATORY = "Mandatory"
CM_ATTR_DATE = "Date"
CM_ATTR_URL = "URL"

# NOTE: Tests are intended to run in the order specified in this file,
# to complete creation prior to testing prior to deletion.


@pytest.fixture
def client() -> AtlanClient:
    return AtlanClient()


def test_001_create_custom_metadata(client: AtlanClient):
    attribute_defs = [
        AttributeDef(
            name=CM_ATTR_LICENSE,
            display_name=CM_ATTR_LICENSE,
            type_name="string",
            options=AttributeDef.Options(),
        ),
        AttributeDef(
            name=CM_ATTR_VERSION,
            display_name=CM_ATTR_VERSION,
            type_name="array<float>",
            options=AttributeDef.Options(multi_value_select=True),
        ),
        AttributeDef(
            name=CM_ATTR_MANDATORY,
            display_name=CM_ATTR_MANDATORY,
            type_name="boolean",
            options=AttributeDef.Options(),
        ),
        AttributeDef(
            name=CM_ATTR_DATE,
            display_name=CM_ATTR_DATE,
            type_name="date",
            options=AttributeDef.Options(),
        ),
        AttributeDef(
            name=CM_ATTR_URL,
            display_name=CM_ATTR_URL,
            type_name="string",
            options=AttributeDef.Options(custom_type="url"),
        ),
    ]
    cm = CustomMetadataDef(
        name=CM_NAME,
        display_name=CM_NAME,
        attribute_defs=attribute_defs,
        options=CustomMetadataDef.Options(emoji="⚖️"),
    )
    response = client.create_typedef(cm)
    print(response)
    assert response
    assert response.custom_metadata_defs
    assert len(response.custom_metadata_defs) == 1


def test_002_custom_metadata_cache():
    cm_id = CustomMetadataCache.get_id_for_name(CM_NAME)
    print("Found ID: ", cm_id)
    assert cm_id
    cm_name = CustomMetadataCache.get_name_for_id(cm_id)
    print("Found name: ", cm_name)
    assert cm_name
    assert cm_name == CM_NAME


def test_003_purge_custom_metadata(client: AtlanClient):
    cm_id = CustomMetadataCache.get_id_for_name(CM_NAME)
    assert cm_id
    client.purge_typedef(cm_id)


def test_custom_metadata_has_human_readable_properties(client: AtlanClient):
    table = client.get_asset_by_guid("5f47cfb9-1313-4f03-9213-9913fff3c878", Table)
    anomalo = table.get_custom_metadata("Anomalo")
    assert hasattr(anomalo, "data_volume")
    assert anomalo.data_volume is None
    assert hasattr(anomalo, "data_volume_details")
    assert anomalo.data_volume_details is None
    assert hasattr(anomalo, "data_freshness")
    assert anomalo.data_freshness is None
    assert hasattr(anomalo, "data_freshness_details")
    assert anomalo.data_freshness_details is None
    assert hasattr(anomalo, "table_url")
    assert anomalo.table_url is None
    assert hasattr(anomalo, "missing_data")
    assert anomalo.missing_data is None
    assert hasattr(anomalo, "missing_data_details")
    assert anomalo.missing_data_details is None
    assert hasattr(anomalo, "table_anomalies")
    assert anomalo.table_anomalies is None
    assert hasattr(anomalo, "table_anomalies_details")
    assert anomalo.table_anomalies_details is None
    assert hasattr(anomalo, "key_metrics")
    assert anomalo.key_metrics is None
    assert hasattr(anomalo, "key_metrics_details")
    assert anomalo.key_metrics_details is None
    assert hasattr(anomalo, "validation_rules")
    assert anomalo.validation_rules is None
    assert hasattr(anomalo, "validation_rules_details")
    assert anomalo.validation_rules_details is None
    monte_carlo = table.get_custom_metadata("Monte Carlo")
    assert monte_carlo is not None


def test_get_custom_metadata():
    custom_metadata = CustomMetadataCache.get_custom_metadata(
        name="RACI", asset_type=Table
    )
    assert custom_metadata is not None


def test_get_custom_metadata_when_name_is_invalid_then_raises_value_error():
    with pytest.raises(
        ValueError, match="No custom metadata with the name: Bogs exist"
    ):
        CustomMetadataCache.get_custom_metadata(name="Bogs", asset_type=Table)
