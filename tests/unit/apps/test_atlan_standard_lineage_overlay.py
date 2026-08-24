# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""HAND-WRITTEN tests for the Standard Lineage builder (CONNECT-182).

The generator's regen only clears files carrying the AUTO-GENERATED banner, so this
file survives regeneration alongside the builder it covers.

Most cases pin the re-scope path rather than create: the builder's job is to change an
existing workflow's set of connections without disturbing the workflow's own connection
entity, and ``client.app.update`` is a full replace — so what is *absent* from the
payload matters as much as what is present.
"""

import json
from unittest.mock import Mock

import pytest

from pyatlan.model.apps import AtlanStandardLineage, AtlanStandardLineageInputs

SLUG = "atlan-standard-lineage-1700000000-Abcd1234"
BQ1 = "default/bigquery/1700000001"
BQ2 = "default/bigquery/1700000002"
BQ3 = "default/bigquery/1700000003"

# The workflow's own connection, as it comes back on the persisted DAG. Every
# attribute matters: the create-connection node republishes this entity, so a
# partial copy would strip the connection's name and admins in Atlan.
OWN_CONNECTION = {
    "typeName": "Connection",
    "attributes": {
        "qualifiedName": "default/standard-lineage/1700000000",
        "name": "bq-cross-connection",
        "connectorName": "standard-lineage",
        "category": "lineage",
        "adminUsers": ["someone"],
        "adminRoles": ["role-guid"],
        "adminGroups": [],
        "rowLimit": 10000,
    },
}


def _client(scope, *, connection=OWN_CONNECTION, connector="bigquery"):
    """A mock client whose app.get() returns a persisted Standard Lineage DAG."""
    args = {"connector": connector, "run_role": "standard-lineage"}
    if connection is not None:
        args["connection"] = connection
    if scope is not None:
        args["cross_connection_qualified_names"] = scope
    client = Mock()
    client.app.get.return_value = Mock(dag={"extract": {"inputs": {"args": args}}})
    client.app.update.return_value = Mock(slug=SLUG, version=1700000009)
    return client


def _sent_inputs(client):
    """The inputs dict actually handed to client.app.update()."""
    return client.app.update.call_args.kwargs["inputs"].to_inputs()


# ── inputs model ────────────────────────────────────────────────────────────
def test_inputs_defaults():
    i = AtlanStandardLineageInputs()
    assert AtlanStandardLineageInputs._APP_ID == "atlan-standard-lineage"
    assert AtlanStandardLineageInputs._ENTRYPOINT == "standard-lineage"
    assert i.connector == ""
    assert i.cross_connection_qualified_names == ""


def test_builder_class_vars():
    assert AtlanStandardLineage._APP_ID == "atlan-standard-lineage"
    assert AtlanStandardLineage._ENTRYPOINT == "standard-lineage"
    # The workflow's OWN connection lives under standard-lineage; the connections
    # in scope are a different connector entirely.
    assert AtlanStandardLineage._CONNECTOR_NAME == "standard-lineage"


# ── create-time scope ───────────────────────────────────────────────────────
def test_connections_json_encodes_and_derives_connector():
    out = (
        AtlanStandardLineage(Mock())
        .connection(name="bq-cross-connection")
        .connections([BQ1, BQ2])
        .preview()
    )
    # Declared `str` in the contract — a native list fails validation server-side.
    assert isinstance(out["cross_connection_qualified_names"], str)
    assert json.loads(out["cross_connection_qualified_names"]) == [BQ1, BQ2]
    assert out["connector"] == "bigquery"
    assert out["run_role"] == "standard-lineage"
    assert out["connection"]["attributes"]["connectorName"] == "standard-lineage"


def test_connections_explicit_connector_wins():
    out = (
        AtlanStandardLineage(Mock())
        .connections([BQ1], connector="bigquery-custom")
        .preview()
    )
    assert out["connector"] == "bigquery-custom"


def test_connections_accepts_a_preencoded_json_string():
    out = AtlanStandardLineage(Mock()).connections(json.dumps([BQ1, BQ2])).preview()
    assert json.loads(out["cross_connection_qualified_names"]) == [BQ1, BQ2]


# ── validation ──────────────────────────────────────────────────────────────
def test_empty_scope_is_rejected():
    with pytest.raises(ValueError, match="at least one connection"):
        AtlanStandardLineage(Mock()).connections([])


def test_mixed_connector_scope_is_rejected():
    with pytest.raises(ValueError, match="same connector"):
        AtlanStandardLineage(Mock()).connections([BQ1, "default/snowflake/1700000004"])


def test_own_connection_as_scope_is_rejected():
    """A natural mistake: passing the workflow's own connection as its scope."""
    with pytest.raises(ValueError, match="not the workflow's own"):
        AtlanStandardLineage(Mock()).connections(["default/standard-lineage/1700000000"])


def test_malformed_qualified_name_is_rejected():
    with pytest.raises(ValueError, match="not a connection qualified name"):
        AtlanStandardLineage(Mock()).connections(["bigquery/1700000001"])


# ── reading an existing workflow ────────────────────────────────────────────
def test_get_connections_reads_a_native_list():
    """Once the Automation Engine renders the DAG the value is a real list."""
    assert AtlanStandardLineage(_client([BQ1, BQ2])).get_connections(SLUG) == [BQ1, BQ2]


def test_get_connections_reads_a_json_string():
    """On the wire it is JSON-encoded, so both shapes have to be readable."""
    assert AtlanStandardLineage(_client(json.dumps([BQ1, BQ2]))).get_connections(SLUG) == [
        BQ1,
        BQ2,
    ]


def test_get_connections_on_empty_scope():
    assert AtlanStandardLineage(_client("")).get_connections(SLUG) == []


def test_missing_extract_args_raises():
    client = Mock()
    client.app.get.return_value = Mock(dag={"publish": {}})
    with pytest.raises(ValueError, match="no extract node args"):
        AtlanStandardLineage(client).get_connections(SLUG)


# ── re-scoping ──────────────────────────────────────────────────────────────
def test_set_connections_preserves_the_persisted_connection_verbatim():
    """The whole reason set_connections reads before it writes.

    ``client.app.update`` is a full replace, and the connection entity is
    republished on every run — so sending a rebuilt or partial connection would
    overwrite the real one in Atlan.
    """
    client = _client([BQ1, BQ2])
    AtlanStandardLineage(client).set_connections(SLUG, [BQ1, BQ2, BQ3])
    sent = _sent_inputs(client)
    assert sent["connection"] == OWN_CONNECTION
    assert sent["run_role"] == "standard-lineage"
    assert json.loads(sent["cross_connection_qualified_names"]) == [BQ1, BQ2, BQ3]
    assert client.app.update.call_args.kwargs["entrypoint"] == "standard-lineage"
    assert client.app.update.call_args.kwargs["slug"] == SLUG


def test_set_connections_refuses_when_the_workflow_has_no_connection():
    client = _client([BQ1], connection=None)
    with pytest.raises(ValueError, match="no connection on its extract node"):
        AtlanStandardLineage(client).set_connections(SLUG, [BQ1, BQ2])
    client.app.update.assert_not_called()


def test_set_connections_refuses_to_empty_the_scope():
    client = _client([BQ1])
    with pytest.raises(ValueError, match="at least one connection"):
        AtlanStandardLineage(client).set_connections(SLUG, [])
    client.app.update.assert_not_called()


def test_add_connections_appends_and_keeps_the_rest():
    client = _client([BQ1, BQ2])
    AtlanStandardLineage(client).add_connections(SLUG, [BQ3])
    assert json.loads(_sent_inputs(client)["cross_connection_qualified_names"]) == [
        BQ1,
        BQ2,
        BQ3,
    ]


def test_add_connections_is_idempotent():
    """The onboarding portal may replay; a no-op must not publish a version."""
    client = _client([BQ1, BQ2])
    assert AtlanStandardLineage(client).add_connections(SLUG, [BQ2]) is None
    client.app.update.assert_not_called()


def test_add_connections_adds_only_the_new_ones():
    client = _client([BQ1])
    AtlanStandardLineage(client).add_connections(SLUG, [BQ1, BQ2])
    assert json.loads(_sent_inputs(client)["cross_connection_qualified_names"]) == [
        BQ1,
        BQ2,
    ]


def test_remove_connections_keeps_the_rest():
    client = _client([BQ1, BQ2, BQ3])
    AtlanStandardLineage(client).remove_connections(SLUG, [BQ2])
    assert json.loads(_sent_inputs(client)["cross_connection_qualified_names"]) == [
        BQ1,
        BQ3,
    ]


def test_remove_connections_not_in_scope_is_a_noop():
    client = _client([BQ1, BQ2])
    assert AtlanStandardLineage(client).remove_connections(SLUG, [BQ3]) is None
    client.app.update.assert_not_called()


def test_remove_last_connection_is_refused():
    client = _client([BQ1])
    with pytest.raises(ValueError, match="at least one connection"):
        AtlanStandardLineage(client).remove_connections(SLUG, [BQ1])
    client.app.update.assert_not_called()
