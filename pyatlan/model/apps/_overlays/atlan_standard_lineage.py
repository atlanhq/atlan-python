# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Overlay for the generated ``AtlanStandardLineage`` builder.

Two things the configmap can't express, so they live here and are mixed into the
generated builder (see :func:`pyatlan.generator.generate_apps._overlay_for`):

* ``cross_connection_qualified_names`` is declared ``str`` in the contract but
  *means* a list — sending a native list fails server-side validation. The
  :meth:`connections` override takes a ``List[str]`` and JSON-encodes it.
* Standard Lineage's defining operation is **re-scoping an existing workflow**
  (adding a connection as it is onboarded) — an update against a slug that must
  preserve the workflow's own connection. See :meth:`set_connections`.

Everything else (``_APP_ID``, ``_INPUTS_CLASS``, ``_HIDDEN_DEFAULTS``,
``.connector()``) is generated from the contract and regenerates automatically.
"""

from __future__ import annotations

import json
import re
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    from pyatlan.model.app import AppResponse
    from pyatlan.model.apps._base import AppInput

#: A connection qualified name is ``default/{connector}/{epoch}``.
_CONNECTION_QN = re.compile(r"^default/([^/]+)/\d+$")

#: The connector of the workflow's *own* connection — distinct from the
#: ``connector`` input, which names the connector of the connections in scope.
_OWN_CONNECTOR = "standard-lineage"

_S = TypeVar("_S", bound="AtlanStandardLineageOverlay")


def _connector_of(qualified_name: str) -> str:
    """Return the connector segment of a connection qualified name."""
    match = _CONNECTION_QN.match(qualified_name)
    if not match:
        raise ValueError(
            f"{qualified_name!r} is not a connection qualified name "
            "(expected 'default/{connector}/{epoch}')"
        )
    return match.group(1)


def _validate_scope(qualified_names: Sequence[str]) -> str:
    """Validate a scope list and return the single connector it covers.

    The app requires a non-empty, same-connector scope and fails the run when that
    does not hold, so this is checked client-side where the error is actionable.
    """
    if not qualified_names:
        raise ValueError(
            "Standard Lineage needs at least one connection in scope; "
            "to stop processing a connection, remove it and leave the rest, "
            "or delete the workflow"
        )
    connectors = {_connector_of(qn) for qn in qualified_names}
    if len(connectors) > 1:
        raise ValueError(
            "every connection in scope must belong to the same connector, got "
            f"{sorted(connectors)}; use one Standard Lineage workflow per connector"
        )
    connector = connectors.pop()
    if connector == _OWN_CONNECTOR:
        raise ValueError(
            "the scope must list the SOURCE connections to build lineage across "
            f"(e.g. 'default/bigquery/1700000000'), not the workflow's own "
            f"{_OWN_CONNECTOR!r} connection"
        )
    return connector


def _parse_scope(value: Any) -> List[str]:
    """Read a scope back out of a persisted workflow.

    The value is a JSON-encoded string on the wire but a native list once the
    Automation Engine has rendered it into the DAG, so both shapes occur.
    """
    if value is None:
        return []
    if isinstance(value, str):
        if not value.strip():
            return []
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            # A bare single qualified name, tolerated rather than crashed on.
            return [value.strip()]
        return [str(v) for v in parsed] if isinstance(parsed, list) else [str(parsed)]
    if isinstance(value, Iterable):
        return [str(v) for v in value]
    return [str(value)]


class AtlanStandardLineageOverlay:
    """Hand-authored methods mixed into the generated ``AtlanStandardLineage``."""

    # Attributes provided by ``AppBuilder`` (the class this mixes into).
    if TYPE_CHECKING:
        _metadata: Dict[str, Any]
        _client: Any
        _INPUTS_CLASS: type[AppInput]
        _ENTRYPOINT: Optional[str]

    # ── Step 3 · Metadata ──────────────────────────────────────────────────
    def connections(
        self: _S,
        qualified_names: Union[Sequence[str], str],
        *,
        connector: Optional[str] = None,
    ) -> _S:
        """Set the connections to build lineage across (create-time scope).

        :param qualified_names: source connection qualified names, e.g.
            ``["default/bigquery/1700000000", ...]``. All must belong to the same
            connector. A pre-encoded JSON string is accepted as-is.
        :param connector: the scope's connector; derived from
            ``qualified_names`` when omitted.
        :raises ValueError: on an empty scope, a malformed qualified name, or a
            scope spanning more than one connector.

        To change the scope of a workflow that already exists, use
        :meth:`add_connections` / :meth:`remove_connections` / :meth:`set_connections`
        — those preserve the workflow's own connection, which this does not know about.
        """
        scope = _parse_scope(qualified_names)
        derived = _validate_scope(scope)
        self._metadata["connector"] = connector or derived
        # The contract declares this field as `str`, so it goes over JSON-encoded;
        # Heracles parses it back into a list for the manifest placeholder.
        self._metadata["cross_connection_qualified_names"] = json.dumps(scope)
        self._metadata["run_role"] = "standard-lineage"
        return self

    # ── Re-scoping an existing workflow (network) ───────────────────────────
    def get_connections(self, slug: str) -> List[str]:
        """Return the connections currently in scope for ``slug``. Read-only."""
        return _parse_scope(
            self._persisted_args(slug).get("cross_connection_qualified_names")
        )

    def add_connections(
        self, slug: str, qualified_names: Union[Sequence[str], str]
    ) -> Optional[AppResponse]:
        """Add connections to an existing workflow's scope, keeping the rest.

        Idempotent: connections already in scope are ignored, and when nothing
        would change no version is published and ``None`` is returned. This is the
        onboarding call — adding each new connection as it is created.
        """
        current = self.get_connections(slug)
        additions = [qn for qn in _parse_scope(qualified_names) if qn not in current]
        if not additions:
            return None
        return self.set_connections(slug, current + additions)

    def remove_connections(
        self, slug: str, qualified_names: Union[Sequence[str], str]
    ) -> Optional[AppResponse]:
        """Remove connections from an existing workflow's scope, keeping the rest.

        Idempotent in the same way as :meth:`add_connections`. Removing every
        connection raises — the app cannot run on an empty scope.

        The next run hands each removed connection back to its own miner and
        crawler, by flipping the per-connection standard-lineage marker off.
        """
        current = self.get_connections(slug)
        removals = set(_parse_scope(qualified_names))
        remaining = [qn for qn in current if qn not in removals]
        if len(remaining) == len(current):
            return None
        return self.set_connections(slug, remaining)

    def set_connections(
        self,
        slug: str,
        qualified_names: Union[Sequence[str], str],
        *,
        connector: Optional[str] = None,
    ) -> AppResponse:
        """Replace an existing workflow's scope with exactly ``qualified_names``.

        Preserves the workflow's own connection, its ``run_role`` and its identity
        by reading them back from the persisted workflow — ``client.app.update`` is
        a full replace, so anything omitted from the payload would be dropped from
        the new version, and the workflow's connection entity is republished on
        every run (a partial one would strip its admins).
        """
        scope = _parse_scope(qualified_names)
        derived = _validate_scope(scope)
        args = self._persisted_args(slug)
        own_connection = args.get("connection")
        if not own_connection:
            raise ValueError(
                f"workflow {slug!r} has no connection on its extract node; refusing "
                "to update, because a partial connection would be republished over "
                "the real one"
            )
        inputs = self._INPUTS_CLASS(
            connection=own_connection,
            connector=connector or args.get("connector") or derived,
            cross_connection_qualified_names=json.dumps(scope),
            run_role=args.get("run_role") or "standard-lineage",
        )
        return self._client.app.update(
            slug=slug, inputs=inputs, entrypoint=self._ENTRYPOINT
        )

    # ── internals ──────────────────────────────────────────────────────────
    def _persisted_args(self, slug: str) -> Dict[str, Any]:
        """Read the persisted workflow's extract-node args.

        ``GET /v1/app/{slug}`` returns the rendered DAG; ``AppSummary`` tolerates
        unmodelled fields, so it arrives as an extra attribute.
        """
        summary = self._client.app.get(slug)
        dag = getattr(summary, "dag", None)
        if not isinstance(dag, dict):
            raise ValueError(
                f"workflow {slug!r} returned no DAG to read the scope from"
            )
        node = dag.get("extract")
        args = ((node or {}).get("inputs") or {}).get("args") if node else None
        if not isinstance(args, dict):
            raise ValueError(
                f"workflow {slug!r} has no extract node args; is it a Standard "
                "Lineage workflow?"
            )
        return args
