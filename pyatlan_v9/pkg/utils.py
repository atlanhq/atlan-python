# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

import logging
import os
from typing import Optional

from pyatlan_v9.client.atlan import AtlanClient

LOGGER = logging.getLogger(__name__)


def get_client(
    impersonate_user_id: Optional[str] = None, set_pkg_headers: Optional[bool] = False
) -> AtlanClient:
    """
    Set up the default v9 Atlan client, based on environment variables.
    This will use an API token if found in ATLAN_API_KEY, and will fallback
    to attempting to impersonate a user if ATLAN_API_KEY is empty.

    :param impersonate_user_id: unique identifier (GUID) of a user or API token
        to impersonate (default is None)
    :param set_pkg_headers: whether to set package headers on the client
        (default is False)
    :returns: an initialized v9 client
    """
    base_url = os.environ.get("ATLAN_BASE_URL", "INTERNAL")
    api_token = os.environ.get("ATLAN_API_KEY", "")
    user_id = os.environ.get("ATLAN_USER_ID", impersonate_user_id)
    oauth_client_id = os.environ.get("ATLAN_OAUTH_CLIENT_ID", "")
    oauth_client_secret = os.environ.get("ATLAN_OAUTH_CLIENT_SECRET", "")

    if oauth_client_id and oauth_client_secret:
        LOGGER.info("Using OAuth client credentials for authentication.")
        client = AtlanClient(
            base_url=base_url,
            oauth_client_id=str(oauth_client_id),
            oauth_client_secret=str(oauth_client_secret),
        )
        if set_pkg_headers:
            client = set_package_headers(client)
        return client
    else:
        LOGGER.info(
            "No OAuth client credentials found. "
            "Attempting to use API token or user impersonation."
        )

    if api_token:
        LOGGER.info("Using provided API token for authentication.")
        api_key = api_token
    elif user_id:
        LOGGER.info("No API token found, attempting to impersonate user: %s", user_id)
        client = AtlanClient(base_url=base_url, api_key="")
        api_key = client.impersonate.user(user_id=user_id)
    else:
        LOGGER.info(
            "No API token or impersonation user, attempting short-lived escalation."
        )
        client = AtlanClient(base_url=base_url, api_key="")
        api_key = client.impersonate.escalate()

    client = AtlanClient(base_url=base_url, api_key=api_key)
    if user_id:
        client._user_id = user_id
    if set_pkg_headers:
        client = set_package_headers(client)
    return client


def set_package_headers(
    client: AtlanClient,
    agent: str = "workflow",
    workflow_id: Optional[str] = None,
    app_name: Optional[str] = None,
    run_id: Optional[str] = None,
) -> AtlanClient:
    """
    Configure the AtlanClient with package headers.

    Each header value can be passed explicitly; if omitted, falls back to the
    corresponding environment variable (X_ATLAN_AGENT_ID,
    X_ATLAN_AGENT_PACKAGE_NAME, X_ATLAN_AGENT_WORKFLOW_ID).

    :param client: AtlanClient instance to configure
    :param agent: value for the x-atlan-agent header (default: "workflow")
    :param workflow_id: value for the x-atlan-agent-id header (default: X_ATLAN_AGENT_ID env var)
    :param app_name: value for the x-atlan-agent-package-name header
        (default: X_ATLAN_AGENT_PACKAGE_NAME env var)
    :param run_id: value for the x-atlan-agent-workflow-id header
        (default: X_ATLAN_AGENT_WORKFLOW_ID env var)
    :returns: updated client instance
    """
    resolved_workflow_id = workflow_id or os.environ.get("X_ATLAN_AGENT_ID")
    if agent and resolved_workflow_id:
        headers = {
            "x-atlan-agent": agent,
            "x-atlan-agent-id": resolved_workflow_id,
            "x-atlan-agent-package-name": app_name
            or os.environ.get("X_ATLAN_AGENT_PACKAGE_NAME", ""),
            "x-atlan-agent-workflow-id": run_id
            or os.environ.get("X_ATLAN_AGENT_WORKFLOW_ID", ""),
        }
        client.update_headers(headers)
    return client
