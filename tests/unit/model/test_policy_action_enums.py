"""Tests for policy-action enums added for the Admin Export utility (BLDX-1505).

These mirror the Java SDK enums in `com.atlan.model.enums`. The Admin Export
utility reads policy actions from the metadata lakehouse as raw Ranger slugs
(the enum *value*) and converts each to its enum *name* to preserve legacy
output parity, so the slug -> name mapping must match the Java SDK exactly.
"""

import pytest

from pyatlan.model.enums import AdminAction, PersonaAIAction, TypeDefAction

# Slug (Ranger value) -> enum name, copied verbatim from the Java SDK enums.
PERSONA_AI_ACTIONS = {
    "persona-ai-application-read": "APP_READ",
    "persona-ai-application-create": "APP_CREATE",
    "persona-ai-application-update": "APP_UPDATE",
    "persona-ai-application-delete": "APP_DELETE",
    "persona-ai-application-business-update-metadata": "APP_UPDATE_CM",
    "persona-ai-application-add-terms": "APP_ADD_TERMS",
    "persona-ai-application-remove-terms": "APP_REMOVE_TERMS",
    "persona-ai-application-add-classification": "APP_ADD_ATLAN_TAGS",
    "persona-ai-application-remove-classification": "APP_REMOVE_ATLAN_TAGS",
    "persona-ai-model-read": "MODEL_READ",
    "persona-ai-model-create": "MODEL_CREATE",
    "persona-ai-model-update": "MODEL_UPDATE",
    "persona-ai-model-delete": "MODEL_DELETE",
    "persona-ai-model-business-update-metadata": "MODEL_UPDATE_CM",
    "persona-ai-model-add-terms": "MODEL_ADD_TERMS",
    "persona-ai-model-remove-terms": "MODEL_REMOVE_TERMS",
    "persona-ai-model-add-classification": "MODEL_ADD_ATLAN_TAGS",
    "persona-ai-model-remove-classification": "MODEL_REMOVE_ATLAN_TAGS",
}

ADMIN_ACTIONS = {
    "admin-task-cud": "ADMIN_TASK_CUD",
    "admin-audits": "ADMIN_AUDITS",
    "admin-export": "ADMIN_EXPORT",
    "admin-featureFlag-cud": "ADMIN_FEATURE_FLAG_CUD",
    "admin-import": "ADMIN_IMPORT",
    "admin-purge": "ADMIN_PURGE",
    "admin-repair-index": "ADMIN_REPAIR_INDEX",
}

TYPE_DEF_ACTIONS = {
    "type-create": "CREATE",
    "type-read": "READ",
    "type-update": "UPDATE",
    "type-delete": "DELETE",
    "entity-add-label": "ADD_LABEL",
    "entity-remove-label": "REMOVE_LABEL",
    "add-relationship": "ADD_RELATIONSHIP",
    "update-relationship": "UPDATE_RELATIONSHIP",
    "remove-relationship": "REMOVE_RELATIONSHIP",
}


@pytest.mark.parametrize(
    ("enum_cls", "expected"),
    [
        (PersonaAIAction, PERSONA_AI_ACTIONS),
        (AdminAction, ADMIN_ACTIONS),
        (TypeDefAction, TYPE_DEF_ACTIONS),
    ],
)
def test_enum_members_match_java_sdk(enum_cls, expected):
    """Every member's (value -> name) pair matches the Java SDK, with no extras."""
    actual = {member.value: member.name for member in enum_cls}
    assert actual == expected


@pytest.mark.parametrize(
    ("enum_cls", "expected"),
    [
        (PersonaAIAction, PERSONA_AI_ACTIONS),
        (AdminAction, ADMIN_ACTIONS),
        (TypeDefAction, TYPE_DEF_ACTIONS),
    ],
)
def test_slug_resolves_to_enum_name(enum_cls, expected):
    """Slug -> name lookup (what the Admin Export utility relies on)."""
    for slug, name in expected.items():
        assert enum_cls(slug).name == name


def test_enums_are_str_backed():
    """Values serialize as their raw Ranger slug (str, Enum)."""
    assert isinstance(PersonaAIAction.APP_READ, str)
    assert PersonaAIAction.APP_READ == "persona-ai-application-read"
    assert AdminAction.ADMIN_EXPORT == "admin-export"
    assert TypeDefAction.ADD_RELATIONSHIP == "add-relationship"
