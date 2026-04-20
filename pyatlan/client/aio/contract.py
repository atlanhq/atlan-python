# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller, ContractInit
from pyatlan.client.constants import (
    CONTRACT_DELETE_SCOPE_HEADER,
    CONTRACT_INIT_API,
    DELETE_ENTITIES_BY_GUIDS,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.enums import AtlanDeleteType
from pyatlan.model.response import AssetMutationResponse


class AsyncContractClient:
    """
    Async version of ContractClient for data contract-specific operations.
    This class does not need to be instantiated directly but can be obtained through the contracts property of AsyncAtlanClient.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def generate_initial_spec(
        self,
        asset: Asset,
    ) -> Optional[str]:
        """
        Generate an initial contract spec for the provided asset (async version).
        The asset must have at least its `qualifiedName` (and `typeName`) populated.

        :param asset: for which to generate the initial contract spec

        :raises AtlanError: if there is an issue interacting with the API
        :returns: YAML for the initial contract spec for the provided asset
        """
        # Prepare request using shared logic
        request_obj = ContractInit.prepare_request(asset)

        # Make async API call
        response = await self._client._call_api(
            CONTRACT_INIT_API, request_obj=request_obj
        )

        # Process response using shared logic
        return ContractInit.process_response(response)

    @validate_arguments
    async def delete(self, guid: str) -> AssetMutationResponse:
        """
        Hard-delete (purge) a data contract and all its versions (async version).
        This deletes every version of the contract associated with the same asset
        and cleans up the asset's contract attributes (hasContract, dataContractLatest,
        dataContractLatestCertified).

        :param guid: unique identifier (GUID) of any version of the contract to delete
        :returns: details of the deleted contract version(s)
        :raises AtlanError: on any API communication issue

        .. warning::
            This is an irreversible operation. All versions of the contract will be permanently removed.
        """
        query_params = {"deleteType": AtlanDeleteType.PURGE.value, "guid": [guid]}
        raw_json = await self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        return AssetMutationResponse(**raw_json)

    @validate_arguments
    async def delete_latest_version(self, guid: str) -> AssetMutationResponse:
        """
        Hard-delete (purge) only the latest version of a data contract (async version).
        The previous version (if any) becomes the new latest, and the asset's
        contract pointers are updated accordingly.

        :param guid: unique identifier (GUID) of the latest contract version to delete
        :returns: details of the deleted contract version
        :raises AtlanError: on any API communication issue
        :raises ApiError: if the specified GUID is not the latest version

        .. warning::
            This is an irreversible operation. Only the latest version will be removed.
        """
        query_params = {"deleteType": AtlanDeleteType.PURGE.value, "guid": [guid]}
        raw_json = await self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS,
            query_params=query_params,
            extra_headers={CONTRACT_DELETE_SCOPE_HEADER: "single"},
        )
        return AssetMutationResponse(**raw_json)
