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

import difflib
import json
from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import Extra, Field

from pyatlan.errors import ErrorCode
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


class AppInputsBuilder:
    """Build a validated ``inputs`` dict for :meth:`AppClient.create` / ``update``.

    A generic, **contract-driven** alternative to passing a raw dict — it wraps
    the structural pieces every app shares (connection, direct credential vs
    agent/SDR, filters) with helpers, and validates arbitrary app-specific fields
    against the app's live input contract (so a typo is caught before submit, not
    server-side). There is **no per-connector class** — the contract is the
    source of truth, so new apps/fields work automatically.

    Obtain via :meth:`AppClient.inputs` (which fetches + supplies the contract),
    or construct directly with a contract (or ``None`` to skip field validation)::

        inputs = (
            client.app.inputs("oracle-crawler", entrypoint="crawler")
            .connection(qualified_name="default/oracle/123", connector_name="oracle",
                        admin_users=["jane"])
            .agent(agent_name="ora-agent", secret_manager="vault", secret_path="kv/ora")
            .filters(include={"SCHEMA": {}})
            .set("system_schema_name", "SYS")
            .build()
        )
        client.app.create(app_id="oracle-crawler", name="prod", inputs=inputs)
    """

    # AgentCredentialSpec: pythonic kwarg -> wire key (hyphenated).
    _AGENT_KEY_MAP = {
        "agent_name": "agent-name",
        "agent_type": "agent-type",
        "auth_type": "auth-type",
        "connect_by": "connectBy",
        "secret_manager": "secret-manager",
        "secret_path": "secret-path",
        "key_type": "key-type",
        "aws_auth_method": "aws-auth-method",
        "aws_region": "aws-region",
        "azure_auth_method": "azure-auth-method",
    }

    def __init__(
        self,
        contract: Optional[AppInputContract] = None,
        app_id: Optional[str] = None,
        entrypoint: Optional[str] = None,
    ):
        self._contract = contract
        self._app_id = app_id
        self._entrypoint = entrypoint
        self._inputs: Dict[str, Any] = {}

    # --------------------------- universal helpers --------------------------- #
    def connection(
        self,
        *,
        qualified_name: str,
        connector_name: str,
        name: Optional[str] = None,
        admin_users: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        default_credential_guid: Optional[str] = None,
        **extra_attributes: Any,
    ) -> "AppInputsBuilder":
        """Set the ``connection`` object (every app workflow needs one).

        ``extra_attributes`` are passed through verbatim (camelCase keys, e.g.
        ``allowQuery=True``).
        """
        attrs: Dict[str, Any] = {
            "qualifiedName": qualified_name,
            "connectorName": connector_name,
        }
        if name is not None:
            attrs["name"] = name
        if admin_users is not None:
            attrs["adminUsers"] = admin_users
        if admin_roles is not None:
            attrs["adminRoles"] = admin_roles
        if admin_groups is not None:
            attrs["adminGroups"] = admin_groups
        if default_credential_guid is not None:
            attrs["defaultCredentialGuid"] = default_credential_guid
        attrs.update(extra_attributes)
        self._inputs["connection"] = {"typeName": "Connection", "attributes": attrs}
        return self

    def direct_credential(
        self,
        guid: Optional[str] = None,
        credential: Optional[Union[Dict[str, Any], Any]] = None,
    ) -> "AppInputsBuilder":
        """Direct (Atlan-vaulted) credential: an existing ``guid`` or a raw
        ``credential`` body (vaulted server-side). Mutually exclusive with
        :meth:`agent`."""
        if guid is not None:
            self._inputs["credential_guid"] = guid
        if credential is not None:
            self._inputs["credential"] = (
                credential.dict() if hasattr(credential, "dict") else credential
            )
        return self

    def agent(
        self,
        *,
        agent_name: str,
        agent_type: Optional[str] = None,
        auth_type: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        connect_by: Optional[str] = None,
        secret_manager: Optional[str] = None,
        secret_path: Optional[str] = None,
        **extras: Any,
    ) -> "AppInputsBuilder":
        """Agent / SDR mode: build ``agent_json`` (secrets stay in your vault).

        ``extras`` carry connector-specific or secret-field-ref keys verbatim.
        Mutually exclusive with :meth:`direct_credential`.
        """
        agent_json: Dict[str, Any] = {"agent-name": agent_name}
        for kwarg, value in (
            ("agent_type", agent_type),
            ("auth_type", auth_type),
            ("connect_by", connect_by),
            ("secret_manager", secret_manager),
            ("secret_path", secret_path),
        ):
            if value is not None:
                agent_json[self._AGENT_KEY_MAP[kwarg]] = value
        if host is not None:
            agent_json["host"] = host
        if port is not None:
            agent_json["port"] = port
        agent_json.update(extras)
        self._inputs["agent_json"] = agent_json
        return self

    def filters(
        self,
        include: Optional[Union[str, Dict[str, Any]]] = None,
        exclude: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> "AppInputsBuilder":
        """Set ``include_filter`` / ``exclude_filter``. Dicts are JSON-stringified
        (connectors commonly type these as a stringified object)."""
        if include is not None:
            self._inputs["include_filter"] = (
                include if isinstance(include, str) else json.dumps(include)
            )
        if exclude is not None:
            self._inputs["exclude_filter"] = (
                exclude if isinstance(exclude, str) else json.dumps(exclude)
            )
        return self

    # ----------------------- generic, contract-validated --------------------- #
    def set(self, field: str, value: Any) -> "AppInputsBuilder":
        """Set any app-specific input, validated against the contract."""
        self._validate_field(field)
        self._inputs[field] = value
        return self

    def update(self, values: Dict[str, Any]) -> "AppInputsBuilder":
        """Set several app-specific inputs at once (each validated)."""
        for field in values:
            self._validate_field(field)
        self._inputs.update(values)
        return self

    def build(self) -> Dict[str, Any]:
        """Validate required fields are present and return the ``inputs`` dict."""
        if self._contract is not None:
            missing = [
                f for f in self._contract.required_fields() if f not in self._inputs
            ]
            if missing:
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    missing,
                    f"{self._app_id or 'app'} inputs (required)",
                    f"required fields: {self._contract.required_fields()}",
                )
        return dict(self._inputs)

    def _validate_field(self, field: str) -> None:
        if self._contract is None:
            return
        valid = set(self._contract.field_names())
        if valid and field not in valid:
            suggestions = difflib.get_close_matches(field, valid, n=3)
            hint = (
                f"did you mean {suggestions}? " if suggestions else ""
            ) + f"valid inputs: {sorted(valid)}"
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                field, f"{self._app_id or 'app'} inputs", hint
            )
