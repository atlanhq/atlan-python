# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AtlanQuicksightInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-quicksight` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-quicksight"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    fetch_folderless_assets: bool = Field(True, alias="fetch-folderless-assets")
    """Fetch all assets without folder? — Fetch assets not linked to any folder, including datasets, analyses & dashboards."""
    include_filter: Dict[str, Any] = Field({}, alias="include-filter")
    """Include Folders — Selected folders will be processed. Exclude gets preference over include."""
    exclude_filter: Dict[str, Any] = Field({}, alias="exclude-filter")
    """Exclude Folders — Selected folders will not be processed."""


class AtlanQuicksight(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-quicksight` app.

    Example::

        resp = (
            AtlanQuicksight(client)
            .iam(username="...", password="...", region="...", accountid="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .fetch_all_assets_without_folder(True)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-quicksight"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "quicksight"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-quicksight"
    _INPUTS_CLASS = AtlanQuicksightInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"extraction_method": "direct"}

    # ── Step 1 · Credential ──
    def iam(
        self, *, username: str, password: str, region: str, accountid: str, **extra: Any
    ) -> "AtlanQuicksight":
        """Direct extraction with iam auth.

        :param username: AWS Access Key.
        :param password: AWS Secret Key.
        :param region: Region.
        :param accountid: AWS Account ID.
        """
        extras: Dict[str, Any] = {}
        extras["region"] = region
        extras["accountid"] = accountid
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-quicksight",
                connector_type="quicksight",
                auth_type="iam",
                username=username,
                password=password,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def fetch_all_assets_without_folder(
        self, enabled: bool = True
    ) -> "AtlanQuicksight":
        """Fetch all assets without folder? — Fetch assets not linked to any folder, including datasets, analyses & dashboards."""
        self._metadata["fetch-folderless-assets"] = enabled
        return self

    def include_folders(self, value: Dict[str, Any]) -> "AtlanQuicksight":
        """Include Folders — Selected folders will be processed. Exclude gets preference over include."""
        self._metadata["include-filter"] = value
        return self

    def exclude_folders(self, value: Dict[str, Any]) -> "AtlanQuicksight":
        """Exclude Folders — Selected folders will not be processed."""
        self._metadata["exclude-filter"] = value
        return self


__all__ = ["AtlanQuicksight", "AtlanQuicksightInputs"]
