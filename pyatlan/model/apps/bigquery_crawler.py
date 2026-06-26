# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""BigQuery crawler app — typed inputs + fluent builder.

Reference hand-written shape, sourced from the app's UI configmaps:
  * inputs form   : /api/service/configmaps/bigquery-crawler?entrypoint=crawler
  * credential    : /api/service/configmaps/atlan-connectors-bigquery?app_id=bigquery-crawler

Only the fields the UI actually surfaces (``ui.hidden`` == false) are exposed;
the hidden runtime/tuning knobs ride along via ``_HIDDEN_DEFAULTS`` so the
submitted payload matches the UI exactly. The configmap-driven generator will
emit this same shape for every app.
"""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Mapping, Optional, Union

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class BigqueryCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the ``bigquery-crawler`` / ``crawler`` app."""

    _APP_ID: ClassVar[str] = "bigquery-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    """Extraction method (``direct`` or ``agent``)."""
    credential_guid: Optional[str] = None
    """Vaulted credential GUID (direct extraction)."""
    agent_json: Optional[Any] = None
    """Self-Deployed Runtime config (agent extraction)."""

    # Step 3 · Metadata
    include_filter: Union[Dict[str, Any], str] = "{}"
    """Include Metadata — datasets to crawl."""
    exclude_filter: Union[Dict[str, Any], str] = "{}"
    """Exclude Metadata — datasets to skip."""
    temp_table_regex: str = ""
    """Exclude regex for tables & views."""
    enable_nested_columns: bool = True
    """Import Nested Columns."""
    enable_bigquery_tag_sync: bool = False
    """Import Tags from BigQuery to Atlan."""
    filter_sharded_tables: bool = True
    """Combine Sharded Tables of the same prefix into one asset."""
    hidden_datasets: bool = False
    """Hidden Assets — access hidden datasets."""
    control_config_strategy: str = "default"
    """Advanced Config (``default`` or ``custom``)."""
    control_config: str = "{}"
    """Custom Config JSON (used when strategy is ``custom``)."""
    preflight_check: str = ""
    """Preflight check payload."""


class BigqueryCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for a BigQuery crawler workflow.

    Example::

        resp = (
            BigqueryCrawler(client)
            .service_account(
                email="svc@my-project.iam.gserviceaccount.com",
                service_account_json=sa_json,
                project_id="my-project",
            )
            .connection(name="prod-bigquery", admin_users=["jdoe"])
            .include({"my-project": ["analytics_*"]})
            .import_nested_columns(True)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "bigquery-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "bigquery"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-bigquery"
    _INPUTS_CLASS = BigqueryCrawlerInputs
    _DEFAULT_HOST: ClassVar[str] = "https://bigquery.googleapis.com"
    _DEFAULT_PORT: ClassVar[int] = 443
    # ui.hidden inputs the UI still submits with these defaults.
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "atlas_auth_type": "internal",
        "list_datasets_per_chunk": 50,
        "mapping_chunk_size": 1000,
        "extract_output_chuck_size": 50000,
        "max_concurrent_activities": 15,
        "max_activities_per_execution": 300,
    }

    # ── Step 1 · Credential ────────────────────────────────────────────────
    def service_account(
        self,
        *,
        email: str,
        service_account_json: str,
        project_id: str,
        connectivity: str = "public",
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> "BigqueryCrawler":
        """Direct extraction with Service Account auth (the UI default).

        :param email: Service Account Email.
        :param service_account_json: Service Account JSON key (vaulted, never logged).
        :param project_id: GCP project ID.
        :param connectivity: ``public`` (Google's endpoint) or ``private`` (PSC).
        :param host: Private Service Connect host (required for ``private``).
        """
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name=self._CONNECTOR_CONFIG,
                connector_type=self._CONNECTOR_NAME,
                auth_type="basic",
                host=host or self._DEFAULT_HOST,
                port=port or self._DEFAULT_PORT,
                username=email,
                password=service_account_json,
                extra={"project_id": project_id, "connect_type": connectivity},
            ),
        )

    def workload_identity_federation(
        self,
        *,
        project_id: str,
        connectivity: str = "public",
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "BigqueryCrawler":
        """Direct extraction with Workload Identity Federation auth."""
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name=self._CONNECTOR_CONFIG,
                connector_type=self._CONNECTOR_NAME,
                auth_type="gcp-wif",
                host=host or self._DEFAULT_HOST,
                port=port or self._DEFAULT_PORT,
                extra={"project_id": project_id, "connect_type": connectivity, **extra},
            ),
        )

    # ── Step 3 · Metadata ──────────────────────────────────────────────────
    def include(self, assets: Union[str, Mapping[str, List[str]]]) -> "BigqueryCrawler":
        """Include Metadata: ``{project: [dataset, ...]}`` (anchored as regex)."""
        self._metadata["include_filter"] = _anchor_filter(assets)
        return self

    def exclude(self, assets: Union[str, Mapping[str, List[str]]]) -> "BigqueryCrawler":
        """Exclude Metadata: ``{project: [dataset, ...]}`` (anchored as regex)."""
        self._metadata["exclude_filter"] = _anchor_filter(assets)
        return self

    def exclude_regex(self, regex: str) -> "BigqueryCrawler":
        """Exclude regex for tables & views."""
        self._metadata["temp_table_regex"] = regex
        return self

    def import_nested_columns(self, enabled: bool = True) -> "BigqueryCrawler":
        self._metadata["enable_nested_columns"] = enabled
        return self

    def import_tags(self, enabled: bool = True) -> "BigqueryCrawler":
        self._metadata["enable_bigquery_tag_sync"] = enabled
        return self

    def combine_sharded_tables(self, enabled: bool = True) -> "BigqueryCrawler":
        self._metadata["filter_sharded_tables"] = enabled
        return self

    def hidden_assets(self, enabled: bool = True) -> "BigqueryCrawler":
        self._metadata["hidden_datasets"] = enabled
        return self

    def custom_config(self, config_json: str) -> "BigqueryCrawler":
        """Advanced Config = custom, with the given JSON feature-flag config."""
        self._metadata["control_config_strategy"] = "custom"
        self._metadata["control_config"] = config_json
        return self


__all__ = ["BigqueryCrawler", "BigqueryCrawlerInputs"]
