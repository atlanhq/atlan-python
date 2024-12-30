# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import logging
import os
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from pydantic.v1 import parse_obj_as, parse_raw_as

from pyatlan.client.atlan import AtlanClient
from pyatlan.pkg.models import RuntimeConfig

LOGGER = logging.getLogger(__name__)

# Try to import OpenTelemetry libraries
try:
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
        OTLPLogExporter,  # type:ignore
    )
    from opentelemetry.sdk._logs import (  # type:ignore
        LogData,
        LoggerProvider,
        LoggingHandler,
    )
    from opentelemetry.sdk._logs._internal.export import (
        BatchLogRecordProcessor,  # type:ignore
    )
    from opentelemetry.sdk.resources import Resource  # type:ignore

    class CustomBatchLogRecordProcessor(BatchLogRecordProcessor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def emit(self, log_data: LogData) -> None:
            if not self._is_valid_type(log_data.log_record.body):
                log_data.log_record.body = str(log_data.log_record.body)
            super().emit(log_data)

        def _is_valid_type(self, value: Any) -> bool:
            # see https://github.com/open-telemetry/opentelemetry-python/blob/c883f6cc1243ab7e0e5bc177169f25cdf0aac29f/
            # exporter/opentelemetry-exporter-otlp-proto-common/src/opentelemetry/exporter/otlp/proto/common/_internal
            # /__init__.py#L69
            # for valid encode types
            if isinstance(value, bool):
                return True
            if isinstance(value, str):
                return True
            if isinstance(value, int):
                return True
            if isinstance(value, float):
                return True
            if isinstance(value, Sequence):
                return all(self._is_valid_type(v) for v in value)
            elif isinstance(value, Mapping):
                return all(
                    self._is_valid_type(k) & self._is_valid_type(v)
                    for k, v in value.items()
                )
            return False

    OTEL_IMPORTS_AVAILABLE = True
except ImportError:
    OTEL_IMPORTS_AVAILABLE = False


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
        client = AtlanClient(base_url=base_url, api_key="")
        client._user_id = user_id
        api_key = client.impersonate.user(user_id=user_id)
    else:
        LOGGER.info(
            "No API token or impersonation user, attempting short-lived escalation."
        )
        client = AtlanClient(base_url=base_url, api_key="")
        api_key = client.impersonate.escalate()

    return AtlanClient(base_url=base_url, api_key=api_key)


def set_package_ops(run_time_config: RuntimeConfig) -> AtlanClient:
    """
    Set up and processing options and configure the AtlanClient

    :param run_time_config: the generated RuntimeConfig from the generated config module
    :returns: an intialized AtlanClient that should be used for any calls to the SDK
    """
    client = get_client(run_time_config.user_id or "")
    if run_time_config.agent == "workflow":
        client = set_package_headers(client)
    return client


def set_package_headers(client: AtlanClient) -> AtlanClient:
    """
    Configure the AtlanClient with package headers from environment variables.

    :param client: AtlanClient instance to configure
    :returns: updated AtlanClient instance.
    """

    if (agent := os.environ.get("X_ATLAN_AGENT")) and (
        agent_id := os.environ.get("X_ATLAN_AGENT_ID")
    ):
        headers: Dict[str, str] = {
            "x-atlan-agent": agent,
            "x-atlan-agent-id": agent_id,
            "x-atlan-agent-package-name": os.environ.get(
                "X_ATLAN_AGENT_PACKAGE_NAME", ""
            ),
            "x-atlan-agent-workflow-id": os.environ.get(
                "X_ATLAN_AGENT_WORKFLOW_ID", ""
            ),
        }
        client.update_headers(headers)
    return client


def validate_multiselect(v):
    """
    This method is used to marshal a multi-select value passed from the custom package ui
    """
    if isinstance(v, str):
        if v.startswith("["):
            data = json.loads(v)
            v = parse_obj_as(List[str], data)
        else:
            v = [v]
    return v


def validate_connection(v):
    """
    This method is used to marshal a connection value passed from the custom package ui
    """
    from pyatlan.model.assets import Connection

    if isinstance(v, Connection):
        return v
    if isinstance(v, dict):
        return Connection.parse_obj(v)
    if isinstance(v, str):
        return Connection.parse_raw(v)
    raise ValueError("Invalid type for connection field")


def validate_connector_and_connection(v):
    """
    This method is used to marshal a connector and connection value passed from the custom package ui
    """
    from pyatlan.pkg.models import ConnectorAndConnection

    return parse_raw_as(ConnectorAndConnection, v)


def has_handler(logger: logging.Logger, handler_class) -> bool:
    c: Optional[logging.Logger] = logger
    while c:
        for hdlr in c.handlers:
            if isinstance(hdlr, handler_class):
                return True
        c = c.parent if c.propagate else None
    return False


def add_otel_handler(
    logger: logging.Logger, level: Union[int, str], resource: dict
) -> None:
    """
    Adds an OpenTelemetry handler to the logger if not already present.

    Args:
        logger (logging.Logger): The logger to which the handler will be added.
        level (int | str): The logging level.
        resource (dict): A dictionary of resource attributes to be associated with the logger.
    """
    if OTEL_IMPORTS_AVAILABLE and not has_handler(logger, LoggingHandler):
        workflow_node_name = os.getenv("OTEL_WF_NODE_NAME", "")
        if workflow_node_name:
            resource["k8s.workflow.node.name"] = workflow_node_name
        logger_provider = LoggerProvider(Resource.create(resource))
        otel_log_exporter = OTLPLogExporter(
            endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"), insecure=True
        )
        logger_provider.add_log_record_processor(
            CustomBatchLogRecordProcessor(otel_log_exporter)
        )

        otel_handler = LoggingHandler(level=level, logger_provider=logger_provider)
        otel_handler.setLevel(level)
        logger.addHandler(otel_handler)
        logger.info("OpenTelemetry handler added to the logger.")
