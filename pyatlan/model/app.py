# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Models for the native (v3) App APIs (BLDX-1472).

The v3 surface uses **snake_case** wire keys (``app_id``, ``run_id``,
``include_filter``, ``agent_json`` …), so these models disable ``AtlanObject``'s
default camelCase alias generator. The ``inputs`` are intentionally a free-form
``Dict[str, Any]`` validated server-side against the app's live input contract —
pyatlan stays generic rather than hard-coding a class per connector.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic.v1 import Extra, Field

from pyatlan.model.core import AtlanObject

# Run statuses that are terminal (no further polling needed).
TERMINAL_RUN_STATUSES = frozenset(
    {"Succeeded", "Failed", "Stopped", "Terminated", "Skipped"}
)


class AppObject(AtlanObject):
    """Base for v3 App models: snake_case wire keys (no camelCase aliasing)."""

    class Config(AtlanObject.Config):
        alias_generator = None  # keep field names as-is (snake_case on the wire)


# --------------------------------------------------------------------------- #
# Requests
# --------------------------------------------------------------------------- #
class AppSchedule(AppObject):
    """A cron schedule attached to an app."""

    cron: str = Field(description="Cron expression, e.g. '0 9 * * *'.")
    timezone: Optional[str] = Field(
        default=None, description="IANA timezone; server defaults to UTC when omitted."
    )


class CreateApp(AppObject):
    """Body for ``POST /v1/app`` (create + version + publish + optional run)."""

    app_id: str = Field(
        description="Marketplace application id, e.g. 'bigquery-crawler'."
    )
    name: str = Field(description="Display label for the app run (NOT the identifier).")
    inputs: Dict[str, Any] = Field(
        description="Values matching the app's input contract (validated server-side)."
    )
    entrypoint: Optional[str] = Field(
        default=None, description="Named operation; omit to use the app's default."
    )
    schedule: Optional[AppSchedule] = Field(
        default=None, description="Optional cron schedule to attach on create."
    )
    run: Optional[bool] = Field(
        default=None,
        description="Submit a run on create. Server defaults to true when omitted.",
    )


class UpdateApp(AppObject):
    """Body for ``PUT /v1/app/{slug}`` — full-replace of inputs (not a sparse patch)."""

    inputs: Dict[str, Any] = Field(
        description="Complete input-contract values (full replace, not a patch)."
    )
    entrypoint: Optional[str] = Field(
        default=None, description="Named operation; omit to use the app's default."
    )


# --------------------------------------------------------------------------- #
# Responses
# --------------------------------------------------------------------------- #
class AppResponse(AppObject):
    """Result of ``POST /v1/app``."""

    execution_mode: Optional[str] = None
    slug: str = Field(
        description="Server-minted identity; persist this for lifecycle ops."
    )
    version: Optional[int] = None
    run_id: Optional[str] = Field(default=None, description="Present unless run=False.")
    schedule_trigger_id: Optional[str] = Field(
        default=None, description="Present only when a schedule was supplied."
    )


class AppSummary(AppObject):
    """A single app as returned by get-one / list (full payload preserved)."""

    class Config(AppObject.Config):
        extra = Extra.allow  # list items are richer than the typed fields below

    slug: Optional[str] = None
    name: Optional[str] = None
    version: Optional[int] = None
    owner: Optional[str] = None
    app_id: Optional[str] = None
    schedules: Optional[List[Dict[str, Any]]] = None


class AppList(AppObject):
    """Result of ``GET /v1/app``."""

    workflows: List[AppSummary] = Field(default_factory=list)
    has_more: bool = False
    next_cursor: Optional[str] = None


class AppDeleteResponse(AppObject):
    slug: Optional[str] = None
    archived: bool = False


class AppRunResponse(AppObject):
    """Result of ``GET /v1/app/runs/{run_id}`` and submit."""

    run_id: Optional[str] = None
    status: Optional[str] = None
    slug: Optional[str] = None
    started_at: Optional[str] = None

    @property
    def is_terminal(self) -> bool:
        """True once the run reaches a terminal status (stop polling)."""
        return self.status in TERMINAL_RUN_STATUSES

    @property
    def is_success(self) -> bool:
        return self.status == "Succeeded"


class AppRunCancelResponse(AppObject):
    run_id: Optional[str] = None
    cancelled: bool = False
    status: Optional[str] = None
    slug: Optional[str] = None


class AppEntrypoint(AppObject):
    name: str


class AppInfo(AppObject):
    """Result of ``GET /v1/apps/{app_id}`` — native-readiness + entrypoints."""

    app_id: Optional[str] = None
    name: Optional[str] = None
    native_ready: bool = False
    execution_mode: Optional[str] = None
    entrypoints: List[AppEntrypoint] = Field(default_factory=list)


class AppScheduleResponse(AppObject):
    trigger_id: Optional[str] = None
    cron: Optional[str] = None
    timezone: Optional[str] = None


class AppScheduleDeleteResponse(AppObject):
    trigger_id: Optional[str] = None
    deleted: bool = False


class AppInputContract(AppObject):
    """The app's input contract (a JSON Schema) for an entrypoint.

    The full schema is preserved (``extra = allow``); convenience accessors help
    callers/agents discover fields at runtime instead of hard-coding them.
    """

    class Config(AppObject.Config):
        extra = Extra.allow  # keep the entire JSON Schema, not just the modeled keys

    title: Optional[str] = None
    type: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)
    defs: Dict[str, Any] = Field(default_factory=dict, alias="$defs")

    def field_names(self) -> List[str]:
        """All input field names declared by the contract."""
        return list(self.properties.keys())

    def required_fields(self) -> List[str]:
        """Field names the contract marks as required."""
        return list(self.required or [])

    def credential_field(self) -> Optional[str]:
        """Best-effort: the field that carries the credential, if any."""
        for candidate in (
            "credential",
            "credential_guid",
            "credential_ref",
            "agent_json",
        ):
            if candidate in self.properties:
                return candidate
        return None

    def describe(self) -> Dict[str, Any]:
        """Compact {field: {type, required, default}} view for quick inspection."""
        req = set(self.required or [])
        out: Dict[str, Any] = {}
        for fname, spec in self.properties.items():
            spec = spec if isinstance(spec, dict) else {}
            out[fname] = {
                "type": spec.get("type") or spec.get("anyOf") or spec.get("$ref"),
                "required": fname in req,
                "default": spec.get("default"),
            }
        return out
