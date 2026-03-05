# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import CONTRACT_INIT_API
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.assets import Asset
from pyatlan_v9.model.contract import InitRequest
from pyatlan_v9.validate import validate_arguments


class V9ContractClient:
    """
    A client for data contract-specific operations.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def generate_initial_spec(
        self,
        asset: Asset,
    ) -> Optional[str]:
        """
        Generate an initial contract spec for the provided asset.
        The asset must have at least its `qualifiedName` (and `typeName`) populated.

        :param asset: for which to generate the initial contract spec

        :raises AtlanError: if there is an issue interacting with the API
        :returns: YAML for the initial contract spec for the provided asset
        """
        request_obj = InitRequest(
            asset_type=asset.type_name,
            asset_qualified_name=asset.qualified_name,
        )
        response = self._client._call_api(CONTRACT_INIT_API, request_obj=request_obj)
        return response.get("contract")
