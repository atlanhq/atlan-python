# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pyatlan.client.common import (
    AsyncApiCaller,
    OpenLineageCreateCredential,
    OpenLineageSend,
)
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.utils import validate_type
from pyatlan_v9.model.assets.connection import Connection
from pyatlan_v9.model.credential import Credential
from pyatlan_v9.model.enums import AtlanConnectorType
from pyatlan_v9.model.open_lineage.event import OpenLineageEvent, OpenLineageRawEvent
from pyatlan_v9.model.response import AssetMutationResponse
from pyatlan_v9.validate import validate_arguments


class V9AsyncOpenLineageClient:
    """
    Async version of OpenLineageClient for interacting with OpenLineage.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def create_connection(
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
        legacy_credential = OpenLineageCreateCredential.prepare_request(connector_type)
        v9_credential = Credential(
            auth_type=legacy_credential.auth_type,
            name=legacy_credential.name,
            connector=legacy_credential.connector,
            connector_config_name=legacy_credential.connector_config_name,
            connector_type=legacy_credential.connector_type,
            extras=legacy_credential.extras,
        )
        credential_response = await self._client.credentials.creator(  # type: ignore[attr-defined]
            credential=v9_credential
        )

        connection = Connection.creator(
            client=self._client,
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )
        connection.default_credential_guid = credential_response.id

        return await self._client.asset.save(connection)  # type: ignore[attr-defined]

    async def send(
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
            if isinstance(request, (dict, str, list)):
                if isinstance(request, str):
                    request = OpenLineageRawEvent.parse_raw(request)
                else:
                    request = OpenLineageRawEvent.parse_obj(request)

            api_endpoint, request_obj, api_options = OpenLineageSend.prepare_request(
                request, connector_type
            )
            await self._client._call_api(
                request_obj=request_obj, api=api_endpoint, **api_options
            )
        except AtlanError as e:
            OpenLineageSend.validate_response(e, connector_type)
