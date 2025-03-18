from http import HTTPStatus
from typing import List, Optional

from pydantic.v1 import validate_arguments

from pyatlan import utils
from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import OPEN_LINEAGE_SEND_EVENT_API
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.assets import Connection
from pyatlan.model.credential import Credential
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.open_lineage.event import OpenLineageEvent
from pyatlan.model.response import AssetMutationResponse


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
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_current_client()

        create_credential = Credential()
        create_credential.auth_type = "atlan_api_key"
        create_credential.name = (
            f"default-{connector_type.value}-{int(utils.get_epoch_timestamp())}-0"
        )
        create_credential.connector = str(connector_type.value)
        create_credential.connector_config_name = (
            f"atlan-connectors-{connector_type.value}"
        )
        create_credential.connector_type = "event"
        create_credential.extras = {
            "events.enable-partial-assets": True,
            "events.enabled": True,
            "events.topic": f"openlineage_{connector_type.value}",
            "events.urlPath": f"/events/openlineage/{connector_type.value}/api/v1/lineage",
        }
        response = client.credentials.creator(credential=create_credential)
        connection = Connection.creator(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )

        connection.default_credential_guid = response.id
        return client.asset.save(connection)

    @validate_arguments
    def send(
        self, request: OpenLineageEvent, connector_type: AtlanConnectorType
    ) -> None:
        """
        Sends the OpenLineage event to Atlan to be consumed.

        :param request: OpenLineage event to send
        :param connector_type: of the connection that should receive the OpenLineage event
        :raises AtlanError: when OpenLineage is not configured OR on any issues with API communication
        """

        try:
            self._client._call_api(
                request_obj=request,
                api=OPEN_LINEAGE_SEND_EVENT_API.format_path(
                    {"connector_type": connector_type.value}
                ),
                text_response=True,
            )
        except AtlanError as e:
            if (
                e.error_code.http_error_code == HTTPStatus.UNAUTHORIZED
                and e.error_code.error_message.startswith(
                    "Unauthorized: url path not configured to receive data, urlPath:"
                )
            ):
                raise ErrorCode.OPENLINEAGE_NOT_CONFIGURED.exception_with_parameters(
                    connector_type.value
                ) from e
            raise e
