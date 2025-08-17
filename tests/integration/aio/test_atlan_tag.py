# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import contextlib
import logging
import os
import urllib.request
from typing import AsyncGenerator, Callable, Optional

import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
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


async def wait_for_successful_tagdef_purge_async(name: str, client: AsyncAtlanClient):
    """Async version of wait_for_successful_tagdef_purge."""
    import asyncio

    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            await client.typedef.purge(name=name, typedef_type=AtlanTagDef)
            break
        except Exception as e:
            attempts += 1
            if attempts >= max_attempts:
                raise e
            await asyncio.sleep(1)


@pytest_asyncio.fixture(scope="module")
async def make_atlan_tag(
    client: AsyncAtlanClient,
) -> AsyncGenerator[Callable[[str], AtlanTagDef], None]:
    created_names = []

    async def _make_atlan_tag(
        name: str,
        color: AtlanTagColor = AtlanTagColor.GREEN,
        image: Optional[AtlanImage] = None,
    ) -> AtlanTagDef:
        atlan_tag_def = AtlanTagDef.create(name=name, color=color, image=image)
        r = await client.typedef.create(atlan_tag_def)
        c = r.atlan_tag_defs[0]
        created_names.append(c.display_name)
        return c

    yield _make_atlan_tag

    for n in created_names:
        try:
            await wait_for_successful_tagdef_purge_async(name=n, client=client)
        except AtlanError as err:
            LOGGER.error(err)


@pytest_asyncio.fixture(scope="module")
async def image(client: AsyncAtlanClient) -> AsyncGenerator[AtlanImage, None]:
    urllib.request.urlretrieve(
        "https://github.com/great-expectations/great_expectations"
        "/raw/develop/docs/docusaurus/static/img/gx-mark-160.png",
        "gx-mark-160.png",
    )
    with open("gx-mark-160.png", "rb") as out_file:
        yield await client.upload_image(file=out_file, filename="gx-mark-160.png")
    os.remove("gx-mark-160.png")


@pytest_asyncio.fixture(scope="module")
async def atlan_tag_with_image(
    client: AsyncAtlanClient,
    image: AtlanImage,
) -> AsyncGenerator[AtlanTagDef, None]:
    cls = AtlanTagDef.create(name=CLS_IMAGE, color=AtlanTagColor.YELLOW, image=image)
    yield (await client.typedef.create(cls)).atlan_tag_defs[0]
    with contextlib.suppress(AtlanError):
        await wait_for_successful_tagdef_purge_async(name=CLS_IMAGE, client=client)


@pytest_asyncio.fixture(scope="module")
async def atlan_tag_with_icon(
    client: AsyncAtlanClient,
) -> AsyncGenerator[AtlanTagDef, None]:
    cls = AtlanTagDef.create(
        name=CLS_ICON,
        color=AtlanTagColor.YELLOW,
        icon=AtlanIcon.BOOK_BOOKMARK,
    )
    yield (await client.typedef.create(cls)).atlan_tag_defs[0]
    with contextlib.suppress(AtlanError):
        await wait_for_successful_tagdef_purge_async(name=CLS_ICON, client=client)


@pytest_asyncio.fixture(scope="module")
async def atlan_tag_with_emoji(
    client: AsyncAtlanClient,
) -> AsyncGenerator[AtlanTagDef, None]:
    cls = AtlanTagDef.create(
        name=CLS_EMOJI,
        emoji="👍",
    )
    yield (await client.typedef.create(cls)).atlan_tag_defs[0]
    with contextlib.suppress(AtlanError):
        await wait_for_successful_tagdef_purge_async(name=CLS_EMOJI, client=client)


async def test_atlan_tag_with_image(atlan_tag_with_image):
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


async def test_atlan_tag_cache(client: AsyncAtlanClient, atlan_tag_with_image):
    cls_name = CLS_IMAGE
    cls_id = await client.atlan_tag_cache.get_id_for_name(cls_name)
    assert cls_id
    assert cls_id == atlan_tag_with_image.name
    cls_name_found = await client.atlan_tag_cache.get_name_for_id(cls_id)
    assert cls_name_found
    assert cls_name_found == cls_name


async def test_atlan_tag_with_icon(atlan_tag_with_icon):
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


async def test_atlan_tag_with_emoji(atlan_tag_with_emoji):
    assert atlan_tag_with_emoji
    assert atlan_tag_with_emoji.guid
    assert atlan_tag_with_emoji.display_name == CLS_EMOJI
    assert atlan_tag_with_emoji.name != CLS_EMOJI
    assert atlan_tag_with_emoji.options
    assert not atlan_tag_with_emoji.options.get("imageID")
    assert "iconType" in atlan_tag_with_emoji.options.keys()
    assert atlan_tag_with_emoji.options.get("iconType") == TagIconType.EMOJI.value
