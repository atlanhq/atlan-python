# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AtlanDynamodbInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-dynamodb` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-dynamodb"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    exclude_filter: str = Field("", alias="exclude-filter")
    """Exclude tables regex — Pipe-separated regex matched against table names. Example: .*_TMP|.*_TEMP|TMP.*|TEMP.*"""
    include_filter: str = Field("", alias="include-filter")
    """Include tables regex — Pipe-separated regex matched against table names. Example: Employee.*"""


class AtlanDynamodb(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-dynamodb` app.

    Example::

        resp = (
            AtlanDynamodb(client)
            .iam_user(username="...", password="...", region="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .exclude_tables_regex("")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-dynamodb"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "dynamodb"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-dynamodb"
    _INPUTS_CLASS = AtlanDynamodbInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def iam_user(
        self,
        *,
        username: str,
        password: str,
        region: str,
        endpoint_url: Optional[str] = None,
        **extra: Any,
    ) -> "AtlanDynamodb":
        """Direct extraction with iam_user auth.

        :param username: AWS Access Key.
        :param password: AWS Secret Key.
        :param region: AWS Region.
        :param endpoint_url: Custom Endpoint URL.
        """
        extras: Dict[str, Any] = {}
        extras["region"] = region
        if endpoint_url is not None:
            extras["endpoint_url"] = endpoint_url
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dynamodb",
                connector_type="dynamodb",
                auth_type="iam_user",
                username=username,
                password=password,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def assume_role(
        self,
        *,
        aws_role_arn: str,
        aws_external_id: Optional[str] = None,
        session_name: Optional[str] = None,
        region: str,
        endpoint_url: Optional[str] = None,
        **extra: Any,
    ) -> "AtlanDynamodb":
        """Direct extraction with assume_role auth.

        :param aws_role_arn: AWS Role ARN.
        :param aws_external_id: AWS External ID.
        :param session_name: Session Name.
        :param region: AWS Region.
        :param endpoint_url: Custom Endpoint URL.
        """
        extras: Dict[str, Any] = {}
        extras["aws_role_arn"] = aws_role_arn
        if aws_external_id is not None:
            extras["aws_external_id"] = aws_external_id
        if session_name is not None:
            extras["session_name"] = session_name
        extras["region"] = region
        if endpoint_url is not None:
            extras["endpoint_url"] = endpoint_url
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dynamodb",
                connector_type="dynamodb",
                auth_type="assume_role",
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def exclude_tables_regex(self, value: str) -> "AtlanDynamodb":
        """Exclude tables regex — Pipe-separated regex matched against table names. Example: .*_TMP|.*_TEMP|TMP.*|TEMP.*"""
        self._metadata["exclude-filter"] = value
        return self

    def include_tables_regex(self, value: str) -> "AtlanDynamodb":
        """Include tables regex — Pipe-separated regex matched against table names. Example: Employee.*"""
        self._metadata["include-filter"] = value
        return self


__all__ = ["AtlanDynamodb", "AtlanDynamodbInputs"]
