# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Databricks creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-databricks-app emits today
(FND-3851 analysis), so a creator change that would re-key existing Databricks assets
fails here.
"""

import hashlib

import pytest

from pyatlan_v9.model import (
    ContextRepository,
    DatabricksAIModelContext,
    DatabricksAIModelVersion,
    DatabricksDashboard,
    DatabricksExternalLocation,
    DatabricksExternalLocationPath,
    DatabricksGenieAgent,
    DatabricksMetricView,
    DatabricksNotebook,
    DatabricksUnityCatalogTag,
    DatabricksVolume,
    DatabricksVolumePath,
    Skill,
    SkillArtifact,
)

CONNECTION_QN = "default/databricks/1712345678"
DATABASE_QN = f"{CONNECTION_QN}/main"
SCHEMA_QN = f"{DATABASE_QN}/sales"
VOLUME_QN = f"{SCHEMA_QN}/landing"
MODEL_QN = f"{SCHEMA_QN}/churn_model"
EXT_LOCATION_QN = f"{CONNECTION_QN}/raw_bucket"
WORKSPACE_ID = "1234567890123456"


def _assert_connection(sut):
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "databricks"


# ---------------------------------------------------------------------------
# Schema-scoped types: {schema_qn}/{name}
# ---------------------------------------------------------------------------

SCHEMA_SCOPED = [
    (DatabricksMetricView, "revenue_metrics", "atlan_schema"),
    (DatabricksVolume, "landing", "databricks_volume_schema"),
    (DatabricksAIModelContext, "churn_model", "databricks_ai_model_schema"),
]


@pytest.mark.parametrize("asset_type, name, parent_field", SCHEMA_SCOPED)
def test_schema_scoped_creator_matches_app_qualified_name(
    asset_type, name, parent_field
):
    sut = asset_type.creator(name=name, schema_qualified_name=SCHEMA_QN)

    assert sut.qualified_name == f"default/databricks/1712345678/main/sales/{name}"
    assert sut.name == name
    assert sut.database_name == "main"
    assert sut.database_qualified_name == DATABASE_QN
    assert sut.schema_name == "sales"
    assert sut.schema_qualified_name == SCHEMA_QN
    assert getattr(sut, parent_field).unique_attributes == {"qualifiedName": SCHEMA_QN}
    _assert_connection(sut)
    sut.validate()


@pytest.mark.parametrize("asset_type, name, _", SCHEMA_SCOPED)
@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"name": None, "schema_qualified_name": SCHEMA_QN}, "name is required"),
        ({"name": "x", "schema_qualified_name": None}, "schema_qualified_name"),
        ({"name": " ", "schema_qualified_name": SCHEMA_QN}, "name cannot be blank"),
        ({"name": "x", "schema_qualified_name": DATABASE_QN}, "Invalid schema"),
    ],
)
def test_schema_scoped_creator_rejects_bad_inputs(asset_type, name, _, kwargs, message):
    with pytest.raises(ValueError, match=message):
        asset_type.creator(**kwargs)


# ---------------------------------------------------------------------------
# DatabricksVolumePath: {volume_qn}/{file_path}, root is {volume_qn}/
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, expected_qn, expected_path",
    [
        (
            "/Volumes/main/sales/landing/2026/orders.csv",
            f"{VOLUME_QN}/2026/orders.csv",
            "/Volumes/main/sales/landing/2026/orders.csv",
        ),
        (
            "dbfs:/Volumes/main/sales/landing/orders.csv",
            f"{VOLUME_QN}/orders.csv",
            "dbfs:/Volumes/main/sales/landing/orders.csv",
        ),
        ("/Volumes/main/sales/landing", f"{VOLUME_QN}/", "/"),
        ("/Volumes/main/sales/landing/", f"{VOLUME_QN}/", "/"),
    ],
)
def test_volume_path_creator_matches_app_qualified_name(
    path, expected_qn, expected_path
):
    sut = DatabricksVolumePath.creator(path=path, volume_qualified_name=VOLUME_QN)

    assert sut.qualified_name == expected_qn
    assert sut.name == path
    assert sut.databricks_volume_path_path == expected_path
    assert sut.databricks_volume_path_volume_name == "landing"
    assert sut.databricks_volume_path_volume_qualified_name == VOLUME_QN
    assert sut.database_qualified_name == DATABASE_QN
    assert sut.schema_qualified_name == SCHEMA_QN
    assert sut.databricks_volume.unique_attributes == {"qualifiedName": VOLUME_QN}
    _assert_connection(sut)


@pytest.mark.parametrize(
    "path, volume_qn, message",
    [
        (None, VOLUME_QN, "path is required"),
        ("/Volumes/main/sales/landing/a.csv", None, "volume_qualified_name"),
        ("/tmp/a.csv", VOLUME_QN, "Invalid path"),
        ("/Volumes/main/sales", VOLUME_QN, "Invalid path"),
        ("/Volumes/main/sales/landing/a.csv", SCHEMA_QN, "Invalid volume"),
    ],
)
def test_volume_path_creator_rejects_bad_inputs(path, volume_qn, message):
    with pytest.raises(ValueError, match=message):
        DatabricksVolumePath.creator(path=path, volume_qualified_name=volume_qn)


# ---------------------------------------------------------------------------
# External locations
# ---------------------------------------------------------------------------


def test_external_location_creator_matches_app_qualified_name():
    sut = DatabricksExternalLocation.creator(
        name="raw_bucket", connection_qualified_name=CONNECTION_QN
    )

    assert sut.qualified_name == "default/databricks/1712345678/raw_bucket"
    assert sut.name == "raw_bucket"
    _assert_connection(sut)
    sut.validate()


def test_external_location_path_creator_hashes_the_raw_path():
    path = "s3://raw-bucket/landing/2026/orders.parquet"
    expected_hash = hashlib.md5(path.encode("utf-8")).hexdigest()

    sut = DatabricksExternalLocationPath.creator(
        path=path, external_location_qualified_name=EXT_LOCATION_QN
    )

    assert sut.qualified_name == f"{EXT_LOCATION_QN}/{expected_hash}"
    assert sut.name == path
    assert sut.databricks_path == path
    assert sut.databricks_parent_name == "raw_bucket"
    assert sut.databricks_parent_qualified_name == EXT_LOCATION_QN
    assert sut.databricks_external_location.unique_attributes == {
        "qualifiedName": EXT_LOCATION_QN
    }
    _assert_connection(sut)
    sut.validate()


@pytest.mark.parametrize(
    "path, ext_qn, message",
    [
        (None, EXT_LOCATION_QN, "path is required"),
        ("s3://b/k", None, "external_location_qualified_name is required"),
        ("s3://b/k", CONNECTION_QN, "Invalid external_location"),
    ],
)
def test_external_location_path_creator_rejects_bad_inputs(path, ext_qn, message):
    with pytest.raises(ValueError, match=message):
        DatabricksExternalLocationPath.creator(
            path=path, external_location_qualified_name=ext_qn
        )


# ---------------------------------------------------------------------------
# Workspace-scoped types
# ---------------------------------------------------------------------------


def test_dashboard_creator_matches_app_qualified_name():
    sut = DatabricksDashboard.creator(
        name="Revenue",
        connection_qualified_name=CONNECTION_QN,
        workspace_id=WORKSPACE_ID,
        dashboard_id="01ef1234abcd",
    )

    assert sut.qualified_name == (
        "default/databricks/1712345678/1234567890123456/dashboards/01ef1234abcd"
    )
    assert sut.asset_source_id == "01ef1234abcd"
    assert sut.databricks_dashboard_workspace_id == WORKSPACE_ID
    _assert_connection(sut)
    sut.validate()


def test_genie_agent_creator_matches_app_qualified_name():
    sut = DatabricksGenieAgent.creator(
        name=" Sales Genie ",
        connection_qualified_name=CONNECTION_QN,
        workspace_id=f" {WORKSPACE_ID} ",
        # "e" + combining acute (NFD) must normalise to the precomposed form (NFC).
        space_id="01ef-café",
    )

    assert sut.qualified_name == (
        "default/databricks/1712345678/1234567890123456/genie-spaces/01ef-café"
    )
    assert sut.name == "Sales Genie"
    assert sut.asset_source_id == "01ef-café"
    assert sut.databricks_genie_agent_workspace_id == WORKSPACE_ID
    _assert_connection(sut)
    sut.validate()


@pytest.mark.parametrize(
    "notebook_path, expected_qn, expected_name",
    [
        (
            "/Users/someone@example.com/train",
            # The app keeps the leading slash of the path, giving "//".
            "default/databricks/1712345678/1234567890123456//Users/someone@example.com/train",
            "train",
        ),
        (
            "Repos/team/etl",
            "default/databricks/1712345678/1234567890123456/Repos/team/etl",
            "etl",
        ),
    ],
)
def test_notebook_creator_matches_app_qualified_name(
    notebook_path, expected_qn, expected_name
):
    sut = DatabricksNotebook.creator(
        connection_qualified_name=CONNECTION_QN,
        workspace_id=WORKSPACE_ID,
        notebook_path=notebook_path,
    )

    assert sut.qualified_name == expected_qn
    assert sut.name == expected_name
    assert sut.databricks_notebook_path == notebook_path
    assert sut.databricks_notebook_workspace_id == WORKSPACE_ID
    _assert_connection(sut)
    sut.validate()


@pytest.mark.parametrize(
    "creator, kwargs, message",
    [
        (
            DatabricksDashboard.creator,
            {"name": "d", "workspace_id": WORKSPACE_ID, "dashboard_id": None},
            "dashboard_id is required",
        ),
        (
            DatabricksDashboard.creator,
            {"name": "d", "workspace_id": " ", "dashboard_id": "x"},
            "workspace_id cannot be blank",
        ),
        (
            DatabricksGenieAgent.creator,
            {"name": "g", "workspace_id": WORKSPACE_ID, "space_id": "  "},
            "space_id cannot be blank",
        ),
        (
            DatabricksGenieAgent.creator,
            {"name": None, "workspace_id": WORKSPACE_ID, "space_id": "s"},
            "name is required",
        ),
        (
            DatabricksNotebook.creator,
            {"workspace_id": WORKSPACE_ID, "notebook_path": None},
            "notebook_path is required",
        ),
        (
            DatabricksNotebook.creator,
            {"workspace_id": WORKSPACE_ID, "notebook_path": "/Users/x/"},
            "name cannot be blank",
        ),
    ],
)
def test_workspace_scoped_creators_reject_bad_inputs(creator, kwargs, message):
    with pytest.raises(ValueError, match=message):
        creator(connection_qualified_name=CONNECTION_QN, **kwargs)


# ---------------------------------------------------------------------------
# DatabricksAIModelVersion: {model_qn}/version/{version}
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("version", [3, "3"])
def test_ai_model_version_creator_matches_app_qualified_name(version):
    sut = DatabricksAIModelVersion.creator(
        model_qualified_name=MODEL_QN, version=version
    )

    assert sut.qualified_name == f"{MODEL_QN}/version/3"
    assert sut.name == "churn_model_v3"
    assert sut.databricks_ai_model_version_id == 3
    assert sut.ai_model_qualified_name == MODEL_QN
    assert sut.database_qualified_name == DATABASE_QN
    assert sut.schema_qualified_name == SCHEMA_QN
    assert sut.databricks_ai_model_context.unique_attributes == {
        "qualifiedName": MODEL_QN
    }
    _assert_connection(sut)
    sut.validate()


@pytest.mark.parametrize(
    "model_qn, version, message",
    [
        # The app skips versions it cannot number, so the creator never emits "version/None".
        (MODEL_QN, None, "version is required"),
        (MODEL_QN, " ", "version cannot be blank"),
        (None, 1, "model_qualified_name is required"),
        (SCHEMA_QN, 1, "Invalid model_qualified_name"),
    ],
)
def test_ai_model_version_creator_rejects_bad_inputs(model_qn, version, message):
    with pytest.raises(ValueError, match=message):
        DatabricksAIModelVersion.creator(model_qualified_name=model_qn, version=version)


# ---------------------------------------------------------------------------
# DatabricksUnityCatalogTag: {conn}/tag/{name}
# ---------------------------------------------------------------------------


def test_unity_catalog_tag_creator_matches_app_qualified_name():
    sut = DatabricksUnityCatalogTag.creator(
        name="pii", connection_qualified_name=CONNECTION_QN, allowed_values=["high"]
    )

    assert sut.qualified_name == "default/databricks/1712345678/tag/pii"
    assert sut.name == "pii"
    assert sut.tag_allowed_values == ["high"]
    _assert_connection(sut)
    sut.validate(for_creation=True)


def test_unity_catalog_tag_creator_without_allowed_values_is_valid_for_creation():
    sut = DatabricksUnityCatalogTag.creator(
        name="pii", connection_qualified_name=CONNECTION_QN
    )

    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qn, message",
    [
        (None, CONNECTION_QN, "name is required"),
        ("pii", "", "connection_qualified_name cannot be blank"),
    ],
)
def test_unity_catalog_tag_creator_rejects_bad_inputs(name, connection_qn, message):
    with pytest.raises(ValueError, match=message):
        DatabricksUnityCatalogTag.creator(
            name=name, connection_qualified_name=connection_qn
        )


# ---------------------------------------------------------------------------
# ContextRepository -> Skill -> SkillArtifact
# ---------------------------------------------------------------------------

SCOPE_OWNER = "someone@example.com"
REPO_QN = f"{CONNECTION_QN}/skills/{SCOPE_OWNER}"
SKILL_QN = f"{CONNECTION_QN}/skill/{SCOPE_OWNER}/sales-report"


def test_context_repository_creator_matches_app_qualified_name():
    sut = ContextRepository.creator(
        scope_owner=SCOPE_OWNER, connection_qualified_name=CONNECTION_QN
    )

    assert (
        sut.qualified_name == "default/databricks/1712345678/skills/someone@example.com"
    )
    assert sut.name == SCOPE_OWNER
    _assert_connection(sut)
    sut.validate()


def test_skill_creator_matches_app_qualified_name():
    sut = Skill.creator(name="sales-report", context_repository_qualified_name=REPO_QN)

    assert sut.qualified_name == (
        "default/databricks/1712345678/skill/someone@example.com/sales-report"
    )
    assert sut.name == "sales-report"
    assert sut.context_source_repository.unique_attributes == {"qualifiedName": REPO_QN}
    _assert_connection(sut)
    sut.validate()


@pytest.mark.parametrize(
    "relative_path, expected_name",
    [("SKILL.md", "SKILL.md"), ("scripts/run.py", "run.py")],
)
def test_skill_artifact_creator_matches_app_qualified_name(
    relative_path, expected_name
):
    sut = SkillArtifact.creator(
        skill_qualified_name=SKILL_QN, relative_path=relative_path, file_type="txt"
    )

    assert sut.qualified_name == f"{SKILL_QN}/artifact/{relative_path}"
    assert sut.name == expected_name
    assert sut.file_type == "txt"
    assert sut.skill_source.unique_attributes == {"qualifiedName": SKILL_QN}
    _assert_connection(sut)
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "creator, kwargs, message",
    [
        (
            ContextRepository.creator,
            {"scope_owner": " ", "connection_qualified_name": CONNECTION_QN},
            "scope_owner cannot be blank",
        ),
        (
            Skill.creator,
            {"name": "s", "context_repository_qualified_name": CONNECTION_QN},
            "Invalid context_repository_qualified_name",
        ),
        (
            Skill.creator,
            {"name": None, "context_repository_qualified_name": REPO_QN},
            "name is required",
        ),
        (
            SkillArtifact.creator,
            {
                "skill_qualified_name": SKILL_QN,
                "relative_path": "a.md",
                "file_type": None,
            },
            "file_type is required",
        ),
        (
            SkillArtifact.creator,
            {
                "skill_qualified_name": REPO_QN,
                "relative_path": "a.md",
                "file_type": "txt",
            },
            "Invalid skill_qualified_name",
        ),
    ],
)
def test_agentic_creators_reject_bad_inputs(creator, kwargs, message):
    with pytest.raises(ValueError, match=message):
        creator(**kwargs)


@pytest.mark.parametrize(
    "asset_type, kwargs",
    [
        (DatabricksExternalLocation, {"name": "raw_bucket"}),
        (DatabricksUnityCatalogTag, {"name": "pii"}),
        (ContextRepository, {"scope_owner": SCOPE_OWNER}),
    ],
)
def test_create_alias(asset_type, kwargs):
    sut = asset_type.create(connection_qualified_name=CONNECTION_QN, **kwargs)

    assert (
        sut.qualified_name
        == asset_type.creator(
            connection_qualified_name=CONNECTION_QN, **kwargs
        ).qualified_name
    )
