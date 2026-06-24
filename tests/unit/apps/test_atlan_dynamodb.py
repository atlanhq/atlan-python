# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanDynamodb, AtlanDynamodbInputs


def test_atlan_dynamodb_inputs_defaults():
    i = AtlanDynamodbInputs()
    assert AtlanDynamodbInputs._APP_ID == "atlan-dynamodb"
    assert AtlanDynamodbInputs._ENTRYPOINT == ""
    assert i.exclude_filter == ""
    assert i.include_filter == ""


def test_atlan_dynamodb_builder_payload():
    out = (
        AtlanDynamodb(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "dynamodb"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_dynamodb_credential_iam_user():
    b = AtlanDynamodb(Mock()).iam_user(username="x", password="x", region="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-dynamodb"
    out = (
        AtlanDynamodb(Mock())
        .iam_user(username="x", password="x", region="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_atlan_dynamodb_credential_assume_role():
    b = AtlanDynamodb(Mock()).assume_role(aws_role_arn="x", region="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-dynamodb"
    out = (
        AtlanDynamodb(Mock())
        .assume_role(aws_role_arn="x", region="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
