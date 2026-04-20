# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    CONTRACT_DELETE_SCOPE_HEADER,
    CONTRACT_INIT_API,
    DELETE_ENTITIES_BY_GUIDS,
)
from pyatlan.errors import ErrorCode
from pyatlan_v9.client.asset import _parse_mutation_response
from pyatlan_v9.model.assets import Asset
from pyatlan_v9.model.contract import InitRequest
from pyatlan_v9.model.enums import AtlanDeleteType
from pyatlan_v9.model.response import AssetMutationResponse
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

    @validate_arguments
    def delete(self, guid: str) -> AssetMutationResponse:
        """
        Hard-delete (purge) a data contract and all its versions.
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
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        return _parse_mutation_response(raw_json)

    @validate_arguments
    def delete_latest_version(self, guid: str) -> AssetMutationResponse:
        """
        Hard-delete (purge) only the latest version of a data contract.
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
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS,
            query_params=query_params,
            extra_headers={CONTRACT_DELETE_SCOPE_HEADER: "single"},
        )
        return _parse_mutation_response(raw_json)
