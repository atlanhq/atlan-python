import pytest

from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Term


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


def test_bool_without_parameters_reaises_value_error():
    with pytest.raises(ValueError) as exc_info:
        Bool()
    assert (
        exc_info.value.args[0][0].exc.args[0]
        == "At least one of must, should, must_not or filter is required"
    )


@pytest.mark.parametrize(
    "terms",
    [
        (Term(field="name", value="Bob")),
        ([Term(field="name", value="Bob"), Term(field="name", value="Dave")]),
    ],
)
def test_bool_to_dict(terms):
    b = Bool(must=terms)
    assert b.to_dict() == {
        "bool": {
            "must": [t.to_dict() for t in terms]
            if isinstance(terms, list)
            else terms.to_dict()
        }
    }


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
