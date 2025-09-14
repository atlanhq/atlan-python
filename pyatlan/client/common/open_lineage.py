# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple

from pyatlan import utils
from pyatlan.client.constants import OPEN_LINEAGE_SEND_EVENT_API
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.assets import Connection
from pyatlan.model.credential import Credential
from pyatlan.model.enums import AtlanConnectorType


class OpenLineageCreateCredential:
    """Shared logic for creating OpenLineage credentials."""

    @staticmethod
    def prepare_request(connector_type: AtlanConnectorType) -> Credential:
        """Prepare the credential object for creation."""
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
        return create_credential


class OpenLineageCreateConnection:
    """Shared logic for creating OpenLineage connections."""

    @staticmethod
    def prepare_request(
        client: Any,
        name: str,
        connector_type: AtlanConnectorType,
        credential_id: str,
        admin_users: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
    ) -> Connection:
        """Prepare the connection object for creation."""
        connection = Connection.creator(
            client=client,
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )
        connection.default_credential_guid = credential_id
        return connection

    @staticmethod
    async def prepare_request_async(
        client: Any,
        name: str,
        connector_type: AtlanConnectorType,
        credential_id: str,
        admin_users: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
    ) -> Connection:
        """Prepare the async connection object for creation."""
        connection = await Connection.creator_async(
            client=client,
            name=name,
            connector_type=connector_type,
            admin_users=admin_users,
            admin_groups=admin_groups,
            admin_roles=admin_roles,
        )
        connection.default_credential_guid = credential_id
        return connection


class OpenLineageSend:
    """Shared logic for sending OpenLineage events."""

    @staticmethod
    def prepare_request(
        request: Any, connector_type: AtlanConnectorType
    ) -> Tuple[str, Any, Dict[str, Any]]:
        """Prepare the send event request."""
        api_endpoint = OPEN_LINEAGE_SEND_EVENT_API.format_path(
            {"connector_type": connector_type.value}
        )
        api_options = {"text_response": True}
        return api_endpoint, request, api_options

    @staticmethod
    def validate_response(
        error: AtlanError, connector_type: AtlanConnectorType
    ) -> None:
        """Validate and handle OpenLineage-specific errors."""
        if (
            error.error_code.http_error_code == HTTPStatus.UNAUTHORIZED
            and error.error_code.error_message.startswith(
                "Unauthorized: url path not configured to receive data, urlPath:"
            )
        ):
            raise ErrorCode.OPENLINEAGE_NOT_CONFIGURED.exception_with_parameters(
                connector_type.value
            ) from error
        raise error
