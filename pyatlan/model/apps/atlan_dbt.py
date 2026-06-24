# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


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
            .api(password="...")
            .connection(name="my-connection", admins=["jdoe"])
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
        self, *, password: str, host: Optional[str] = None, **extra: Any
    ) -> "AtlanDbt":
        """Direct extraction with api auth.

        :param password: API Token.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="api",
            password=password,
            host=host or "https://cloud.getdbt.com",
            extra=extras,
        )
        return self

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
