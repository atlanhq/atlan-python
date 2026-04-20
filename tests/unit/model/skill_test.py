import pytest

from pyatlan.model.assets import Skill

SKILL_NAME = "my-test-skill"


@pytest.mark.parametrize(
    "name, message",
    [
        (None, "name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(name: str, message: str):
    with pytest.raises(ValueError, match=message):
        Skill.creator(name=name)


def test_creator():
    sut = Skill.creator(name=SKILL_NAME)

    assert sut.name == SKILL_NAME
    assert sut.type_name == "Skill"
    assert sut.qualified_name
    assert sut.qualified_name.startswith("default/skill/")


def test_creator_generates_unique_qualified_names():
    sut1 = Skill.creator(name=SKILL_NAME)
    sut2 = Skill.creator(name=SKILL_NAME)

    assert sut1.qualified_name != sut2.qualified_name


def test_skill_version_getter_setter():
    sut = Skill.creator(name=SKILL_NAME)
    assert sut.skill_version is None

    sut.skill_version = "1.0.0"
    assert sut.skill_version == "1.0.0"


def test_skill_artifacts_getter_setter():
    sut = Skill.creator(name=SKILL_NAME)
    assert sut.skill_artifacts is None

    sut.skill_artifacts = []
    assert sut.skill_artifacts == []


def test_type_name_is_immutable():
    sut = Skill.creator(name=SKILL_NAME)
    with pytest.raises(TypeError):
        sut.type_name = "NotSkill"
