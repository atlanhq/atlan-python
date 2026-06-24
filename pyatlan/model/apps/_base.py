# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Bases for the app abstraction.

Two layers, both derived from an app's UI configmaps so nothing is hand-tuned:

* ``AppInput`` — a typed ``inputs`` payload (the metadata model). Field names are
  the snake_case wire keys, so serialization needs no aliasing. Pass an instance
  straight to ``client.app.create(..., inputs=...)``.
* ``AppBuilder`` — a fluent, UI-mirroring builder. It walks the same 3 steps as
  the "new app" wizard (Credential → Connection → Metadata): you give it typed
  credential fields + a connection name + metadata toggles, and ``create()``
  vaults the credential, mints the connection qualified name, assembles the full
  payload (including the hidden defaults the UI submits), and runs the app — so a
  caller never hand-builds a connection object or guesses an input key.
"""

from __future__ import annotations

import json
import time
from typing import Any, ClassVar, Dict, List, Mapping, Optional, Type, Union

from pydantic.v1 import BaseModel, Extra

from pyatlan.model.credential import Credential


class AppInput(BaseModel):
    """A typed, configmap-derived ``inputs`` payload for an app workflow."""

    class Config:
        extra = Extra.allow  # tolerate fields newer than the generated snapshot
        allow_population_by_field_name = True
        validate_assignment = True

    def to_inputs(self) -> Dict[str, Any]:
        """Return the ``inputs`` dict for ``client.app.create()``.

        Includes the user-facing defaults (matching the UI), drops unset optionals.
        """
        return self.dict(exclude_none=True)


def _anchor_filter(assets: Union[str, Mapping[str, List[str]]]) -> str:
    """Turn a friendly ``{db: [schema, ...]}`` map into the UI's anchored-regex
    filter JSON (``{"^db$": ["^schema$"]}``). A string is passed through as-is."""
    if isinstance(assets, str):
        return assets

    def anchor(token: str) -> str:
        return token if token.startswith("^") and token.endswith("$") else f"^{token}$"

    return json.dumps(
        {anchor(db): [anchor(s) for s in schemas] for db, schemas in assets.items()}
    )


class AppBuilder:
    """Base fluent builder mirroring the UI's 3-step "new app" wizard.

    Subclasses set the app/connector class vars and add typed step methods; the
    shared mechanics (connection minting, credential vaulting, payload assembly,
    submit) live here so every per-app builder stays thin.
    """

    # — set by each per-app subclass —
    _APP_ID: ClassVar[str] = ""
    _ENTRYPOINT: ClassVar[Optional[str]] = None
    _CONNECTOR_NAME: ClassVar[str] = ""
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS: ClassVar[Type[AppInput]] = AppInput
    #: Hidden (``ui.hidden``) inputs the UI still submits with their defaults.
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    def __init__(self, client: Any):
        self._client = client
        self._extraction_method: str = "direct"
        self._credential: Optional[Credential] = None
        self._credential_guid: Optional[str] = None
        self._agent_json: Optional[Any] = None
        self._connection_name: Optional[str] = None
        self._connection_qualified_name: Optional[str] = None
        self._admin_users: List[str] = []
        self._admin_groups: List[str] = []
        self._admin_roles: List[str] = []
        self._metadata: Dict[str, Any] = {}

    # ── Step 1 · Credential ────────────────────────────────────────────────
    def credential_guid(self, guid: str):
        """Reuse an already-vaulted credential instead of creating a new one."""
        self._credential_guid = guid
        return self

    def agent(self, agent_json: Union[Dict[str, Any], str]):
        """Use Self-Deployed Runtime (agent) extraction; secrets stay in the
        customer's vault and only ``agent_json`` travels in the payload."""
        self._extraction_method = "agent"
        self._agent_json = agent_json
        return self

    # ── Step 2 · Connection ────────────────────────────────────────────────
    def connection(
        self,
        name: Optional[str] = None,
        *,
        admins: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        admin_roles: Optional[List[str]] = None,
        qualified_name: Optional[str] = None,
    ):
        """Configure the connection.

        To **create** a new connection (e.g. crawlers), pass ``name`` (the UI mints
        ``default/{connector}/{epoch}``). To **reference an existing** connection
        (e.g. miners), pass only ``qualified_name`` — on ``create()``/``run()`` the
        builder looks up that connection and reuses its own credential (its
        ``defaultCredentialGuid``), so no credential step is needed.
        """
        self._connection_name = name
        self._admin_users = list(admins or [])
        self._admin_groups = list(admin_groups or [])
        self._admin_roles = list(admin_roles or [])
        self._connection_qualified_name = qualified_name
        return self

    # ── assembly (no network) ──────────────────────────────────────────────
    def _build_connection(self, qualified_name: str) -> Dict[str, Any]:
        # Derive the connector from the QN (``default/{connector}/{epoch}``) so a
        # referenced existing connection (e.g. for miners) reports the right
        # connectorName, not the builder's app-id-derived fallback.
        parts = qualified_name.split("/")
        connector = (
            parts[1]
            if len(parts) >= 3 and parts[0] == "default"
            else self._CONNECTOR_NAME
        )
        attrs: Dict[str, Any] = {
            "qualifiedName": qualified_name,
            "connectorName": connector,
        }
        if self._connection_name:
            attrs["name"] = self._connection_name
        if self._admin_users:
            attrs["adminUsers"] = self._admin_users
        if self._admin_groups:
            attrs["adminGroups"] = self._admin_groups
        if self._admin_roles:
            attrs["adminRoles"] = self._admin_roles
        return {"typeName": "Connection", "attributes": attrs}

    def _raw_credential(self, *, epoch: int, redact: bool = False) -> Dict[str, Any]:
        """Serialize the staged credential to the camelCase raw-credential body the
        create endpoint vaults server-side (``authType`` + ``extra.*`` …). The
        secret never persists in the workflow — it is stripped after vaulting."""
        cred = self._credential
        assert cred is not None
        out: Dict[str, Any] = {
            "authType": cred.auth_type,
            "name": cred.name or f"default-{self._CONNECTOR_NAME}-{epoch}-0",
            "connectorConfigName": cred.connector_config_name,
        }
        if cred.connector_type:
            out["connectorType"] = cred.connector_type
        if cred.host:
            out["host"] = cred.host
        if cred.port:
            out["port"] = cred.port
        if cred.username:
            out["username"] = cred.username
        if cred.password is not None:
            out["password"] = "***" if redact else cred.password
        if cred.extras:
            out["extra"] = cred.extras
        return out

    def _assemble(
        self, *, qualified_name: str, epoch: int, redact: bool = False
    ) -> AppInput:
        kwargs: Dict[str, Any] = dict(self._HIDDEN_DEFAULTS)
        kwargs.update(self._metadata)
        kwargs["connection"] = self._build_connection(qualified_name)
        kwargs["extraction_method"] = self._extraction_method
        if self._extraction_method == "agent":
            kwargs["agent_json"] = self._agent_json
        elif self._credential_guid is not None:
            # Reference an already-vaulted credential.
            kwargs["credential_guid"] = self._credential_guid
        elif self._credential is not None:
            # Net-new: embed the raw credential; the create endpoint vaults it and
            # overwrites credential_guid with the issued guid. The contract types
            # credential_guid as a (non-null) string, so send "" to satisfy
            # validation — omitting it is read as null and rejected.
            kwargs["credential"] = self._raw_credential(epoch=epoch, redact=redact)
            kwargs["credential_guid"] = ""
        else:
            # No credential resolved (e.g. preview, or the connection lookup found
            # nothing) — send "" to satisfy the contract's non-null string so
            # create() validates. For miners, _create() auto-resolves the existing
            # connection's credential before assembly.
            kwargs["credential_guid"] = ""
        return self._INPUTS_CLASS(**kwargs)

    def preview(self) -> Dict[str, Any]:
        """Assemble and return the ``inputs`` payload without any network call —
        handy for inspection and tests. The secret is redacted; a placeholder QN
        is used."""
        qn = self._connection_qualified_name or f"default/{self._CONNECTOR_NAME}/0"
        return self._assemble(qualified_name=qn, epoch=0, redact=True).to_inputs()

    # ── create (network) ───────────────────────────────────────────────────
    def create(self, *, name: Optional[str] = None, schedule: Optional[Any] = None):
        """Create the workflow **without** running it (``run=False``).

        Mints the connection and assembles the payload (embedding a raw credential
        for the server to vault, or referencing an existing guid). Use :meth:`run`
        to create and submit a run in one call.
        """
        return self._create(name=name, run=False, schedule=schedule)

    def run(self, *, name: Optional[str] = None, schedule: Optional[Any] = None):
        """Create the workflow **and** submit a run immediately (``run=True``)."""
        return self._create(name=name, run=True, schedule=schedule)

    def _resolve_connection_credential(self, qualified_name: str) -> Optional[str]:
        """Look up an existing connection's ``defaultCredentialGuid`` so a caller
        referencing a connection by QN (e.g. miners) reuses that connection's
        credential without having to know its guid. Best-effort: returns None if
        the connection can't be read."""
        try:
            from pyatlan.model.assets import Connection
            from pyatlan.model.fluent_search import FluentSearch

            request = (
                FluentSearch()
                .where(Connection.TYPE_NAME.eq("Connection"))
                .where(Connection.QUALIFIED_NAME.eq(qualified_name))
                .include_on_results(Connection.DEFAULT_CREDENTIAL_GUID)
                .page_size(1)
            ).to_request()
            for asset in self._client.asset.search(request):
                return asset.default_credential_guid
        except Exception:  # noqa: BLE001
            return None
        return None

    def _create(self, *, name: Optional[str], run: bool, schedule: Optional[Any]):
        epoch = int(time.time())
        qn = (
            self._connection_qualified_name or f"default/{self._CONNECTOR_NAME}/{epoch}"
        )
        # Referencing an existing connection without a credential (e.g. miners):
        # reuse that connection's own credential (its defaultCredentialGuid), looked
        # up by QN — so the caller only needs to supply the connection.
        if (
            self._extraction_method != "agent"
            and self._credential is None
            and self._credential_guid is None
            and self._connection_qualified_name
        ):
            self._credential_guid = self._resolve_connection_credential(qn)
        inputs = self._assemble(qualified_name=qn, epoch=epoch)
        return self._client.app.create(
            app_id=self._APP_ID,
            entrypoint=self._ENTRYPOINT,
            name=name or self._connection_name or self._APP_ID,
            inputs=inputs,
            run=run,
            schedule=schedule,
        )
