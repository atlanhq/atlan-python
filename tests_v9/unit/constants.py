# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

# Non-validation constants from the legacy test suite.
from tests.unit.constants import (  # noqa: F401, F403
    APPLICABLE_AI_ASSET_TYPES,
    APPLICABLE_ASSET_TYPES,
    APPLICABLE_CONNECTIONS,
    APPLICABLE_DOMAIN_TYPES,
    APPLICABLE_DOMAINS,
    APPLICABLE_ENTITY_TYPES,
    APPLICABLE_GLOSSARIES,
    APPLICABLE_GLOSSARY_TYPES,
    APPLICABLE_OTHER_ASSET_TYPES,
    TEST_ATTRIBUTE_DEF_APPLICABLE_ASSET_TYPES,
    TEST_ENUM_DEF,
    TEST_STRUCT_DEF,
)
from tests.unit.model.constants import *  # noqa: F401, F403

from pyatlan_v9.model.assets import AtlasGlossary
from pyatlan_v9.model.enums import AtlanWorkflowPhase
from pyatlan_v9.model.workflow import (
    ScheduleQueriesSearchRequest,
    WorkflowMetadata,
    WorkflowResponse,
    WorkflowSpec,
)

TEST_ASSET_CLIENT_METHODS = {
    "find_personas_by_name": [
        ([[123], ["attributes"]], "name\n  str type expected"),
        ([None, ["attributes"]], "none is not an allowed value"),
        (["name", 123], "value is not a valid list"),
    ],
    "find_purposes_by_name": [
        ([[123], ["attributes"]], "name\n  str type expected"),
        ([None, ["attributes"]], "none is not an allowed value"),
        (["name", 123], "value is not a valid list"),
    ],
    "get_by_qualified_name": [
        ([[123], "asset-type"], "name\n  str type expected"),
        ([None, "asset-type"], "none is not an allowed value"),
        (["qn", None], "none is not an allowed value"),
        (["qn", "asset-type"], "asset_type\n  a class is expected"),
    ],
    "get_by_guid": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "retrieve_minimal": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "upsert": [
        ([123], "entity\n  value is not a valid Asset or List[Asset]"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity -> 0\n  instance of Asset expected"),
        ([[None]], "entity -> 0\n  none is not an allowed value"),
    ],
    "save": [
        ([123], "entity\n  value is not a valid Asset or List[Asset]"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity -> 0\n  instance of Asset expected"),
        ([[None]], "entity -> 0\n  none is not an allowed value"),
    ],
    "upsert_merging_cm": [
        ([123], "entity\n  value is not a valid Asset or List[Asset]"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity -> 0\n  instance of Asset expected"),
        ([[None]], "entity -> 0\n  none is not an allowed value"),
    ],
    "save_merging_cm": [
        ([123], "entity\n  value is not a valid Asset or List[Asset]"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity -> 0\n  instance of Asset expected"),
        ([[None]], "entity -> 0\n  none is not an allowed value"),
    ],
    "update_merging_cm": [
        ([123], "entity\n  instance of Asset expected"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  instance of Asset expected"),
        ([[None]], "entity\n  instance of Asset expected"),
    ],
    "upsert_replacing_cm": [
        ([123], "entity\n  value is not a valid Asset or List[Asset]"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity -> 0\n  instance of Asset expected"),
        ([[None]], "entity -> 0\n  none is not an allowed value"),
    ],
    "save_replacing_cm": [
        ([123], "entity\n  value is not a valid Asset or List[Asset]"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity -> 0\n  instance of Asset expected"),
        ([[None]], "entity -> 0\n  none is not an allowed value"),
    ],
    "update_replacing_cm": [
        ([123], "entity\n  instance of Asset expected"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  instance of Asset expected"),
        ([[None]], "entity\n  instance of Asset expected"),
    ],
    "purge_by_guid": [
        ([int], "guid\n  value is not a valid str or List[str]"),
        ([None], "none is not an allowed value"),
        ([[int]], "guid -> 0\n  str type expected"),
        ([[None]], "guid -> 0\n  none is not an allowed value"),
    ],
    "restore": [
        (["asset-type", [123]], "name\n  str type expected"),
        (["asset-type", None], "none is not an allowed value"),
        ([None, "qn"], "none is not an allowed value"),
        (["asset-type", "qn"], "asset_type\n  a class is expected"),
    ],
    "add_atlan_tags": [
        (["asset-type", [123], "tag-name"], "name\n  str type expected"),
        (["asset-type", None, "tag-name"], "none is not an allowed value"),
        ([None, "qn", "tag-name"], "none is not an allowed value"),
        (["asset-type", "qn", "tag-name"], "asset_type\n  a class is expected"),
        ([AtlasGlossary, "qn", [int]], "atlan_tag_names -> 0\n  str type expected"),
        ([AtlasGlossary, "qn", None], "none is not an allowed value"),
    ],
    "update_atlan_tags": [
        (["asset-type", [123], "tag-name"], "name\n  str type expected"),
        (["asset-type", None, "tag-name"], "none is not an allowed value"),
        ([None, "qn", "tag-name"], "none is not an allowed value"),
        (["asset-type", "qn", "tag-name"], "asset_type\n  a class is expected"),
        ([AtlasGlossary, "qn", [int]], "atlan_tag_names -> 0\n  str type expected"),
        ([AtlasGlossary, "qn", None], "none is not an allowed value"),
    ],
    "remove_atlan_tag": [
        (["asset-type", [123], "tag-name"], "name\n  str type expected"),
        (["asset-type", None, "tag-name"], "none is not an allowed value"),
        ([None, "qn", "tag-name"], "none is not an allowed value"),
        (["asset-type", "qn", "tag-name"], "asset_type\n  a class is expected"),
        ([AtlasGlossary, "qn", [123]], "atlan_tag_name\n  str type expected"),
        ([AtlasGlossary, "qn", None], "none is not an allowed value"),
    ],
    "remove_atlan_tags": [
        (["asset-type", [123], ["tag-name"]], "name\n  str type expected"),
        (["asset-type", None, ["tag-name"]], "none is not an allowed value"),
        ([None, "qn", ["tag-name"]], "none is not an allowed value"),
        (["asset-type", "qn", ["tag-name"]], "asset_type\n  a class is expected"),
        (
            [AtlasGlossary, "qn", "tag-name"],
            "atlan_tag_names\n  value is not a valid list",
        ),
        ([AtlasGlossary, "qn", None], "none is not an allowed value"),
    ],
    "update_certificate": [
        (["asset-type", [123], "name", "cert-status"], "name\n  str type expected"),
        (
            ["asset-type", None, "name", "cert-status"],
            "none is not an allowed value",
        ),
        ([None, "qn", "tag-name", "cert-status"], "none is not an allowed value"),
        (
            ["asset-type", "qn", "name", "cert-status"],
            "asset_type\n  a class is expected",
        ),
        (
            [AtlasGlossary, "qn", [123], "cert-status"],
            "name\n  str type expected",
        ),
        ([AtlasGlossary, "qn", None, "cert-status"], "none is not an allowed value"),
        (
            [AtlasGlossary, "qn", "name", "cert-status"],
            "certificate_status\n  value is not a valid enumeration member",
        ),
        ([AtlasGlossary, "qn", "name", None], "none is not an allowed value"),
    ],
    "remove_certificate": [
        (["asset-type", [123], "name"], "name\n  str type expected"),
        (
            ["asset-type", None, "name"],
            "none is not an allowed value",
        ),
        ([None, "qn", "tag-name"], "none is not an allowed value"),
        (
            ["asset-type", "qn", "name"],
            "asset_type\n  a class is expected",
        ),
        (
            [AtlasGlossary, "qn", [123]],
            "name\n  str type expected",
        ),
        ([AtlasGlossary, "qn", None], "none is not an allowed value"),
    ],
    "update_announcement": [
        (["asset-type", [123], "name"], "name\n  str type expected"),
        (
            ["asset-type", None, "name"],
            "none is not an allowed value",
        ),
        ([None, "qn", "tag-name", "announcement"], "none is not an allowed value"),
        (
            ["asset-type", "qn", "name"],
            "asset_type\n  a class is expected",
        ),
        (
            [AtlasGlossary, "qn", [123]],
            "name\n  str type expected",
        ),
        ([AtlasGlossary, "qn", None], "none is not an allowed value"),
    ],
    "update_custom_metadata_attributes": [
        ([[123], ["cm"]], "guid\n  str type expected"),
        ([None, ["cm"]], "none is not an allowed value"),
        (["name", 123], "custom_metadata\n  instance of CustomMetadataDict expected"),
        (["name", None], "none is not an allowed value"),
    ],
    "replace_custom_metadata": [
        ([[123], ["cm"]], "guid\n  str type expected"),
        ([None, ["cm"]], "none is not an allowed value"),
        (["name", 123], "custom_metadata\n  instance of CustomMetadataDict expected"),
        (["name", None], "none is not an allowed value"),
    ],
    "remove_custom_metadata": [
        ([[123], ["cm"]], "guid\n  str type expected"),
        ([None, ["cm"]], "none is not an allowed value"),
        (["name", [123]], "cm_name\n  str type expected"),
        (["name", None], "none is not an allowed value"),
    ],
    "append_terms": [
        (["asset-type", "terms"], "asset_type\n  a class is expected"),
        ([None, "cm"], "none is not an allowed value"),
        (
            [AtlasGlossary, [123]],
            "terms -> 0\n  instance of AtlasGlossaryTerm expected",
        ),
        ([AtlasGlossary, None], "none is not an allowed value"),
    ],
    "replace_terms": [
        (["asset-type", "terms"], "asset_type\n  a class is expected"),
        ([None, "cm"], "none is not an allowed value"),
        (
            [AtlasGlossary, [123]],
            "terms -> 0\n  instance of AtlasGlossaryTerm expected",
        ),
        ([AtlasGlossary, None], "none is not an allowed value"),
    ],
    "remove_terms": [
        (["asset-type", "terms"], "asset_type\n  a class is expected"),
        ([None, "cm"], "none is not an allowed value"),
        (
            [AtlasGlossary, [123]],
            "terms -> 0\n  instance of AtlasGlossaryTerm expected",
        ),
        ([AtlasGlossary, None], "none is not an allowed value"),
    ],
    "find_connections_by_name": [
        ([[123], "connector-type"], "name\n  str type expected"),
        ([None, "connector-type"], "none is not an allowed value"),
        (["name", [123]], "connector_type\n  value is not a valid enumeration member"),
        (["name", None], "none is not an allowed value"),
    ],
    "find_category_fast_by_name": [
        ([[123], "glossary-qn"], "name\n  str type expected"),
        ([None, "glossary-qn"], "none is not an allowed value"),
        (["name", [123]], "glossary_qualified_name\n  str type expected"),
        (["name", None], "none is not an allowed value"),
    ],
    "find_term_fast_by_name": [
        ([[123], "glossary-qn"], "name\n  str type expected"),
        ([None, "glossary-qn"], "none is not an allowed value"),
        (["name", [123]], "glossary_qualified_name\n  str type expected"),
        (["name", None], "none is not an allowed value"),
    ],
    "find_term_by_name": [
        ([[123], "glossary-qn"], "name\n  str type expected"),
        ([None, "glossary-qn"], "none is not an allowed value"),
        (["name", [123]], "glossary_name\n  str type expected"),
        (["name", None], "none is not an allowed value"),
    ],
    "find_domain_by_name": [
        (
            [None, ["attributes"]],
            "1 validation error for FindDomainByName\nname\n  none is not an allowed value",
        ),
        (
            [" ", ["attributes"]],
            "1 validation error for FindDomainByName\nname\n  ensure this value has at least 1 characters",
        ),
        (
            ["test-domain", "attributes"],
            "1 validation error for FindDomainByName\nattributes\n  value is not a valid list",
        ),
    ],
    "find_product_by_name": [
        (
            [None, ["attributes"]],
            "1 validation error for FindProductByName\nname\n  none is not an allowed value",
        ),
        (
            [" ", ["attributes"]],
            "1 validation error for FindProductByName\nname\n  ensure this value has at least 1 characters",
        ),
        (
            ["test-product", "attributes"],
            "1 validation error for FindProductByName\nattributes\n  value is not a valid list",
        ),
    ],
}

TEST_ADMIN_CLIENT_METHODS = {
    "get_keycloak_events": [
        (
            ["keycloak-req"],
            "keycloak_request\n  instance of KeycloakEventRequest expected",
        ),
        ([None], "none is not an allowed value"),
    ],
    "get_admin_events": [
        (["admin-req"], "admin_request\n  instance of AdminEventRequest expected"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_AUDIT_CLIENT_METHODS = {
    "search": [
        (["audit-search-req"], "criteria\n  instance of AuditSearchRequest expected"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_GROUP_CLIENT_METHODS = {
    "create": [
        ("group", "too many positional arguments"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        (["group"], "group\n  instance of AtlanGroup expected"),
        ([None], "none is not an allowed value"),
    ],
    "purge": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "get": [
        (
            [None, None, None, "count", 123],
            "count\n  value is not a valid boolean",
        ),
        ([None, None, None, None, 123], "none is not an allowed value"),
        ([None, None, None, True, "offset"], "offset\n  value is not a valid int"),
        ([None, None, None, True, None], "none is not an allowed value"),
    ],
    "get_all": [
        (["limit"], "limit\n  value is not a valid int"),
        ([None], "none is not an allowed value"),
    ],
    "get_by_name": [
        ([[123]], "alias\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "get_members": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "remove_users": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_ROLE_CLIENT_METHODS = {
    "get": [
        (["limit", None, None, True, 123], "limit\n  value is not a valid int"),
        ([None, None, None, True, 123], "none is not an allowed value"),
        (
            [123, None, None, "count", 123],
            "count\n  value is not a valid boolean",
        ),
        ([123, None, None, None, "offset"], "none is not an allowed value"),
        ([123, None, None, True, "offset"], "offset\n  value is not a valid int"),
        ([123, None, None, True, None], "none is not an allowed value"),
    ],
}

TEST_SL_CLIENT_METHODS = {
    "search": [
        (["search-log-req"], "criteria\n  instance of SearchLogRequest expected"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_TOKEN_CLIENT_METHODS = {
    "get": [
        (
            [None, None, None, "count", 123],
            "count\n  value is not a valid boolean",
        ),
        ([None, None, None, None, 123], "none is not an allowed value"),
        ([None, None, None, True, "offset"], "offset\n  value is not a valid int"),
        ([None, None, None, True, None], "none is not an allowed value"),
    ],
    "get_by_name": [
        ([[123]], "display_name\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "get_by_id": [
        ([[123]], "client_id\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "create": [
        ([[123]], "display_name\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        ([[123], "display-name"], "guid\n  str type expected"),
        ([None, "display-name"], "none is not an allowed value"),
        (["guid", [[123]]], "display_name\n  str type expected"),
        (["guid", None], "none is not an allowed value"),
    ],
    "purge": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_TYPEDEF_CLIENT_METHODS = {
    "get": [
        (
            ["atlan-type-category"],
            "type_category\n  value is not a valid AtlanTypeCategory or List[AtlanTypeCategory]",
        ),
        ([None], "none is not an allowed value"),
    ],
    "create": [
        (["typedef"], "typedef\n  instance of TypeDef expected"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        (["typedef"], "typedef\n  instance of TypeDef expected"),
        ([None], "none is not an allowed value"),
    ],
    "purge": [
        ([[123], "typedef"], "name\n  str type expected"),
        ([None, "typedef"], "none is not an allowed value"),
        (["name", "typedef"], "typedef_type\n  instance of type expected"),
        (["name", None], "none is not an allowed value"),
    ],
}

TEST_USER_CLIENT_METHODS = {
    "create": [
        ([123], "users\n  value is not a valid list"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        ([[123], "user"], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
        (["guid", "user"], "user\n  instance of AtlanUser expected"),
        (["guid", None], "none is not an allowed value"),
    ],
    "change_role": [
        ([[123], "role-id"], "guid\n  str type expected"),
        ([None, "role-id"], "none is not an allowed value"),
        (["guid", [123]], "role_id\n  str type expected"),
        (["guid", None], "none is not an allowed value"),
    ],
    "get": [
        (
            [None, None, None, "count", 123],
            "count\n  value is not a valid boolean",
        ),
        ([None, None, None, None, 123], "none is not an allowed value"),
        ([None, None, None, True, "offset"], "offset\n  value is not a valid int"),
        ([None, None, None, True, None], "none is not an allowed value"),
    ],
    "get_all": [
        (["limit"], "limit\n  value is not a valid int"),
        ([None], "none is not an allowed value"),
    ],
    "get_by_email": [
        ([[123]], "email\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "get_by_username": [
        ([[123]], "username\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "add_to_groups": [
        ([[123], ["grp-ids"]], "guid\n  str type expected"),
        ([None, ["grp-ids"]], "none is not an allowed value"),
        (["guid", 123], "group_ids\n  value is not a valid list"),
        (["guid", None], "none is not an allowed value"),
    ],
    "get_groups": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "add_as_admin": [
        ([[123], "imp-token"], "asset_guid\n  str type expected"),
        ([None, "imp-token"], "none is not an allowed value"),
        (["guid", [123]], "impersonation_token\n  str type expected"),
        (["guid", None], "none is not an allowed value"),
    ],
    "add_as_viewer": [
        ([[123], "imp-token"], "asset_guid\n  str type expected"),
        ([None, "imp-token"], "none is not an allowed value"),
        (["guid", [123]], "impersonation_token\n  str type expected"),
        (["guid", None], "none is not an allowed value"),
    ],
}

TEST_FILE_CLIENT_METHODS = {
    "generate_presigned_url": [
        ([123], "request\n  instance of PresignedURLRequest expected"),
        ([None], "none is not an allowed value"),
    ],
    "upload_file": [
        ([[123], "file-path"], "presigned_url\n  str type expected"),
        ([None, "file-path"], "none is not an allowed value"),
        (
            ["test-url", [123]],
            "file_path\n  str type expected",
        ),
        (
            ["test-url", None],
            "none is not an allowed value",
        ),
    ],
    "download_file": [
        ([[123], "file-path"], "presigned_url\n  str type expected"),
        ([None, "file-path"], "none is not an allowed value"),
        (
            ["test-url", [123]],
            "file_path\n  str type expected",
        ),
        (
            ["test-url", None],
            "none is not an allowed value",
        ),
    ],
}


TEST_WORKFLOW_CLIENT_METHODS = {
    "update": [
        (["abc"], "instance of Workflow expected"),
        ([None], "none is not an allowed value"),
    ],
    "find_by_type": [
        (["abc"], "value is not a valid enumeration member"),
        ([None], "none is not an allowed value"),
    ],
    "monitor": [
        (["abc", "test-logger"], "instance of WorkflowResponse expected"),
        (
            [
                WorkflowResponse(metadata=WorkflowMetadata(), spec=WorkflowSpec()),
                "test-logger",
            ],
            "instance of Logger expected",
        ),
    ],
    "get_runs": [
        ([[123], AtlanWorkflowPhase.RUNNING, 123, 456], "str type expected"),
        ([None, AtlanWorkflowPhase.RUNNING, 123, 456], "none is not an allowed value"),
    ],
    "stop": [
        ([[123]], "str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "delete": [
        ([[123]], "str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "get_scheduled_run": [
        ([[123]], "str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "find_schedule_query": [
        ([[123], 10], "saved_query_id\n  str type expected"),
        ([None, 10], "none is not an allowed value"),
        (["test-query-id", [123]], "max_results\n  value is not a valid int"),
        (["test-query-id", None], "none is not an allowed value"),
    ],
    "re_run_schedule_query": [
        ([[123]], "schedule_query_id\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "find_schedule_query_between": [
        ([[123], True], "instance of ScheduleQueriesSearchRequest expected"),
        ([None, True], "none is not an allowed value"),
        (
            [ScheduleQueriesSearchRequest(start_date="start", end_date="end"), [123]],
            "missed\n  value is not a valid boolean",
        ),
        (
            [ScheduleQueriesSearchRequest(start_date="start", end_date="end"), None],
            "none is not an allowed value",
        ),
    ],
    "update_owner": [
        ([[123], 10], "workflow_name\n  str type expected"),
        ([None, 10], "none is not an allowed value"),
        (["test-workflow", [123]], "username\n  str type expected"),
        (["test-workflow", None], "none is not an allowed value"),
    ],
}

# Async-specific constants (same as sync but with AsyncCustomMetadataDict)
TEST_ASSET_CLIENT_METHODS_ASYNC = {
    **TEST_ASSET_CLIENT_METHODS,
    "update_custom_metadata_attributes": [
        ([[123], ["cm"]], "guid\n  str type expected"),
        ([None, ["cm"]], "none is not an allowed value"),
        (
            ["name", 123],
            "custom_metadata\n  instance of AsyncCustomMetadataDict expected",
        ),
        (["name", None], "none is not an allowed value"),
    ],
    "replace_custom_metadata": [
        ([[123], ["cm"]], "guid\n  str type expected"),
        ([None, ["cm"]], "none is not an allowed value"),
        (
            ["name", 123],
            "custom_metadata\n  instance of AsyncCustomMetadataDict expected",
        ),
        (["name", None], "none is not an allowed value"),
    ],
}


# Rename create/update keys to creator/updater for v9 sub-clients
_V9_WF_METHODS = dict(TEST_WORKFLOW_CLIENT_METHODS)
TEST_WORKFLOW_CLIENT_METHODS = {  # noqa: F811
    ("updater" if k == "update" else k): v for k, v in _V9_WF_METHODS.items()
}
