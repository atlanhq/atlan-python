# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
import json
import logging
import os
import sys
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from pydantic.v1 import parse_obj_as, parse_raw_as

from pyatlan.client.atlan import AtlanClient
from pyatlan.pkg.models import RuntimeConfig

LOGGER = logging.getLogger(__name__)

# Try to import OpenTelemetry libraries
try:
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (  # type:ignore
        OTLPLogExporter,
    )
    from opentelemetry.sdk._logs import (  # type:ignore
        LogData,
        LoggerProvider,
        LoggingHandler,
    )
    from opentelemetry.sdk._logs._internal.export import (  # type:ignore
        BatchLogRecordProcessor,
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
    return client


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
    """
    Checks if a logger or its ancestor has a handler of a specific class. The function
    iterates through the logger's handlers and optionally ascends the logger hierarchy,
    checking each logger's handlers for an instance of the specified handler class.

    Args:
        logger (logging.Logger): The logger to inspect for the handler.
        handler_class: The class of the handler to look for.

    Returns:
        bool: True if the handler of the specified class is found, False otherwise.
    """
    c: Optional[logging.Logger] = logger
    while c:
        for hdlr in c.handlers:
            if isinstance(hdlr, handler_class):
                return True
        c = c.parent if c.propagate else None
    return False


def add_otel_handler(
    logger: logging.Logger, level: Union[int, str], resource: dict
) -> Optional[logging.Handler]:
    """
    Adds an OpenTelemetry logging handler to the provided logger if the necessary
    OpenTelemetry imports are available and the handler is not already present.
    This function uses the provided logging level and resource configuration for
    setting up the OpenTelemetry handler. The handler is set up with a custom
    formatter for log messages. This function also makes use of workflow-specific
    environment variables to enrich the resource data with workflow node
    information if available.

    Parameters:
    logger (logging.Logger): The logger instance to which the OpenTelemetry
        handler will be added.
    level (Union[int, str]): The logging level to be set for the OpenTelemetry
        handler, such as logging.INFO or logging.DEBUG.
    resource (dict): A dictionary representing the OpenTelemetry resource
        configuration. Additional resource attributes may be dynamically added
        inside the function.

    Returns:
    Optional[logging.Logger]: The created OpenTelemetry handler if successfully
        added; otherwise, None.
    """
    if OTEL_IMPORTS_AVAILABLE and not has_handler(logger, LoggingHandler):
        if workflow_node_name := os.getenv("OTEL_WF_NODE_NAME", ""):
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
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        otel_handler.setFormatter(formatter)
        logger.addHandler(otel_handler)
        logger.info("OpenTelemetry handler with formatter added to the logger.")
        return otel_handler
    return None


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Ignore KeyboardInterrupt so a console python program can exit with Ctrl + C.
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    LOGGER.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_uncaught_exception
