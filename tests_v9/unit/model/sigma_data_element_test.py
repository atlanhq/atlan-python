# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SigmaDataElement.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-sigma-app emits for a `data_elements` record
(FND-3838 census), so a creator change that would re-key existing assets fails here.
"""

import pytest

from pyatlan_v9.model import SigmaDataElement

NAME = "Revenue"
PAGE_QUALIFIED_NAME = (
    "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34"
)
PAGE_NAME = "Summary"
WORKBOOK_NAME = "Sales Overview"
DATA_ELEMENT_ID = "el-Xy9Zw8Vu"
EXPECTED_QN = "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34/el-Xy9Zw8Vu"


def _creator_kwargs(**overrides):
    return {
        "name": NAME,
        "page_qualified_name": PAGE_QUALIFIED_NAME,
        "page_name": PAGE_NAME,
        "workbook_name": WORKBOOK_NAME,
        "data_element_id": DATA_ELEMENT_ID,
        **overrides,
    }


def _creator(**overrides):
    return SigmaDataElement.creator(**_creator_kwargs(**overrides))


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.connection_qualified_name == "default/sigma/1712345678"
    assert sut.connector_name == "sigma"
    assert (
        sut.sigma_page_qualified_name
        == "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34"
    )
    assert sut.sigma_page_name == "Summary"
    assert (
        sut.sigma_workbook_qualified_name
        == "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f"
    )
    assert sut.sigma_workbook_name == "Sales Overview"
    assert sut.sigma_page.unique_attributes == {
        "qualifiedName": "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34"
    }
    sut.validate(for_creation=True)


def test_create_alias():
    assert SigmaDataElement.create(**_creator_kwargs()).qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "param",
    ["name", "page_qualified_name", "page_name", "workbook_name", "data_element_id"],
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
        # workbook qn, one segment short
        (
            "page_qualified_name",
            "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f",
        ),
        # data element qn, one segment long
        (
            "page_qualified_name",
            "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34/el-Xy9Zw8Vu",
        ),
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(param, bad_qn):
    with pytest.raises(ValueError, match=f"Invalid {param}"):
        _creator(**{param: bad_qn})


def test_updater():
    sut = SigmaDataElement.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": EXPECTED_QN, "name": NAME, param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        SigmaDataElement.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, SigmaDataElement)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
