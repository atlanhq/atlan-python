# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanQuicksight, AtlanQuicksightInputs


def test_atlan_quicksight_inputs_defaults():
    i = AtlanQuicksightInputs()
    assert AtlanQuicksightInputs._APP_ID == "atlan-quicksight"
    assert AtlanQuicksightInputs._ENTRYPOINT == ""
    assert i.fetch_folderless_assets is True
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"


def test_atlan_quicksight_builder_payload():
    out = (
        AtlanQuicksight(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .include_folders({"SharedFolders": {}})
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "quicksight"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    # folders are serialized to the JSON-string form the input contract expects
    assert out["include_filter"] == '{"SharedFolders": {}}'


def test_atlan_quicksight_credential_iam():
    b = AtlanQuicksight(Mock()).iam(
        username="x", password="x", region="x", accountid="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
