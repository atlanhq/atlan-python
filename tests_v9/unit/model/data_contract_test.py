# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataContract model in pyatlan_v9."""

from json import dumps
from typing import Union
from unittest.mock import MagicMock

import pytest

from pyatlan_v9.errors import InvalidRequestError
from pyatlan_v9.model import DataContract, Table
from pyatlan_v9.model.contract import DataContractSpec
from pyatlan_v9.model.response import AssetMutationResponse
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
            asset_type=Table,
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
            asset_type=Table,
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
        asset_type=Table,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str():
    """Test DataContract.creator for YAML string payload."""
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_spec=DATA_CONTRACT_SPEC_STR,
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str_without_dataset():
    """Test creator defaults contract name from asset QN when dataset is absent."""
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_spec=DATA_CONTRACT_SPEC_STR_WITHOUT_DATASET,
    )
    _assert_contract(test_contract, contract_name=DATA_CONTRACT_NAME_DEFAULT)


def test_creator_with_required_parameters_spec_model():
    """Test DataContract.creator for DataContractSpec model payload."""
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_spec=spec,
    )
    _assert_contract(test_contract)


def test_creator_sets_data_contract_asset_latest():
    """Creator should set data_contract_asset_latest with the correct asset ref."""
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    ref = test_contract.data_contract_asset_latest
    assert ref is not None
    assert ref.type_name == "Table"
    assert ref.unique_attributes == {"qualifiedName": ASSET_QUALIFIED_NAME}


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


class TestSaveContract:
    def test_save_delegates_to_asset_client(self):
        """save() should delegate to client.asset.save()."""
        mock_client = MagicMock()
        contract = DataContract.creator(
            asset_qualified_name=ASSET_QUALIFIED_NAME,
            asset_type=Table,
            contract_json=dumps(DATA_CONTRACT_JSON),
        )
        expected_response = MagicMock(spec=AssetMutationResponse)
        mock_client.asset.save.return_value = expected_response

        result = DataContract.save(client=mock_client, contract=contract)

        assert result == expected_response
        mock_client.asset.save.assert_called_once_with(contract)


class TestDeleteContract:
    def test_delete_retrieves_contract_and_clears_linked_asset(self):
        """delete() should retrieve the contract, find the linked asset, clear state, and purge."""
        mock_client = MagicMock()

        # Mock the contract retrieved by get_by_guid
        mock_linked_asset = MagicMock()
        mock_linked_asset.type_name = "Table"
        mock_linked_asset.guid = "asset-guid-456"
        mock_linked_asset.qualified_name = "default/test/table-qn"
        mock_linked_asset.name = "test-table"
        mock_contract = MagicMock(spec=DataContract)
        mock_contract.data_contract_asset_latest = mock_linked_asset
        mock_client.asset.get_by_guid.return_value = mock_contract

        delete_response = MagicMock(spec=AssetMutationResponse)
        mock_client.asset.purge_by_guid.return_value = delete_response
        mock_client._call_api.return_value = {"mutatedEntities": {}}

        result = DataContract.delete(
            client=mock_client,
            contract_guid="contract-guid-123",
        )

        from pyatlan_v9.model.assets.asset import Asset
        from pyatlan_v9.model.assets.referenceable import Referenceable

        assert result[0] == delete_response
        mock_client.asset.get_by_guid.assert_called_once_with(
            "contract-guid-123",
            asset_type=DataContract,
            attributes=["dataContractAssetLatest"],
            related_attributes=[
                Asset.NAME,
                Referenceable.QUALIFIED_NAME,
                Referenceable.TYPE_NAME,
            ],
        )
        mock_client.asset.purge_by_guid.assert_called_once_with("contract-guid-123")
        # Verify the raw API call clears contract state
        mock_client._call_api.assert_called_once()
        payload = mock_client._call_api.call_args[0][2]
        entity = payload["entities"][0]
        assert entity["guid"] == "asset-guid-456"
        assert entity["typeName"] == "Table"
        assert entity["attributes"]["qualifiedName"] == "default/test/table-qn"
        assert entity["attributes"]["name"] == "test-table"
        assert entity["attributes"]["hasContract"] is False
        assert entity["relationshipAttributes"]["dataContractLatest"] is None
        assert entity["relationshipAttributes"]["dataContractLatestCertified"] is None

    def test_delete_raises_when_no_linked_asset(self):
        """delete() should raise ValueError when contract has no linked asset."""
        mock_client = MagicMock()
        mock_contract = MagicMock(spec=DataContract)
        mock_contract.data_contract_asset_latest = None
        mock_client.asset.get_by_guid.return_value = mock_contract

        with pytest.raises(ValueError, match="Cannot determine the linked asset"):
            DataContract.delete(
                client=mock_client,
                contract_guid="contract-guid-123",
            )
