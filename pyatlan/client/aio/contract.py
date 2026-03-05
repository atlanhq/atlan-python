# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller, ContractInit
from pyatlan.client.constants import CONTRACT_INIT_API
from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset


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
