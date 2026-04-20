# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataContract model in pyatlan_v9."""

from json import dumps
from typing import Union
from unittest.mock import MagicMock

import pytest

from pyatlan.client.constants import CONTRACT_DELETE_SCOPE_HEADER
from pyatlan.model.enums import AtlanDeleteType, DataContractStatus
from pyatlan_v9.client.contract import V9ContractClient
from pyatlan_v9.errors import InvalidRequestError
from pyatlan_v9.model import DataContract
from pyatlan_v9.model.assets import Table
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


# ---------------------------------------------------------------------------
# DataContractSpec (v9 msgspec-based) — parsing tests
# ---------------------------------------------------------------------------


def test_v9_spec_from_yaml_parses_basic_fields():
    # v9 uses msgspec: status stays as raw str after from_yaml (no enum coercion)
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)

    assert spec.kind == "DataContract"
    assert spec.status == DataContractStatus.DRAFT.value
    assert spec.type == "Table"
    assert spec.dataset == "some-asset-name"


def test_v9_spec_from_yaml_parses_columns():
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


def test_v9_spec_from_yaml_parses_owners():
    spec = DataContractSpec.from_yaml(SPEC_YAML_WITH_OWNERS)

    assert spec.owners
    assert spec.owners.users == ["alice", "bob"]
    assert spec.owners.groups == ["data-team"]


# ---------------------------------------------------------------------------
# DataContractSpec (v9) — mutation tests
# ---------------------------------------------------------------------------


def test_v9_spec_mutation_status_draft_to_verified():
    """Flip status DRAFT → VERIFIED (mirrors publish_contract() in test.py)."""
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    assert spec.status == DataContractStatus.DRAFT.value  # raw str after from_yaml

    spec.status = DataContractStatus.VERIFIED

    assert spec.status == DataContractStatus.VERIFIED


def test_v9_spec_mutation_description():
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    spec.description = "E2E test - VERIFIED v1"

    assert spec.description == "E2E test - VERIFIED v1"


# ---------------------------------------------------------------------------
# DataContractSpec (v9) — YAML roundtrip
# (msgspec.to_builtins serialises all fields, so kind/template_version are
#  always present — unlike pydantic's exclude_unset behaviour)
# ---------------------------------------------------------------------------


def test_v9_spec_yaml_roundtrip_preserves_top_level_fields():
    original = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    reloaded = DataContractSpec.from_yaml(original.to_yaml())

    assert reloaded.kind == original.kind
    assert reloaded.status == original.status
    assert reloaded.type == original.type
    assert reloaded.dataset == original.dataset


def test_v9_spec_yaml_roundtrip_preserves_columns():
    original = DataContractSpec.from_yaml(SPEC_YAML_WITH_COLUMNS)
    reloaded = DataContractSpec.from_yaml(original.to_yaml())

    assert reloaded.columns and len(reloaded.columns) == len(original.columns)
    for orig_col, reload_col in zip(original.columns, reloaded.columns):
        assert reload_col.name == orig_col.name
        assert reload_col.data_type == orig_col.data_type


def test_v9_spec_yaml_roundtrip_after_mutation():
    spec = DataContractSpec.from_yaml(DATA_CONTRACT_SPEC_STR)
    spec.status = DataContractStatus.VERIFIED
    spec.description = "E2E test - VERIFIED v2"

    reloaded = DataContractSpec.from_yaml(spec.to_yaml())

    # After roundtrip the enum value is serialised as its string and re-parsed as str
    assert reloaded.status == DataContractStatus.VERIFIED.value
    assert reloaded.description == "E2E test - VERIFIED v2"


def test_v9_spec_to_yaml_includes_kind_and_template_version_by_default():
    """v9 uses msgspec.to_builtins, so defaults are always serialised."""
    spec = DataContractSpec(
        status=DataContractStatus.DRAFT,
        type="Table",
        dataset="FCT_ORDERS",
    )
    yaml_out = spec.to_yaml()

    assert "DataContract" in yaml_out
    assert "0.0.2" in yaml_out


@pytest.mark.parametrize(
    "status_str",
    ["draft", "verified"],
)
def test_v9_spec_from_yaml_status_case_variants(status_str: str):
    # v9 msgspec keeps status as raw string after from_yaml
    yaml_input = (
        f"kind: DataContract\nstatus: {status_str}\ntype: Table\ndataset: test\n"
    )
    spec = DataContractSpec.from_yaml(yaml_input)
    assert spec.status == status_str


# ---------------------------------------------------------------------------
# V9ContractClient — unit tests (mocked, no HTTP)
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_api_caller_v9():
    """MagicMock satisfying the runtime-checkable ApiCaller Protocol."""
    mock = MagicMock()
    mock._call_api = MagicMock()
    mock.max_retries = MagicMock()
    mock._s3_presigned_url_file_upload = MagicMock()
    mock._azure_blob_presigned_url_file_upload = MagicMock()
    mock._gcs_presigned_url_file_upload = MagicMock()
    mock._presigned_url_file_download = MagicMock()
    return mock


@pytest.fixture()
def v9_contract_client(mock_api_caller_v9):
    return V9ContractClient(client=mock_api_caller_v9)


def test_v9_contract_client_init_rejects_non_api_caller():
    with pytest.raises(Exception, match="Invalid parameter type"):
        V9ContractClient(client="not-a-caller")  # type: ignore


def test_v9_generate_initial_spec_returns_yaml_string(
    v9_contract_client: V9ContractClient, mock_api_caller_v9
):
    yaml_response = (
        "kind: DataContract\nstatus: draft\ntype: Table\ndataset: FCT_ORDERS\n"
    )
    mock_api_caller_v9._call_api.return_value = {"contract": yaml_response}

    asset = Table.updater(
        qualified_name="default/snowflake/1234/db/schema/FCT_ORDERS",
        name="FCT_ORDERS",
    )
    result = v9_contract_client.generate_initial_spec(asset)

    assert result == yaml_response
    mock_api_caller_v9._call_api.assert_called_once()


def test_v9_generate_initial_spec_returns_none_when_contract_absent(
    v9_contract_client: V9ContractClient, mock_api_caller_v9
):
    mock_api_caller_v9._call_api.return_value = {}

    asset = Table.updater(
        qualified_name="default/snowflake/1234/db/schema/FCT_ORDERS",
        name="FCT_ORDERS",
    )
    result = v9_contract_client.generate_initial_spec(asset)

    assert result is None


def test_v9_delete_sends_purge_type_and_guid(
    v9_contract_client: V9ContractClient, mock_api_caller_v9
):
    mock_api_caller_v9._call_api.return_value = {}

    v9_contract_client.delete("aaaa-bbbb-cccc")

    _, kwargs = mock_api_caller_v9._call_api.call_args
    query_params = kwargs.get("query_params", {})
    assert query_params["deleteType"] == AtlanDeleteType.PURGE.value
    assert "aaaa-bbbb-cccc" in query_params["guid"]


def test_v9_delete_does_not_set_scope_header(
    v9_contract_client: V9ContractClient, mock_api_caller_v9
):
    mock_api_caller_v9._call_api.return_value = {}

    v9_contract_client.delete("some-guid")

    _, kwargs = mock_api_caller_v9._call_api.call_args
    extra_headers = kwargs.get("extra_headers") or {}
    assert CONTRACT_DELETE_SCOPE_HEADER not in extra_headers


def test_v9_delete_latest_version_sends_single_scope_header(
    v9_contract_client: V9ContractClient, mock_api_caller_v9
):
    mock_api_caller_v9._call_api.return_value = {}

    v9_contract_client.delete_latest_version("dddd-eeee-ffff")

    _, kwargs = mock_api_caller_v9._call_api.call_args
    extra_headers = kwargs.get("extra_headers", {})
    assert extra_headers.get(CONTRACT_DELETE_SCOPE_HEADER) == "single"


def test_v9_delete_latest_version_sends_purge_type_and_guid(
    v9_contract_client: V9ContractClient, mock_api_caller_v9
):
    mock_api_caller_v9._call_api.return_value = {}
    test_guid = "dddd-eeee-ffff"

    v9_contract_client.delete_latest_version(test_guid)

    _, kwargs = mock_api_caller_v9._call_api.call_args
    query_params = kwargs.get("query_params", {})
    assert query_params["deleteType"] == AtlanDeleteType.PURGE.value
    assert test_guid in query_params["guid"]
