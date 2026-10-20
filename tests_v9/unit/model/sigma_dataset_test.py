# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SigmaDataset.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-sigma-app emits for a `datasets` record
(FND-3838 census), so a creator change that would re-key existing assets fails here.
"""

import pytest

from pyatlan_v9.model import SigmaDataset

NAME = "Revenue"
CONNECTION_QUALIFIED_NAME = "default/sigma/1712345678"
DATASET_ID = "9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b"
EXPECTED_QN = "default/sigma/1712345678/9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b"


def _creator_kwargs(**overrides):
    return {
        "name": NAME,
        "connection_qualified_name": CONNECTION_QUALIFIED_NAME,
        "dataset_id": DATASET_ID,
        **overrides,
    }


def _creator(**overrides):
    return SigmaDataset.creator(**_creator_kwargs(**overrides))


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.connection_qualified_name == "default/sigma/1712345678"
    assert sut.connector_name == "sigma"
    sut.validate(for_creation=True)


def test_create_alias():
    assert SigmaDataset.create(**_creator_kwargs()).qualified_name == EXPECTED_QN


@pytest.mark.parametrize("param", ["name", "connection_qualified_name", "dataset_id"])
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    with pytest.raises(ValueError, match=f"{param} {message}"):
        _creator(**{param: value})


def test_updater():
    sut = SigmaDataset.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": EXPECTED_QN, "name": NAME, param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        SigmaDataset.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, SigmaDataset)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
