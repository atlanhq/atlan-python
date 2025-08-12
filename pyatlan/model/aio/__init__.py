"""
Async Models for Atlan
=======================

This module provides async versions of Atlan model classes that support
async iteration and pagination.

These models follow the same API as their sync counterparts but use async/await
for all operations that involve API calls or iteration.
"""

from .asset import AsyncIndexSearchResults, AsyncSearchResults
from .audit import AsyncAuditSearchResults
from .core import AsyncAtlanRequest, AsyncAtlanResponse
from .group import AsyncGroupResponse
from .keycloak_events import AsyncAdminEventResponse, AsyncKeycloakEventResponse
from .lineage import AsyncLineageListResults
from .retranslators import AsyncAtlanTagRetranslator, AsyncBaseRetranslator
from .search_log import AsyncSearchLogResults
from .task import AsyncTaskSearchResponse
from .translators import AsyncAtlanTagTranslator, AsyncBaseTranslator
from .user import AsyncUserResponse
from .workflow import AsyncWorkflowSearchResponse
from .custom_metadata import AsyncCustomMetadataDict, AsyncCustomMetadataProxy

__all__ = [
    # Asset search results
    "AsyncSearchResults",
    "AsyncIndexSearchResults",
    # Audit search results
    "AsyncAuditSearchResults",
    # Admin event results
    "AsyncAdminEventResponse",
    "AsyncKeycloakEventResponse",
    # Core async classes
    "AsyncAtlanRequest",
    "AsyncAtlanResponse",
    # Lineage results
    "AsyncLineageListResults",
    # Search log results
    "AsyncSearchLogResults",
    # User response
    "AsyncUserResponse",
    # Group response
    "AsyncGroupResponse",
    # Workflow search response
    "AsyncWorkflowSearchResponse",
    # Task search response
    "AsyncTaskSearchResponse",
    # Async translators
    "AsyncBaseTranslator",
    "AsyncAtlanTagTranslator",
    # Async retranslators
    "AsyncBaseRetranslator",
    "AsyncAtlanTagRetranslator",
    # Async custom metadata dict
    "AsyncCustomMetadataDict",
    # Async custom metadata proxy
    "AsyncCustomMetadataProxy",
]
