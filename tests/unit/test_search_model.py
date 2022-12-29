import pytest

from pyatlan.model.search import Bool, Term


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
