# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for S3Prefix.creator in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import S3Prefix

CONNECTION_QN = "default/s3/1700000000"
BUCKET_NAME = "example-bucket"
BUCKET_QN = f"{CONNECTION_QN}/{BUCKET_NAME}"


def _create(prefix: str, **kwargs) -> S3Prefix:
    return S3Prefix.creator(
        connection_qualified_name=CONNECTION_QN,
        s3_bucket_name=BUCKET_NAME,
        s3_bucket_qualified_name=BUCKET_QN,
        prefix=prefix,
        **kwargs,
    )


@pytest.mark.parametrize(
    "connection_qualified_name, s3_bucket_name, s3_bucket_qualified_name, prefix, message",
    [
        (None, BUCKET_NAME, BUCKET_QN, "a/", "connection_qualified_name is required"),
        (CONNECTION_QN, None, BUCKET_QN, "a/", "s3_bucket_name is required"),
        (
            CONNECTION_QN,
            BUCKET_NAME,
            None,
            "a/",
            "s3_bucket_qualified_name is required",
        ),
        (CONNECTION_QN, BUCKET_NAME, BUCKET_QN, None, "prefix is required"),
        (CONNECTION_QN, BUCKET_NAME, BUCKET_QN, " ", "prefix cannot be blank"),
        (CONNECTION_QN, BUCKET_NAME, BUCKET_QN, "a//b/", "empty segments"),
        (CONNECTION_QN, BUCKET_NAME, BUCKET_QN, "/", "empty segments"),
        ("default/s3", BUCKET_NAME, BUCKET_QN, "a/", "Invalid connection"),
        ("default/gcs/1", BUCKET_NAME, BUCKET_QN, "a/", "Invalid connection"),
    ],
)
def test_creator_with_invalid_parameters_raises_value_error(
    connection_qualified_name, s3_bucket_name, s3_bucket_qualified_name, prefix, message
):
    with pytest.raises(ValueError, match=message):
        S3Prefix.creator(
            connection_qualified_name=connection_qualified_name,
            s3_bucket_name=s3_bucket_name,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
            prefix=prefix,
        )


def test_creator_root_prefix():
    sut = _create("raw/")

    assert sut.name == "raw"
    assert sut.qualified_name == f"{BUCKET_QN}/raw/"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "s3"
    assert sut.s3_bucket_name == BUCKET_NAME
    assert sut.s3_bucket_qualified_name == BUCKET_QN
    assert sut.s3_bucket.qualified_name == BUCKET_QN
    assert sut.s3_parent_prefix_qualified_name is UNSET
    assert sut.s3_prefix_hierarchy is UNSET


def test_creator_nested_prefix_sets_parent_and_hierarchy():
    sut = _create("raw/2025/data/")

    assert sut.name == "data"
    assert sut.qualified_name == f"{BUCKET_QN}/raw/2025/data/"
    assert sut.s3_parent_prefix_qualified_name == f"{BUCKET_QN}/raw/2025/"
    assert sut.s3_prefix_hierarchy == [
        {"name": "2025", "qualifiedName": f"{BUCKET_QN}/raw/2025/"},
        {"name": "raw", "qualifiedName": f"{BUCKET_QN}/raw/"},
    ]


@pytest.mark.parametrize("prefix", ["a/b", "a/b/", "/a/b/"])
def test_creator_normalises_slashes(prefix):
    assert _create(prefix).qualified_name == f"{BUCKET_QN}/a/b/"


def test_creator_explicit_name():
    assert _create("a/b/", name="B folder").name == "B folder"


def test_parity_s3_app():
    """atlan-s3-app: {bucket_qn}/{prefix_key} where prefix_key keeps its trailing slash."""
    prefix_key = "a/b/"
    sut = _create(prefix_key)
    assert sut.qualified_name == f"{BUCKET_QN}/{prefix_key}"
    assert sut.name == prefix_key.split("/")[-2]
    assert sut.s3_parent_prefix_qualified_name == f"{BUCKET_QN}/a/"


def test_parity_bridge_app():
    """atlan-bridge-app: {conn}/{bucket}/{parent_folder_path}/{name}/."""
    parent_folder_path, name = "/raw/2025/", "data"
    full_path = f"{parent_folder_path.strip('/')}/{name.strip('/')}".strip("/")
    sut = _create(full_path)
    assert sut.qualified_name == f"{CONNECTION_QN}/{BUCKET_NAME}/{full_path}/"
    assert sut.name == name


@pytest.mark.parametrize("prefix", ["raw/", "raw/2025/data/"])
def test_creator_output_passes_generated_validation(prefix):
    _create(prefix).validate(for_creation=True)


def test_parity_s3_app_literal_qualified_name():
    sut = S3Prefix.creator(
        connection_qualified_name="default/s3/1700000000",
        s3_bucket_name="example-bucket",
        s3_bucket_qualified_name="default/s3/1700000000/example-bucket",
        prefix="a/b/",
    )
    assert sut.qualified_name == "default/s3/1700000000/example-bucket/a/b/"
