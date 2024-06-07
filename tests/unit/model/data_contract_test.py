from typing import Union

import pytest

from pyatlan.model.assets import DataContract
from tests.unit.model.constants import (
    ASSET_QUALIFIED_NAME,
    DATA_CONTRACT_JSON,
    DATA_CONTRACT_NAME,
    DATA_CONTRACT_QUALIFIED_NAME,
)


def _assert_contract(
    contract: Union[DataContract, DataContract.Attributes], assert_json: bool = True
) -> None:
    assert contract.name == DATA_CONTRACT_NAME
    assert contract.qualified_name == DATA_CONTRACT_QUALIFIED_NAME
    if assert_json:
        assert contract.data_contract_json == str(DATA_CONTRACT_JSON)


@pytest.mark.parametrize(
    "name, asset_qualified_name, contract_json, message",
    [
        (None, "qn", "json", "name is required"),
        ("name", None, "json", "asset_qualified_name is required"),
        ("name", "qn", None, "contract_json is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, asset_qualified_name: str, contract_json: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataContract.creator(
            name=name,
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
        )


def test_creator_atttributes_with_required_parameters():
    attributes = DataContract.Attributes.creator(
        name=DATA_CONTRACT_NAME,
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=str(DATA_CONTRACT_JSON),
    )
    _assert_contract(attributes)


def test_creator_with_required_parameters():
    test_contract = DataContract.creator(
        name=DATA_CONTRACT_NAME,
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=str(DATA_CONTRACT_JSON),
    )
    _assert_contract(test_contract)


def test_create_for_modification():
    test_contract = DataContract.create_for_modification(
        name=DATA_CONTRACT_NAME,
        qualified_name=DATA_CONTRACT_QUALIFIED_NAME,
    )
    _assert_contract(test_contract, False)


def test_trim_to_required():
    test_contract = DataContract.create_for_modification(
        name=DATA_CONTRACT_NAME,
        qualified_name=DATA_CONTRACT_QUALIFIED_NAME,
    ).trim_to_required()
    _assert_contract(test_contract, False)
