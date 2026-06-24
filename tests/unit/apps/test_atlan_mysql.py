# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanMysql, AtlanMysqlInputs


def test_atlan_mysql_inputs_defaults():
    i = AtlanMysqlInputs()
    assert AtlanMysqlInputs._APP_ID == "atlan-mysql"
    assert AtlanMysqlInputs._ENTRYPOINT == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.exclude_table_regex == ""


def test_atlan_mysql_builder_payload():
    out = (
        AtlanMysql(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "mysql"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_mysql_credential_basic():
    b = AtlanMysql(Mock()).basic(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-mysql"
    out = (
        AtlanMysql(Mock())
        .basic(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_atlan_mysql_credential_iam_user():
    b = AtlanMysql(Mock()).iam_user(username="x", password="x", username_2="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-mysql"
    out = (
        AtlanMysql(Mock())
        .iam_user(username="x", password="x", username_2="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_atlan_mysql_credential_iam_role():
    b = AtlanMysql(Mock()).iam_role(username="x", aws_role_arn="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-mysql"
    out = (
        AtlanMysql(Mock())
        .iam_role(username="x", aws_role_arn="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
