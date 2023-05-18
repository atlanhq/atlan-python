# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
from typing import Callable, Generator

import pytest
from retry import retry

from pyatlan.cache.classification_cache import ClassificationCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.error import AtlanError
from pyatlan.model.enums import AtlanClassificationColor
from pyatlan.model.typedef import ClassificationDef

LOGGER = logging.getLogger(__name__)


CLS_NAME = "psdk-classification"


@pytest.fixture(scope="module", autouse=True)
def make_classification(
    client: AtlanClient,
) -> Generator[Callable[[str], ClassificationDef], None, None]:
    created_names = []

    @retry(
        AtlanError,
        delay=1,
        tries=3,
        max_delay=5,
        backoff=2,
        jitter=(0, 1),
        logger=LOGGER,
    )
    def _wait_for_successful_purge(name: str):
        client.purge_typedef(name, typedef_type=ClassificationDef)

    def _make_classification(name: str) -> ClassificationDef:
        classification_def = ClassificationDef.create(
            name=name, color=AtlanClassificationColor.GREEN
        )
        r = client.create_typedef(classification_def)
        c = r.classification_defs[0]
        created_names.append(c.display_name)
        return c

    yield _make_classification

    for n in created_names:
        try:
            _wait_for_successful_purge(n)
        except AtlanError as err:
            LOGGER.error(err)


@pytest.fixture(scope="module")
def classification_def(
    client: AtlanClient, make_classification: Callable[[str], ClassificationDef]
) -> ClassificationDef:
    return make_classification(CLS_NAME)


def test_classification_def(classification_def: ClassificationDef):
    assert classification_def
    assert classification_def.guid
    assert classification_def.display_name == CLS_NAME
    assert classification_def.name != CLS_NAME
    assert classification_def.options
    assert "color" in classification_def.options.keys()
    assert (
        classification_def.options.get("color") == AtlanClassificationColor.GREEN.value
    )


def test_classification_cache(classification_def: ClassificationDef):
    cls_id = ClassificationCache.get_id_for_name(CLS_NAME)
    assert cls_id
    assert cls_id == classification_def.name
    cls_name = ClassificationCache.get_name_for_id(cls_id)
    assert cls_name
    assert cls_name == CLS_NAME
