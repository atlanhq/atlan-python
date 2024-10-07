from typing import Optional, Union

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import CONTRACT_INIT_API
from pyatlan.errors import ErrorCode
from pyatlan.model.contract import DataContractSpec, InitRequest


class ContractClient:
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
        asset_type: str,
        asset_qualified_name: str,
        return_raw: bool = False,
    ) -> Union[DataContractSpec, Optional[str]]:
        """
        Generate an initial contract spec for the given asset type and qualified name.

        :param asset_type: type of the asset, e.g: `Table`, `Column`, etc
        :param asset_qualified_name: `qualifiedName` of the asset.
        :param return_raw: if `True`, returns the raw data contract spec (with comments)
        without any Pydantic model deserialization of response. Defaults to `False`

        :raises AtlanError: if there is an issue interacting with the API
        :returns: DataContractSpec object for the asset's initial contract,
        or the raw contract spec string if `return_raw` is `True`
        """
        response = self._client._call_api(
            CONTRACT_INIT_API,
            request_obj=InitRequest(
                asset_type=asset_type, asset_qualified_name=asset_qualified_name
            ),
        )
        if return_raw:
            return response.get("contract")
        return DataContractSpec.from_yaml(response.get("contract"))
