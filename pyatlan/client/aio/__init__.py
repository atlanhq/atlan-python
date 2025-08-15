"""
Async Atlan Client (AIO)
========================

This module provides async versions of all Atlan client functionality
with the same API as the sync versions, just requiring await.

Pattern: All async methods reuse shared business logic from pyatlan.client.common
to ensure identical behavior with sync clients.

Usage:
    from pyatlan.client.aio import AsyncAtlanClient

    async with AsyncAtlanClient() as client:
        results = await client.asset.search(criteria)

        # Async iteration through paginated results
        async for asset in results:
            print(asset.name)
"""

from pyatlan.model.aio import (
    AsyncIndexSearchResults,
    AsyncLineageListResults,
    AsyncSearchResults,
)

from .admin import AsyncAdminClient
from .asset import AsyncAssetClient
from .audit import AsyncAuditClient
from .batch import AsyncBatch
from .client import AsyncAtlanClient
from .contract import AsyncContractClient
from .credential import AsyncCredentialClient
from .file import AsyncFileClient
from .group import AsyncGroupClient
from .impersonate import AsyncImpersonationClient
from .open_lineage import AsyncOpenLineageClient
from .query import AsyncQueryClient
from .role import AsyncRoleClient
from .search_log import AsyncSearchLogClient
from .sso import AsyncSSOClient
from .task import AsyncTaskClient
from .token import AsyncTokenClient
from .typedef import AsyncTypeDefClient
from .user import AsyncUserClient
from .workflow import AsyncWorkflowClient

__all__ = [
    "AsyncAtlanClient",
    "AsyncAdminClient",
    "AsyncAssetClient",
    "AsyncAuditClient",
    "AsyncAuditSearchResults",
    "AsyncBatch",
    "AsyncContractClient",
    "AsyncCredentialClient",
    "AsyncFileClient",
    "AsyncGroupClient",
    "AsyncGroupResponse",
    "AsyncImpersonationClient",
    "AsyncIndexSearchResults",
    "AsyncLineageListResults",
    "AsyncOpenLineageClient",
    "AsyncQueryClient",
    "AsyncRoleClient",
    "AsyncSearchLogClient",
    "AsyncSearchLogResults",
    "AsyncSearchResults",
    "AsyncSSOClient",
    "AsyncTaskClient",
    "AsyncTaskSearchResponse",
    "AsyncTokenClient",
    "AsyncTypeDefClient",
    "AsyncUserClient",
    "AsyncUserResponse",
    "AsyncWorkflowClient",
    "AsyncWorkflowSearchResponse",
]
