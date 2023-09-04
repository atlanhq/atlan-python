# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import patch

import pytest

from pyatlan.utils import (
    list_attributes_to_params,
    unflatten_custom_metadata,
    unflatten_custom_metadata_for_entity,
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
