# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import patch

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.utils import (
    ComparisonCategory,
    get_base_type,
    is_comparable_type,
    list_attributes_to_params,
    unflatten_custom_metadata,
    unflatten_custom_metadata_for_entity,
    validate_type,
)


def test_list_attributes_to_params_with_no_query_parms():
    assert list_attributes_to_params([{"first": "Dave"}]) == {"attr_0:first": "Dave"}


def test_list_attributes_to_params_with_query_parms():
    assert list_attributes_to_params([{"first": "Dave"}], {"last": "Jo"}) == {
        "attr_0:first": "Dave",
        "last": "Jo",
    }


@pytest.mark.parametrize(
    "attributes, flattened_attributes, custom_metadata",
    [
        (None, None, None),
        (
            None,
            {
                "qualifiedName": "default/glue/1688357913/AwsDataCatalog/development_published_impact/holding_rating"
            },
            None,
        ),
        (["ihnLo19fqaT4x9pU8JKWbQ.Cyw6GbqST9M1dhXIBE1yHp"], None, None),
        (
            [
                "ihnLo19fqaT4x9pU8JKWbQ.Cyw6GbqST9M1dhXIBE1yHp",
                "ihnLo19fqaT4x9pU8JKWbQ.mdplQ3q9dk0T11vo817wyJ",
                "ihnLo19fqaT4x9pU8JKWbQ.Xb3awoTsZGPu6vqnNxrzYF",
                "mwkVZhWne8ApD5t1BetxLd.IBTIot8BAicd74XmnPGytU",
            ],
            {
                "ihnLo19fqaT4x9pU8JKWbQ.Cyw6GbqST9M1dhXIBE1yHp": 1688137200000,
                "ihnLo19fqaT4x9pU8JKWbQ.mdplQ3q9dk0T11vo817wyJ": 1685890800000,
                "mwkVZhWne8ApD5t1BetxLd.IBTIot8BAicd74XmnPGytU": 12,
                "qualifiedName": "default/glue/1688357913/AwsDataCatalog/development_published_impact/holding_rating",
                "name": "holding_rating",
            },
            {
                "mwkVZhWne8ApD5t1BetxLd": {"IBTIot8BAicd74XmnPGytU": 12},
                "ihnLo19fqaT4x9pU8JKWbQ": {
                    "Cyw6GbqST9M1dhXIBE1yHp": 1688137200000,
                    "mdplQ3q9dk0T11vo817wyJ": 1685890800000,
                },
            },
        ),
        (
            [
                "ihnLo19fqaT4x9pU8JKWbQ.Cyw6GbqST9M1dhXIBE1yHp",
                "ihnLo19fqaT4x9pU8JKWbQ.mdplQ3q9dk0T11vo817wyJ",
                "ihnLo19fqaT4x9pU8JKWbQ.Xb3awoTsZGPu6vqnNxrzYF",
                "mwkVZhWne8ApD5t1BetxLd.IBTIot8BAicd74XmnPGytU",
            ],
            {
                "qualifiedName": "default/glue/1688357913/AwsDataCatalog/development_published_impact/holding_rating",
                "name": "holding_rating",
            },
            {},
        ),
    ],
)
def test_unflatten_custom_metadata(attributes, flattened_attributes, custom_metadata):
    assert custom_metadata == unflatten_custom_metadata(
        attributes=attributes, asset_attributes=flattened_attributes
    )


@patch("pyatlan.utils.unflatten_custom_metadata")
def test_unflatten_custom_metadata_for_entity(mock_unflatten_custom_metadata):
    custom_metadata = {"mwkVZhWne8ApD5t1BetxLd": {"IBTIot8BAicd74XmnPGytU": 12}}
    mock_unflatten_custom_metadata.return_value = custom_metadata
    entity = {"attributes": {"name": "dave"}}
    attributes = ["name"]

    unflatten_custom_metadata_for_entity(entity=entity, attributes=attributes)

    assert "businessAttributes" in entity
    assert entity["businessAttributes"] == custom_metadata
    assert mock_unflatten_custom_metadata.callled_once_with(
        attributes=attributes, asset_attributes=entity["attributes"]
    )


@patch("pyatlan.utils.unflatten_custom_metadata")
def test_unflatten_custom_metadata_for_entity_when_empty_dict_returned_does_not_modify(
    mock_unflatten_custom_metadata,
):
    mock_unflatten_custom_metadata.return_value = {}
    entity = {"attributes": {"name": "dave"}}
    attributes = ["name"]

    unflatten_custom_metadata_for_entity(entity=entity, attributes=attributes)

    assert "businessAttributes" not in entity
    assert mock_unflatten_custom_metadata.callled_once_with(
        attributes=attributes, asset_attributes=entity["attributes"]
    )


@pytest.mark.parametrize("entity", [({"attributes": {"name": "dave"}}), ({})])
@patch("pyatlan.utils.unflatten_custom_metadata")
def test_unflatten_custom_metadata_for_entity_when_none_returned_does_not_modify(
    mock_unflatten_custom_metadata, entity
):
    mock_unflatten_custom_metadata.return_value = None
    attributes = ["name"]

    unflatten_custom_metadata_for_entity(entity=entity, attributes=attributes)

    assert "businessAttributes" not in entity
    assert mock_unflatten_custom_metadata.callled_once_with(
        attributes=attributes, asset_attrubtes=entity.get("attributes", None)
    )


@pytest.mark.parametrize(
    "value, result",
    [
        ("string", "string"),
        ("array<string>", "string"),
        ("array<map<string>>", "string"),
        ("map<string>", "string"),
    ],
)
def test_get_base_type(value, result):
    assert get_base_type(value) == result


@pytest.mark.parametrize(
    "attribute_type",
    [
        "boolean",
        "array<boolean>",
        "array<map<boolean>>",
        "map<boolean>",
    ],
)
@pytest.mark.parametrize(
    "to, expected",
    [
        (ComparisonCategory.BOOLEAN, True),
        (ComparisonCategory.STRING, False),
        (ComparisonCategory.NUMBER, False),
    ],
)
def test_is_comparable_type_b(attribute_type, to, expected):
    assert is_comparable_type(attribute_type=attribute_type, to=to) == expected


@pytest.mark.parametrize(
    "attribute_type",
    [
        "string",
        "array<string>",
        "array<map<string>>",
        "map<string>",
    ],
)
@pytest.mark.parametrize(
    "to, expected",
    [
        (ComparisonCategory.STRING, True),
        (ComparisonCategory.BOOLEAN, False),
        (ComparisonCategory.NUMBER, False),
    ],
)
def test_is_comparable_type_s(attribute_type, to, expected):
    assert is_comparable_type(attribute_type=attribute_type, to=to) == expected


@pytest.mark.parametrize(
    "attribute_type",
    [
        attribute_type
        for inner_type in ["int", "long", "date", "float"]
        for attribute_type in [f"{inner_type}", f"array<{inner_type}>"]
    ],
)
@pytest.mark.parametrize(
    "to, expected",
    [
        (ComparisonCategory.NUMBER, True),
        (ComparisonCategory.BOOLEAN, False),
        (ComparisonCategory.STRING, False),
    ],
)
def test_is_comparable_type_n(attribute_type, to, expected):
    assert is_comparable_type(attribute_type=attribute_type, to=to) == expected


@pytest.mark.parametrize(
    "name, the_type, value, message",
    [
        (
            "bob",
            int,
            "a",
            "ATLAN-PYTHON-400-048 Invalid parameter type for bob should be int",
        ),
        (
            "bob",
            int,
            False,
            "ATLAN-PYTHON-400-048 Invalid parameter type for bob should be int",
        ),
        (
            "bob",
            int,
            None,
            "ATLAN-PYTHON-400-048 Invalid parameter type for bob should be int",
        ),
        (
            "bob",
            bool,
            None,
            "ATLAN-PYTHON-400-048 Invalid parameter type for bob should be bool",
        ),
        (
            "bob",
            bool,
            1,
            "ATLAN-PYTHON-400-048 Invalid parameter type for bob should be bool",
        ),
        (
            "bob",
            bool,
            "True",
            "ATLAN-PYTHON-400-048 Invalid parameter type for bob should be bool",
        ),
    ],
)
def test_validate_type_with_invalid_values(name, the_type, value, message):
    with pytest.raises(InvalidRequestError, match=message):
        validate_type(name=name, _type=the_type, value=value)


@pytest.mark.parametrize(
    "name, the_type, value",
    [
        ("bob", int, 1),
        ("bob", str, "abc"),
        ("bob", bool, False),
        ("bob", object, {}),
    ],
)
def test_validate_type_with_valid_values(name, the_type, value):
    validate_type(name=name, _type=the_type, value=value)
