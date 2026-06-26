# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class AtlanGlueInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-glue` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-glue"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    catalog_id: str = Field("AwsDataCatalog", alias="catalog-id")
    """Catalog ID — The Glue Data Catalog ID to crawl. Use 'AwsDataCatalog' for the default catalog. For S3 Table Buckets (federated catalogs), use '<account_id>:s3tablescatalog/<bucket_name>'."""
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Only the selected databases will be extracted. Exclude gets preference over include for common databases, if present, in the config."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected databases won't be extracted."""
    exclude_table_regex: str = Field("", alias="exclude-table-regex")
    """Exclude table regex — Regex of tables to exclude. Defaults to empty string and includes all tables."""


class AtlanGlue(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-glue` app.

    Example::

        resp = (
            AtlanGlue(client)
            .iam(username="...", password="...", region="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .catalog_id("")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-glue"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "glue"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-glue"
    _INPUTS_CLASS = AtlanGlueInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def iam(
        self, *, username: str, password: str, region: str, **extra: Any
    ) -> "AtlanGlue":
        """Direct extraction with iam auth.

        :param username: AWS Access Key.
        :param password: AWS Secret Key.
        :param region: Region.
        """
        extras: Dict[str, Any] = {}
        extras["region"] = region
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-glue",
                connector_type="glue",
                auth_type="iam",
                username=username,
                password=password,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def role(
        self,
        *,
        aws_role_arn: Optional[str] = None,
        aws_external_id: Optional[str] = None,
        region: str,
        **extra: Any,
    ) -> "AtlanGlue":
        """Direct extraction with role auth.

        :param aws_role_arn: AWS Role ARN.
        :param aws_external_id: AWS External ID.
        :param region: Region.
        """
        extras: Dict[str, Any] = {}
        if aws_role_arn is not None:
            extras["aws_role_arn"] = aws_role_arn
        if aws_external_id is not None:
            extras["aws_external_id"] = aws_external_id
        extras["region"] = region
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-glue",
                connector_type="glue",
                auth_type="role",
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def catalog_id(self, value: str) -> "AtlanGlue":
        """Catalog ID — The Glue Data Catalog ID to crawl. Use 'AwsDataCatalog' for the default catalog. For S3 Table Buckets (federated catalogs), use '<account_id>:s3tablescatalog/<bucket_name>'."""
        self._metadata["catalog-id"] = value
        return self

    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanGlue":
        """Include Metadata — Only the selected databases will be extracted. Exclude gets preference over include for common databases, if present, in the config."""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanGlue":
        """Exclude Metadata — Selected databases won't be extracted."""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_table_regex(self, value: str) -> "AtlanGlue":
        """Exclude table regex — Regex of tables to exclude. Defaults to empty string and includes all tables."""
        self._metadata["exclude-table-regex"] = value
        return self


__all__ = ["AtlanGlue", "AtlanGlueInputs"]
