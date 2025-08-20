# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared business logic for sync and async clients.

This package contains all shared business logic used by both
sync (AtlanClient) and async (AsyncAtlanClient) implementations.

All classes here use static methods for prepare_request() and process_response()
to ensure zero code duplication between sync and async clients.
"""

from __future__ import annotations

# Import protocol first to avoid circular imports
from pyatlan.client.protocol import (
    CONNECTION_RETRY,
    HTTP_PREFIX,
    HTTPS_PREFIX,
    ApiCaller,
    AsyncApiCaller,
)

# Admin shared logic classes
from .admin import AdminGetAdminEvents, AdminGetKeycloakEvents

# Asset shared logic classes
from .asset import (
    DeleteByGuid,
    FindAssetsByName,
    FindCategoryFastByName,
    FindConnectionsByName,
    FindDomainByName,
    FindGlossaryByName,
    FindPersonasByName,
    FindProductByName,
    FindPurposesByName,
    FindTermFastByName,
    GetByGuid,
    GetByQualifiedName,
    GetHierarchy,
    GetLineageList,
    ManageAssetAttributes,
    ManageCustomMetadata,
    ManageTerms,
    ModifyAtlanTags,
    PurgeByGuid,
    RemoveAnnouncement,
    RemoveCertificate,
    RemoveCustomMetadata,
    ReplaceCustomMetadata,
    RestoreAsset,
    Save,
    Search,
    SearchForAssetWithName,
    UpdateAnnouncement,
    UpdateAsset,
    UpdateAssetByAttribute,
    UpdateCertificate,
    UpdateCustomMetadataAttributes,
)

# Audit shared logic classes
from .audit import AuditSearch

# Contract shared logic classes
from .contract import ContractInit

# Credential shared logic classes
from .credential import (
    CredentialCreate,
    CredentialGet,
    CredentialGetAll,
    CredentialPurge,
    CredentialTest,
    CredentialTestAndUpdate,
)

# File shared logic classes
from .file import FileDownload, FilePresignedUrl, FileUpload

# Group shared logic classes
from .group import (
    GroupCreate,
    GroupGet,
    GroupGetMembers,
    GroupPurge,
    GroupRemoveUsers,
    GroupUpdate,
)

# Impersonate shared logic classes
from .impersonate import (
    ImpersonateEscalate,
    ImpersonateGetClientSecret,
    ImpersonateGetUserId,
    ImpersonateUser,
)

# OpenLineage shared logic classes
from .open_lineage import (
    OpenLineageCreateConnection,
    OpenLineageCreateCredential,
    OpenLineageSend,
)

# Query shared logic classes
from .query import QueryStream

# Role shared logic classes
from .role import RoleGet, RoleGetAll

# Search log shared logic classes
from .search_log import SearchLogSearch

# SSO shared logic classes
from .sso import (
    SSOCheckExistingMappings,
    SSOCreateGroupMapping,
    SSODeleteGroupMapping,
    SSOGetAllGroupMappings,
    SSOGetGroupMapping,
    SSOUpdateGroupMapping,
)

# Task shared logic classes
from .task import TaskSearch

# Token shared logic classes
from .token import (
    TokenCreate,
    TokenGet,
    TokenGetByGuid,
    TokenGetById,
    TokenGetByName,
    TokenPurge,
    TokenUpdate,
)

# TypeDef shared logic classes
from .typedef import (
    TypeDefCreate,
    TypeDefFactory,
    TypeDefGet,
    TypeDefGetByName,
    TypeDefPurge,
    TypeDefUpdate,
)

# User shared logic classes
from .user import (
    UserAddToGroups,
    UserChangeRole,
    UserCreate,
    UserGet,
    UserGetByEmail,
    UserGetByEmails,
    UserGetByUsername,
    UserGetByUsernames,
    UserGetCurrent,
    UserGetGroups,
    UserUpdate,
)

# Workflow shared logic classes
from .workflow import (
    WorkflowDelete,
    WorkflowFindById,
    WorkflowFindByType,
    WorkflowFindCurrentRun,
    WorkflowFindLatestRun,
    WorkflowFindRuns,
    WorkflowFindRunsByStatusAndTimeRange,
    WorkflowFindScheduleQuery,
    WorkflowFindScheduleQueryBetween,
    WorkflowGetAllScheduledRuns,
    WorkflowGetScheduledRun,
    WorkflowParseResponse,
    WorkflowRerun,
    WorkflowReRunScheduleQuery,
    WorkflowRun,
    WorkflowScheduleUtils,
    WorkflowStop,
    WorkflowUpdate,
    WorkflowUpdateOwner,
)

__all__ = [
    # Protocol and constants
    "ApiCaller",
    "AsyncApiCaller",
    "HTTPS_PREFIX",
    "HTTP_PREFIX",
    "CONNECTION_RETRY",
    # Admin shared logic classes
    "AdminGetAdminEvents",
    "AdminGetKeycloakEvents",
    # Asset shared logic classes
    "DeleteByGuid",
    "FindAssetsByName",
    "FindCategoryFastByName",
    "FindConnectionsByName",
    "FindDomainByName",
    "FindGlossaryByName",
    "FindPersonasByName",
    "FindProductByName",
    "FindPurposesByName",
    "FindTermFastByName",
    "GetByGuid",
    "GetByQualifiedName",
    "GetHierarchy",
    "GetLineageList",
    "ManageAssetAttributes",
    "ManageCustomMetadata",
    "ManageTerms",
    "ModifyAtlanTags",
    "PurgeByGuid",
    "RemoveAnnouncement",
    "RemoveCertificate",
    "RemoveCustomMetadata",
    "ReplaceCustomMetadata",
    "RestoreAsset",
    "Save",
    "Search",
    "SearchForAssetWithName",
    "UpdateAnnouncement",
    "UpdateAsset",
    "UpdateAssetByAttribute",
    "UpdateCertificate",
    "UpdateCustomMetadataAttributes",
    # Audit shared logic classes
    "AuditSearch",
    # Contract shared logic classes
    "ContractInit",
    # Credential shared logic classes
    "CredentialCreate",
    "CredentialGet",
    "CredentialGetAll",
    "CredentialPurge",
    "CredentialTest",
    "CredentialTestAndUpdate",
    # File shared logic classes
    "FileDownload",
    "FilePresignedUrl",
    "FileUpload",
    # Group shared logic classes
    "GroupCreate",
    "GroupGet",
    "GroupGetMembers",
    "GroupPurge",
    "GroupRemoveUsers",
    "GroupUpdate",
    # Impersonate shared logic classes
    "ImpersonateEscalate",
    "ImpersonateGetClientSecret",
    "ImpersonateGetUserId",
    "ImpersonateUser",
    # OpenLineage shared logic classes
    "OpenLineageCreateConnection",
    "OpenLineageCreateCredential",
    "OpenLineageSend",
    # Query shared logic classes
    "QueryStream",
    # Role shared logic classes
    "RoleGet",
    "RoleGetAll",
    # Search log shared logic classes
    "SearchLogSearch",
    # SSO shared logic classes
    "SSOCheckExistingMappings",
    "SSOCreateGroupMapping",
    "SSODeleteGroupMapping",
    "SSOGetAllGroupMappings",
    "SSOGetGroupMapping",
    "SSOUpdateGroupMapping",
    # Task shared logic classes
    "TaskSearch",
    # Token shared logic classes
    "TokenCreate",
    "TokenGet",
    "TokenGetById",
    "TokenGetByGuid",
    "TokenGetByName",
    "TokenPurge",
    "TokenUpdate",
    # TypeDef shared logic classes
    "TypeDefCreate",
    "TypeDefFactory",
    "TypeDefGet",
    "TypeDefGetByName",
    "TypeDefPurge",
    "TypeDefUpdate",
    # User shared logic classes
    "UserAddToGroups",
    "UserChangeRole",
    "UserCreate",
    "UserGet",
    "UserGetByEmail",
    "UserGetByEmails",
    "UserGetByUsername",
    "UserGetByUsernames",
    "UserGetCurrent",
    "UserGetGroups",
    "UserUpdate",
    # Workflow shared logic classes
    "WorkflowDelete",
    "WorkflowFindById",
    "WorkflowFindByType",
    "WorkflowFindCurrentRun",
    "WorkflowFindLatestRun",
    "WorkflowFindRuns",
    "WorkflowFindRunsByStatusAndTimeRange",
    "WorkflowFindScheduleQuery",
    "WorkflowFindScheduleQueryBetween",
    "WorkflowGetAllScheduledRuns",
    "WorkflowGetScheduledRun",
    "WorkflowParseResponse",
    "WorkflowRerun",
    "WorkflowReRunScheduleQuery",
    "WorkflowRun",
    "WorkflowScheduleUtils",
    "WorkflowStop",
    "WorkflowUpdate",
    "WorkflowUpdateOwner",
]
