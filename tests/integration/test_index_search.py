# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from dataclasses import dataclass, field
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.search import (
    DSL,
    Exists,
    IndexSearchRequest,
    Match,
    Prefix,
    Range,
    Regexp,
    Term,
    Wildcard,
)

VALUES_FOR_TERM_QUERIES = {
    "with_categories": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_classification_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_classifications_text": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_connector_name": AtlanConnectorType.SNOWFLAKE,
    "with_create_time_as_timestamp": 1665727666701,
    "with_created_by": "bryan",
    "with_glossary": "mweSfpXBwfYWedQTvA3Gi",
    "with_guid": "b95eed37-fe38-48d7-8240-0c3390ef4e48",
    "with_has_lineage": True,
    "with_meanings": "2EqDFWZ6sCjbxcDNL0jFV@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_meanings_text": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_modified_by": "bryan",
    "with_name": "Schema",
    "with_owner_groups": "data_engineering",
    "with_owner_users": "ravi",
    "with_parent_category": "fWB1bJLOhEd4ik1Um1EJ8@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_qualified_name": "default/oracle/1665680872/ORCL/SCALE_TEST/TABLE_MVD_3042/PERSON_ID",
    "with_state": "ACTIVE",
    "with_super_type_names": "SQL",
    "with_type_name": "Schema",
    "with_update_time_as_timestamp": 1665723703029,
}

VALUES_FOR_TEXT_QUERIES = {
    "with_categories": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_classification_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_classifications_text": "RBmhFJqX50bl5RAeJhwt1a",
    "with_created_by": "bryan",
    "with_description": "snapshot",
    "with_glossary": "mweSfpXBwfYWedQTvA3Gi",
    "with_guid": "b95eed37-fe38-48d7-8240-0c3390ef4e48",
    "with_has_lineage": True,
    "with_meanings": "2EqDFWZ6sCjbxcDNL0jFV@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_meanings_text": "Term Test",
    "with_modification_timestamp": 1665086276846,
    "with_modified_by": "bryan",
    "with_name": "Schema",
    "with_parent_category": "fWB1bJLOhEd4ik1Um1EJ8@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_propagated_classification_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_qualified_name": "default",
    "with_state": "ACTIVE",
    "with_super_type_names": "ObjectStore SQL",
    "with_timestamp": 1665727666701,
    "with_trait_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_propagated_trait_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_type_name": "Schema",
    "with_user_description": "this",
}


@dataclass()
class AssetTracker:
    missing_types: set[str] = field(default_factory=set)
    found_types: set[str] = field(default_factory=set)


@pytest.fixture(scope="module")
def client() -> AtlanClient:
    return AtlanClient()


@pytest.fixture(scope="module")
def asset_tracker() -> Generator[AssetTracker, None, None]:
    tracker = AssetTracker()
    yield tracker
    print("Total number of asset types found: ", len(tracker.found_types))
    print("Total number of asset types missing: ", len(tracker.missing_types))
    print("Assets were not found for the following types:")
    for name in sorted(tracker.missing_types):
        print("\t", name)
    print("Assets were found for the following types:")
    for name in sorted(tracker.found_types):
        print("\t", name)


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


@pytest.mark.parametrize("cls", [(cls) for cls in get_all_subclasses(Asset)])
def test_search(client: AtlanClient, asset_tracker, cls):
    name = cls.__name__
    query = Term.with_state("ACTIVE")
    post_filter = Term.with_type_name(name)
    dsl = DSL(query=query, post_filter=post_filter)
    request = IndexSearchRequest(dsl=dsl, attributes=["name"])
    results = client.search(criteria=request)
    if results.count > 0:
        asset_tracker.found_types.add(name)
        counter = 0
        for asset in results:
            assert isinstance(asset, cls)
            counter += 1
            if counter > 3:
                break
    else:
        asset_tracker.missing_types.add(name)


def test_search_next_page(client: AtlanClient):
    size = 15
    dsl = DSL(
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name(value="Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.count > size
    assert len(results.current_page()) == size
    counter = 0
    while True:
        for _ in results.current_page():
            counter += 1
        if results.next_page() is not True:
            break
    assert counter == results.count


def test_search_iter(client: AtlanClient):
    size = 15
    dsl = DSL(
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name("Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.count > size
    assert len([a for a in results]) == results.count


def test_search_next_when_start_changed_returns_remaining(client: AtlanClient):
    size = 2
    dsl = DSL(
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name("Database"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = client.search(criteria=request)
    assert results.next_page(start=results.count - size) is True
    assert len(list(results)) == size


@pytest.fixture()
def term_query_value(request):
    return VALUES_FOR_TERM_QUERIES[request.param]


@pytest.fixture()
def text_query_value(request):
    return VALUES_FOR_TEXT_QUERIES[request.param]


@pytest.mark.parametrize(
    "term_query_value, method, clazz",
    [
        (method, method, query)
        for query in [Term, Prefix, Regexp, Wildcard]
        for method in sorted(dir(query))
        if method.startswith("with_")
    ],
    indirect=["term_query_value"],
)
def test_term_queries_factory(client: AtlanClient, term_query_value, method, clazz):
    assert hasattr(clazz, method)
    query = getattr(clazz, method)(term_query_value)
    filter = ~Term.with_type_name("__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = client.search(criteria=request)
    assert results.count > 0


@pytest.mark.parametrize(
    "with_name", [(method) for method in dir(Exists) if method.startswith("with_")]
)
def test_exists_query_factory(client: AtlanClient, with_name):
    assert hasattr(Exists, with_name)
    query = getattr(Exists, with_name)()
    dsl = DSL(query=query, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = client.search(criteria=request)
    assert results.count > 0


@pytest.mark.parametrize(
    "text_query_value, method, clazz",
    [
        (method, method, query)
        for query in [Match]
        for method in sorted(dir(query))
        if method.startswith("with_")
    ],
    indirect=["text_query_value"],
)
def test_text_queries_factory(client: AtlanClient, text_query_value, method, clazz):
    assert hasattr(clazz, method)
    query = getattr(clazz, method)(text_query_value)
    filter = ~Term.with_type_name("__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    # print(request.json(by_alias=True, exclude_none=True))
    results = client.search(criteria=request)
    assert results.count > 0


@pytest.mark.parametrize(
    "value, method, format",
    [
        (0, "with_popularity_score", None),
        (1665727666701, "with_create_time_as_timestamp", None),
        ("2023-01", "with_create_time_as_date", "yyyy-MM"),
        (1665727666701, "with_update_time_as_timestamp", None),
        ("2023-01", "with_update_time_as_date", "yyyy-MM"),
    ],
)
def test_range_factory(client: AtlanClient, value, method, format):
    assert hasattr(Range, method)
    query = getattr(Range, method)(lt=value, format=format)
    filter = ~Term.with_type_name("__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = client.search(criteria=request)
    assert results.count > 0
