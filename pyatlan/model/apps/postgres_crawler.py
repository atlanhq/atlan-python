# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class PostgresCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `postgres-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "postgres-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Only the selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected databases and schemas won't be extracted."""
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore."""
    advanced_config: str = Field("default", alias="advanced-config")
    """Advanced Config — Set advanced configuration of the crawler."""
    use_source_schema_filtering: str = Field(
        "false", alias="use-source-schema-filtering"
    )
    """Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source."""
    control_config_strategy: str = Field("default", alias="control-config-strategy")
    """Control Config — Controls custom experimental feature flags for the crawler."""
    control_config: str = Field("{}", alias="control-config")
    """Custom Config — Custom JSON config controlling experimental feature flags."""


class PostgresCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `postgres-crawler` / `crawler` app.

    Example::

        resp = (
            PostgresCrawler(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "postgres-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "postgres"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-postgres"
    _INPUTS_CLASS = PostgresCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"use_jdbc_internal_methods": "true"}

    # ── Step 1 · Credential ──
    def basic(self, *, username: str, password: str, **extra: Any) -> "PostgresCrawler":
        """Direct extraction with Basic Authentication auth.

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
        aws_region: str,
        rds_port: Optional[str] = None,
        **extra: Any,
    ) -> "PostgresCrawler":
        """Direct extraction with IAM User auth.

        :param username: AWS Access Key.
        :param password: AWS Secret Key.
        :param username_2: Database Username.
        :param aws_region: AWS Region.
        :param rds_port: RDS Port.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["username"] = username_2
        extras["aws_region"] = aws_region
        if rds_port is not None:
            extras["rds_port"] = rds_port
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="iam_user",
            username=username,
            password=password,
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
        aws_region: str,
        rds_port: Optional[str] = None,
        **extra: Any,
    ) -> "PostgresCrawler":
        """Direct extraction with IAM Role auth.

        :param username: Database Username.
        :param aws_role_arn: AWS Role ARN.
        :param aws_external_id: AWS External ID.
        :param aws_region: AWS Region.
        :param rds_port: RDS Port.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["aws_role_arn"] = aws_role_arn
        if aws_external_id is not None:
            extras["aws_external_id"] = aws_external_id
        extras["aws_region"] = aws_region
        if rds_port is not None:
            extras["rds_port"] = rds_port
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="iam_role",
            username=username,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "PostgresCrawler":
        """Include Metadata — Only the selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config."""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "PostgresCrawler":
        """Exclude Metadata — Selected databases and schemas won't be extracted."""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "PostgresCrawler":
        """Exclude regex for tables & views — Regex of tables & views to ignore."""
        self._metadata["temp-table-regex"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "PostgresCrawler":
        """Advanced Config — Set advanced configuration of the crawler."""
        self._metadata["advanced-config"] = value
        return self

    def enable_source_level_filtering(
        self, value: Literal["true", "false"]
    ) -> "PostgresCrawler":
        """Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source."""
        self._metadata["use-source-schema-filtering"] = value
        return self

    def control_config(self, value: Literal["default", "custom"]) -> "PostgresCrawler":
        """Control Config — Controls custom experimental feature flags for the crawler."""
        self._metadata["control-config-strategy"] = value
        return self

    def custom_config(self, value: str) -> "PostgresCrawler":
        """Custom Config — Custom JSON config controlling experimental feature flags."""
        self._metadata["control-config"] = value
        return self


__all__ = ["PostgresCrawler", "PostgresCrawlerInputs"]
