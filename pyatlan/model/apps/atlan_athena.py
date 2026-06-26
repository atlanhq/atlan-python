# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class AtlanAthenaInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-athena` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-athena"
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
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string"""
    advanced_config: str = Field("default", alias="advanced-config")
    """Advanced Config — Set advanced configuration of the crawler"""
    use_source_schema_filtering: str = Field(
        "false", alias="use-source-schema-filtering"
    )
    """Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source. Schemas selected in the include filter will be fetched."""


class AtlanAthena(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-athena` app.

    Example::

        resp = (
            AtlanAthena(client)
            .basic(username="...", password="...", s3_output_location="...", host="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-athena"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "athena"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-athena"
    _INPUTS_CLASS = AtlanAthenaInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "extraction_method": "direct",
        "use_jdbc_internal_methods": "true",
        "fetch_partitions": "false",
    }

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        s3_output_location: str,
        workgroup: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanAthena":
        """Direct extraction with basic auth.

        :param username: AWS Access Key.
        :param password: AWS Secret Key.
        :param s3_output_location: S3 Output Location.
        :param workgroup: Workgroup.
        """
        extras: Dict[str, Any] = {}
        extras["s3_output_location"] = s3_output_location
        if workgroup is not None:
            extras["workgroup"] = workgroup
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-athena",
                connector_type="athena",
                auth_type="basic",
                username=username,
                password=password,
                host=host,
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def role(
        self,
        *,
        aws_role_arn: Optional[str] = None,
        aws_external_id: Optional[str] = None,
        s3_output_location: str,
        workgroup: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanAthena":
        """Direct extraction with role auth.

        :param aws_role_arn: AWS Role ARN.
        :param aws_external_id: External ID.
        :param s3_output_location: S3 Output Location.
        :param workgroup: Workgroup.
        """
        extras: Dict[str, Any] = {}
        if aws_role_arn is not None:
            extras["aws_role_arn"] = aws_role_arn
        if aws_external_id is not None:
            extras["aws_external_id"] = aws_external_id
        extras["s3_output_location"] = s3_output_location
        if workgroup is not None:
            extras["workgroup"] = workgroup
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-athena",
                connector_type="athena",
                auth_type="role",
                host=host,
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanAthena":
        """Include Metadata"""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanAthena":
        """Exclude Metadata"""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "AtlanAthena":
        """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string"""
        self._metadata["temp-table-regex"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "AtlanAthena":
        """Advanced Config — Set advanced configuration of the crawler"""
        self._metadata["advanced-config"] = value
        return self

    def enable_source_level_filtering(
        self, value: Literal["true", "false"]
    ) -> "AtlanAthena":
        """Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source. Schemas selected in the include filter will be fetched."""
        self._metadata["use-source-schema-filtering"] = value
        return self


__all__ = ["AtlanAthena", "AtlanAthenaInputs"]
