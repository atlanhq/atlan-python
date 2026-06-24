# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AtlanDbtInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-dbt` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-dbt"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    extraction_type: str = Field("api", alias="extraction-type")
    """Source — How the connector pulls dbt metadata: dbt Cloud API or pre-extracted artifacts from object storage."""
    manifest_source: str = Field("atlan", alias="manifest-source")
    """Manifest Source — Where dbt artifacts are stored: Atlan's object storage (no extra credential needed) or an external cloud bucket (AWS/GCP/Azure)."""
    core_extract_output_prefix: str = Field("", alias="core-extract-output-prefix")
    """Object Storage Prefix — Path in Atlan's object storage where dbt artifacts are stored. Example: artifacts/apps/dbt/workflows/my-run/metadata"""
    include_filter: Dict[str, Any] = Field("{}", alias="include-filter")
    """Include Metadata — Only selected projects and jobs will be processed. Exclude gets preference over include."""
    exclude_filter: Dict[str, Any] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected projects and jobs will not be processed."""
    include_filter_core: str = Field("*", alias="include-filter-core")
    """Include Folder Filter — Pipe-separated folder name patterns to include during Core extraction. Defaults to * (include all). Example: project_a|project_b"""
    exclude_filter_core: str = Field("*", alias="exclude-filter-core")
    """Exclude Folder Filter — Pipe-separated folder name patterns to exclude during Core extraction. Defaults to * (exclude none). Example: old_project|archive"""
    enable_dbt_tagsync: bool = Field(False, alias="enable-dbt-tagsync")
    """Import Tags — Sync dbt tags to Atlan tags. If disabled, dbt tags import as standalone attributes."""
    advanced_options_config: bool = Field(False, alias="advanced-options-config")
    """Advanced options — Advanced options used when processing the extracted data."""
    enrich_materialised_sql_assets: bool = Field(
        True, alias="enrich-materialised-sql-assets"
    )
    """Enrich Metadata in Materialized Assets — Default behaviour is to add enrichment to the dbt Assets and the Materialized Assets. Select No to enrich only the dbt Assets."""


class AtlanDbt(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-dbt` app.

    Example::

        resp = (
            AtlanDbt(client)
            .connection(qualified_name="default/dbt/1700000000")
            .source('api')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-dbt"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "dbt"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-dbt"
    _INPUTS_CLASS = AtlanDbtInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"extraction_method": "direct"}

    # ── Step 1 · Credential ──
    def api(
        self,
        *,
        password: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanDbt":
        """Direct extraction with api auth.

        :param password: API Token.
        """
        extras: Dict[str, Any] = {}
        extras.update(extra)
        return self._stage_credential(
            "api_credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dbt",
                connector_type="dbt",
                auth_type="api",
                password=password,
                host=host or "https://cloud.getdbt.com",
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def aws(
        self,
        *,
        object_store_access_type: Optional[str] = None,
        aws_role_arn: Optional[str] = None,
        bucket: str,
        prefix: str,
        region: str,
        **extra: Any,
    ) -> "AtlanDbt":
        """Direct extraction with aws auth.

        :param object_store_access_type: Authentication.
        :param aws_role_arn: AWS Role ARN.
        :param bucket: Bucket Name.
        :param prefix: Prefix.
        :param region: Region.
        """
        extras: Dict[str, Any] = {}
        if object_store_access_type is not None:
            extras["object_store_access_type"] = object_store_access_type
        if aws_role_arn is not None:
            extras["aws_role_arn"] = aws_role_arn
        extras["bucket"] = bucket
        extras["prefix"] = prefix
        extras["region"] = region
        extras.update(extra)
        return self._stage_credential(
            "object_store_credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dbt-objectstore",
                connector_type="dbt-objectstore",
                auth_type="aws",
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def gcp(
        self,
        *,
        object_store_access_type: Optional[str] = None,
        project_id: str,
        service_account_json: str,
        bucket: str,
        prefix: str,
        **extra: Any,
    ) -> "AtlanDbt":
        """Direct extraction with gcp auth.

        :param object_store_access_type: Authentication.
        :param project_id: Project ID.
        :param service_account_json: Service Account JSON.
        :param bucket: Bucket Name.
        :param prefix: Prefix.
        """
        extras: Dict[str, Any] = {}
        if object_store_access_type is not None:
            extras["object_store_access_type"] = object_store_access_type
        extras["project_id"] = project_id
        extras["service_account_json"] = service_account_json
        extras["bucket"] = bucket
        extras["prefix"] = prefix
        extras.update(extra)
        return self._stage_credential(
            "object_store_credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dbt-objectstore",
                connector_type="dbt-objectstore",
                auth_type="gcp",
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def azure(
        self,
        *,
        object_store_access_type: Optional[str] = None,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        account_name: str,
        bucket: str,
        prefix: str,
        **extra: Any,
    ) -> "AtlanDbt":
        """Direct extraction with azure auth.

        :param object_store_access_type: Authentication.
        :param tenant_id: Tenant ID.
        :param client_id: Client ID.
        :param client_secret: Client Secret.
        :param account_name: Account Name.
        :param bucket: Container Name.
        :param prefix: Prefix.
        """
        extras: Dict[str, Any] = {}
        if object_store_access_type is not None:
            extras["object_store_access_type"] = object_store_access_type
        extras["tenant_id"] = tenant_id
        extras["client_id"] = client_id
        extras["client_secret"] = client_secret
        extras["account_name"] = account_name
        extras["bucket"] = bucket
        extras["prefix"] = prefix
        extras.update(extra)
        return self._stage_credential(
            "object_store_credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dbt-objectstore",
                connector_type="dbt-objectstore",
                auth_type="azure",
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def source(self, value: Literal["api", "objectstore"]) -> "AtlanDbt":
        """Source — How the connector pulls dbt metadata: dbt Cloud API or pre-extracted artifacts from object storage."""
        self._metadata["extraction-type"] = value
        return self

    def manifest_source(self, value: Literal["atlan", "external"]) -> "AtlanDbt":
        """Manifest Source — Where dbt artifacts are stored: Atlan's object storage (no extra credential needed) or an external cloud bucket (AWS/GCP/Azure)."""
        self._metadata["manifest-source"] = value
        return self

    def object_storage_prefix(self, value: str) -> "AtlanDbt":
        """Object Storage Prefix — Path in Atlan's object storage where dbt artifacts are stored. Example: artifacts/apps/dbt/workflows/my-run/metadata"""
        self._metadata["core-extract-output-prefix"] = value
        return self

    def include_metadata(self, value: Dict[str, Any]) -> "AtlanDbt":
        """Include Metadata — Only selected projects and jobs will be processed. Exclude gets preference over include."""
        self._metadata["include-filter"] = value
        return self

    def exclude_metadata(self, value: Dict[str, Any]) -> "AtlanDbt":
        """Exclude Metadata — Selected projects and jobs will not be processed."""
        self._metadata["exclude-filter"] = value
        return self

    def include_folder_filter(self, value: str) -> "AtlanDbt":
        """Include Folder Filter — Pipe-separated folder name patterns to include during Core extraction. Defaults to * (include all). Example: project_a|project_b"""
        self._metadata["include-filter-core"] = value
        return self

    def exclude_folder_filter(self, value: str) -> "AtlanDbt":
        """Exclude Folder Filter — Pipe-separated folder name patterns to exclude during Core extraction. Defaults to * (exclude none). Example: old_project|archive"""
        self._metadata["exclude-filter-core"] = value
        return self

    def import_tags(self, enabled: bool = True) -> "AtlanDbt":
        """Import Tags — Sync dbt tags to Atlan tags. If disabled, dbt tags import as standalone attributes."""
        self._metadata["enable-dbt-tagsync"] = enabled
        return self

    def advanced_options(self, enabled: bool = True) -> "AtlanDbt":
        """Advanced options — Advanced options used when processing the extracted data."""
        self._metadata["advanced-options-config"] = enabled
        return self

    def enrich_metadata_in_materialized_assets(
        self, enabled: bool = True
    ) -> "AtlanDbt":
        """Enrich Metadata in Materialized Assets — Default behaviour is to add enrichment to the dbt Assets and the Materialized Assets. Select No to enrich only the dbt Assets."""
        self._metadata["enrich-materialised-sql-assets"] = enabled
        return self


__all__ = ["AtlanDbt", "AtlanDbtInputs"]
