from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    OpenLineageCreateConnection,
    OpenLineageCreateCredential,
    OpenLineageSend,
)
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.open_lineage.event import OpenLineageEvent, OpenLineageRawEvent
from pyatlan.model.response import AssetMutationResponse
from pyatlan.utils import validate_type


class OpenLineageClient:
    """
    A client for interacting with OpenLineage.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def create_connection(
        self,
        name: str,
        connector_type: AtlanConnectorType = AtlanConnectorType.SPARK,
        admin_users: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
    ) -> AssetMutationResponse:
        """
        Creates a connection for OpenLineage.

        :param name:  name for the new connection
        :param connector_type: for the new connection to be associated with
        :param admin_users: list of admin users to associate with this connection
        :param admin_roles: list of admin roles to associate with this connection
        :param admin_groups:list of admin groups to associate with this connection
        :return: details of the connection created
        """
        # Step 1: Create credential using shared logic
        create_credential = OpenLineageCreateCredential.prepare_request(connector_type)
        credential_response = self._client.credentials.creator(  # type: ignore[attr-defined]
            credential=create_credential
        )

        # Step 2: Create connection using shared logic
        connection = OpenLineageCreateConnection.prepare_request(
            client=self._client,
            name=name,
            connector_type=connector_type,
            credential_id=credential_response.id,
            admin_users=admin_users,
            admin_roles=admin_roles,
            admin_groups=admin_groups,
        )

        # Save connection and return response directly
        return self._client.asset.save(connection)  # type: ignore[attr-defined]

    def send(
        self,
        request: Union[
            OpenLineageEvent,
            OpenLineageRawEvent,
            List[Dict[str, Any]],
            Dict[str, Any],
            str,
        ],
        connector_type: AtlanConnectorType,
    ) -> None:
        """
        Sends the OpenLineage event to Atlan to be consumed.

        :param request: OpenLineage event to send - can be an OpenLineageEvent, OpenLineageRawEvent, list of dicts, dict, or JSON string
        :param connector_type: of the connection that should receive the OpenLineage event
        :raises AtlanError: when OpenLineage is not configured OR on any issues with API communication
        """
        validate_type(
            name="request",
            _type=(OpenLineageEvent, OpenLineageRawEvent, list, dict, str),
            value=request,
        )
        validate_type(
            name="connector_type",
            _type=(AtlanConnectorType),
            value=connector_type,
        )
        try:
            # Convert raw list/dict/str/ of dicts to OpenLineageRawEvent if needed
            if isinstance(request, (dict, str, list)):
                if isinstance(request, str):
                    request = OpenLineageRawEvent.parse_raw(request)
                else:
                    # For list or dict, use parse_obj
                    request = OpenLineageRawEvent.parse_obj(request)

            # Prepare request using shared logic
            api_endpoint, request_obj, api_options = OpenLineageSend.prepare_request(
                request, connector_type
            )
            # Make API call - _call_api handles JSON conversion automatically
            self._client._call_api(
                request_obj=request_obj, api=api_endpoint, **api_options
            )
        except AtlanError as e:
            # Validate and handle OpenLineage-specific errors using shared logic
            OpenLineageSend.validate_response(e, connector_type)
