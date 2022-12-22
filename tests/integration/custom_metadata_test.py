import pytest

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.typedef import TypeDefClient
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
def client() -> TypeDefClient:
    return TypeDefClient(AtlanClient())


def test_001_create_custom_metadata(client: TypeDefClient):
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


def test_003_purge_custom_metadata(client: TypeDefClient):
    cm_id = CustomMetadataCache.get_id_for_name(CM_NAME)
    assert cm_id
    client.purge_typedef(cm_id)
