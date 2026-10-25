# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class AtlanCloudsqlPostgresCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-cloudsql-postgres` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-cloudsql-postgres"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    cloud_provider: str = Field("", alias="cloud-provider")
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string"""
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Only selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected databases and schemas wont be extracted."""
    redact_sql_text: bool = Field(False, alias="redact-sql-text")
    """Redact SQL Text — Replaces string and numeric literals in extracted SQL definitions with placeholders, in memory, before anything is written to disk. SQL that can't be parsed is kept as-is. Query structure and lineage are preserved. Note: Increases extraction runtime."""


class AtlanCloudsqlPostgresCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-cloudsql-postgres` / `crawler` app.

    Example::

        resp = (
            AtlanCloudsqlPostgresCrawler(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .cloud_provider("")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-cloudsql-postgres"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "cloudsql-postgres"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-cloudsql-postgres"
    _INPUTS_CLASS = AtlanCloudsqlPostgresCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        database: Optional[str] = None,
        ip_type: Optional[str] = None,
        sqlalchemy_url: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Direct extraction with Basic Authentication auth.

        :param username: Username.
        :param password: Password.
        :param ip_type: IP type.
        :param sqlalchemy_url: SQLAlchemy Args.
        :param host: Hostname of the cloudsql-postgres instance (defaults to 'host').
        :param port: Port to connect on (defaults to 5432).
        """
        extras: Dict[str, Any] = {}
        if database is not None:
            extras["database"] = database
        if ip_type is not None:
            extras["ip_type"] = ip_type
        if sqlalchemy_url is not None:
            extras["sqlalchemy_url"] = sqlalchemy_url
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-cloudsql-postgres",
                auth_type="basic",
                username=username,
                password=password,
                host=host or "host",
                port=port or 5432,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def iam_user(
        self,
        *,
        username: str,
        password: str,
        name: str,
        database: Optional[str] = None,
        ip_type: Optional[str] = None,
        sqlalchemy_url: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Direct extraction with IAM User Authentication auth.

        :param username: IAM Username.
        :param password: IAM Auth Token.
        :param name: Connection Name.
        :param ip_type: IP type.
        :param sqlalchemy_url: SQLAlchemy Args.
        :param host: Hostname of the cloudsql-postgres instance (defaults to 'host').
        :param port: Port to connect on (defaults to 5432).
        """
        extras: Dict[str, Any] = {}
        extras["__name"] = name
        if database is not None:
            extras["database"] = database
        if ip_type is not None:
            extras["ip_type"] = ip_type
        if sqlalchemy_url is not None:
            extras["sqlalchemy_url"] = sqlalchemy_url
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-cloudsql-postgres",
                auth_type="iam_user",
                username=username,
                password=password,
                host=host or "host",
                port=port or 5432,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def iam_service_account(
        self,
        *,
        username: str,
        password: str,
        name: str,
        gcp_service_account: Optional[str] = None,
        database: Optional[str] = None,
        ip_type: Optional[str] = None,
        sqlalchemy_url: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Direct extraction with IAM Service Account auth.

        :param username: IAM Service Account name.
        :param password: Password.
        :param name: Connection Name.
        :param gcp_service_account: IAM Service Account key.
        :param ip_type: IP type.
        :param sqlalchemy_url: SQLAlchemy Args.
        :param host: Hostname of the cloudsql-postgres instance (defaults to 'host').
        :param port: Port to connect on (defaults to 5432).
        """
        extras: Dict[str, Any] = {}
        extras["__name"] = name
        if gcp_service_account is not None:
            extras["__gcp_service_account"] = gcp_service_account
        if database is not None:
            extras["database"] = database
        if ip_type is not None:
            extras["ip_type"] = ip_type
        if sqlalchemy_url is not None:
            extras["sqlalchemy_url"] = sqlalchemy_url
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-cloudsql-postgres",
                auth_type="iam_service_account",
                username=username,
                password=password,
                host=host or "host",
                port=port or 5432,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def workload_identity_federation(
        self,
        *,
        username: str,
        name: str,
        database: Optional[str] = None,
        ip_type: Optional[str] = None,
        sqlalchemy_url: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Direct extraction with Workload Identity Federation auth.

        :param username: IAM Service Account Name.
        :param name: Connection Name.
        :param ip_type: IP type.
        :param sqlalchemy_url: SQLAlchemy Args.
        :param host: Hostname of the cloudsql-postgres instance (defaults to 'host').
        :param port: Port to connect on (defaults to 5432).
        """
        extras: Dict[str, Any] = {}
        extras["__name"] = name
        if database is not None:
            extras["database"] = database
        if ip_type is not None:
            extras["ip_type"] = ip_type
        if sqlalchemy_url is not None:
            extras["sqlalchemy_url"] = sqlalchemy_url
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-cloudsql-postgres",
                auth_type="workload_identity_federation",
                username=username,
                host=host or "host",
                port=port or 5432,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def cloud_provider(self, value: str) -> "AtlanCloudsqlPostgresCrawler":
        self._metadata["cloud-provider"] = value
        return self

    def exclude_regex_for_tables_views(
        self, value: str
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string"""
        self._metadata["temp-table-regex"] = value
        return self

    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Include Metadata — Only selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config."""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanCloudsqlPostgresCrawler":
        """Exclude Metadata — Selected databases and schemas wont be extracted."""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def redact_sql_text(self, enabled: bool = True) -> "AtlanCloudsqlPostgresCrawler":
        """Redact SQL Text — Replaces string and numeric literals in extracted SQL definitions with placeholders, in memory, before anything is written to disk. SQL that can't be parsed is kept as-is. Query structure and lineage are preserved. Note: Increases extraction runtime."""
        self._metadata["redact-sql-text"] = enabled
        return self


__all__ = ["AtlanCloudsqlPostgresCrawler", "AtlanCloudsqlPostgresCrawlerInputs"]
