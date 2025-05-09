# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import patch

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanConnectionCategory, AtlanConnectorType
from pyatlan.model.utils import construct_object_key
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


@pytest.mark.parametrize(
    "prefix, name, expected_key",
    [
        ("", "file.txt", "file.txt"),
        ("folder", "file.txt", "folder/file.txt"),
        ("folder/", "//file.txt", "folder/file.txt"),
        ("folder/", "/////file.txt//", "folder/file.txt"),
        ("/folder/", "file.txt", "/folder/file.txt"),
        ("folder/subfolder", "file.txt", "folder/subfolder/file.txt"),
        ("folder/subfolder/", "file.txt", "folder/subfolder/file.txt"),
        ("/", "file.txt", "/file.txt"),
        ("/", "file.txt/", "/file.txt"),
        # Additional edge cases
        ("//tmp/iicer-miner/", "file.txt", "//tmp/iicer-miner/file.txt"),
        ("//logs/", "output.log", "//logs/output.log"),
        ("test-bucket//", "file.txt", "test-bucket//file.txt"),
        ("//", "file.txt", "//file.txt"),
        ("//", "/file.txt", "//file.txt"),
        ("/tmp/", "/data/file.txt", "/tmp/data/file.txt"),
        ("/data//", "nested/file.txt", "/data//nested/file.txt"),
        ("///deep/path/", "/to/file.txt", "///deep/path/to/file.txt"),
        ("/tmp/iics-miner/input/", "file.txt", "/tmp/iics-miner/input/file.txt"),
    ],
)
def test_contruct_object_key(prefix, name, expected_key):
    key = construct_object_key(prefix, name)
    assert key == expected_key


@pytest.mark.parametrize(
    "custom_connectors",
    [
        [
            AtlanConnectorType.CREATE_CUSTOM(
                name="FOO", value="foo", category=AtlanConnectionCategory.BI
            ),
            AtlanConnectorType.CREATE_CUSTOM(
                name="BAR", value="bar", category=AtlanConnectionCategory.API
            ),
            AtlanConnectorType.CREATE_CUSTOM(
                name="BAZ", value="baz", category=AtlanConnectionCategory.WAREHOUSE
            ),
        ]
    ],
)
def test_atlan_connector_type_create_custom(custom_connectors):
    for custom_connector in custom_connectors:
        assert custom_connector and custom_connector.category
        assert custom_connector.value in AtlanConnectorType.get_values()
        assert custom_connector.strip() in AtlanConnectorType.get_values()
        assert custom_connector.name in AtlanConnectorType.get_names()
        assert (
            custom_connector.name,
            custom_connector.value,
        ) in AtlanConnectorType.get_items()


@pytest.mark.parametrize(
    "custom_asset_qns",
    [
        [
            "default/c1/1234567890/asset/name",
            "default/c2/1234567890/asset/name",
            "default/c3/1234567890/asset/name",
            # Duplicate custom connector names
            "default/c1/1234567890/asset/name",
            "default/c2/1234567890/asset/name",
            "default/c3/1234567890/asset/name",
            # Duplicate custom connector names
            "default/c1/1234567890/asset/name",
            "default/c2/1234567890/asset/name",
            "default/c3/1234567890/asset/name",
        ]
    ],
)
def test_atlan_connector_type_custom_asset_qn(custom_asset_qns):
    # Calculate the unique custom QNs
    unique_custom_qns = set(custom_asset_qns)

    # Calculate the initial lengths of predefined values, names, and items
    len_get_values = len(AtlanConnectorType.get_values())
    len_get_names = len(AtlanConnectorType.get_names())
    len_get_items = len(AtlanConnectorType.get_items())

    # Check each custom QN
    for custom_qn in custom_asset_qns:
        custom_connector = AtlanConnectorType._get_connector_type_from_qualified_name(
            custom_qn
        )
        custom_connector.category = AtlanConnectionCategory.CUSTOM
        assert custom_connector.value in AtlanConnectorType.get_values()
        assert custom_connector.strip() in AtlanConnectorType.get_values()
        assert (
            custom_connector.name,
            custom_connector.value,
        ) in AtlanConnectorType.get_items()

    # Ensure the value is only added once (i.e no duplicates)
    assert len(AtlanConnectorType.get_values()) == len_get_values + len(
        unique_custom_qns
    )
    assert len(AtlanConnectorType.get_names()) == len_get_names + len(unique_custom_qns)
    assert len(AtlanConnectorType.get_items()) == len_get_items + len(unique_custom_qns)


@pytest.mark.parametrize(
    "custom_connection_qns",
    [
        [
            "default/cm1/1234567890",
            "default/cm2/1234567890",
            "default/cm3/1234567890",
            # Duplicate custom connector names
            "default/cm1/1234567890",
            "default/cm2/1234567890",
            "default/cm3/1234567890",
            # Duplicate custom connector names
            "default/cm1/1234567890",
            "default/cm2/1234567890",
            "default/cm3/1234567890",
        ]
    ],
)
def test_atlan_connector_type_custom_connection_qn(custom_connection_qns):
    # Calculate the unique custom QNs
    unique_custom_qns = set(custom_connection_qns)

    # Calculate the initial lengths of predefined values, names, and items
    len_get_values = len(AtlanConnectorType.get_values())
    len_get_names = len(AtlanConnectorType.get_names())
    len_get_items = len(AtlanConnectorType.get_items())

    # Check each custom QN
    for custom_qn in custom_connection_qns:
        custom_connector_name = AtlanConnectorType.get_connector_name(custom_qn)
        assert custom_connector_name in AtlanConnectorType.get_values()
        assert custom_connector_name.strip() in AtlanConnectorType.get_values()

    # Ensure the value is only added once (i.e no duplicates)
    assert len(AtlanConnectorType.get_values()) == len_get_values + len(
        unique_custom_qns
    )
    assert len(AtlanConnectorType.get_names()) == len_get_names + len(unique_custom_qns)
    assert len(AtlanConnectorType.get_items()) == len_get_items + len(unique_custom_qns)
