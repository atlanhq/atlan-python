# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

from pyatlan.cache.classification_cache import ClassificationCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import AtlanClassificationColor, AtlanTypeCategory
from pyatlan.model.typedef import ClassificationDef

CLS_NAME = "psdk-classification"


class ClassificationTest:
    @staticmethod
    def create_classification(client: AtlanClient, name: str) -> ClassificationDef:
        classification_def = ClassificationDef.create(
            name=name, color=AtlanClassificationColor.GREEN
        )
        response = client.create_typedef(classification_def)
        assert response
        assert len(response.classification_defs) == 1
        created = response.classification_defs[0]
        assert created.category == AtlanTypeCategory.CLASSIFICATION
        assert created.name
        assert created.guid
        assert created.name != name
        assert created.display_name == name
        return created

    @staticmethod
    def delete_classification(client: AtlanClient, cls: ClassificationDef) -> None:
        client.purge_typedef(cls.name)


@pytest.fixture(scope="session")
def client() -> AtlanClient:
    return AtlanClient()


@pytest.fixture(scope="module")
def cls(client: AtlanClient):
    c = ClassificationTest.create_classification(client, CLS_NAME)
    yield c
    ClassificationTest.delete_classification(client, c)


@pytest.mark.usefixtures("cls")
def test_classification_cache():
    cls_id = ClassificationCache.get_id_for_name(CLS_NAME)
    assert cls_id
    cls_name = ClassificationCache.get_name_for_id(cls_id)
    assert cls_name
    assert cls_name == CLS_NAME
