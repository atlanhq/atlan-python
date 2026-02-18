# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataContract model in pyatlan_v9."""

from json import dumps
from typing import Union

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan_v9.model import DataContract
from pyatlan_v9.model.contract import DataContractSpec
from tests_v9.unit.model.constants import (
    ASSET_QUALIFIED_NAME,
    DATA_CONTRACT_JSON,
    DATA_CONTRACT_NAME,
    DATA_CONTRACT_NAME_DEFAULT,
    DATA_CONTRACT_QUALIFIED_NAME,
    DATA_CONTRACT_SPEC_STR,
    DATA_CONTRACT_SPEC_STR_WITHOUT_DATASET,
)


def _assert_contract(
    contract: Union[DataContract, DataContract.Attributes],
    is_json: bool = False,
    contract_name: str = DATA_CONTRACT_NAME,
) -> None:
    assert contract.name == contract_name
    assert contract.qualified_name == DATA_CONTRACT_QUALIFIED_NAME
    if is_json:
        assert contract.data_contract_json == dumps(DATA_CONTRACT_JSON)


@pytest.mark.parametrize(
    "asset_qualified_name, contract_json, contract_spec, message",
    [
        (None, "json", "spec", "asset_qualified_name is required"),
        ("qn", "json", "spec", "Both `contract_json` and `contract_spec` cannot be"),
        ("qn", None, None, "At least one of `contract_json` or `contract_spec`"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    asset_qualified_name: str, contract_json: str, contract_spec: str, message: str
):
    """Test creator raises ValueError for invalid input combinations."""
    with pytest.raises(ValueError, match=message):
        DataContract.creator(  # type: ignore[arg-type]
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
            contract_spec=contract_spec,
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
    """Test creator raises InvalidRequestError for invalid contract JSON payloads."""
    with pytest.raises(InvalidRequestError, match=error_msg):
        DataContract.creator(
            asset_qualified_name=asset_qualified_name,
            contract_json=contract_json,
        )


def test_creator_attributes_with_required_parameters():
    """Test DataContract.Attributes.creator for JSON payload."""
    attributes = DataContract.Attributes.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(attributes, is_json=True)


def test_creator_with_required_parameters_json():
    """Test DataContract.creator for JSON payload."""
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str():
    """Test DataContract.creator for YAML string payload."""
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_spec=DATA_CONTRACT_SPEC_STR,
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str_without_dataset():
    """Test creator defaults contract name from asset QN when dataset is absent."""
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_spec=DATA_CONTRACT_SPEC_STR_WITHOUT_DATASET,
    )
    _assert_contract(test_contract, contract_name=DATA_CONTRACT_NAME_DEFAULT)


def test_creator_with_required_parameters_spec_model():
    """Test DataContract.creator for DataContractSpec model payload."""
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_spec=spec,
    )
    _assert_contract(test_contract)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATA_CONTRACT_NAME, "qualified_name is required"),
        (DATA_CONTRACT_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_missing_parameters_raise_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DataContract.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates update-ready DataContract."""
    test_contract = DataContract.updater(
        name=DATA_CONTRACT_NAME,
        qualified_name=DATA_CONTRACT_QUALIFIED_NAME,
    )
    _assert_contract(test_contract, False)


def test_trim_to_required():
    """Test trim_to_required preserves only required update fields."""
    test_contract = DataContract.updater(
        name=DATA_CONTRACT_NAME,
        qualified_name=DATA_CONTRACT_QUALIFIED_NAME,
    ).trim_to_required()
    _assert_contract(test_contract, False)
