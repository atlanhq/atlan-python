from http import HTTPStatus

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import OPEN_LINEAGE_SEND_EVENT_API
from pyatlan.errors import AtlanError, ErrorCode
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
                    {"connector_type": connector_type}
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
