# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SigmaDataModelColumn.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-sigma-app emits for a `data_model_columns` record
(FND-3838 census), so a creator change that would re-key existing assets fails here.
"""

import pytest

from pyatlan_v9.model import SigmaDataModelColumn

NAME = "Revenue"
DATA_MODEL_QUALIFIED_NAME = "default/sigma/1712345678/dataModels/dm-1a2b3c4d"
DATA_MODEL_NAME = "Orders Model"
ELEMENT_ID = "dmel_Mn5Op4"
COLUMN_ID = "col_Gh3Ij2"
EXPECTED_QN = "default/sigma/1712345678/dataModels/dm-1a2b3c4d/dmel_Mn5Op4/col_Gh3Ij2"


def _creator_kwargs(**overrides):
    return {
        "name": NAME,
        "data_model_qualified_name": DATA_MODEL_QUALIFIED_NAME,
        "data_model_name": DATA_MODEL_NAME,
        "element_id": ELEMENT_ID,
        "column_id": COLUMN_ID,
        **overrides,
    }


def _creator(**overrides):
    return SigmaDataModelColumn.creator(**_creator_kwargs(**overrides))


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.connection_qualified_name == "default/sigma/1712345678"
    assert sut.connector_name == "sigma"
    assert (
        sut.sigma_data_model_qualified_name
        == "default/sigma/1712345678/dataModels/dm-1a2b3c4d"
    )
    assert sut.sigma_data_model_name == "Orders Model"
    assert sut.asset_source_id == "col_Gh3Ij2"
    assert sut.sigma_data_model.unique_attributes == {
        "qualifiedName": "default/sigma/1712345678/dataModels/dm-1a2b3c4d"
    }
    sut.validate(for_creation=True)


def test_create_alias():
    assert (
        SigmaDataModelColumn.create(**_creator_kwargs()).qualified_name == EXPECTED_QN
    )


@pytest.mark.parametrize(
    "param",
    ["name", "data_model_qualified_name", "data_model_name", "element_id", "column_id"],
)
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    with pytest.raises(ValueError, match=f"{param} {message}"):
        _creator(**{param: value})


@pytest.mark.parametrize(
    "param, bad_qn",
    [
        # connection qn, one segment short
        ("data_model_qualified_name", "default/sigma/1712345678"),
        # right length, no dataModels segment
        (
            "data_model_qualified_name",
            "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34",
        ),
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(param, bad_qn):
    with pytest.raises(ValueError, match=f"Invalid {param}"):
        _creator(**{param: bad_qn})


def test_updater():
    sut = SigmaDataModelColumn.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": EXPECTED_QN, "name": NAME, param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        SigmaDataModelColumn.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, SigmaDataModelColumn)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
