from json import dumps
from typing import Union

import pytest

from pyatlan.errors import InvalidRequestError
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
        assert contract.data_contract_json == dumps(DATA_CONTRACT_JSON)


@pytest.mark.parametrize(
    "asset_qualified_name, contract_json, message",
    [
        (None, "json", "asset_qualified_name is required"),
        ("qn", None, "contract_json is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    asset_qualified_name: str, contract_json: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataContract.creator(
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
        )


@pytest.mark.parametrize(
    "asset_qualified_name, contract_json, error_msg",
    [
        (
            "asset-qn",
            "some-invalid-json",
            "ATLAN-PYTHON-400-062 Provided data contract JSON is invalid.",
        ),
        (
            "asset-qn",
            '{"kind":"DataContract", "description":"Missing dataset property"}',
            "ATLAN-PYTHON-400-062 Provided data contract JSON is invalid.",
        ),
    ],
)
def test_creator_with_invalid_contract_json_raises_error(
    asset_qualified_name: str, contract_json: str, error_msg: str
):
    with pytest.raises(InvalidRequestError, match=error_msg):
        DataContract.creator(
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
        )


def test_creator_atttributes_with_required_parameters():
    attributes = DataContract.Attributes.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(attributes)


def test_creator_with_required_parameters():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=dumps(DATA_CONTRACT_JSON),
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
