from json import dumps
from typing import Union
from unittest.mock import MagicMock

import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.model.assets import DataContract, Table
from pyatlan.model.contract import DataContractSpec
from pyatlan.model.response import AssetMutationResponse
from tests.unit.model.constants import (
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
    contract_name=DATA_CONTRACT_NAME,
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
    with pytest.raises(ValueError, match=message):
        DataContract.creator(  # type: ignore
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
    with pytest.raises(InvalidRequestError, match=error_msg):
        DataContract.creator(
            asset_qualified_name=asset_qualified_name,
            asset_type=Table,
            contract_json=contract_json,
        )


def test_creator_atttributes_with_required_parameters():
    attributes = DataContract.Attributes.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(attributes, is_json=True)


def test_creator_with_required_parameters_json():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_spec=DATA_CONTRACT_SPEC_STR,
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str_without_dataset():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        asset_type=Table,
        contract_spec=DATA_CONTRACT_SPEC_STR_WITHOUT_DATASET,
    )
    # Ensure the default contract name is extracted from the table's qualified name (QN).
    _assert_contract(test_contract, contract_name=DATA_CONTRACT_NAME_DEFAULT)


def test_creator_with_required_parameters_spec_model():
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
    assert ref.unique_attributes == {"qualifiedName": ASSET_QUALIFIED_NAME}


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
        asset_response = MagicMock(spec=AssetMutationResponse)
        mock_client.asset.purge_by_guid.return_value = delete_response
        mock_client.asset.save.return_value = asset_response

        result = DataContract.delete(
            client=mock_client,
            contract_guid="contract-guid-123",
        )

        assert result == (delete_response, asset_response)
        from pyatlan.model.assets import Asset

        mock_client.asset.get_by_guid.assert_called_once_with(
            "contract-guid-123",
            asset_type=DataContract,
            attributes=[DataContract.DATA_CONTRACT_ASSET_LATEST],
            related_attributes=[Asset.NAME, Asset.QUALIFIED_NAME, Asset.TYPE_NAME],
        )
        mock_client.asset.purge_by_guid.assert_called_once_with("contract-guid-123")
        asset_update = mock_client.asset.save.call_args[0][0]
        assert asset_update.guid == "asset-guid-456"
        assert asset_update.has_contract is False
        assert asset_update.data_contract_latest is None
        assert asset_update.data_contract_latest_certified is None

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
