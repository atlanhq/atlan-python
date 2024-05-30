from pyatlan.model.assets import AtlasGlossary
from pyatlan.model.constants import (
    AssetTypes,
    DomainTypes,
    EntityTypes,
    GlossaryTypes,
    OtherAssetTypes,
)
from pyatlan.model.enums import AtlanWorkflowPhase
from pyatlan.model.workflow import (
    ScheduleQueriesSearchRequest,
    WorkflowMetadata,
    WorkflowResponse,
    WorkflowSchedule,
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
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "none is not an allowed value"),
    ],
    "save": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "none is not an allowed value"),
    ],
    "upsert_merging_cm": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "'NoneType' is not iterable"),
    ],
    "save_merging_cm": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "'NoneType' is not iterable"),
    ],
    "update_merging_cm": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "'NoneType' is not iterable"),
    ],
    "upsert_replacing_cm": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "'NoneType' is not iterable"),
    ],
    "save_replacing_cm": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "'NoneType' is not iterable"),
    ],
    "update_replacing_cm": [
        ([123], "entity\n  argument of type 'int' is not iterable"),
        ([None], "none is not an allowed value"),
        ([[123]], "entity\n  argument of type 'int' is not iterable"),
        ([[None]], "'NoneType' is not iterable"),
    ],
    "purge_by_guid": [
        ([int], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
        ([[int]], "guid\n  str type expected"),
        ([[None]], "guid\n  str type expected"),
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
            "terms -> 0\n  argument of type 'int' is not iterable",
        ),
        ([AtlasGlossary, None], "none is not an allowed value"),
    ],
    "replace_terms": [
        (["asset-type", "terms"], "asset_type\n  a class is expected"),
        ([None, "cm"], "none is not an allowed value"),
        (
            [AtlasGlossary, [123]],
            "terms -> 0\n  argument of type 'int' is not iterable",
        ),
        ([AtlasGlossary, None], "none is not an allowed value"),
    ],
    "remove_terms": [
        (["asset-type", "terms"], "asset_type\n  a class is expected"),
        ([None, "cm"], "none is not an allowed value"),
        (
            [AtlasGlossary, [123]],
            "terms -> 0\n  argument of type 'int' is not iterable",
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
        (["keycloak-req"], "keycloak_request\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "get_admin_events": [
        (["admin-req"], "admin_request\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_AUDIT_CLIENT_METHODS = {
    "search": [
        (["audit-search-req"], "criteria\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_GROUP_CLIENT_METHODS = {
    "create": [
        ("group", "group\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        (["group"], "group\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "purge": [
        ([[123]], "guid\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "get": [
        (
            [None, None, None, "count", 123],
            "count\n  value could not be parsed to a boolean",
        ),
        ([None, None, None, None, 123], "none is not an allowed value"),
        ([None, None, None, True, "offset"], "offset\n  value is not a valid integer"),
        ([None, None, None, True, None], "none is not an allowed value"),
    ],
    "get_all": [
        (["limit"], "limit\n  value is not a valid integer"),
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
        (["limit", None, None, True, 123], "limit\n  value is not a valid integer"),
        ([None, None, None, True, 123], "none is not an allowed value"),
        (
            [123, None, None, "count", 123],
            "count\n  value could not be parsed to a boolean",
        ),
        ([123, None, None, None, "offset"], "none is not an allowed value"),
        ([123, None, None, True, "offset"], "offset\n  value is not a valid integer"),
        ([123, None, None, True, None], "none is not an allowed value"),
    ],
}

TEST_SL_CLIENT_METHODS = {
    "search": [
        (["search-log-req"], "criteria\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
}

TEST_TOKEN_CLIENT_METHODS = {
    "get": [
        (
            [None, None, None, "count", 123],
            "count\n  value could not be parsed to a boolean",
        ),
        ([None, None, None, None, 123], "none is not an allowed value"),
        ([None, None, None, True, "offset"], "offset\n  value is not a valid integer"),
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
            "type_category\n  value is not a valid enumeration member",
        ),
        ([None], "none is not an allowed value"),
    ],
    "create": [
        (["typedef"], "typedef\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        (["typedef"], "typedef\n  value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "purge": [
        ([[123], "typedef"], "name\n  str type expected"),
        ([None, "typedef"], "none is not an allowed value"),
        (["name", "typedef"], "typedef_type\n  a class is expected"),
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
        (["guid", "user"], "user\n  value is not a valid dict"),
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
            "count\n  value could not be parsed to a boolean",
        ),
        ([None, None, None, None, 123], "none is not an allowed value"),
        ([None, None, None, True, "offset"], "offset\n  value is not a valid integer"),
        ([None, None, None, True, None], "none is not an allowed value"),
    ],
    "get_all": [
        (["limit"], "limit\n  value is not a valid integer"),
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
        ([123], "request\n  value is not a valid dict"),
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
    "run": [
        (["abc"], "value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "rerun": [
        (["abc"], "value is not a valid enumeration member"),
        ([None], "none is not an allowed value"),
    ],
    "update": [
        (["abc"], "value is not a valid dict"),
        ([None], "none is not an allowed value"),
    ],
    "find_by_type": [
        (["abc"], "value is not a valid enumeration member"),
        ([None], "none is not an allowed value"),
    ],
    "monitor": [
        (["abc", "test-logger"], "value is not a valid dict"),
        (
            [
                WorkflowResponse(metadata=WorkflowMetadata(), spec=WorkflowSpec()),
                "test-logger",
            ],
            "instance of Logger expected",
        ),
        ([None, "test-logger"], "none is not an allowed value"),
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
    "add_schedule": [
        (
            [[123], WorkflowSchedule(timezone="atlan", cron_schedule="*")],
            "value is not a valid dict",
        ),
        (
            [[123], WorkflowSchedule(timezone="atlan", cron_schedule="*")],
            "value is not a valid enumeration member",
        ),
        (
            [None, WorkflowSchedule(timezone="atlan", cron_schedule="*")],
            "none is not an allowed value",
        ),
    ],
    "remove_schedule": [
        ([[123]], "value is not a valid dict"),
        ([[123]], "value is not a valid enumeration member"),
        ([None], "none is not an allowed value"),
    ],
    "get_scheduled_run": [
        ([[123]], "str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "find_schedule_query": [
        ([[123], 10], "saved_query_id\n  str type expected"),
        ([None, 10], "none is not an allowed value"),
        (["test-query-id", [123]], "max_results\n  value is not a valid integer"),
        (["test-query-id", None], "none is not an allowed value"),
    ],
    "re_run_schedule_query": [
        ([[123]], "schedule_query_id\n  str type expected"),
        ([None], "none is not an allowed value"),
    ],
    "find_schedule_query_between": [
        ([[123], True], "value is not a valid dict"),
        ([None, True], "none is not an allowed value"),
        (
            [ScheduleQueriesSearchRequest(start_date="start", end_date="end"), [123]],
            "missed\n  value could not be parsed to a boolean",
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

APPLICABLE_GLOSSARIES = "applicable_glossaries"

APPLICABLE_DOMAINS = "applicable_domains"

APPLICABLE_CONNECTIONS = "applicable_connections"

APPLICABLE_ENTITY_TYPES = "applicable_entity_types"

APPLICABLE_OTHER_ASSET_TYPES = "applicable_other_asset_types"

APPLICABLE_GLOSSARY_TYPES = "applicable_glossary_types"

APPLICABLE_DOMAIN_TYPES = "applicable_domain_types"

APPLICABLE_ASSET_TYPES = "applicable_asset_types"

TEST_ENUM_DEF = {
    "category": "ENUM",
    "guid": "f2e6763b-a29d-4fb5-8447-10ba9da14259",
    "createdBy": "service-account-atlan-argo",
    "updatedBy": "service-account-atlan-argo",
    "createTime": 1646710766297,
    "updateTime": 1657756889921,
    "version": 95,
    "name": "AtlasGlossaryTermRelationshipStatus",
    "description": "TermRelationshipStatus defines how reliable the relationship is between two glossary terms",
    "typeVersion": "1.0",
    "serviceType": "atlas_core",
    "elementDefs": [
        {
            "value": "DRAFT",
            "description": "DRAFT means the relationship is under development.",
            "ordinal": 0,
        },
        {
            "value": "ACTIVE",
            "description": "ACTIVE means the relationship is validated and in use.",
            "ordinal": 1,
        },
        {
            "value": "DEPRECATED",
            "description": "DEPRECATED means the the relationship is being phased out.",
            "ordinal": 2,
        },
        {
            "value": "OBSOLETE",
            "description": "OBSOLETE means that the relationship should not be used anymore.",
            "ordinal": 3,
        },
        {
            "value": "OTHER",
            "description": "OTHER means that there is another status.",
            "ordinal": 99,
        },
    ],
}

TEST_STRUCT_DEF = {
    "category": "STRUCT",
    "guid": "8afb807f-26f7-4787-b15f-7872d00220ea",
    "createdBy": "service-account-atlan-argo",
    "updatedBy": "service-account-atlan-argo",
    "createTime": 1652745663724,
    "updateTime": 1657756890174,
    "version": 59,
    "name": "AwsTag",
    "description": "Atlas Type representing a tag/value pair associated with an AWS object, eg S3 bucket",
    "typeVersion": "1.0",
    "serviceType": "aws",
    "attributeDefs": [
        {
            "description": "stuff",
            "name": "awsTagKey",
            "typeName": "string",
            "isOptional": False,
            "cardinality": "SINGLE",
            "valuesMinCount": 1,
            "valuesMaxCount": 1,
            "isUnique": False,
            "isIndexable": True,
            "includeInNotification": False,
            "skipScrubbing": False,
            "searchWeight": -1,
            "indexType": "STRING",
            "isNew": True,
        },
        {
            "description": "stuff",
            "name": "awsTagValue",
            "typeName": "string",
            "isOptional": False,
            "cardinality": "SINGLE",
            "valuesMinCount": 1,
            "valuesMaxCount": 1,
            "isUnique": False,
            "isIndexable": False,
            "includeInNotification": False,
            "skipScrubbing": False,
            "searchWeight": -1,
            "indexType": "STRING",
            "isNew": True,
        },
    ],
}

TEST_ATTRIBUTE_DEF_APPLICABLE_ASSET_TYPES = [
    (
        APPLICABLE_ASSET_TYPES,
        1,
        f"ATLAN-PYTHON-400-048 Invalid parameter type for applicable_asset_types should be {AssetTypes}",
    ),
    (
        APPLICABLE_ASSET_TYPES,
        {"Bogus"},
        "ATLAN-PYTHON-400-051 {'Bogus'} is an invalid value for applicable_asset_types should be in ",
    ),
    (
        APPLICABLE_GLOSSARY_TYPES,
        1,
        f"ATLAN-PYTHON-400-048 Invalid parameter type for applicable_glossary_types should be {GlossaryTypes}",
    ),
    (
        APPLICABLE_GLOSSARY_TYPES,
        {"Bogus"},
        "ATLAN-PYTHON-400-051 {'Bogus'} is an invalid value for applicable_glossary_types should be in ",
    ),
    (
        APPLICABLE_DOMAIN_TYPES,
        1,
        f"ATLAN-PYTHON-400-048 Invalid parameter type for applicable_domain_types should be {DomainTypes}",
    ),
    (
        APPLICABLE_DOMAIN_TYPES,
        {"Bogus"},
        "ATLAN-PYTHON-400-051 {'Bogus'} is an invalid value for applicable_domain_types should be in ",
    ),
    (
        APPLICABLE_OTHER_ASSET_TYPES,
        1,
        f"ATLAN-PYTHON-400-048 Invalid parameter type for applicable_other_asset_types should be {OtherAssetTypes}",
    ),
    (
        APPLICABLE_OTHER_ASSET_TYPES,
        {"Bogus"},
        "ATLAN-PYTHON-400-051 {'Bogus'} is an invalid value for applicable_other_asset_types should be in ",
    ),
    (
        APPLICABLE_ENTITY_TYPES,
        1,
        f"ATLAN-PYTHON-400-048 Invalid parameter type for applicable_entity_types should be {EntityTypes}",
    ),
    (
        APPLICABLE_CONNECTIONS,
        1,
        "ATLAN-PYTHON-400-048 Invalid parameter type for applicable_connections should be Set[str]",
    ),
    (
        APPLICABLE_GLOSSARIES,
        1,
        "ATLAN-PYTHON-400-048 Invalid parameter type for applicable_glossaries should be Set[str]",
    ),
]
