# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""Shared integration test utilities for v9."""

from typing import List, Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
)

from pyatlan_v9.errors import AtlanError, NotFoundError
from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Persona, Purpose
from pyatlan_v9.model.fluent_search import FluentSearch
from pyatlan_v9.model.search import IndexSearchRequest
from pyatlan_v9.model.typedef import AtlanTagDef, CustomMetadataDef, EnumDef


@retry(
    retry=retry_if_exception_type(AtlanError),
    wait=wait_random_exponential(multiplier=1, max=5),
    stop=stop_after_attempt(3),
)
def wait_for_successful_tagdef_purge(name: str, client: AtlanClient):
    client.typedef.purge(name, typedef_type=AtlanTagDef)


@retry(
    retry=retry_if_exception_type(AtlanError),
    wait=wait_random_exponential(multiplier=1, max=5),
    stop=stop_after_attempt(3),
)
def wait_for_successful_custometadatadef_purge(name: str, client: AtlanClient):
    client.typedef.purge(name, typedef_type=CustomMetadataDef)


@retry(
    retry=retry_if_exception_type(AtlanError),
    wait=wait_random_exponential(multiplier=1, max=5),
    stop=stop_after_attempt(3),
)
def wait_for_successful_enumadef_purge(name: str, client: AtlanClient):
    client.typedef.purge(name, typedef_type=EnumDef)


def find_personas_by_name_with_retry(
    client: AtlanClient, name: str, attributes: Optional[List[str]] = None
) -> List[Persona]:
    @retry(
        reraise=True,
        retry=retry_if_exception_type(NotFoundError),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _retry_find_personas():
        return client.asset.find_personas_by_name(name=name, attributes=attributes)

    return _retry_find_personas()


def find_purposes_by_name_with_retry(
    client: AtlanClient, name: str, attributes: Optional[List[str]] = None
) -> List[Purpose]:
    @retry(
        reraise=True,
        retry=retry_if_exception_type(NotFoundError),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _retry_find_purposes():
        return client.asset.find_purposes_by_name(name=name, attributes=attributes)

    return _retry_find_purposes()


def fluent_search_count_with_retry(
    fluent_search: FluentSearch, client: AtlanClient, expected_count: int
) -> int:
    @retry(
        reraise=True,
        retry=retry_if_result(lambda count: count < expected_count),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _retry_count():
        return fluent_search.count(client)

    return _retry_count()


def search_request_count_with_retry(
    client: AtlanClient, request: IndexSearchRequest, expected_count: int
) -> int:
    @retry(
        reraise=True,
        retry=retry_if_result(lambda count: count < expected_count),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _retry_search():
        response = client.asset.search(request)
        return response.count

    return _retry_search()


def assert_search_count_with_retry(
    client: AtlanClient, request: IndexSearchRequest, expected_count: int
) -> None:
    actual_count = search_request_count_with_retry(client, request, expected_count)
    assert actual_count == expected_count, (
        f"Expected {expected_count} results, got {actual_count}"
    )


def assert_fluent_search_count_with_retry(
    fluent_search: FluentSearch, client: AtlanClient, expected_count: int
) -> None:
    actual_count = fluent_search_count_with_retry(fluent_search, client, expected_count)
    assert actual_count == expected_count, (
        f"Expected {expected_count} results, got {actual_count}"
    )
