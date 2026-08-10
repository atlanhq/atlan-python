# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class CsaUberAssetExportBasicInputs(AppInput):
    """Typed, UI-facing inputs for the `csa-uber-asset-export-basic` / `asset-export-basic` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "csa-uber-asset-export-basic"
    _ENTRYPOINT: ClassVar[Optional[str]] = 'asset-export-basic'

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    delivery_type: str = Field('DIRECT', alias="delivery-type")
    """Export via — How to deliver the export. Download keeps it in Atlan (Runs tab); Email sends it to the recipients below; Object storage uploads to S3 / GCS / ADLS / Google Sheet."""
    email_addresses: str = Field("", alias="email-addresses")
    """Recipient email address(es) — Comma-separated email addresses to send the export to as an attachment. Only commas are supported as separators. Leave blank to skip email."""
    export_scope: str = Field('ENRICHED_ONLY', alias="export-scope")
    """Export scope — Whether to export only assets enriched by users, or all assets with the qualified name prefix."""
    qn_prefix: str = Field('default', alias="qn-prefix")
    """Qualified name prefix (for assets) — Starting value for a qualifiedName that determines which assets to export."""
    include_description: bool = Field(True, alias="include-description")
    """Include description? — Whether to also include system-level description (Yes), or only user-entered description (No)."""
    include_glossaries: bool = Field(False, alias="include-glossaries")
    """Include glossaries? — Whether glossaries (and their terms and categories) should be exported too."""
    include_products: bool = Field(False, alias="include-products")
    """Include data products? — Whether data products (and their domains) should be exported too."""
    include_archived: bool = Field(False, alias="include-archived")
    """Include archived? — Whether to include archived assets in the export (Yes) or only active assets (No)."""


class CsaUberAssetExportBasic(AppBuilder):
    """Fluent, UI-equivalent builder for the `csa-uber-asset-export-basic` / `asset-export-basic` app.

    Example::

        resp = (
            CsaUberAssetExportBasic(client)
            .s3(username="...", password="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .export_via('DIRECT')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "csa-uber-asset-export-basic"
    _ENTRYPOINT: ClassVar[Optional[str]] = 'asset-export-basic'
    _CONNECTOR_NAME: ClassVar[str] = "csa-connectors-objectstore"
    _CONNECTOR_CONFIG: ClassVar[str] = "csa-connectors-objectstore"
    _INPUTS_CLASS = CsaUberAssetExportBasicInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {'all_attributes': False}

    # ── Step 1 · Credential ──
    def s3(self, *, username: str, password: str, aws_role_arn: Optional[str] = None, region: Optional[str] = None, s3_bucket: Optional[str] = None, **extra: Any) -> "CsaUberAssetExportBasic":
        """Direct extraction with S3 auth.

        :param username: AWS access key.
        :param password: AWS secret key.
        :param aws_role_arn: AWS Role ARN.
        :param region: Region.
        :param s3_bucket: Bucket.
        """
        extras: Dict[str, Any] = {}
        if aws_role_arn is not None:
            extras["aws_role_arn"] = aws_role_arn
        if region is not None:
            extras["region"] = region
        if s3_bucket is not None:
            extras["s3_bucket"] = s3_bucket
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="csa-connectors-objectstore",
                auth_type="s3",
                username=username,
                password=password,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def gcs(self, *, username: str, password: str, gcs_bucket: Optional[str] = None, **extra: Any) -> "CsaUberAssetExportBasic":
        """Direct extraction with GCS auth.

        :param username: Project ID.
        :param password: Service account JSON.
        :param gcs_bucket: Bucket.
        """
        extras: Dict[str, Any] = {}
        if gcs_bucket is not None:
            extras["gcs_bucket"] = gcs_bucket
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="csa-connectors-objectstore",
                auth_type="gcs",
                username=username,
                password=password,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def adls(self, *, username: str, password: str, azure_tenant_id: Optional[str] = None, storage_account_name: Optional[str] = None, adls_container: Optional[str] = None, **extra: Any) -> "CsaUberAssetExportBasic":
        """Direct extraction with ADLS auth.

        :param username: Azure client ID.
        :param password: Azure client secret.
        :param azure_tenant_id: Azure tenant ID.
        :param storage_account_name: Storage account name.
        :param adls_container: Container.
        """
        extras: Dict[str, Any] = {}
        if azure_tenant_id is not None:
            extras["azure_tenant_id"] = azure_tenant_id
        if storage_account_name is not None:
            extras["storage_account_name"] = storage_account_name
        if adls_container is not None:
            extras["adls_container"] = adls_container
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="csa-connectors-objectstore",
                auth_type="adls",
                username=username,
                password=password,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def export_via(self, value: Literal['DIRECT', 'EMAIL', 'CLOUD']) -> "CsaUberAssetExportBasic":
        """Export via — How to deliver the export. Download keeps it in Atlan (Runs tab); Email sends it to the recipients below; Object storage uploads to S3 / GCS / ADLS / Google Sheet."""
        self._metadata["delivery-type"] = value
        return self

    def recipient_email_addresses(self, value: str) -> "CsaUberAssetExportBasic":
        """Recipient email address(es) — Comma-separated email addresses to send the export to as an attachment. Only commas are supported as separators. Leave blank to skip email."""
        self._metadata["email-addresses"] = value
        return self

    def export_scope(self, value: Literal['GLOSSARIES_ONLY', 'PRODUCTS_ONLY', 'ENRICHED_ONLY', 'ALL']) -> "CsaUberAssetExportBasic":
        """Export scope — Whether to export only assets enriched by users, or all assets with the qualified name prefix."""
        self._metadata["export-scope"] = value
        return self

    def qualified_name_prefix_for_assets(self, value: str) -> "CsaUberAssetExportBasic":
        """Qualified name prefix (for assets) — Starting value for a qualifiedName that determines which assets to export."""
        self._metadata["qn-prefix"] = value
        return self

    def include_description(self, enabled: bool = True) -> "CsaUberAssetExportBasic":
        """Include description? — Whether to also include system-level description (Yes), or only user-entered description (No)."""
        self._metadata["include-description"] = enabled
        return self

    def include_glossaries(self, enabled: bool = True) -> "CsaUberAssetExportBasic":
        """Include glossaries? — Whether glossaries (and their terms and categories) should be exported too."""
        self._metadata["include-glossaries"] = enabled
        return self

    def include_data_products(self, enabled: bool = True) -> "CsaUberAssetExportBasic":
        """Include data products? — Whether data products (and their domains) should be exported too."""
        self._metadata["include-products"] = enabled
        return self

    def include_archived(self, enabled: bool = True) -> "CsaUberAssetExportBasic":
        """Include archived? — Whether to include archived assets in the export (Yes) or only active assets (No)."""
        self._metadata["include-archived"] = enabled
        return self


__all__ = ["CsaUberAssetExportBasic", "CsaUberAssetExportBasicInputs"]
