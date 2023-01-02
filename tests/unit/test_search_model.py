import pytest

from pyatlan.model.search import (
    DSL,
    Bool,
    IndexSearchRequest,
    MatchAll,
    MatchNone,
    Term,
)


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


def test_dsl():
    dsl = DSL(
        query=Term(field="__typeName.keyword", value="Schema"),
        post_filter=Term(field="databaseName.keyword", value="ATLAN_SAMPLE_DATA"),
    )
    assert (
        dsl.json(by_alias=True)
        == '{"from": 0, "size": 100, "post_filter": {"term": {"databaseName.keyword": '
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
        request.json(by_alias=True)
        == '{"dsl": {"from": 0, "size": 100, "post_filter": {"term": {"databaseName.keyword": '
        '{"value": "ATLAN_SAMPLE_DATA"}}}, "query": {"term": {"__typeName.keyword": {"value": "Schema"}}}}, '
        '"attributes": ["schemaName", "databaseName"]}'
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
