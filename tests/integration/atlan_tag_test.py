# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
import os
import urllib.request
from typing import Callable, Generator

import pytest
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from pyatlan.cache.atlan_tag_cache import AtlanTagCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError
from pyatlan.model.atlan_image import AtlanImage
from pyatlan.model.enums import AtlanIcon, AtlanTagColor, TagIconType
from pyatlan.model.typedef import AtlanTagDef
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("CLS")

CLS_IMAGE = f"{MODULE_NAME}_image"
CLS_ICON = f"{MODULE_NAME}_icon"
CLS_EMOJI = f"{MODULE_NAME}_emoji"

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def make_atlan_tag(
    client: AtlanClient,
) -> Generator[Callable[[str], AtlanTagDef], None, None]:
    created_names = []

    @retry(
        retry=retry_if_exception_type(AtlanError),
        wait=wait_random_exponential(multiplier=1, max=5),
        stop=stop_after_attempt(3),
    )
    def _wait_for_successful_purge(name: str):
        client.typedef.purge(name, typedef_type=AtlanTagDef)

    def _make_atlan_tag(name: str) -> AtlanTagDef:
        atlan_tag_def = AtlanTagDef.create(name=name, color=AtlanTagColor.GREEN)
        r = client.typedef.create(atlan_tag_def)
        c = r.atlan_tag_defs[0]
        created_names.append(c.display_name)
        return c

    yield _make_atlan_tag

    for n in created_names:
        try:
            _wait_for_successful_purge(n)
        except AtlanError as err:
            LOGGER.error(err)


@pytest.fixture(scope="module")
def image(client: AtlanClient) -> Generator[AtlanImage, None, None]:
    urllib.request.urlretrieve(
        "https://github.com/great-expectations/great_expectations"
        "/raw/develop/docs/docusaurus/static/img/gx-mark-160.png",
        "gx-mark-160.png",
    )
    with open("gx-mark-160.png", "rb") as out_file:
        yield client.upload_image(file=out_file, filename="gx-mark-160.png")
        os.remove("gx-mark-160.png")


@pytest.fixture(scope="module")
def atlan_tag_with_image(
    client: AtlanClient,
    image: AtlanImage,
) -> Generator[AtlanTagDef, None, None]:
    cls = AtlanTagDef.create(name=CLS_IMAGE, color=AtlanTagColor.YELLOW, image=image)
    yield client.typedef.create(cls).atlan_tag_defs[0]
    client.typedef.purge(CLS_IMAGE, typedef_type=AtlanTagDef)


@pytest.fixture(scope="module")
def atlan_tag_with_icon(
    client: AtlanClient,
) -> Generator[AtlanTagDef, None, None]:
    cls = AtlanTagDef.create(
        name=CLS_ICON,
        color=AtlanTagColor.YELLOW,
        icon=AtlanIcon.BOOK_BOOKMARK,
    )
    yield client.typedef.create(cls).atlan_tag_defs[0]
    client.typedef.purge(CLS_ICON, typedef_type=AtlanTagDef)


@pytest.fixture(scope="module")
def atlan_tag_with_emoji(
    client: AtlanClient,
) -> Generator[AtlanTagDef, None, None]:
    cls = AtlanTagDef.create(
        name=CLS_EMOJI,
        emoji="👍",
    )
    yield client.typedef.create(cls).atlan_tag_defs[0]
    client.typedef.purge(CLS_EMOJI, typedef_type=AtlanTagDef)


def test_atlan_tag_with_image(atlan_tag_with_image):
    assert atlan_tag_with_image
    assert atlan_tag_with_image.guid
    assert atlan_tag_with_image.display_name == CLS_IMAGE
    assert atlan_tag_with_image.name != CLS_IMAGE
    assert atlan_tag_with_image.options
    assert "color" in atlan_tag_with_image.options.keys()
    assert atlan_tag_with_image.options.get("color") == AtlanTagColor.YELLOW.value
    assert "imageID" in atlan_tag_with_image.options.keys()
    assert atlan_tag_with_image.options.get("imageID")
    assert "iconType" in atlan_tag_with_image.options.keys()
    assert atlan_tag_with_image.options.get("iconType") == TagIconType.IMAGE.value


def test_atlan_tag_cache(atlan_tag_with_image):
    cls_name = CLS_IMAGE
    cls_id = AtlanTagCache.get_id_for_name(cls_name)
    assert cls_id
    assert cls_id == atlan_tag_with_image.name
    cls_name_found = AtlanTagCache.get_name_for_id(cls_id)
    assert cls_name_found
    assert cls_name_found == cls_name


def test_atlan_tag_with_icon(atlan_tag_with_icon):
    assert atlan_tag_with_icon
    assert atlan_tag_with_icon.guid
    assert atlan_tag_with_icon.display_name == CLS_ICON
    assert atlan_tag_with_icon.name != CLS_ICON
    assert atlan_tag_with_icon.options
    assert "color" in atlan_tag_with_icon.options.keys()
    assert atlan_tag_with_icon.options.get("color") == AtlanTagColor.YELLOW.value
    assert not atlan_tag_with_icon.options.get("imageID")
    assert "iconType" in atlan_tag_with_icon.options.keys()
    assert atlan_tag_with_icon.options.get("iconType") == TagIconType.ICON.value


def test_atlan_tag_with_emoji(atlan_tag_with_emoji):
    assert atlan_tag_with_emoji
    assert atlan_tag_with_emoji.guid
    assert atlan_tag_with_emoji.display_name == CLS_EMOJI
    assert atlan_tag_with_emoji.name != CLS_EMOJI
    assert atlan_tag_with_emoji.options
    assert not atlan_tag_with_emoji.options.get("imageID")
    assert "iconType" in atlan_tag_with_emoji.options.keys()
    assert atlan_tag_with_emoji.options.get("iconType") == TagIconType.EMOJI.value
