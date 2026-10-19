# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SigmaDataModel.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-sigma-app emits for a `data_models` record
(FND-3838 census), so a creator change that would re-key existing assets fails here.
"""

import pytest

from pyatlan_v9.model import SigmaDataModel

NAME = "Revenue"
CONNECTION_QUALIFIED_NAME = "default/sigma/1712345678"
DATA_MODEL_ID = "dm-1a2b3c4d"
EXPECTED_QN = "default/sigma/1712345678/dataModels/dm-1a2b3c4d"


def _creator_kwargs(**overrides):
    return {
        "name": NAME,
        "connection_qualified_name": CONNECTION_QUALIFIED_NAME,
        "data_model_id": DATA_MODEL_ID,
        **overrides,
    }


def _creator(**overrides):
    return SigmaDataModel.creator(**_creator_kwargs(**overrides))


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.connection_qualified_name == "default/sigma/1712345678"
    assert sut.connector_name == "sigma"
    assert sut.asset_source_id == "dm-1a2b3c4d"
    sut.validate(for_creation=True)


def test_create_alias():
    assert SigmaDataModel.create(**_creator_kwargs()).qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "param", ["name", "connection_qualified_name", "data_model_id"]
)
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    with pytest.raises(ValueError, match=f"{param} {message}"):
        _creator(**{param: value})


def test_updater():
    sut = SigmaDataModel.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": EXPECTED_QN, "name": NAME, param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        SigmaDataModel.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, SigmaDataModel)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_pattern_requires_data_models_segment():
    page_qn = (
        "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34"
    )
    assert not SigmaDataModel._QUALIFIED_NAME_PATTERN.match(page_qn)
