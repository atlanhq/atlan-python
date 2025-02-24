import pytest

from pyatlan.model.assets import Badge
from pyatlan.model.enums import BadgeComparisonOperator, BadgeConditionColor
from pyatlan.model.structs import BadgeCondition

CM_ATTRIBUTE_NAME = "dummy"

CM_SET_NAME = "Monte Carlo"

BADGE_NAME = "bob"

BADGE_CONDITION = BadgeCondition.create(
    badge_condition_operator=BadgeComparisonOperator.EQ,
    badge_condition_value="1",
    badge_condition_colorhex=BadgeConditionColor.RED,
)
CM_ATTR_ID = "WQ6XGXwq9o7UnZlkWyKhQN"


CM_ID = "scAesIb5UhKQdTwu4GuCSN"
BADGE_QUALIFIED_NAME = f"badges/global/{CM_ID}.{CM_ATTR_ID}"
BADGE_METADATA_ATTRIBUTE = f"{CM_ID}.{CM_ATTR_ID}"


@pytest.mark.parametrize(
    "name, cm_name, cm_attribute, badge_conditions, message",
    [
        (None, "Bob", "Dave", [BADGE_CONDITION], "name is required"),
        ("Bob", None, "Dave", [BADGE_CONDITION], "cm_name is required"),
        ("Bob", "", "Dave", [BADGE_CONDITION], "cm_name cannot be blank"),
        ("Bob", "Dave", None, [BADGE_CONDITION], "cm_attribute is required"),
        ("Bob", "Dave", "", [BADGE_CONDITION], "cm_attribute cannot be blank"),
        ("Bob", "tom", "Dave", None, "badge_conditions is required"),
        ("Bob", "tom", "Dave", [], "badge_conditions cannot be an empty list"),
    ],
)
def test_create_when_required_parameters_are_missing_raises_value_error(
    name, cm_name, cm_attribute, badge_conditions, message
):
    with pytest.raises(ValueError, match=message):
        Badge.create(
            name=name,
            cm_name=cm_name,
            cm_attribute=cm_attribute,
            badge_conditions=badge_conditions,
        )


def test_create(mock_custom_metadata_cache):
    mock_custom_metadata_cache.get_attr_id_for_name.return_value = CM_ATTR_ID
    mock_custom_metadata_cache.get_id_for_name.return_value = CM_ID

    badge = Badge.create(
        name=BADGE_NAME,
        cm_name=CM_SET_NAME,
        cm_attribute=CM_ATTRIBUTE_NAME,
        badge_conditions=[BADGE_CONDITION],
    )
    assert badge.name == BADGE_NAME
    assert badge.qualified_name == BADGE_QUALIFIED_NAME
    assert badge.badge_metadata_attribute == f"{CM_ID}.{CM_ATTR_ID}"
    assert badge.badge_conditions == [BADGE_CONDITION]


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, BADGE_QUALIFIED_NAME, "qualified_name is required"),
        (BADGE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Badge.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Badge.create_for_modification(
        qualified_name=BADGE_QUALIFIED_NAME, name=BADGE_NAME
    )

    assert sut.qualified_name == BADGE_QUALIFIED_NAME
    assert sut.name == BADGE_NAME


def test_trim_to_required():
    sut = Badge.create_for_modification(
        qualified_name=BADGE_QUALIFIED_NAME, name=BADGE_NAME
    ).trim_to_required()

    assert sut.qualified_name == BADGE_QUALIFIED_NAME
    assert sut.name == BADGE_NAME
