# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

from pyatlan.cache.classification_cache import ClassificationCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.typedef import ClassificationDef

CLS_NAME = "psdk-ClassificationTest"

# NOTE: Tests are intended to run in the order specified in this file,
# to complete creation prior to testing prior to deletion.


@pytest.fixture
def client() -> AtlanClient:
    return AtlanClient()


def test_001_create_classification(client: AtlanClient):
    cls = ClassificationDef(
        name=CLS_NAME, display_name=CLS_NAME, options={"color": "GREEN"}
    )
    response = client.create_typedef(cls)
    print(response)
    assert response
    assert response.classification_defs
    assert len(response.classification_defs) == 1


def test_002_classification_cache():
    cls_id = ClassificationCache.get_id_for_name(CLS_NAME)
    print("Found ID: ", cls_id)
    assert cls_id
    cls_name = ClassificationCache.get_name_for_id(cls_id)
    print("Found name: ", cls_name)
    assert cls_name
    assert cls_name == CLS_NAME


def test_003_purge_classification(client: AtlanClient):
    cls_id = ClassificationCache.get_id_for_name(CLS_NAME)
    assert cls_id
    client.purge_typedef(cls_id)
