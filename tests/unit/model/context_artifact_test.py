import pytest

from pyatlan.model.assets import ContextArtifact
from pyatlan.model.enums import FileType

CONTEXT_ARTIFACT_NAME = "my-test-context-artifact"
CONTEXT_REPO_QUALIFIED_NAME = "default/context/abc123"


@pytest.mark.parametrize(
    "name, context_repository_qualified_name, file_type, message",
    [
        (None, CONTEXT_REPO_QUALIFIED_NAME, FileType.TXT, "name is required"),
        (
            CONTEXT_ARTIFACT_NAME,
            None,
            FileType.TXT,
            "context_repository_qualified_name is required",
        ),
        (
            CONTEXT_ARTIFACT_NAME,
            CONTEXT_REPO_QUALIFIED_NAME,
            None,
            "file_type is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    context_repository_qualified_name: str,
    file_type: FileType,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        ContextArtifact.creator(
            name=name,
            context_repository_qualified_name=context_repository_qualified_name,
            file_type=file_type,
        )


def test_creator():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )

    assert sut.name == CONTEXT_ARTIFACT_NAME
    assert sut.type_name == "ContextArtifact"
    assert sut.file_type == FileType.TXT
    assert sut.qualified_name
    assert sut.qualified_name.startswith(f"{CONTEXT_REPO_QUALIFIED_NAME}/artifact/txt/")
    assert sut.context_repository_qualified_name == CONTEXT_REPO_QUALIFIED_NAME


def test_creator_with_yaml_file_type():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.YAML,
    )

    assert sut.file_type == FileType.YAML
    assert "/artifact/yaml/" in sut.qualified_name


def test_creator_with_sql_file_type():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.SQL,
    )

    assert sut.file_type == FileType.SQL
    assert "/artifact/sql/" in sut.qualified_name


def test_creator_with_md_file_type():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.MD,
    )

    assert sut.file_type == FileType.MD
    assert "/artifact/md/" in sut.qualified_name


def test_creator_populates_context_repository_ref():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )

    assert sut.context_repository is not None
    assert sut.context_repository.qualified_name == CONTEXT_REPO_QUALIFIED_NAME


def test_creator_generates_unique_qualified_names():
    sut1 = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )
    sut2 = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )

    assert sut1.qualified_name != sut2.qualified_name


def test_artifact_version_getter_setter():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )
    assert sut.artifact_version is None

    sut.artifact_version = "2.0"
    assert sut.artifact_version == "2.0"


def test_file_path_getter_setter():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )
    assert sut.file_path is None

    sut.file_path = "s3://bucket/path/to/file.txt"
    assert sut.file_path == "s3://bucket/path/to/file.txt"


def test_type_name_is_immutable():
    sut = ContextArtifact.creator(
        name=CONTEXT_ARTIFACT_NAME,
        context_repository_qualified_name=CONTEXT_REPO_QUALIFIED_NAME,
        file_type=FileType.TXT,
    )
    with pytest.raises(TypeError):
        sut.type_name = "NotContextArtifact"
