# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Sigma creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-sigma-app emits today
(FND-3838 census), so a creator change that would re-key existing Sigma assets fails here.
"""

import pytest

from pyatlan_v9.model import (
    SigmaDataElement,
    SigmaDataElementField,
    SigmaDataModel,
    SigmaDataModelColumn,
    SigmaDataset,
    SigmaPage,
    SigmaWorkbook,
)

CONNECTION_QN = "default/sigma/1712345678"
WORKBOOK_ID = "3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f"
PAGE_ID = "pg_Ab12Cd34"
DATA_ELEMENT_ID = "el-Xy9Zw8Vu"
FIELD_ID = "fld_Qr7St6"
DATASET_ID = "9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b"
DATA_MODEL_ID = "dm-1a2b3c4d"
ELEMENT_ID = "dmel_Mn5Op4"
COLUMN_ID = "col_Gh3Ij2"

WORKBOOK_QN = f"{CONNECTION_QN}/{WORKBOOK_ID}"
PAGE_QN = f"{WORKBOOK_QN}/{PAGE_ID}"
DATA_ELEMENT_QN = f"{PAGE_QN}/{DATA_ELEMENT_ID}"
DATA_MODEL_QN = f"{CONNECTION_QN}/dataModels/{DATA_MODEL_ID}"

NAME = "Revenue"
WORKBOOK_NAME = "Sales Overview"
PAGE_NAME = "Summary"
DATA_ELEMENT_NAME = "Revenue by Region"
DATA_MODEL_NAME = "Orders Model"

# (type, creator kwargs, the literal qualifiedName atlan-sigma-app emits)
ALL_TYPES = [
    (
        SigmaWorkbook,
        dict(connection_qualified_name=CONNECTION_QN, workbook_id=WORKBOOK_ID),
        "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f",
    ),
    (
        SigmaDataset,
        dict(connection_qualified_name=CONNECTION_QN, dataset_id=DATASET_ID),
        "default/sigma/1712345678/9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b",
    ),
    (
        SigmaDataModel,
        dict(connection_qualified_name=CONNECTION_QN, data_model_id=DATA_MODEL_ID),
        "default/sigma/1712345678/dataModels/dm-1a2b3c4d",
    ),
    (
        SigmaPage,
        dict(
            workbook_qualified_name=WORKBOOK_QN,
            workbook_name=WORKBOOK_NAME,
            page_id=PAGE_ID,
        ),
        "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34",
    ),
    (
        SigmaDataElement,
        dict(
            page_qualified_name=PAGE_QN,
            page_name=PAGE_NAME,
            workbook_name=WORKBOOK_NAME,
            data_element_id=DATA_ELEMENT_ID,
        ),
        "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34"
        "/el-Xy9Zw8Vu",
    ),
    (
        SigmaDataElementField,
        dict(
            data_element_qualified_name=DATA_ELEMENT_QN,
            data_element_name=DATA_ELEMENT_NAME,
            page_name=PAGE_NAME,
            workbook_name=WORKBOOK_NAME,
            field_id=FIELD_ID,
        ),
        "default/sigma/1712345678/3f2b9c1e-7a4d-4e8b-9c0d-1a2b3c4d5e6f/pg_Ab12Cd34"
        "/el-Xy9Zw8Vu/fld_Qr7St6",
    ),
    (
        SigmaDataModelColumn,
        dict(
            data_model_qualified_name=DATA_MODEL_QN,
            data_model_name=DATA_MODEL_NAME,
            element_id=ELEMENT_ID,
            column_id=COLUMN_ID,
        ),
        "default/sigma/1712345678/dataModels/dm-1a2b3c4d/dmel_Mn5Op4/col_Gh3Ij2",
    ),
]
IDS = [t[0].__name__ for t in ALL_TYPES]


@pytest.mark.parametrize("asset_type, kwargs, expected_qn", ALL_TYPES, ids=IDS)
def test_creator_matches_app_qualified_name(asset_type, kwargs, expected_qn):
    sut = asset_type.creator(name=NAME, **kwargs)

    assert sut.qualified_name == expected_qn
    assert sut.name == NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "sigma"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize("asset_type, kwargs, expected_qn", ALL_TYPES, ids=IDS)
def test_create_alias(asset_type, kwargs, expected_qn):
    assert asset_type.create(name=NAME, **kwargs).qualified_name == expected_qn


@pytest.mark.parametrize("asset_type, kwargs, _", ALL_TYPES, ids=IDS)
def test_creator_rejects_missing_or_blank_inputs(asset_type, kwargs, _):
    for param in ["name", *kwargs]:
        args = {"name": NAME, **kwargs}
        args[param] = None
        with pytest.raises(ValueError, match=f"{param} is required"):
            asset_type.creator(**args)
        args[param] = "  "
        with pytest.raises(ValueError, match=f"{param} cannot be blank"):
            asset_type.creator(**args)


def test_page_sets_workbook():
    sut = SigmaPage.creator(
        name=NAME,
        workbook_qualified_name=WORKBOOK_QN,
        workbook_name=WORKBOOK_NAME,
        page_id=PAGE_ID,
    )

    assert sut.sigma_workbook.qualified_name == WORKBOOK_QN
    assert sut.sigma_workbook_qualified_name == WORKBOOK_QN
    assert sut.sigma_workbook_name == WORKBOOK_NAME


def test_data_element_sets_page_and_workbook():
    sut = SigmaDataElement.creator(
        name=NAME,
        page_qualified_name=PAGE_QN,
        page_name=PAGE_NAME,
        workbook_name=WORKBOOK_NAME,
        data_element_id=DATA_ELEMENT_ID,
    )

    assert sut.sigma_page.qualified_name == PAGE_QN
    assert sut.sigma_page_qualified_name == PAGE_QN
    assert sut.sigma_page_name == PAGE_NAME
    assert sut.sigma_workbook_qualified_name == WORKBOOK_QN
    assert sut.sigma_workbook_name == WORKBOOK_NAME


def test_data_element_field_sets_all_ancestors():
    sut = SigmaDataElementField.creator(
        name=NAME,
        data_element_qualified_name=DATA_ELEMENT_QN,
        data_element_name=DATA_ELEMENT_NAME,
        page_name=PAGE_NAME,
        workbook_name=WORKBOOK_NAME,
        field_id=FIELD_ID,
    )

    assert sut.sigma_data_element.qualified_name == DATA_ELEMENT_QN
    assert sut.sigma_data_element_qualified_name == DATA_ELEMENT_QN
    assert sut.sigma_data_element_name == DATA_ELEMENT_NAME
    assert sut.sigma_page_qualified_name == PAGE_QN
    assert sut.sigma_page_name == PAGE_NAME
    assert sut.sigma_workbook_qualified_name == WORKBOOK_QN
    assert sut.sigma_workbook_name == WORKBOOK_NAME


def test_data_model_sets_asset_source_id():
    sut = SigmaDataModel.creator(
        name=NAME, connection_qualified_name=CONNECTION_QN, data_model_id=DATA_MODEL_ID
    )

    assert sut.asset_source_id == DATA_MODEL_ID


def test_data_model_column_sets_data_model():
    sut = SigmaDataModelColumn.creator(
        name=NAME,
        data_model_qualified_name=DATA_MODEL_QN,
        data_model_name=DATA_MODEL_NAME,
        element_id=ELEMENT_ID,
        column_id=COLUMN_ID,
    )

    assert sut.sigma_data_model.qualified_name == DATA_MODEL_QN
    assert sut.sigma_data_model_qualified_name == DATA_MODEL_QN
    assert sut.sigma_data_model_name == DATA_MODEL_NAME
    assert sut.asset_source_id == COLUMN_ID


@pytest.mark.parametrize(
    "asset_type, parent_param, bad_parent_qn",
    [
        (SigmaPage, "workbook_qualified_name", CONNECTION_QN),
        (SigmaPage, "workbook_qualified_name", PAGE_QN),
        (SigmaDataElement, "page_qualified_name", WORKBOOK_QN),
        (SigmaDataElement, "page_qualified_name", DATA_ELEMENT_QN),
        (SigmaDataElementField, "data_element_qualified_name", PAGE_QN),
        (SigmaDataElementField, "data_element_qualified_name", f"{DATA_ELEMENT_QN}/x"),
        (SigmaDataModelColumn, "data_model_qualified_name", CONNECTION_QN),
        # a page qn has the data model's segment count but not the `dataModels` literal
        (SigmaDataModelColumn, "data_model_qualified_name", PAGE_QN),
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(
    asset_type, parent_param, bad_parent_qn
):
    kwargs = next(k for t, k, _ in ALL_TYPES if t is asset_type)
    with pytest.raises(ValueError, match=f"Invalid {parent_param}"):
        asset_type.creator(name=NAME, **{**kwargs, parent_param: bad_parent_qn})


def test_data_model_patterns_require_data_models_segment():
    assert not SigmaDataModel._QUALIFIED_NAME_PATTERN.match(PAGE_QN)
    assert not SigmaDataModelColumn._QUALIFIED_NAME_PATTERN.match(DATA_ELEMENT_QN)
