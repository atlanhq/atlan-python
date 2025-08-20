# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, AsyncGenerator, Optional

from httpx_retries import Retry
from pydantic.v1 import HttpUrl

from pyatlan.client.atlan import DEFAULT_RETRY

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


@contextlib.asynccontextmanager
async def client_connection(
    client: AsyncAtlanClient,
    base_url: Optional[HttpUrl] = None,
    api_key: Optional[str] = None,
    connect_timeout: float = 30.0,
    read_timeout: float = 120.0,
    retry: Retry = DEFAULT_RETRY,
) -> AsyncGenerator[AsyncAtlanClient, None]:
    """
    Creates a new async client created with the given base_url and/api_key.

    :param base_url: the base_url to be used for the new connection.
    If not specified the current value will be used
    :param api_key: the api_key to be used for the new connection.
    If not specified the current value will be used
    :param connect_timeout: connection timeout for the new client
    :param read_timeout: read timeout for the new client
    :param retry: retry configuration for the new client
    """
    from pyatlan.client.aio.client import AsyncAtlanClient

    tmp_client = AsyncAtlanClient(
        base_url=base_url or client.base_url,
        api_key=api_key or client.api_key,
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
        retry=retry,
    )
    yield tmp_client
