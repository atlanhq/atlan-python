# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.model.assets import Asset
from pyatlan.model.contract import InitRequest


class ContractInit:
    """
    Shared business logic for contract initialization operations.
    """

    @staticmethod
    def prepare_request(asset: Asset) -> InitRequest:
        """
        Prepare the InitRequest for generating an initial contract spec.

        :param asset: asset for which to generate the initial contract spec
        :returns: InitRequest object ready for API call
        """
        return InitRequest(
            asset_type=asset.type_name, asset_qualified_name=asset.qualified_name
        )

    @staticmethod
    def process_response(response: dict) -> Optional[str]:
        """
        Process the response from the contract initialization API.

        :param response: raw response from the API
        :returns: YAML for the initial contract spec, or None if not found
        """
        return response.get("contract")
