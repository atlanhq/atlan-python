# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from datetime import datetime
from typing import Literal, Union

import pytest
from pydantic import StrictBool, StrictStr, ValidationError

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.search import (
    DSL,
    Bool,
    Exists,
    Fuzzy,
    IndexSearchRequest,
    Match,
    MatchAll,
    MatchNone,
    Prefix,
    Range,
    Regexp,
    SortItem,
    SortOrder,
    Term,
    TermAttributes,
    Terms,
    Wildcard,
)

NOW = datetime.now()
VALUES_BY_TYPE: dict[Union[type, object], Union[str, datetime, object]] = {
    StrictStr: "abc",
    StrictBool: True,
    datetime: NOW,
    Literal["ACTIVE", "DELETED"]: "ACTIVE",
    float: 1.0,
    AtlanConnectorType: AtlanConnectorType.SNOWFLAKE,
}

INCOMPATIPLE_QUERY: dict[type, set[TermAttributes]] = {
    Wildcard: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
    },
    Regexp: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
    },
    Fuzzy: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
    },
    Prefix: {
        TermAttributes.CONNECTOR_NAME,
        TermAttributes.HAS_LINEAGE,
        TermAttributes.UPDATE_TIME_AS_TIMESTAMP,
        TermAttributes.CREATE_TIME_AS_TIMESTAMP,
        TermAttributes.POPULARITY_SCORE,
    },
    Term: {
        TermAttributes.POPULARITY_SCORE,
    },
}


@pytest.mark.parametrize(
    "parameters, expected",
    [
        ({}, "__init__() missing 2 required positional arguments: 'field' and 'value'"),
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
    with pytest.raises(TypeError) as exc_info:
        Term(**parameters)
    assert exc_info.value.args[0] == expected


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
    with pytest.raises(ValidationError):
        DSL()


def test_dsl():
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    assert (
        dsl.json(by_alias=True, exclude_none=True)
        == '{"from": 0, "size": 100, "track_total_hits": true, "post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": '
        '{"__typeName.keyword": {"value": "Schema"}}}}'
    )


def test_index_search_request():
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    request = IndexSearchRequest(dsl=dsl, attributes=["schemaName", "databaseName"])
    assert (
        request.json(by_alias=True, exclude_none=True)
        == '{"dsl": {"from": 0, "size": 100, "track_total_hits": true, '
        '"post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": {"__typeName.keyword": {"value": "Schema"}}}}, '
        '"attributes": ["schemaName", "databaseName"], "relationAttributes": []}'
    )


def test_adding_terms_results_in_must_bool():
    term_1 = Term(field="name", value="Bob")
    term_2 = Term(field="name", value="Dave")
    result = term_1 + term_2
    assert isinstance(result, Bool)
    assert len(result.must) == 2
    assert term_1 in result.must and term_2 in result.must


def test_anding_terms_results_in_must_bool():
    term_1 = Term(field="name", value="Bob")
    term_2 = Term(field="name", value="Dave")
    result = term_1 & term_2
    assert isinstance(result, Bool)
    assert len(result.must) == 2
    assert term_1 in result.must and term_2 in result.must


def test_oring_terms_results_in_must_bool():
    term_1 = Term(field="name", value="Bob")
    term_2 = Term(field="name", value="Dave")
    result = term_1 | term_2
    assert isinstance(result, Bool)
    assert len(result.should) == 2
    assert term_1 in result.should and term_2 in result.should


def test_negate_terms_results_must_not_bool():
    term_1 = Term(field="name", value="Bob")
    result = ~term_1
    assert isinstance(result, Bool)
    assert len(result.must_not) == 1
    assert term_1 in result.must_not


@pytest.mark.parametrize(
    "q1, q2, expected",
    [
        (
            Bool(must=[Term(field="name", value="Bob")]),
            Bool(must=[Term(field="name", value="Dave")]),
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
            Term(field="name", value="Bob"),
            Bool(must=[Term(field="name", value="Fred")]),
            {
                "bool": {
                    "must": [
                        {"term": {"name": {"value": "Fred"}}},
                        {"term": {"name": {"value": "Bob"}}},
                    ]
                }
            },
        ),
        (
            Bool(must=[Term(field="name", value="Fred")]),
            Term(field="name", value="Bob"),
            {
                "bool": {
                    "must": [
                        {"term": {"name": {"value": "Fred"}}},
                        {"term": {"name": {"value": "Bob"}}},
                    ]
                }
            },
        ),
    ],
)
def test_add_boolean(q1, q2, expected):
    b = q1 + q2
    assert b.to_dict() == expected


def test_match_none_to_dict():
    assert MatchNone().to_dict() == {"match_none": {}}


def test_match_none_plus_other_is_match_none():
    assert MatchNone() + Term(field="name", value="bob") == MatchNone()


def test_match_one_or_other_is_other():
    assert MatchNone() | Term(field="name", value="bob") == Term(
        field="name", value="bob"
    )


def test_nagate_match_one_is_match_all():
    assert ~MatchNone() == MatchAll()


@pytest.mark.parametrize(
    "boost, expected", [(None, {"match_all": {}}), (1.2, {"match_all": {"boost": 1.2}})]
)
def test_match_all_to_dict(boost, expected):
    assert MatchAll(boost=boost).to_dict() == expected


def test_match_all_and_other_is_other():
    assert MatchAll() & Term(field="name", value="bob") == Term(
        field="name", value="bob"
    )


def test_match_all_or_other_is_match_all():
    assert MatchAll() | Term(field="name", value="bob") == MatchAll()


def test_negate_match_all_is_match_none():
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
    b = q1 | q2
    assert b.to_dict() == expected


def test_negate_empty_bool_is_match_none():
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
    b = q1 & q2
    assert b.to_dict() == expected


@pytest.fixture()
def with_name(request):
    attribute = request.param
    return "with_" + attribute.name.lower()


def test_terms_to_dict():
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
    if incompatable:
        assert not hasattr(a_class, with_name)
    else:
        assert hasattr(a_class, with_name)
        t = getattr(a_class, with_name)(value)
        assert isinstance(t, a_class)
        assert t.field == field
        assert t.value == value


@pytest.mark.parametrize(
    "with_name,  field", [(a, a.value) for a in TermAttributes], indirect=["with_name"]
)
def test_by_methods_on_exists(with_name, field):
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
    ],
)
def test_range_to_dict(gt, gte, lt, lte, boost, format, relation, timezone, expected):
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
            "with_" + a.name.lower(),
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
