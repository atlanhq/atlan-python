import pytest

from pyatlan.model.assets import (
    Agentic,
    Artifact,
    Context,
    ContextArtifact,
    ContextRepository,
    Skill,
    SkillArtifact,
)


def test_agentic_type_name():
    sut = Agentic()
    assert sut.type_name == "Agentic"


def test_agentic_type_name_is_immutable():
    sut = Agentic()
    with pytest.raises(TypeError):
        sut.type_name = "NotAgentic"


def test_type_hierarchy():
    """Verify MRO: concrete types extend through Agentic → Catalog."""
    assert issubclass(Skill, Agentic)
    assert issubclass(SkillArtifact, Artifact)
    assert issubclass(Artifact, Agentic)
    assert issubclass(ContextRepository, Context)
    assert issubclass(ContextArtifact, Context)
    assert issubclass(Context, Agentic)


def test_isinstance_checks():
    """Creator instances are recognizable as their parent types."""
    skill = Skill.creator(name="test-skill")
    assert isinstance(skill, Skill)
    assert isinstance(skill, Agentic)

    repo = ContextRepository.creator(name="test-repo")
    assert isinstance(repo, ContextRepository)
    assert isinstance(repo, Context)
    assert isinstance(repo, Agentic)
