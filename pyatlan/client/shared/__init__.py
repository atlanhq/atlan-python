"""
Shared business logic for sync and async clients.

This package contains all shared business logic used by both
sync (AtlanClient) and async (AsyncAtlanClient) implementations.

All classes here use static methods for prepare_request() and process_response()
to ensure zero code duplication between sync and async clients.
"""

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

__all__ = [
    "Search",
    "GetLineageList",
    "GetByGuid",
    "GetByQualifiedName",
    "GetHierarchy",
    "FindAssetsByName",
    "FindPersonasByName",
    "FindPurposesByName",
    "Save",
    "UpdateAsset",
    "PurgeByGuid",
    "DeleteByGuid",
    "RestoreAsset",
    "ModifyAtlanTags",
    "ManageAssetAttributes",
    "UpdateCertificate",
    "RemoveCertificate",
    "UpdateAnnouncement",
    "RemoveAnnouncement",
    "UpdateAssetByAttribute",
    "ManageCustomMetadata",
    "UpdateCustomMetadataAttributes",
    "ReplaceCustomMetadata",
    "RemoveCustomMetadata",
    "ManageTerms",
    "SearchForAssetWithName",
    "FindConnectionsByName",
    "FindGlossaryByName",
    "FindCategoryFastByName",
    "FindTermFastByName",
    "FindDomainByName",
    "FindProductByName",
]
