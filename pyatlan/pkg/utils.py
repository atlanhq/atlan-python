# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import logging
import os

from pyatlan.client.atlan import AtlanClient
from pyatlan.pkg.models import RuntimeConfig

LOGGER = logging.getLogger(__name__)


def get_client(impersonate_user_id: str) -> AtlanClient:
    """
    Set up the default Atlan client, based on environment variables.
    This will use an API token if found in ATLAN_API_KEY, and will fallback to attempting to impersonate a user if
    ATLAN_API_KEY is empty.

    :param impersonate_user_id: unique identifier (GUID) of a user or API token to impersonate
    :returns: an initialized client
    """
    base_url = os.environ.get("ATLAN_BASE_URL", "INTERNAL")
    api_token = os.environ.get("ATLAN_API_KEY", "")
    user_id = os.environ.get("ATLAN_USER_ID", impersonate_user_id)
    if api_token:
        LOGGER.info("Using provided API token for authentication.")
        api_key = api_token
    elif user_id:
        LOGGER.info("No API token found, attempting to impersonate user: %s", user_id)
        api_key = AtlanClient(base_url=base_url, api_key="").impersonate.user(
            user_id=user_id
        )
    else:
        LOGGER.info(
            "No API token or impersonation user, attempting short-lived escalation."
        )
        api_key = AtlanClient(base_url=base_url, api_key="").impersonate.escolate()
    return AtlanClient(base_url=base_url, api_key=api_key)


def set_package_ops(run_time_config: RuntimeConfig) -> AtlanClient:
    """
    Set up and processing options and configure the AtlanClient

    :param run_time_config: the generated RuntimeConfig from the generated config module
    :returns: an intialized AtlanClient that should be used for any calls to the SDK
    """
    client = get_client(run_time_config.user_id or "")
    if run_time_config.agent == "workflow":
        headers: dict[str, str] = {}
        if run_time_config.agent:
            headers["x-atlan-agent"] = run_time_config.agent
        if run_time_config.agent_pkg:
            headers["x-atlan-agent-package-name"] = run_time_config.agent_pkg
        if run_time_config.agent_wfl:
            headers["x-atlan-agent-workflow-id"] = run_time_config.agent_wfl
        if run_time_config.agent_id:
            headers["x-atlan-agent-id"] = run_time_config.agent_id
        client.update_headers(headers)
    return client
