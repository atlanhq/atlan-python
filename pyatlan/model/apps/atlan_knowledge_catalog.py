# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AtlanKnowledgeCatalogInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-knowledge-catalog` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-knowledge-catalog"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_projects: Dict[str, Any] = Field({}, alias="include-projects")
    """Include Projects (Optional) — Select GCP projects to include. If empty, all accessible projects are ingested."""
    exclude_projects: Dict[str, Any] = Field({}, alias="exclude-projects")
    """Exclude Projects (Optional) — Select GCP projects to exclude from ingestion."""
    include_aspect_types: Dict[str, Any] = Field({}, alias="include-aspect-types")
    """Include Aspect Types — Select specific Aspect Types to include. If specified, ONLY these aspects will be extracted. Leave empty to extract all aspects."""
    exclude_aspect_types: Dict[str, Any] = Field({}, alias="exclude-aspect-types")
    """Exclude Aspect Types — Select Aspect Types to exclude. These aspects will be skipped during extraction."""
    ingest_aspects: str = Field("no", alias="ingest-aspects")
    """Ingest Knowledge Catalog Aspect Metadata? — When enabled, discovers all Knowledge Catalog Aspect Types across accessible GCP projects and writes per-asset aspect metadata to Atlan assets."""
    ingest_dq: str = Field("no", alias="ingest-dq")
    """Ingest Data Quality Metadata? — When enabled, fetches DATA_QUALITY scan results from Knowledge Catalog and writes DQ scores, rules, and dimension breakdowns to Atlan table and column assets."""
    ingest_profiling: str = Field("no", alias="ingest-profiling")
    """Ingest Data Profiling Metadata? — When enabled, fetches DATA_PROFILE scan results from Knowledge Catalog and writes per-column profiling metrics (missing values, distinct values, top values, min/max/mean, etc.) to Atlan column assets."""
    preflight_check: str = Field("", alias="preflight-check")


class AtlanKnowledgeCatalog(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-knowledge-catalog` app.

    Example::

        resp = (
            AtlanKnowledgeCatalog(client)
            .basic(service_account_json="...", project_id="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .include_projects_optional({})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-knowledge-catalog"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "dataplex"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-dataplex"
    _INPUTS_CLASS = AtlanKnowledgeCatalogInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "enable_aspects_reverse_sync": "no",
        "extraction_method": "direct",
    }

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        network_connectivity: Optional[str] = None,
        psc_host: Optional[str] = None,
        service_account_json: str,
        project_id: str,
        **extra: Any,
    ) -> "AtlanKnowledgeCatalog":
        """Direct extraction with Service Account Authentication auth.

        :param network_connectivity: Network Connectivity.
        :param psc_host: PSC Hostname.
        :param service_account_json: Service Account JSON.
        :param project_id: Home Project Id.
        """
        extras: Dict[str, Any] = {}
        if network_connectivity is not None:
            extras["network_connectivity"] = network_connectivity
        if psc_host is not None:
            extras["psc_host"] = psc_host
        extras["service_account_json"] = service_account_json
        extras["project_id"] = project_id
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dataplex",
                connector_type="dataplex",
                auth_type="basic",
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def gcp_wif(
        self,
        *,
        network_connectivity: Optional[str] = None,
        psc_host: Optional[str] = None,
        service_account_email: str,
        wif_pool_provider_id: str,
        atlan_oauth_id: str,
        atlan_oauth_secret: str,
        project_id: str,
        **extra: Any,
    ) -> "AtlanKnowledgeCatalog":
        """Direct extraction with Workload Identity Federation auth.

        :param network_connectivity: Network Connectivity.
        :param psc_host: PSC Hostname.
        :param service_account_email: Service Account Email.
        :param wif_pool_provider_id: WIF Pool Provider ID.
        :param atlan_oauth_id: Atlan OAuth Client ID.
        :param atlan_oauth_secret: Atlan OAuth Client Secret.
        :param project_id: Home Project Id.
        """
        extras: Dict[str, Any] = {}
        if network_connectivity is not None:
            extras["network_connectivity"] = network_connectivity
        if psc_host is not None:
            extras["psc_host"] = psc_host
        extras["service_account_email"] = service_account_email
        extras["wif_pool_provider_id"] = wif_pool_provider_id
        extras["atlan_oauth_id"] = atlan_oauth_id
        extras["atlan_oauth_secret"] = atlan_oauth_secret
        extras["project_id"] = project_id
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-dataplex",
                connector_type="dataplex",
                auth_type="gcp-wif",
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_projects_optional(
        self, value: Dict[str, Any]
    ) -> "AtlanKnowledgeCatalog":
        """Include Projects (Optional) — Select GCP projects to include. If empty, all accessible projects are ingested."""
        self._metadata["include-projects"] = value
        return self

    def exclude_projects_optional(
        self, value: Dict[str, Any]
    ) -> "AtlanKnowledgeCatalog":
        """Exclude Projects (Optional) — Select GCP projects to exclude from ingestion."""
        self._metadata["exclude-projects"] = value
        return self

    def include_aspect_types(self, value: Dict[str, Any]) -> "AtlanKnowledgeCatalog":
        """Include Aspect Types — Select specific Aspect Types to include. If specified, ONLY these aspects will be extracted. Leave empty to extract all aspects."""
        self._metadata["include-aspect-types"] = value
        return self

    def exclude_aspect_types(self, value: Dict[str, Any]) -> "AtlanKnowledgeCatalog":
        """Exclude Aspect Types — Select Aspect Types to exclude. These aspects will be skipped during extraction."""
        self._metadata["exclude-aspect-types"] = value
        return self

    def ingest_knowledge_catalog_aspect_metadata(
        self, value: Literal["yes", "no"]
    ) -> "AtlanKnowledgeCatalog":
        """Ingest Knowledge Catalog Aspect Metadata? — When enabled, discovers all Knowledge Catalog Aspect Types across accessible GCP projects and writes per-asset aspect metadata to Atlan assets."""
        self._metadata["ingest-aspects"] = value
        return self

    def ingest_data_quality_metadata(
        self, value: Literal["yes", "no"]
    ) -> "AtlanKnowledgeCatalog":
        """Ingest Data Quality Metadata? — When enabled, fetches DATA_QUALITY scan results from Knowledge Catalog and writes DQ scores, rules, and dimension breakdowns to Atlan table and column assets."""
        self._metadata["ingest-dq"] = value
        return self

    def ingest_data_profiling_metadata(
        self, value: Literal["yes", "no"]
    ) -> "AtlanKnowledgeCatalog":
        """Ingest Data Profiling Metadata? — When enabled, fetches DATA_PROFILE scan results from Knowledge Catalog and writes per-column profiling metrics (missing values, distinct values, top values, min/max/mean, etc.) to Atlan column assets."""
        self._metadata["ingest-profiling"] = value
        return self

    def preflight_check(self, value: str) -> "AtlanKnowledgeCatalog":
        self._metadata["preflight-check"] = value
        return self


__all__ = ["AtlanKnowledgeCatalog", "AtlanKnowledgeCatalogInputs"]
