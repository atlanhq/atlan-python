# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import MongodbatlasAtlas, MongodbatlasAtlasInputs


def test_mongodbatlas_atlas_inputs_defaults():
    i = MongodbatlasAtlasInputs()
    assert MongodbatlasAtlasInputs._APP_ID == "mongodbatlas-atlas"
    assert MongodbatlasAtlasInputs._ENTRYPOINT == ""
    assert i.include_filter == ""
    assert i.exclude_filter == ""


def test_mongodbatlas_atlas_builder_payload():
    out = (
        MongodbatlasAtlas(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "mongodb"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_mongodbatlas_atlas_credential_basic():
    b = MongodbatlasAtlas(Mock()).basic(
        username="x",
        password="x",
        native_host="x",
        default_database="x",
        authsource="x",
        ssl="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
