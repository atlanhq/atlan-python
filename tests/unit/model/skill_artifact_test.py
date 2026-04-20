import pytest

from pyatlan.model.assets import SkillArtifact
from pyatlan.model.enums import FileType

SKILL_ARTIFACT_NAME = "my-test-artifact"
SKILL_QUALIFIED_NAME = "default/skill/abc123"


@pytest.mark.parametrize(
    "name, skill_qualified_name, file_type, message",
    [
        (None, SKILL_QUALIFIED_NAME, FileType.TXT, "name is required"),
        (SKILL_ARTIFACT_NAME, None, FileType.TXT, "skill_qualified_name is required"),
        (SKILL_ARTIFACT_NAME, SKILL_QUALIFIED_NAME, None, "file_type is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, skill_qualified_name: str, file_type: FileType, message: str
):
    with pytest.raises(ValueError, match=message):
        SkillArtifact.creator(
            name=name,
            skill_qualified_name=skill_qualified_name,
            file_type=file_type,
        )


def test_creator():
    sut = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )

    assert sut.name == SKILL_ARTIFACT_NAME
    assert sut.type_name == "SkillArtifact"
    assert sut.file_type == FileType.TXT
    assert sut.qualified_name
    assert sut.qualified_name.startswith(f"{SKILL_QUALIFIED_NAME}/artifact/txt/")


def test_creator_with_yaml_file_type():
    sut = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.YAML,
    )

    assert sut.file_type == FileType.YAML
    assert "/artifact/yaml/" in sut.qualified_name


def test_creator_with_sql_file_type():
    sut = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.SQL,
    )

    assert sut.file_type == FileType.SQL
    assert "/artifact/sql/" in sut.qualified_name


def test_creator_populates_skill_source_ref():
    sut = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )

    assert sut.skill_source is not None
    assert sut.skill_source.qualified_name == SKILL_QUALIFIED_NAME


def test_creator_generates_unique_qualified_names():
    sut1 = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )
    sut2 = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )

    assert sut1.qualified_name != sut2.qualified_name


def test_type_name_is_immutable():
    sut = SkillArtifact.creator(
        name=SKILL_ARTIFACT_NAME,
        skill_qualified_name=SKILL_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )
    with pytest.raises(TypeError):
        sut.type_name = "NotSkillArtifact"
