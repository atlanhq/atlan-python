from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    ContextArtifact,
    ContextRepository,
    Skill,
    SkillArtifact,
)
from pyatlan.model.enums import CertificateStatus, EntityStatus, FileType
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("AGENTIC")

SKILL_NAME = f"{MODULE_NAME}-skill"
SKILL_ARTIFACT_NAME = f"{MODULE_NAME}-skill-artifact"
CONTEXT_REPO_NAME = f"{MODULE_NAME}-context-repo"
CONTEXT_ARTIFACT_NAME = f"{MODULE_NAME}-context-artifact"

CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."


# ── Skill fixtures ──────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def skill(client: AtlanClient) -> Generator[Skill, None, None]:
    to_create = Skill.creator(name=SKILL_NAME)
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Skill)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Skill)


@pytest.fixture(scope="module")
def skill_artifact(
    client: AtlanClient, skill: Skill
) -> Generator[SkillArtifact, None, None]:
    assert skill.qualified_name
    to_create = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=skill.qualified_name,
        file_type=FileType.TXT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SkillArtifact)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SkillArtifact)


# ── Context fixtures ────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def context_repository(
    client: AtlanClient,
) -> Generator[ContextRepository, None, None]:
    to_create = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ContextRepository)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ContextRepository)


@pytest.fixture(scope="module")
def context_artifact(
    client: AtlanClient, context_repository: ContextRepository
) -> Generator[ContextArtifact, None, None]:
    assert context_repository.qualified_name
    to_create = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=context_repository.qualified_name,
        file_type=FileType.TXT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ContextArtifact)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ContextArtifact)


# ── Skill tests ─────────────────────────────────────────────────────────────


def test_skill(client: AtlanClient, skill: Skill):
    assert skill
    assert skill.guid
    assert skill.qualified_name
    assert skill.name == SKILL_NAME


def test_skill_artifact(
    client: AtlanClient, skill: Skill, skill_artifact: SkillArtifact
):
    assert skill_artifact
    assert skill_artifact.guid
    assert skill_artifact.qualified_name
    assert skill_artifact.name == SKILL_ARTIFACT_NAME


@pytest.mark.order(after="test_skill_artifact")
def test_retrieve_skill(client: AtlanClient, skill: Skill):
    retrieved = client.asset.get_by_guid(
        skill.guid, asset_type=Skill, ignore_relationships=False
    )
    assert retrieved
    assert retrieved.guid == skill.guid
    assert retrieved.qualified_name == skill.qualified_name
    assert retrieved.name == SKILL_NAME


@pytest.mark.order(after="test_skill_artifact")
def test_update_skill_certificate(client: AtlanClient, skill: Skill):
    assert skill.name
    assert skill.qualified_name
    updated = client.asset.update_certificate(
        name=skill.name,
        asset_type=Skill,
        qualified_name=skill.qualified_name,
        message=CERTIFICATE_MESSAGE,
        certificate_status=CERTIFICATE_STATUS,
    )
    assert updated
    assert updated.certificate_status == CERTIFICATE_STATUS


# ── Context tests ───────────────────────────────────────────────────────────


def test_context_repository(client: AtlanClient, context_repository: ContextRepository):
    assert context_repository
    assert context_repository.guid
    assert context_repository.qualified_name
    assert context_repository.name == CONTEXT_REPO_NAME


def test_context_artifact(
    client: AtlanClient,
    context_repository: ContextRepository,
    context_artifact: ContextArtifact,
):
    assert context_artifact
    assert context_artifact.guid
    assert context_artifact.qualified_name
    assert context_artifact.name == CONTEXT_ARTIFACT_NAME


@pytest.mark.order(after="test_context_artifact")
def test_retrieve_context_repository(
    client: AtlanClient, context_repository: ContextRepository
):
    retrieved = client.asset.get_by_guid(
        context_repository.guid,
        asset_type=ContextRepository,
        ignore_relationships=False,
    )
    assert retrieved
    assert retrieved.guid == context_repository.guid
    assert retrieved.qualified_name == context_repository.qualified_name
    assert retrieved.name == CONTEXT_REPO_NAME


@pytest.mark.order(after="test_context_artifact")
def test_delete_context_artifact(
    client: AtlanClient, context_artifact: ContextArtifact
):
    response = client.asset.delete_by_guid(context_artifact.guid)
    assert response
    deleted = response.assets_deleted(asset_type=ContextArtifact)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == context_artifact.guid
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_context_artifact")
def test_restore_context_artifact(
    client: AtlanClient, context_artifact: ContextArtifact
):
    assert context_artifact.qualified_name
    assert client.asset.restore(
        asset_type=ContextArtifact,
        qualified_name=context_artifact.qualified_name,
    )
    restored = client.asset.get_by_qualified_name(
        asset_type=ContextArtifact,
        qualified_name=context_artifact.qualified_name,
    )
    assert restored
    assert restored.guid == context_artifact.guid
    assert restored.status == EntityStatus.ACTIVE
