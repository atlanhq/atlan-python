# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from datetime import datetime
from re import escape
from typing import Dict, Literal, Set, Union

import pytest

from pyatlan.model.enums import AtlanConnectorType, CertificateStatus, SortOrder
from pyatlan_v9.model.audit import AuditSearchRequest
from pyatlan_v9.model.search import (
    DSL,
    Bool,
    Exists,
    Fuzzy,
    IndexSearchRequest,
    Match,
    MatchAll,
    MatchNone,
    MatchPhrase,
    Prefix,
    Range,
    Regexp,
    SortItem,
    Term,
    TermAttributes,
    Terms,
    Wildcard,
    with_active_category,
    with_active_glossary,
    with_active_term,
)
from pyatlan_v9.model.search_log import SearchLogRequest
from tests.unit.model.constants import (
    GLOSSARY_CATEGORY_NAME,
    GLOSSARY_NAME,
    GLOSSARY_QUALIFIED_NAME,
    GLOSSARY_TERM_NAME,
)

NOW = datetime.now()
NOW_TIMESTAMP = int(NOW.timestamp() * 1000)
VALUES_BY_TYPE: Dict[Union[type, object], Union[str, datetime, object]] = {
    str: "abc",
    bool: True,
    datetime: NOW,
    Literal["ACTIVE", "DELETED", "PURGED"]: "ACTIVE",
    float: 1.0,
    AtlanConnectorType: AtlanConnectorType.SNOWFLAKE,
    CertificateStatus: CertificateStatus.VERIFIED,
}

INCOMPATIPLE_QUERY: Dict[type, Set[TermAttributes]] = {
    Wildcard: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
        TermAttributes.CERTIFICATE_STATUS,
    },
    Regexp: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
        TermAttributes.CERTIFICATE_STATUS,
    },
    Fuzzy: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
        TermAttributes.CERTIFICATE_STATUS,
    },
    Prefix: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
        TermAttributes.CERTIFICATE_STATUS,
    },
    Term: {
        TermAttributes.POPULARITY_SCORE,
    },
}


@pytest.mark.parametrize(
    "parameters, expected",
    [
        (
            {},
            "__init__() missing 2 required positional arguments: 'field' and 'value'",
        ),
        (
            [
                {"field": "bob"},
                "__init__() missing 1 required positional argument: 'value'",
            ]
        ),
        (
            [
                {"value": "bob"},
                "__init__() missing 1 required positional argument: 'field'",
            ]
        ),
    ],
)
def test_term_without_parameters_value_raises_exception(parameters, expected):
    """Test that Term raises TypeError when required fields are missing."""
    with pytest.raises(
        TypeError,
        match=escape(expected),
    ):
        Term(**parameters)


@pytest.mark.parametrize(
    "parameters, expected",
    [
        (
            {"field": "name", "value": NOW},
            {"term": {"name": {"value": int(NOW.timestamp() * 1000)}}},
        ),
        ({"field": "name", "value": "dave"}, {"term": {"name": {"value": "dave"}}}),
        (
            {"field": "name", "value": "dave", "case_insensitive": True},
            {"term": {"name": {"value": "dave", "case_insensitive": True}}},
        ),
        (
            {"field": "name", "value": "dave", "case_insensitive": False},
            {"term": {"name": {"value": "dave", "case_insensitive": False}}},
        ),
        (
            {"field": "name", "value": "dave", "boost": 0.9},
            {"term": {"name": {"value": "dave", "boost": 0.9}}},
        ),
    ],
)
def test_term_to_dict(parameters, expected):
    """Test that Term.to_dict() produces the expected Elasticsearch query dict."""
    t = Term(**parameters)
    assert t.to_dict() == expected


@pytest.mark.parametrize(
    "must, should, must_not, filter, boost,  minimum_should_match, expected",
    [
        (
            [],
            [],
            [],
            [],
            None,
            None,
            {"bool": {}},
        ),
        (
            [Term(field="name", value="Bob")],
            [],
            [],
            [],
            None,
            None,
            {"bool": {"must": [{"term": {"name": {"value": "Bob"}}}]}},
        ),
        (
            [Term(field="name", value="Bob"), Term(field="name", value="Dave")],
            [],
            [],
            [],
            None,
            None,
            {
                "bool": {
                    "must": [
                        {"term": {"name": {"value": "Bob"}}},
                        {"term": {"name": {"value": "Dave"}}},
                    ]
                }
            },
        ),
        (
            [Term(field="name", value="Bob")],
            [Term(field="name", value="Dave")],
            [],
            [],
            None,
            None,
            {
                "bool": {
                    "must": [{"term": {"name": {"value": "Bob"}}}],
                    "should": [
                        {"term": {"name": {"value": "Dave"}}},
                    ],
                }
            },
        ),
        (
            [],
            [],
            [Term(field="name", value="Bob")],
            [],
            None,
            None,
            {"bool": {"must_not": [{"term": {"name": {"value": "Bob"}}}]}},
        ),
        (
            [],
            [],
            [],
            [Term(field="name", value="Bob")],
            None,
            None,
            {"bool": {"filter": [{"term": {"name": {"value": "Bob"}}}]}},
        ),
        (
            [Term(field="name", value="Bob")],
            [],
            [],
            [],
            1.0,
            None,
            {"bool": {"boost": 1.0, "must": [{"term": {"name": {"value": "Bob"}}}]}},
        ),
        (
            [Term(field="name", value="Bob")],
            [],
            [],
            [],
            None,
            3,
            {
                "bool": {
                    "minimum_should_match": 3,
                    "must": [{"term": {"name": {"value": "Bob"}}}],
                }
            },
        ),
    ],
)
def test_bool_to_dict_without_optional_fields(
    must, should, must_not, filter, boost, minimum_should_match, expected
):
    """Test that Bool.to_dict() produces expected output for various combinations."""
    assert (
        Bool(
            must=must,
            should=should,
            must_not=must_not,
            filter=filter,
            boost=boost,
            minimum_should_match=minimum_should_match,
        ).to_dict()
        == expected
    )


def test_dsl_without_query_and_post_filter_raises_validation_error():
    """Test that DSL raises ValueError when neither query nor post_filter is provided."""
    with pytest.raises(ValueError):
        DSL()


def test_dsl():
    """Test DSL JSON serialization produces correct output."""
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    assert (
        dsl.json(by_alias=True, exclude_none=True)
        == '{"from": 0, "size": 300, "aggregations": {}, "track_total_hits": true, '
        '"post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": '
        '{"__typeName.keyword": {"value": "Schema"}}}, "sort": []}'
    )


def test_index_search_request():
    """Test IndexSearchRequest JSON serialization produces correct output."""
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    request = IndexSearchRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
    assert (
        request.json(by_alias=True, exclude_none=True)
        == '{"attributes": ["schemaName", "databaseName"],'
        ' "dsl": {"from": 0, "size": 300, "aggregations": {}, "track_total_hits": true, '
        '"post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": {"__typeName.keyword": {"value": "Schema"}}}, '
        '"sort": [{"__guid": {"order": "asc"}}]}, "relationAttributes": [], "includeRelationshipAttributes": false, '
        '"requestMetadata": {"saveSearchLog": false, "utmTags": ["project_sdk_python"]}}'
    )


def test_index_search_request_with_enable_full_restriction():
    """Test IndexSearchRequest with enableFullRestriction parameter."""
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )

    # Test with enableFullRestriction=True
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["schemaName", "databaseName"],
        enable_full_restriction=True,
    )
    json_str = request.json(by_alias=True, exclude_none=True)

    # Verify the parameter is serialized correctly
    assert "enableFullRestriction" in json_str
    assert '"enableFullRestriction": true' in json_str

    # Test with enableFullRestriction=False
    request_false = IndexSearchRequest(
        dsl=DSL(
            query=Term(field="__typeName.keyword", value="Schema"),
            post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
        ),
        attributes=["schemaName"],
        enable_full_restriction=False,
    )
    json_str_false = request_false.json(by_alias=True, exclude_none=True)
    assert '"enableFullRestriction": false' in json_str_false

    # Test without the parameter (should not appear in JSON)
    request_none = IndexSearchRequest(
        dsl=DSL(
            query=Term(field="__typeName.keyword", value="Schema"),
            post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
        ),
        attributes=["schemaName"],
    )
    json_str_none = request_none.json(by_alias=True, exclude_none=True)
    assert "enableFullRestriction" not in json_str_none


def test_audit_search_request():
    """Test AuditSearchRequest JSON serialization produces correct output."""
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    request = AuditSearchRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
    assert (
        request.json(by_alias=True, exclude_none=True)
        == '{"attributes": ["schemaName", "databaseName"],'
        ' "dsl": {"from": 0, "size": 300, "aggregations": {}, "track_total_hits": true, '
        '"post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": {"__typeName.keyword": {"value": "Schema"}}}, '
        '"sort": [{"entityId": {"order": "asc"}}]}}'
    )


def test_search_log_request():
    """Test SearchLogRequest JSON serialization produces correct output."""
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    request = SearchLogRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
    assert (
        request.json(by_alias=True, exclude_none=True)
        == '{"attributes": ["schemaName", "databaseName"],'
        ' "dsl": {"from": 0, "size": 300, "aggregations": {}, "track_total_hits": true, '
        '"post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": {"__typeName.keyword": {"value": "Schema"}}}, '
        '"sort": [{"entityGuidsAll": {"order": "asc"}}]}}'
    )


def test_adding_terms_results_in_must_bool():
    """Test that adding two Terms produces a Bool with both in filter."""
    term_1 = Term(field="name", value="Bob")
    term_2 = Term(field="name", value="Dave")
    result = term_1 + term_2
    assert isinstance(result, Bool)
    assert len(result.filter) == 2
    assert term_1 in result.filter and term_2 in result.filter


def test_anding_terms_results_in_must_bool():
    """Test that ANDing two Terms produces a Bool with both in filter."""
    term_1 = Term(field="name", value="Bob")
    term_2 = Term(field="name", value="Dave")
    result = term_1 & term_2
    assert isinstance(result, Bool)
    assert len(result.filter) == 2
    assert term_1 in result.filter and term_2 in result.filter


def test_oring_terms_results_in_must_bool():
    """Test that ORing two Terms produces a Bool with both in should."""
    term_1 = Term(field="name", value="Bob")
    term_2 = Term(field="name", value="Dave")
    result = term_1 | term_2
    assert isinstance(result, Bool)
    assert len(result.should) == 2
    assert term_1 in result.should and term_2 in result.should


def test_negate_terms_results_must_not_bool():
    """Test that negating a Term produces a Bool with it in must_not."""
    term_1 = Term(field="name", value="Bob")
    result = ~term_1
    assert isinstance(result, Bool)
    assert len(result.must_not) == 1
    assert term_1 in result.must_not


@pytest.mark.parametrize(
    "q1, q2, expected",
    [
        (
            Bool(filter=[Term(field="name", value="Bob")]),
            Bool(filter=[Term(field="name", value="Dave")]),
            {
                "bool": {
                    "filter": [
                        {"term": {"name": {"value": "Bob"}}},
                        {"term": {"name": {"value": "Dave"}}},
                    ]
                }
            },
        ),
        (
            Term(field="name", value="Bob"),
            Bool(filter=[Term(field="name", value="Fred")]),
            {
                "bool": {
                    "filter": [
                        {"term": {"name": {"value": "Fred"}}},
                        {"term": {"name": {"value": "Bob"}}},
                    ]
                }
            },
        ),
        (
            Bool(filter=[Term(field="name", value="Fred")]),
            Term(field="name", value="Bob"),
            {
                "bool": {
                    "filter": [
                        {"term": {"name": {"value": "Fred"}}},
                        {"term": {"name": {"value": "Bob"}}},
                    ]
                }
            },
        ),
    ],
)
def test_add_boolean(q1, q2, expected):
    """Test Bool addition combines filter clauses correctly."""
    b = q1 + q2
    assert b.to_dict() == expected


def test_match_none_to_dict():
    """Test MatchNone produces correct dict."""
    assert MatchNone().to_dict() == {"match_none": {}}


def test_match_none_plus_other_is_match_none():
    """Test that MatchNone + any query is still MatchNone."""
    assert MatchNone() + Term(field="name", value="bob") == MatchNone()


def test_match_one_or_other_is_other():
    """Test that MatchNone | any query is the other query."""
    assert MatchNone() | Term(field="name", value="bob") == Term(
        field="name", value="bob"
    )


def test_nagate_match_one_is_match_all():
    """Test that negating MatchNone produces MatchAll."""
    assert ~MatchNone() == MatchAll()


@pytest.mark.parametrize(
    "boost, expected",
    [(None, {"match_all": {}}), (1.2, {"match_all": {"boost": 1.2}})],
)
def test_match_all_to_dict(boost, expected):
    """Test MatchAll produces correct dict with optional boost."""
    assert MatchAll(boost=boost).to_dict() == expected


def test_match_all_and_other_is_other():
    """Test that MatchAll & any query is the other query."""
    assert MatchAll() & Term(field="name", value="bob") == Term(
        field="name", value="bob"
    )


def test_match_all_or_other_is_match_all():
    """Test that MatchAll | any query is still MatchAll."""
    assert MatchAll() | Term(field="name", value="bob") == MatchAll()


def test_negate_match_all_is_match_none():
    """Test that negating MatchAll produces MatchNone."""
    assert ~MatchAll() == MatchNone()


@pytest.mark.parametrize(
    "q1, q2, expected",
    [
        (
            Term(field="name", value="Bob"),
            Bool(must=[Term(field="name", value="Fred")]),
            {
                "bool": {
                    "should": [
                        {"bool": {"must": [{"term": {"name": {"value": "Fred"}}}]}},
                        {"term": {"name": {"value": "Bob"}}},
                    ]
                }
            },
        )
    ],
)
def test_bool_or(q1, q2, expected):
    """Test Bool OR combines queries into should clause correctly."""
    b = q1 | q2
    assert b.to_dict() == expected


def test_negate_empty_bool_is_match_none():
    """Test that negating an empty Bool produces MatchNone."""
    assert ~Bool() == MatchNone()


@pytest.mark.parametrize(
    "q, expected",
    [
        (
            Bool(must=[Term(field="name", value="Fred")]),
            {"bool": {"must_not": [{"term": {"name": {"value": "Fred"}}}]}},
        ),
        (
            Bool(should=[Term(field="name", value="Fred")]),
            {"bool": {"must_not": [{"term": {"name": {"value": "Fred"}}}]}},
        ),
        (
            Bool(
                must=[
                    Term(field="name", value="Fred"),
                    Term(field="name", value="Dave"),
                ]
            ),
            {
                "bool": {
                    "should": [
                        {"bool": {"must_not": [{"term": {"name": {"value": "Fred"}}}]}},
                        {"bool": {"must_not": [{"term": {"name": {"value": "Dave"}}}]}},
                    ]
                }
            },
        ),
    ],
)
def test_negate_bool(q, expected):
    """Test Bool negation produces correct must_not clauses."""
    b = ~q
    assert b.to_dict() == expected


@pytest.mark.parametrize(
    "q1, q2, expected",
    [
        (
            Bool(should=[Term(field="name", value="Dave")]),
            Term(field="name", value="Bob"),
            {
                "bool": {
                    "should": [{"term": {"name": {"value": "Dave"}}}],
                    "must": [{"term": {"name": {"value": "Bob"}}}],
                    "minimum_should_match": 1,
                }
            },
        ),
        (
            Bool(should=[Term(field="name", value="Dave")]),
            Bool(must=[Term(field="name", value="Bob")]),
            {
                "bool": {
                    "must": [
                        {"term": {"name": {"value": "Bob"}}},
                        {"term": {"name": {"value": "Dave"}}},
                    ]
                }
            },
        ),
    ],
)
def test_bool_and(q1, q2, expected):
    """Test Bool AND combines queries correctly."""
    b = q1 & q2
    assert b.to_dict() == expected


@pytest.fixture()
def with_name(request):
    """Fixture to generate with_<attribute> method names."""
    attribute = request.param
    return f"with_{attribute.name.lower()}"


def test_terms_to_dict():
    """Test Terms query produces correct dict."""
    assert Terms(field="name", values=["john", "dave"]).to_dict() == {
        "terms": {"name": ["john", "dave"]}
    }


@pytest.mark.parametrize(
    "a_class, with_name, value, field, incompatable",
    [
        (
            c,
            a,
            VALUES_BY_TYPE[a.attribute_type],
            a.value,
            c in INCOMPATIPLE_QUERY and a in INCOMPATIPLE_QUERY[c],
        )
        for a in TermAttributes
        for c in [Term, Prefix, Regexp, Wildcard]
    ],
    indirect=["with_name"],
)
def test_by_methods_on_term_prefix_regexp_wildcard(
    a_class, with_name, value, field, incompatable
):
    """Test with_<attribute> class methods on Term, Prefix, Regexp, Wildcard."""
    if incompatable:
        assert not hasattr(a_class, with_name)
    else:
        assert hasattr(a_class, with_name)
        t = getattr(a_class, with_name)(value)
        assert isinstance(t, a_class)
        assert t.field == field
        assert t.value == value


@pytest.mark.parametrize(
    "with_name,  field",
    [(a, a.value) for a in TermAttributes],
    indirect=["with_name"],
)
def test_by_methods_on_exists(with_name, field):
    """Test with_<attribute> class methods on Exists query."""
    assert hasattr(Exists, with_name)
    t = getattr(Exists, with_name)()
    assert isinstance(t, Exists)
    assert t.field == field


@pytest.mark.parametrize(
    "gt, gte, lt, lte, boost, format, relation, timezone, expected",
    [
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"range": {"Bob": {}}},
        ),
        (
            0,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"range": {"Bob": {"gt": 0}}},
        ),
        (
            10,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"range": {"Bob": {"gt": 10}}},
        ),
        (
            None,
            10,
            None,
            None,
            None,
            None,
            None,
            None,
            {"range": {"Bob": {"gte": 10}}},
        ),
        (
            None,
            None,
            10,
            None,
            None,
            None,
            None,
            None,
            {"range": {"Bob": {"lt": 10}}},
        ),
        (
            None,
            None,
            None,
            10,
            None,
            None,
            None,
            None,
            {"range": {"Bob": {"lte": 10}}},
        ),
        (
            None,
            None,
            None,
            None,
            2.0,
            None,
            None,
            None,
            {"range": {"Bob": {"boost": 2.0}}},
        ),
        (
            None,
            None,
            None,
            None,
            None,
            "YY/MM/DD",
            None,
            None,
            {"range": {"Bob": {"format": "YY/MM/DD"}}},
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            "CONTAINS",
            None,
            {"range": {"Bob": {"relation": "CONTAINS"}}},
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "-01:00",
            {"range": {"Bob": {"time_zone": "-01:00"}}},
        ),
        (
            1,
            2,
            3,
            4,
            2.0,
            "YY/MM/DD",
            "WITHIN",
            "-01:00",
            {
                "range": {
                    "Bob": {
                        "gt": 1,
                        "gte": 2,
                        "lt": 3,
                        "lte": 4,
                        "boost": 2.0,
                        "format": "YY/MM/DD",
                        "relation": "WITHIN",
                        "time_zone": "-01:00",
                    }
                }
            },
        ),
        (
            NOW,
            2,
            3,
            4,
            2.0,
            "YY/MM/DD",
            "WITHIN",
            "-01:00",
            {
                "range": {
                    "Bob": {
                        "gt": NOW_TIMESTAMP,
                        "gte": 2,
                        "lt": 3,
                        "lte": 4,
                        "boost": 2.0,
                        "format": "YY/MM/DD",
                        "relation": "WITHIN",
                        "time_zone": "-01:00",
                    }
                }
            },
        ),
    ],
)
def test_range_to_dict(gt, gte, lt, lte, boost, format, relation, timezone, expected):
    """Test Range query produces correct dict for various parameter combinations."""
    assert (
        Range(
            field="Bob",
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            boost=boost,
            format=format,
            relation=relation,
            time_zone=timezone,
        ).to_dict()
        == expected
    )


@pytest.mark.parametrize(
    "field,  order, expected",
    [
        ("name.keyword", SortOrder.ASCENDING, {"name.keyword": {"order": "asc"}}),
        ("name.keyword", None, {"name.keyword": {"order": "asc"}}),
        ("name.keyword", SortOrder.DESCENDING, {"name.keyword": {"order": "desc"}}),
    ],
)
def test_sort_item_to_dict(field, order, expected):
    """Test SortItem produces correct dict with various sort orders."""
    assert SortItem(field=field, order=order).to_dict() == expected


@pytest.mark.parametrize(
    "field, value, fuzziness, max_expansions, prefix_length, transpositions, rewrite, expected",
    [
        (
            "user",
            "ki",
            None,
            None,
            None,
            None,
            None,
            {"fuzzy": {"user": {"value": "ki"}}},
        ),
        (
            "user",
            "ki",
            "AUTO",
            None,
            None,
            None,
            None,
            {"fuzzy": {"user": {"value": "ki", "fuzziness": "AUTO"}}},
        ),
        (
            "user",
            "ki",
            "AUTO",
            3,
            None,
            None,
            None,
            {
                "fuzzy": {
                    "user": {"value": "ki", "fuzziness": "AUTO", "max_expansions": 3}
                }
            },
        ),
        (
            "user",
            "ki",
            "AUTO",
            3,
            0,
            None,
            None,
            {
                "fuzzy": {
                    "user": {
                        "value": "ki",
                        "fuzziness": "AUTO",
                        "max_expansions": 3,
                        "prefix_length": 0,
                    }
                }
            },
        ),
        (
            "user",
            "ki",
            "AUTO",
            3,
            0,
            1,
            None,
            {
                "fuzzy": {
                    "user": {
                        "value": "ki",
                        "fuzziness": "AUTO",
                        "max_expansions": 3,
                        "prefix_length": 0,
                        "transpositions": 1,
                    }
                }
            },
        ),
        (
            "user",
            "ki",
            "AUTO",
            3,
            0,
            1,
            "constant_score",
            {
                "fuzzy": {
                    "user": {
                        "value": "ki",
                        "fuzziness": "AUTO",
                        "max_expansions": 3,
                        "prefix_length": 0,
                        "transpositions": 1,
                        "rewrite": "constant_score",
                    }
                }
            },
        ),
    ],
)
def test_fuzzy_to_dict(
    field,
    value,
    fuzziness,
    max_expansions,
    prefix_length,
    transpositions,
    rewrite,
    expected,
):
    """Test Fuzzy query produces correct dict for various parameter combinations."""
    assert (
        Fuzzy(
            field=field,
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        ).to_dict()
        == expected
    )


@pytest.mark.parametrize(
    "name, value, fuzziness, max_expansions, prefix_length, transpositions, rewrite, attributes, incompatable",
    [
        (
            f"with_{a.name.lower()}",
            "ki",
            "AUTO",
            3,
            0,
            1,
            "constant_score",
            a,
            Fuzzy in INCOMPATIPLE_QUERY and a in INCOMPATIPLE_QUERY[Fuzzy],
        )
        for a in TermAttributes
    ],
)
def test_fuzziness_with(
    name,
    value,
    fuzziness,
    max_expansions,
    prefix_length,
    transpositions,
    rewrite,
    attributes,
    incompatable,
):
    """Test Fuzzy with_<attribute> class methods for all TermAttributes."""
    if incompatable:
        assert not hasattr(Fuzzy, name)
    else:
        assert hasattr(Fuzzy, name)
        t = getattr(Fuzzy, name)(
            value=value,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            transpositions=transpositions,
            rewrite=rewrite,
        )
        assert isinstance(t, Fuzzy)
        assert t.field == attributes.value


@pytest.mark.parametrize(
    "field, query, analyzer, auto_generate_synonyms_phrase_query, fuzziness, fuzzy_transpositions,  fuzzy_rewrite,"
    "lenient, operator, minimum_should_match, zero_terms_query, max_expansions, ,prefix_length, expected",
    [
        (
            "name",
            "test",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"match": {"name": {"query": "test"}}},
        ),
        (
            "name",
            "test",
            "an analyzer",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"match": {"name": {"query": "test", "analyzer": "an analyzer"}}},
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            None,
            None,
            None,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            True,
            None,
            None,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                        "lenient": True,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            True,
            "OR",
            None,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                        "lenient": True,
                        "operator": "OR",
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            True,
            "OR",
            3,
            None,
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                        "lenient": True,
                        "operator": "OR",
                        "minimum_should_match": 3,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            True,
            "OR",
            3,
            "none",
            None,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                        "lenient": True,
                        "operator": "OR",
                        "minimum_should_match": 3,
                        "zero_terms_query": "none",
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            True,
            "OR",
            3,
            "none",
            4,
            None,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                        "lenient": True,
                        "operator": "OR",
                        "minimum_should_match": 3,
                        "zero_terms_query": "none",
                        "max_expansions": 4,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            True,
            "0",
            False,
            "constant_score",
            True,
            "OR",
            3,
            "none",
            4,
            2,
            {
                "match": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "auto_generate_synonyms_phrase_query": True,
                        "fuzziness": "0",
                        "fuzzy_transpositions": False,
                        "fuzzy_rewrite": "constant_score",
                        "lenient": True,
                        "operator": "OR",
                        "minimum_should_match": 3,
                        "zero_terms_query": "none",
                        "max_expansions": 4,
                        "prefix_length": 2,
                    }
                }
            },
        ),
    ],
)
def test_match_to_string(
    field,
    query,
    analyzer,
    auto_generate_synonyms_phrase_query,
    fuzziness,
    fuzzy_transpositions,
    fuzzy_rewrite,
    lenient,
    operator,
    minimum_should_match,
    zero_terms_query,
    max_expansions,
    prefix_length,
    expected,
):
    """Test Match query produces correct dict for various parameter combinations."""
    assert (
        Match(
            field=field,
            query=query,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
        ).to_dict()
        == expected
    )


@pytest.mark.parametrize(
    "parameters, expected",
    [
        (
            {"field": "name", "value": "C_*_SK"},
            {"wildcard": {"name": {"value": "C_*_SK"}}},
        ),
        (
            {"field": "name", "value": "C_*_SK"},
            {"wildcard": {"name": {"value": "C_*_SK"}}},
        ),
        (
            {"field": "name", "value": "C_*_SK", "case_insensitive": True},
            {"wildcard": {"name": {"value": "C_*_SK", "case_insensitive": True}}},
        ),
        (
            {"field": "name", "value": "C_*_SK", "case_insensitive": False},
            {"wildcard": {"name": {"value": "C_*_SK", "case_insensitive": False}}},
        ),
        (
            {"field": "name", "value": "C_*_SK", "boost": 0.9},
            {"wildcard": {"name": {"value": "C_*_SK", "boost": 0.9}}},
        ),
    ],
)
def test_wildcard_to_dict(parameters, expected):
    """Test Wildcard query produces correct dict for various parameter combinations."""
    wildcard = Wildcard(**parameters)
    assert wildcard.to_dict() == expected


@pytest.mark.parametrize(
    "parameters, expected",
    [
        (
            {"field": "name", "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK"},
            {"regexp": {"name": {"value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK"}}},
        ),
        (
            {"field": "name", "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK"},
            {"regexp": {"name": {"value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK"}}},
        ),
        (
            {
                "field": "name",
                "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                "case_insensitive": True,
            },
            {
                "regexp": {
                    "name": {
                        "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                        "case_insensitive": True,
                    }
                }
            },
        ),
        (
            {
                "field": "name",
                "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                "case_insensitive": True,
                "max_determinized_states": 1,
            },
            {
                "regexp": {
                    "name": {
                        "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                        "case_insensitive": True,
                        "max_determinized_states": 1,
                    }
                }
            },
        ),
        (
            {
                "field": "name",
                "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                "case_insensitive": False,
            },
            {
                "regexp": {
                    "name": {
                        "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                        "case_insensitive": False,
                    }
                }
            },
        ),
        (
            {
                "field": "name",
                "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                "boost": 0.9,
            },
            {
                "regexp": {
                    "name": {
                        "value": "C_[A-Za-z0-9_]*ADDR[A-Za-z0-9_]*_SK",
                        "boost": 0.9,
                    }
                }
            },
        ),
    ],
)
def test_regexp_to_dict(parameters, expected):
    """Test Regexp query produces correct dict for various parameter combinations."""
    regexp = Regexp(**parameters)
    assert regexp.to_dict() == expected


@pytest.mark.parametrize(
    "name, message",
    [
        (
            None,
            "name must not be None",
        ),
        (
            " ",
            "name must have at least 1 non-whitespace character",
        ),
    ],
)
def test_with_active_glossary_when_invalid_parameter_raises_value_error(name, message):
    """Test with_active_glossary raises ValueError for invalid name."""
    with pytest.raises(ValueError, match=message):
        with_active_glossary(name)


def test_with_active_glossary():
    """Test with_active_glossary produces correct Bool filter."""
    sut = with_active_glossary(name=GLOSSARY_NAME)

    assert sut.filter
    assert 3 == len(sut.filter)
    term1, term2, term3 = sut.filter
    assert isinstance(term1, Term) is True
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossary"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_NAME


@pytest.mark.parametrize(
    "name, glossary_qualified_name, message",
    [
        (
            None,
            GLOSSARY_QUALIFIED_NAME,
            "name must not be None",
        ),
        (
            " ",
            GLOSSARY_QUALIFIED_NAME,
            "name must have at least 1 non-whitespace character",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            None,
            "glossary_qualified_name must not be None",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            " ",
            "glossary_qualified_name must have at least 1 non-whitespace character",
        ),
    ],
)
def test_with_active_category_when_invalid_parameter_raises_value_error(
    name, glossary_qualified_name, message
):
    """Test with_active_category raises ValueError for invalid parameters."""
    with pytest.raises(ValueError, match=message):
        with_active_category(name=name, glossary_qualified_name=glossary_qualified_name)


def test_with_active_category():
    """Test with_active_category produces correct Bool filter."""
    sut = with_active_category(
        name=GLOSSARY_CATEGORY_NAME, glossary_qualified_name=GLOSSARY_QUALIFIED_NAME
    )

    assert sut.filter
    assert 4 == len(sut.filter)
    term1, term2, term3, term4 = sut.filter
    assert isinstance(term1, Term) is True
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossaryCategory"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_CATEGORY_NAME
    assert isinstance(term4, Term) is True
    assert term4.field == "__glossary"
    assert term4.value == GLOSSARY_QUALIFIED_NAME


@pytest.mark.parametrize(
    "name, glossary_qualified_name, message",
    [
        (
            None,
            GLOSSARY_QUALIFIED_NAME,
            "name must not be None",
        ),
        (
            " ",
            GLOSSARY_QUALIFIED_NAME,
            "name must have at least 1 non-whitespace character",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            "glossary_qualified_name must not be None",
        ),
        (
            GLOSSARY_TERM_NAME,
            " ",
            "glossary_qualified_name must have at least 1 non-whitespace character",
        ),
    ],
)
def test_with_active_term_when_invalid_parameter_raises_value_error(
    name, glossary_qualified_name, message
):
    """Test with_active_term raises ValueError for invalid parameters."""
    with pytest.raises(ValueError, match=message):
        with_active_term(name=name, glossary_qualified_name=glossary_qualified_name)


def test_with_active_term():
    """Test with_active_term produces correct Bool filter."""
    sut = with_active_term(
        name=GLOSSARY_TERM_NAME, glossary_qualified_name=GLOSSARY_QUALIFIED_NAME
    )

    assert sut.filter
    assert 4 == len(sut.filter)
    term1, term2, term3, term4 = sut.filter
    assert isinstance(term1, Term) is True
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossaryTerm"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_TERM_NAME
    assert isinstance(term4, Term) is True
    assert term4.field == "__glossary"
    assert term4.value == GLOSSARY_QUALIFIED_NAME


def test_dsl_serialization_and_deserialization():
    """Test DSL serialization and deserialization produce consistent output."""
    dsl_through_model = DSL(
        from_=0,
        aggregations={
            "main_agg": {
                "terms": {"field": "main_field"},
                "aggregations": {
                    "sub_agg_1": {"avg": {"field": "sub_field_1"}},
                    "sub_agg_2": {
                        "date_histogram": {"field": "timestamp", "interval": "month"}
                    },
                },
            }
        },
        size=500,
        sort=[
            SortItem(field="created", order=SortOrder.ASCENDING),
            SortItem(field="updated", order=SortOrder.DESCENDING),
            SortItem(
                field="entityId", order=SortOrder.ASCENDING, nested_path="nested_test"
            ),
        ],
        query=Bool(
            must=[
                Term(field="type.keyword", value="Schema"),
                Range(field="created", gte="2025-01-01"),
                Term(field="status", value="active"),
            ],
            should=[Term(field="category.keyword", value="Tech")],
            must_not=[Term(field="archived", value="true")],
            filter=[
                Bool(
                    must=[
                        Term(field="region.keyword", value="EMEA"),
                        Range(field="created", lte="2025-12-31"),
                    ],
                    should=[Term(field="sub_category.keyword", value="Hardware")],
                )
            ],
        ),
        track_total_hits=False,
    )

    raw_dsl_data = {
        "from_": 0,
        "aggregations": {
            "main_agg": {
                "terms": {"field": "main_field"},
                "aggregations": {
                    "sub_agg_1": {"avg": {"field": "sub_field_1"}},
                    "sub_agg_2": {
                        "date_histogram": {"field": "timestamp", "interval": "month"}
                    },
                },
            }
        },
        "size": 500,
        "sort": [
            {"created": {"order": "asc"}},
            {"updated": {"order": "desc"}},
            {"entityId": {"order": "asc", "nested": {"path": "nested_test"}}},
        ],
        "query": {
            "bool": {
                "must": [
                    {"term": {"type.keyword": {"value": "Schema"}}},
                    {"range": {"created": {"gte": "2025-01-01"}}},
                    {"term": {"status": {"value": "active"}}},
                ],
                "should": [{"term": {"category.keyword": {"value": "Tech"}}}],
                "must_not": [{"term": {"archived": {"value": "true"}}}],
                "filter": [
                    {
                        "bool": {
                            "must": [
                                {"term": {"region.keyword": {"value": "EMEA"}}},
                                {"range": {"created": {"lte": "2025-12-31"}}},
                            ],
                            "should": [
                                {
                                    "term": {
                                        "sub_category.keyword": {"value": "Hardware"}
                                    }
                                }
                            ],
                        }
                    }
                ],
            }
        },
        "track_total_hits": False,
    }
    dsl_through_raw = DSL(**raw_dsl_data)

    assert dsl_through_raw.json(
        exclude_unset=True, by_alias=True
    ) == dsl_through_model.json(exclude_unset=True, by_alias=True)

    assert dsl_through_raw.json() == dsl_through_model.json()


@pytest.mark.parametrize(
    "field, query, analyzer, slop, zero_terms_query, boost, expected",
    [
        (
            "name",
            "test",
            None,
            None,
            None,
            None,
            {"match_phrase": {"name": {"query": "test"}}},
        ),
        (
            "name",
            "test",
            "an analyzer",
            None,
            None,
            None,
            {"match_phrase": {"name": {"query": "test", "analyzer": "an analyzer"}}},
        ),
        (
            "name",
            "test",
            "an analyzer",
            2,
            None,
            None,
            {
                "match_phrase": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "slop": 2,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            "an analyzer",
            2,
            "none",
            1.0,
            {
                "match_phrase": {
                    "name": {
                        "query": "test",
                        "analyzer": "an analyzer",
                        "slop": 2,
                        "zero_terms_query": "none",
                        "boost": 1.0,
                    }
                }
            },
        ),
        (
            "name",
            "test",
            None,
            0,
            "all",
            2.0,
            {
                "match_phrase": {
                    "name": {
                        "query": "test",
                        "slop": 0,
                        "zero_terms_query": "all",
                        "boost": 2.0,
                    }
                }
            },
        ),
        (
            "description",
            "another test",
            "standard",
            1,
            "none",
            None,
            {
                "match_phrase": {
                    "description": {
                        "query": "another test",
                        "analyzer": "standard",
                        "slop": 1,
                        "zero_terms_query": "none",
                    }
                }
            },
        ),
    ],
)
def test_match_phrase_to_dict(
    field,
    query,
    analyzer,
    slop,
    zero_terms_query,
    boost,
    expected,
):
    """Test MatchPhrase query produces correct dict for various parameter combinations."""
    assert (
        MatchPhrase(
            field=field,
            query=query,
            analyzer=analyzer,
            slop=slop,
            zero_terms_query=zero_terms_query,
            boost=boost,
        ).to_dict()
        == expected
    )


@pytest.mark.skip(reason="FluentSearch not yet migrated to v9")
def test_match_phrase_textfield():
    """Test MatchPhrase integration with FluentSearch text field methods.

    NOTE: Skipped because FluentSearch is not yet migrated to pyatlan_v9.
    """
    pass
