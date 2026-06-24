# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


class AtlanMysqlInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-mysql` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-mysql"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata"""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata"""
    exclude_table_regex: str = Field("", alias="exclude-table-regex")
    """Exclude regex for tables & views — Regular expression to exclude temporary tables and views."""


class AtlanMysql(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-mysql` app.

    Example::

        resp = (
            AtlanMysql(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-mysql"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "mysql"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-mysql"
    _INPUTS_CLASS = AtlanMysqlInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self, *, username: str, password: str, port: Optional[int] = None, **extra: Any
    ) -> "AtlanMysql":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            port=port or 3306,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def iam_user(
        self,
        *,
        username: str,
        password: str,
        username_2: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanMysql":
        """Direct extraction with iam_user auth.

        :param username: AWS Access Key ID.
        :param password: AWS Secret Access Key.
        :param username_2: Database User.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["username"] = username_2
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="iam_user",
            username=username,
            password=password,
            port=port or 3306,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def iam_role(
        self,
        *,
        username: str,
        aws_role_arn: str,
        aws_external_id: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanMysql":
        """Direct extraction with iam_role auth.

        :param username: Database User.
        :param aws_role_arn: IAM Role ARN.
        :param aws_external_id: AWS External ID.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["aws_role_arn"] = aws_role_arn
        if aws_external_id is not None:
            extras["aws_external_id"] = aws_external_id
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="iam_role",
            username=username,
            port=port or 3306,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanMysql":
        """Include Metadata"""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanMysql":
        """Exclude Metadata"""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "AtlanMysql":
        """Exclude regex for tables & views — Regular expression to exclude temporary tables and views."""
        self._metadata["exclude-table-regex"] = value
        return self


__all__ = ["AtlanMysql", "AtlanMysqlInputs"]
