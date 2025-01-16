from http import HTTPStatus
from typing import List, Optional

from pydantic.v1 import validate_arguments

from pyatlan import utils
from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import CREATE_OL_CREDENTIALS, OPEN_LINEAGE_SEND_EVENT_API
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.assets import Connection
from pyatlan.model.credential import CredentialResponse
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.open_lineage.event import OpenLineageEvent


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

    def _create_credential(self, connector_name: str) -> CredentialResponse:
        """
        Creates an OpenLineage credential for the specified connector.

        :param connector_name: of the connection that should be OpenLineage event
        :return: details of the created credential
        """
        body = {
            "authType": "atlan_api_key",
            "name": f"default-{connector_name}-{int(utils.get_epoch_timestamp())}-0",
            "connectorConfigName": f"atlan-connectors-{connector_name}",
            "connector": f"{connector_name}",
            "connectorType": "event",
            "extra": {
                "events.enable-partial-assets": True,
                "events.enabled": True,
                "events.topic": f"openlineage_{connector_name}",
                "events.urlPath": f"/events/openlineage/{connector_name}/api/v1/lineage",
            },
        }
        raw_json = self._client._call_api(
            api=CREATE_OL_CREDENTIALS.format_path_with_params(),
            query_params={"testCredential": "true"},
            request_obj=body,
        )
        return CredentialResponse(**raw_json)

    @validate_arguments
    def create_connection(
        self,
        name: str,
        connector_type: AtlanConnectorType = AtlanConnectorType.SPARK,
        admin_users: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
    ) -> Connection:
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

        client = AtlanClient.get_default_client()

        response = self._create_credential(connector_name=connector_type.value)
        guid = response.id
        connection = Connection.creator(
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )

        connection.default_credential_guid = response.id
        response = client.asset.save(connection)  # type: ignore
        return connection

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
                    connector_type
                ) from e
            raise e
