import pytest

from pyatlan.model.assets import ContextRepository
from pyatlan.model.enums import ContextLifecycleStatus

CONTEXT_REPO_NAME = "my-test-context-repo"


@pytest.mark.parametrize(
    "name, message",
    [
        (None, "name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(name: str, message: str):
    with pytest.raises(ValueError, match=message):
        ContextRepository.creator(name=name)


def test_creator():
    sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)

    assert sut.name == CONTEXT_REPO_NAME
    assert sut.type_name == "ContextRepository"
    assert sut.qualified_name
    assert sut.qualified_name.startswith("default/context/")


def test_creator_generates_unique_qualified_names():
    sut1 = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    sut2 = ContextRepository.creator(name=CONTEXT_REPO_NAME)

    assert sut1.qualified_name != sut2.qualified_name


def test_lifecycle_status_getter_setter():
    sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    assert sut.context_repository_lifecycle_status is None

    sut.context_repository_lifecycle_status = ContextLifecycleStatus.ACTIVE
    assert sut.context_repository_lifecycle_status == ContextLifecycleStatus.ACTIVE


def test_agent_instructions_getter_setter():
    sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    assert sut.context_repository_agent_instructions is None

    sut.context_repository_agent_instructions = "Use SQL for queries"
    assert sut.context_repository_agent_instructions == "Use SQL for queries"


def test_target_connection_qn_getter_setter():
    sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    assert sut.context_repository_target_connection_qualified_name is None

    sut.context_repository_target_connection_qualified_name = "default/snowflake/123"
    assert (
        sut.context_repository_target_connection_qualified_name
        == "default/snowflake/123"
    )


def test_context_artifacts_getter_setter():
    sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    assert sut.context_artifacts is None

    sut.context_artifacts = []
    assert sut.context_artifacts == []


def test_all_lifecycle_statuses():
    for status in ContextLifecycleStatus:
        sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)
        sut.context_repository_lifecycle_status = status
        assert sut.context_repository_lifecycle_status == status


def test_type_name_is_immutable():
    sut = ContextRepository.creator(name=CONTEXT_REPO_NAME)
    with pytest.raises(TypeError):
        sut.type_name = "NotContextRepository"
