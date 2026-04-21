from json import dumps
from typing import Union
from unittest.mock import MagicMock

import pytest

from pyatlan.client.contract import CONTRACT_DELETE_SCOPE_HEADER, ContractClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.assets import DataContract, Table
from pyatlan.model.contract import DataContractSpec
from pyatlan.model.enums import AtlanDeleteType, DataContractStatus
from tests.unit.model.constants import (
    ASSET_QUALIFIED_NAME,
    DATA_CONTRACT_JSON,
    DATA_CONTRACT_NAME,
    DATA_CONTRACT_NAME_DEFAULT,
    DATA_CONTRACT_QUALIFIED_NAME,
    DATA_CONTRACT_SPEC_STR,
    DATA_CONTRACT_SPEC_STR_WITHOUT_DATASET,
)

# ---------------------------------------------------------------------------
# Additional YAML fixtures for DataContractSpec tests
# ---------------------------------------------------------------------------

SPEC_YAML_WITH_COLUMNS = """\
kind: DataContract
status: draft
template_version: 0.0.2
type: Table
dataset: FCT_ORDERS
description: ''
columns:
- name: OWNER_ID
  description: Owner identifier
  data_type: VARCHAR
- name: AMOUNT
  description: Transaction amount
  data_type: NUMBER
  not_null: true
  valid_min: 0
  valid_max: 1000000
"""

SPEC_YAML_WITH_OWNERS = """\
kind: DataContract
status: draft
template_version: 0.0.2
type: Table
dataset: orders-table
owners:
  users:
  - alice
  - bob
  groups:
  - data-team
"""

SPEC_YAML_WITH_CERTIFICATION = """\
kind: DataContract
status: verified
template_version: 0.0.2
type: Table
dataset: FCT_ORDERS
certification:
  status: VERIFIED
  message: Certified by data team
"""


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
            contract_json=contract_json,
        )


def test_creator_atttributes_with_required_parameters():
    attributes = DataContract.Attributes.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(attributes, is_json=True)


def test_creator_with_required_parameters_json():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_json=dumps(DATA_CONTRACT_JSON),
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_spec=DATA_CONTRACT_SPEC_STR,
    )
    _assert_contract(test_contract)


def test_creator_with_required_parameters_spec_str_without_dataset():
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_spec=DATA_CONTRACT_SPEC_STR_WITHOUT_DATASET,
    )
    # Ensure the default contract name is extracted from the table's qualified name (QN).
    _assert_contract(test_contract, contract_name=DATA_CONTRACT_NAME_DEFAULT)


def test_creator_with_required_parameters_spec_model():
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    test_contract = DataContract.creator(
        asset_qualified_name=ASSET_QUALIFIED_NAME,
        contract_spec=spec,
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


# ---------------------------------------------------------------------------
# DataContractSpec – parsing tests
# ---------------------------------------------------------------------------


def test_spec_from_yaml_parses_basic_fields():
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)

    assert spec.kind == "DataContract"
    assert spec.status == DataContractStatus.DRAFT
    assert spec.type == "Table"
    assert spec.dataset == "some-asset-name"


def test_spec_from_yaml_parses_columns():
    spec = DataContractSpec.from_yaml(SPEC_YAML_WITH_COLUMNS)

    assert spec.columns and len(spec.columns) == 2

    owner_col = spec.columns[0]
    assert owner_col.name == "OWNER_ID"
    assert owner_col.data_type == "VARCHAR"

    amount_col = spec.columns[1]
    assert amount_col.name == "AMOUNT"
    assert amount_col.data_type == "NUMBER"
    assert amount_col.not_null is True
    assert amount_col.valid_min == 0
    assert amount_col.valid_max == 1000000


def test_spec_from_yaml_parses_owners():
    spec = DataContractSpec.from_yaml(SPEC_YAML_WITH_OWNERS)

    assert spec.owners
    assert spec.owners.users == ["alice", "bob"]
    assert spec.owners.groups == ["data-team"]


def test_spec_from_yaml_parses_certification():
    spec = DataContractSpec.from_yaml(SPEC_YAML_WITH_CERTIFICATION)

    assert spec.certification
    assert spec.certification.message == "Certified by data team"


# ---------------------------------------------------------------------------
# DataContractSpec – mutation tests
# (mirrors publish_contract() / create_contract() steps in test.py)
# ---------------------------------------------------------------------------


def test_spec_mutation_status_draft_to_verified():
    """Simulates the publish_contract() step: flip status to VERIFIED."""
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    assert spec.status == DataContractStatus.DRAFT

    spec.status = DataContractStatus.VERIFIED

    assert spec.status == DataContractStatus.VERIFIED


def test_spec_mutation_description():
    """Simulates description suffix update done across create/publish steps."""
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    spec.description = "E2E test - VERIFIED v1"

    assert spec.description == "E2E test - VERIFIED v1"


def test_spec_mutation_preserves_other_fields():
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    spec.description = "updated"
    spec.status = DataContractStatus.VERIFIED

    assert spec.kind == "DataContract"
    assert spec.type == "Table"
    assert spec.dataset == "some-asset-name"


# ---------------------------------------------------------------------------
# DataContractSpec – roundtrip serialisation (from_yaml → to_yaml → from_yaml)
# ---------------------------------------------------------------------------


def test_spec_yaml_roundtrip_preserves_top_level_fields():
    original = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    reloaded = DataContractSpec.from_yaml(original.to_yaml())

    assert reloaded.kind == original.kind
    assert reloaded.status == original.status
    assert reloaded.type == original.type
    assert reloaded.dataset == original.dataset


def test_spec_yaml_roundtrip_preserves_columns():
    original = DataContractSpec.from_yaml(SPEC_YAML_WITH_COLUMNS)
    reloaded = DataContractSpec.from_yaml(original.to_yaml())

    assert reloaded.columns and len(reloaded.columns) == len(original.columns)
    for orig_col, reload_col in zip(original.columns, reloaded.columns):
        assert reload_col.name == orig_col.name
        assert reload_col.data_type == orig_col.data_type


def test_spec_yaml_roundtrip_after_mutation():
    """Mutate spec as test.py does (status + description), then round-trip."""
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    spec.status = DataContractStatus.VERIFIED
    spec.description = "E2E test - VERIFIED v2"

    reloaded = DataContractSpec.from_yaml(spec.to_yaml())

    assert reloaded.status == DataContractStatus.VERIFIED
    assert reloaded.description == "E2E test - VERIFIED v2"


@pytest.mark.parametrize(
    "status_str,expected",
    [
        ("draft", DataContractStatus.DRAFT),
        ("verified", DataContractStatus.VERIFIED),
    ],
)
def test_spec_from_yaml_status_case_variants(
    status_str: str, expected: DataContractStatus
):
    yaml_input = (
        f"kind: DataContract\nstatus: {status_str}\ntype: Table\ndataset: test\n"
    )
    spec = DataContractSpec.from_yaml(yaml_input)
    assert spec.status == expected


# ---------------------------------------------------------------------------
# ContractClient – unit tests (API-layer behaviour, no real HTTP)
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_api_caller():
    """A MagicMock that satisfies the runtime-checkable ApiCaller Protocol."""
    mock = MagicMock()
    mock._call_api = MagicMock()
    mock.max_retries = MagicMock()
    mock._s3_presigned_url_file_upload = MagicMock()
    mock._azure_blob_presigned_url_file_upload = MagicMock()
    mock._gcs_presigned_url_file_upload = MagicMock()
    mock._presigned_url_file_download = MagicMock()
    return mock


@pytest.fixture()
def contract_client(mock_api_caller):
    return ContractClient(client=mock_api_caller)


def test_contract_client_init_rejects_non_api_caller():
    with pytest.raises(Exception, match="Invalid parameter type"):
        ContractClient(client="not-a-caller")  # type: ignore


def test_generate_initial_spec_returns_yaml_string(
    contract_client: ContractClient, mock_api_caller
):
    """When the API returns {"contract": "<yaml>"}, the YAML string is forwarded."""
    yaml_response = (
        "kind: DataContract\nstatus: draft\ntype: Table\ndataset: FCT_ORDERS\n"
    )
    mock_api_caller._call_api.return_value = {"contract": yaml_response}

    asset = Table.updater(
        qualified_name="default/snowflake/1234/db/schema/FCT_ORDERS",
        name="FCT_ORDERS",
    )
    result = contract_client.generate_initial_spec(asset)

    assert result == yaml_response
    mock_api_caller._call_api.assert_called_once()


def test_generate_initial_spec_returns_none_when_contract_absent(
    contract_client: ContractClient, mock_api_caller
):
    """When the API response has no 'contract' key, None is returned."""
    mock_api_caller._call_api.return_value = {}

    asset = Table.updater(
        qualified_name="default/snowflake/1234/db/schema/FCT_ORDERS",
        name="FCT_ORDERS",
    )
    result = contract_client.generate_initial_spec(asset)

    assert result is None


def test_delete_sends_purge_type_and_guid(
    contract_client: ContractClient, mock_api_caller
):
    """client.contracts.delete() must pass deleteType=PURGE and the guid."""
    mock_api_caller._call_api.return_value = {}
    test_guid = "aaaa-bbbb-cccc"

    contract_client.delete(test_guid)

    _, kwargs = mock_api_caller._call_api.call_args
    query_params = kwargs.get("query_params", {})
    assert query_params["deleteType"] == AtlanDeleteType.PURGE.value
    assert test_guid in query_params["guid"]


def test_delete_does_not_set_scope_header(
    contract_client: ContractClient, mock_api_caller
):
    """client.contracts.delete() must NOT send the contract scope header."""
    mock_api_caller._call_api.return_value = {}

    contract_client.delete("some-guid")

    _, kwargs = mock_api_caller._call_api.call_args
    extra_headers = kwargs.get("extra_headers") or {}
    assert CONTRACT_DELETE_SCOPE_HEADER not in extra_headers


def test_delete_latest_version_sends_single_scope_header(
    contract_client: ContractClient, mock_api_caller
):
    """client.contracts.delete_latest_version() must set scope header to 'single'."""
    mock_api_caller._call_api.return_value = {}
    test_guid = "dddd-eeee-ffff"

    contract_client.delete_latest_version(test_guid)

    _, kwargs = mock_api_caller._call_api.call_args
    extra_headers = kwargs.get("extra_headers", {})
    assert extra_headers.get(CONTRACT_DELETE_SCOPE_HEADER) == "single"


def test_delete_latest_version_sends_purge_type_and_guid(
    contract_client: ContractClient, mock_api_caller
):
    """client.contracts.delete_latest_version() must still use PURGE and the right guid."""
    mock_api_caller._call_api.return_value = {}
    test_guid = "dddd-eeee-ffff"

    contract_client.delete_latest_version(test_guid)

    _, kwargs = mock_api_caller._call_api.call_args
    query_params = kwargs.get("query_params", {})
    assert query_params["deleteType"] == AtlanDeleteType.PURGE.value
    assert test_guid in query_params["guid"]
