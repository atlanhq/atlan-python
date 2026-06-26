# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Generate typed inputs + fluent builders for app workflows.

Source of truth is each app's **UI configmaps** (not the raw input contract), so
the generated classes mirror exactly what the UI surfaces — friendly labels,
the hidden-field set, enums, and the credential form:

* inputs form  : ``GET /api/service/configmaps/{app_id}?entrypoint={ep}``
* credential   : ``GET /api/service/configmaps/{connector_config}?app_id={app_id}``
  (the ``connector_config`` is read off the inputs form's credential widget).

For each app it emits a module with a ``{Name}Inputs`` model (only ``ui.hidden``
== false fields) and a ``{Name}`` :class:`AppBuilder` whose method names come
from the configmap labels (e.g. "Import Nested Columns" -> ``import_nested_columns``)
and whose Step-1 credential methods are generated per auth-type
(``.basic_auth(...)`` / ``.gcp_wif(...)`` …). Hidden runtime knobs ride along via
``_HIDDEN_DEFAULTS`` so the payload matches the UI.

Hand-authored builders (see ``_HAND_WRITTEN``) are never overwritten.

Run (needs ATLAN_BASE_URL + ATLAN_API_KEY for a tenant with the apps deployed):

    uv run python -m pyatlan.generator.generate_apps
"""

from __future__ import annotations

import json
import keyword
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

from pyatlan.client.atlan import AtlanClient

# Modules with a hand-polished builder — the generator leaves these untouched.
# databricks_crawler has a hand-written multi-mode asset_selection (the configmap
# can't express its include/exclude × hierarchy/regex widget).
_HAND_WRITTEN = {"bigquery_crawler", "databricks_crawler", "kafka_confluent"}

# Apps to generate even when not currently deployed/running on the tenant
# (configmaps are served per app-id, so live discovery alone misses these).
# Union'd with discovery — extend as more connectors are installed.
MANIFEST: List[Tuple[str, Optional[str]]] = [
    ("snowflake-crawler", "crawler"),
    ("snowflake-miner", "miner"),
    ("bigquery-miner", "miner"),
    ("atlan-dbt", None),
    ("atlan-glue", None),
    ("atlan-dynamodb", None),
    ("atlan-sigma", None),
    ("mongodbatlas-atlas", None),
]

# Widgets handled by the builder/base as Step 1/2 plumbing — not metadata methods.
# ``connectionSelector`` is the miner-style "pick an existing connection" widget;
# like ``connection`` it maps to the builder's connection(), not a metadata field.
_PLUMBING_WIDGETS = {
    "credential",
    "agent",
    "connection",
    "connectionSelector",
    "sageV2",
}

# Handshake/infra ids never accepted as inputs (stripped server-side).
_HANDSHAKE = {"user-id", "user_id", "workflow_id", "correlation_id"}

_PRIMITIVE = {
    "boolean": "bool",
    "integer": "int",
    "number": "float",
    "string": "str",
    # object fields are submitted as a JSON string (the contract accepts a string
    # or array, and the worker json.loads it), so accept either a dict or a string.
    "object": "Union[Dict[str, Any], str]",
    "array": "List[Any]",
}


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def _snake(text: str) -> str:
    s = str(text)
    # drop possessive apostrophes and parens so e.g. "project's" -> "projects"
    # and "Project(s)" -> "projects" (not "project_s")
    s = re.sub(r"['’]s\b", "s", s)
    s = s.replace("'", "").replace("’", "").replace("(", "").replace(")", "")
    # split camelCase / PascalCase boundaries (e.g. schemaRegistryHost,
    # HTTPHost) so they become proper snake_case
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"[^0-9A-Za-z]+", "_", s).strip("_").lower()
    if not s:
        return "field"
    if s[0].isdigit():
        s = f"f_{s}"
    if keyword.iskeyword(s):
        s = f"{s}_"
    return s


def _tokens(text: str) -> List[str]:
    """Split into alphanumeric tokens, collapsing consecutive duplicates
    (case-insensitive) so e.g. ``anaplan-anaplan`` -> ``[anaplan]``."""
    out: List[str] = []
    for p in re.split(r"[^0-9A-Za-z]+", str(text)):
        if p and (not out or out[-1].lower() != p.lower()):
            out.append(p)
    return out


def _camel(text: str) -> str:
    return "".join(p.capitalize() for p in _tokens(text))


# Friendlier class names than the app-id tokens would produce.
_CLASS_OVERRIDE = {"mongodbatlas-atlas": "MongodbAtlas"}


def _class_base(app_id: str, entrypoint: str) -> str:
    if app_id in _CLASS_OVERRIDE:
        return _CLASS_OVERRIDE[app_id]
    base = _camel(app_id)
    ep = _camel(entrypoint or "")
    if ep and ep.lower() not in base.lower():
        base += ep
    return base


def _module_name(app_id: str, entrypoint: str) -> str:
    base = "_".join(t.lower() for t in _tokens(app_id))
    ep = "_".join(t.lower() for t in _tokens(entrypoint or ""))
    if ep and ep not in base:
        base = f"{base}_{ep}"
    return base


def _py_type(spec: Dict[str, Any]) -> str:
    t = spec.get("type")
    if t in _PRIMITIVE:
        return _PRIMITIVE[t]
    if t == "conditional":  # configmap conditional fields are usually filters/strings
        return "Union[Dict[str, Any], str]"
    return "Any"


def _ui(spec: Dict[str, Any]) -> Dict[str, Any]:
    return spec.get("ui") or {}


def _doc(spec: Dict[str, Any]) -> str:
    ui = _ui(spec)
    label = (ui.get("label") or "").strip()
    help_ = (ui.get("help") or "").strip()
    text = " — ".join(p for p in (label, help_) if p) or label or help_
    return text.replace('"""', "'''")


# --------------------------------------------------------------------------- #
# configmap fetch
# --------------------------------------------------------------------------- #
class _ConfigMaps:
    def __init__(self, base_url: str, api_key: str):
        self._base = base_url.rstrip("/")
        self._client = httpx.Client(
            timeout=60.0, headers={"Authorization": f"Bearer {api_key}"}
        )

    def get(self, name: str, **params: str) -> Optional[Dict[str, Any]]:
        # The configmap service throttles bursts — retry transient failures
        # generously so a partial generation never silently drops modules.
        for attempt in range(8):
            try:
                r = self._client.get(
                    f"{self._base}/api/service/configmaps/{name}", params=params
                )
                if r.status_code == 200:
                    return json.loads(r.json()["data"]["config"])
                if r.status_code in (429, 500, 502, 503, 504):
                    time.sleep(2.0 * (attempt + 1))
                    continue
                return None
            except Exception:  # noqa: BLE001
                time.sleep(2.0 * (attempt + 1))
        return None


# --------------------------------------------------------------------------- #
# metadata (Step 3) — fields + fluent methods
# --------------------------------------------------------------------------- #
def _metadata_fields(cfg: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any]]]:
    """Return (snake_name, original_key, spec) for each visible metadata field."""
    out = []
    for key, spec in (cfg.get("properties") or {}).items():
        spec = spec if isinstance(spec, dict) else {}
        ui = _ui(spec)
        if ui.get("hidden") or key in _HANDSHAKE:
            continue
        if ui.get("widget") in _PLUMBING_WIDGETS or key == "extraction-method":
            continue
        out.append((_snake(key), key, spec))
    return out


def _hidden_defaults(cfg: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, spec in (cfg.get("properties") or {}).items():
        spec = spec if isinstance(spec, dict) else {}
        if not _ui(spec).get("hidden") or key in _HANDSHAKE:
            continue
        if _ui(spec).get("widget") in _PLUMBING_WIDGETS:
            continue
        if "default" in spec and spec["default"] not in ("", None):
            out[_snake(key)] = spec["default"]
    return out


# --------------------------------------------------------------------------- #
# credentials (Step 1) — auth methods from the connector configmap
# --------------------------------------------------------------------------- #
def _auth_keys(props: Dict[str, Any]) -> List[str]:
    """Auth-type keys within a credential-props root (an ``auth-type`` enum, or
    top-level nested auth objects)."""
    at = props.get("auth-type") or {}
    if at.get("enum"):
        return list(at["enum"])
    return [
        k
        for k, s in props.items()
        if isinstance(s, dict)
        and s.get("type") == "object"
        and isinstance(s.get("properties"), dict)
        and any(f in s["properties"] for f in ("username", "password", "extra"))
    ]


def _credential_props(cfg2: Dict[str, Any]) -> Dict[str, Any]:
    """The credential properties to read auth + host/port/extra from.

    JDBC-URL connectors (``AdvancedJDBCUrlGroup``) put some credential fields under
    ``jdbcUrl`` — and split them inconsistently: mssql nests *everything* there,
    while hive/postgres keep the ``auth-type``/auth objects at the top level but
    the ``host``/``port``/``extra`` under ``jdbcUrl``. So merge the two (top-level
    wins on conflict), giving a single view with auth + host/port regardless of
    where each lives. Connectors without a JDBC-URL group are unchanged."""
    props = dict(cfg2.get("properties") or {})
    jdbc = (props.get("jdbcUrl") or {}).get("properties")
    if isinstance(jdbc, dict):
        merged = dict(jdbc)
        merged.update(props)  # top-level values take precedence over the group's
        return merged
    return props


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
_COMMENT_HEADER = (
    "# SPDX-License-Identifier: Apache-2.0\n"
    "# Copyright 2026 Atlan Pte. Ltd.\n"
    "# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.\n"
    "# Regenerate: uv run python -m pyatlan.generator.generate_apps\n"
    "from __future__ import annotations\n\n"
)

_TYPING_NAMES = (
    "Any",
    "ClassVar",
    "Dict",
    "List",
    "Literal",
    "Mapping",
    "Optional",
    "Union",
)


def _module_header(body: str) -> str:
    """Build a header importing only the names ``body`` actually uses (no F401)."""
    out = [_COMMENT_HEADER.rstrip("\n") + "\n\n"]
    if re.search(r"\bjson\.", body):
        out.append("import json\n\n")
    typing_used = [n for n in _TYPING_NAMES if re.search(rf"\b{n}\b", body)]
    if typing_used:
        out.append(f"from typing import {', '.join(typing_used)}\n\n")
    if "Field(" in body:
        out.append("from pydantic.v1 import Field\n\n")
    if "Credential(" in body:
        out.append("from pyatlan.model.credential import Credential\n\n")
    base = ["AppBuilder", "AppInput"]
    if "_anchor_filter(" in body:
        base.append("_anchor_filter")
    out.append(f"from ._base import {', '.join(sorted(base))}\n\n\n")
    return "".join(out)


# reserved names a metadata/credential method must not collide with.
_RESERVED = {
    "connection",
    "agent",
    "credential_guid",
    "create",
    "preview",
    "service_account",
}


def _render_inputs(cls: str, app_id: str, ep: str, cfg: Dict[str, Any]) -> str:
    lines = [
        f"class {cls}(AppInput):",
        f'    """Typed, UI-facing inputs for the `{app_id}`'
        + (f" / `{ep}`" if ep else "")
        + ' app (generated from its configmap)."""',
        "",
        f'    _APP_ID: ClassVar[str] = "{app_id}"',
        f"    _ENTRYPOINT: ClassVar[Optional[str]] = {ep!r}",
        "",
        "    # Step 1 · Credential / Connection plumbing",
        "    connection: Optional[Any] = None",
        '    extraction_method: str = "direct"',
        "    credential_guid: Optional[str] = None",
        "    agent_json: Optional[Any] = None",
        "",
        "    # Step 3 · Metadata (only fields the UI surfaces)",
    ]
    for snake, key, spec in _metadata_fields(cfg):
        ptype = _py_type(spec)
        default = _default_repr(spec)
        if default == "None":
            ptype = f"Optional[{ptype}]"
        alias = "" if snake == key else f', alias="{key}"'
        if snake == key and not alias:
            lines.append(f"    {snake}: {ptype} = {default}")
        else:
            lines.append(f"    {snake}: {ptype} = Field({default}{alias})")
        doc = _doc(spec)
        if doc:
            lines.append(f'    """{doc}"""')
    return "\n".join(lines) + "\n"


# Type-appropriate empty defaults so every visible field is always submitted
# (the UI posts all form fields; the contract rejects null for typed fields).
_EMPTY_DEFAULT = {
    "boolean": "False",
    "string": '""',
    "conditional": '"{}"',  # include/exclude filters
    "object": "{}",
    "array": "[]",
    "integer": "0",
    "number": "0",
}


def _cmp(repr_val: str) -> str:
    """Use identity comparison for singletons (ruff E712/E711), else equality."""
    return "is" if repr_val in ("True", "False", "None") else "=="


def _placeholder_default(spec: Dict[str, Any]) -> Any:
    """A UI placeholder that is a *concrete* value usable as a default — a number
    (e.g. port 443) or a URL — as opposed to hint text ("Project ID", "host").
    The UI surfaces some real defaults via the placeholder rather than ``default``."""
    ph = str(_ui(spec).get("placeholder") or "").strip()
    if not ph:
        return None
    if ph.isdigit():
        return int(ph)
    if ph.startswith(("http://", "https://")):
        return ph
    return None


def _default_repr(spec: Dict[str, Any]) -> str:
    if "default" in spec and spec["default"] is not None:
        return repr(spec["default"])
    enum = spec.get("enum")
    if enum:  # a constrained field defaults to its first allowed value
        return repr(enum[0])
    ph = _placeholder_default(spec)  # the UI's concrete-placeholder default
    if ph is not None:
        return repr(ph)
    return _EMPTY_DEFAULT.get(spec.get("type") or "", "None")


def _render_credential_method(
    av: str, props: Dict[str, Any], target_field: str, config_name: str, used: set
) -> Tuple[str, Dict[str, Any]]:
    """Render one credential method for auth-type ``av`` within a credential-props
    root (top-level, or a JDBC-URL group — see :func:`_credential_props`).

    ``target_field`` is the input field the vaulted credential lands in (e.g.
    ``credential_guid`` or dbt's ``api_credential_guid``); ``config_name`` is that
    credential's connector config. Returns (code, info)."""
    nested = (props.get(av) or {}).get("properties") or {}
    # Concise, stable method name from the auth-type key (e.g. basic, ntlm, jwt).
    mname = _snake(av)
    if mname in _RESERVED or mname in used:
        mname = f"{mname}_auth"
    used.add(mname)

    params: List[str] = ["self", "*"]
    body_extras: List[Tuple[str, str, bool]] = []
    required_params: List[str] = []
    # connector_type is intentionally omitted: the vault stores credentials with an
    # empty connector_type, and a non-empty value blocks vaulting into a named field
    # (e.g. dbt's api_credential_guid). connector_config_name identifies the connector.
    cred_kwargs: List[str] = [
        f'connector_config_name="{config_name}"',
        f'auth_type="{av}"',
    ]
    doc_lines: List[str] = []
    pnames: set = set()  # dedupe param names within this method

    def label_of(spec: Dict[str, Any]) -> str:
        return (_ui(spec).get("label") or "").strip()

    def unique(name: str) -> str:
        candidate, i = name, 2
        while candidate in pnames or candidate in ("self", "extra"):
            candidate, i = f"{name}_{i}", i + 1
        pnames.add(candidate)
        return candidate

    # username / password (the secret-bearing fields)
    for field in ("username", "password"):
        if field in nested:
            pn = unique(field)
            params.append(f"{pn}: str")
            cred_kwargs.append(f"{field}={pn}")
            required_params.append(pn)
            lbl = label_of(nested[field])
            if lbl:
                doc_lines.append(f":param {pn}: {lbl}.")

    # extra.* sub-fields -> explicit kwargs folded into extras. Two sources:
    # the auth object's own ``extra`` and a sibling ``extra`` at the props root
    # (e.g. a JDBC-URL group's database / ssl flags).
    extra_sources = [
        (nested.get("extra") or {}).get("properties") or {},
        (props.get("extra") or {}).get("properties") or {},
    ]
    for extra_props in extra_sources:
        for ekey, espec in extra_props.items():
            pname = unique(_snake(ekey))
            required = espec.get("required")
            params.append(
                f"{pname}: str" if required else f"{pname}: Optional[str] = None"
            )
            body_extras.append((ekey, pname, bool(required)))
            if required:
                required_params.append(pname)
            lbl = label_of(espec)
            if lbl:
                doc_lines.append(f":param {pname}: {lbl}.")

    # top-level connectivity (extra.connect_type)
    conn_spec = props.get("extra.connect_type") or {}
    has_connectivity = bool(conn_spec)
    conn_param = ""
    if has_connectivity:
        default = (conn_spec.get("enum") or ["public"])[0]
        conn_param = unique("connectivity")
        params.append(f'{conn_param}: str = "{default}"')

    # host / port — exposed when the credential form has them. Defaulted from the
    # configmap when it provides one; otherwise required (e.g. mssql host/port).
    host_spec = props.get("host")
    port_spec = props.get("port")
    # Fall back to a concrete UI placeholder (e.g. port 443, a URL host) when the
    # configmap provides no explicit `default`.
    host_default = (host_spec or {}).get("default")
    if host_default is None and host_spec:
        host_default = _placeholder_default(host_spec)
    port_default = (port_spec or {}).get("default")
    if port_default is None and port_spec:
        port_default = _placeholder_default(port_spec)
    host_param = port_param = ""
    if host_spec is not None:
        host_param = unique("host")
        if host_default is not None:
            params.append(f"{host_param}: Optional[str] = None")
        else:
            params.append(f"{host_param}: str")
            required_params.append(host_param)
    if port_spec is not None:
        port_param = unique("port")
        if port_default is not None:
            params.append(f"{port_param}: Optional[int] = None")
        else:
            params.append(f"{port_param}: int")
            required_params.append(port_param)
    params.append("**extra: Any")

    code = [f'    def {mname}({", ".join(params)}) -> "{{cls}}":']
    lbl = (_ui(props.get(av, {})).get("label") or av).strip()
    docstring = f"Direct extraction with {lbl} auth."
    code.append(f'        """{docstring}')
    code.append("")
    for dl in doc_lines:
        code.append(f"        {dl}")
    code.append('        """')
    # extras assembly
    code.append("        extras: Dict[str, Any] = {}")
    for ekey, pname, required in body_extras:
        if required:
            code.append(f'        extras["{ekey}"] = {pname}')
        else:
            code.append(f"        if {pname} is not None:")
            code.append(f'            extras["{ekey}"] = {pname}')
    if has_connectivity:
        code.append(f'        extras["connect_type"] = {conn_param}')
    code.append("        extras.update(extra)")
    if host_param:
        cred_kwargs.append(
            f"host={host_param} or {host_default!r}"
            if host_default is not None
            else f"host={host_param}"
        )
    if port_param:
        cred_kwargs.append(
            f"port={port_param} or {port_default!r}"
            if port_default is not None
            else f"port={port_param}"
        )
    cred_kwargs.append("extra=extras")  # 'extra' is the Credential field alias
    code.append("        return self._stage_credential(")
    code.append(f'            "{target_field}",')
    code.append("            Credential(")
    for kw in cred_kwargs:
        code.append(f"                {kw},")
    code.append("            ),")
    code.append("        )")
    return "\n".join(code), {"name": mname, "required": required_params}


def _value_type(spec: Dict[str, Any]) -> str:
    """Python type hint for a metadata method's value param, incl. Literal enums."""
    enum = spec.get("enum")
    if enum and all(isinstance(e, str) for e in enum):
        return "Literal[" + ", ".join(repr(e) for e in enum) + "]"
    return _py_type(spec)


def _render_metadata_method(
    snake: str, key: str, spec: Dict[str, Any], used: set
) -> Tuple[str, str, str]:
    """Render one metadata method. Returns (code, method_name, sample_arg) — the
    sample is a representative argument used in the class docstring example."""
    ui = _ui(spec)
    label = (ui.get("label") or "").strip()
    mname = _snake(label) if label else snake
    if mname in _RESERVED or mname in used:
        mname = f"set_{snake}"
    used.add(mname)
    widget = ui.get("widget")
    doc = _doc(spec)
    docstring = f'        """{doc}"""' if doc else ""
    if widget == "boolean":
        sig = f'    def {mname}(self, enabled: bool = True) -> "{{cls}}":'
        body = f'        self._metadata["{key}"] = enabled'
        sample = "True"
    elif widget == "sqltree":
        sig = (
            f"    def {mname}(self, assets: "
            'Union[str, Mapping[str, List[str]]]) -> "{cls}":'
        )
        body = f'        self._metadata["{key}"] = _anchor_filter(assets)'
        sample = '{"my_db": ["my_schema"]}'
    elif spec.get("type") in ("object", "conditional"):
        # object/filter fields are submitted as a JSON string: the contract accepts
        # a string or array (not a nested object), and the worker json.loads it back.
        vtype = _value_type(spec)
        sig = f'    def {mname}(self, value: {vtype}) -> "{{cls}}":'
        body = (
            f'        self._metadata["{key}"] = '
            "value if isinstance(value, str) else json.dumps(value)"
        )
        sample = "{}"
    else:
        vtype = _value_type(spec)
        sig = f'    def {mname}(self, value: {vtype}) -> "{{cls}}":'
        body = f'        self._metadata["{key}"] = value'
        enum = spec.get("enum")
        if enum:
            sample = repr(enum[0])
        elif vtype == "str":
            sample = '""'
        elif vtype.startswith(("Dict", "Union")):
            sample = "{}"
        elif vtype == "int":
            sample = "0"
        elif vtype == "float":
            sample = "0.0"
        elif vtype.startswith("List"):
            sample = "[]"
        else:
            sample = "None"
    parts = [sig]
    if docstring:
        parts.append(docstring)
    parts.append(body)
    parts.append("        return self")
    return "\n".join(parts), mname, sample


def _render_builder(
    cls: str,
    inputs_cls: str,
    app_id: str,
    ep: str,
    cfg: Dict[str, Any],
    creds: List[Tuple[str, Dict[str, Any], str]],
    connector_name: str,
    connector_config: str,
) -> Tuple[str, List[Dict[str, Any]]]:
    hidden = _hidden_defaults(cfg)
    auth_infos: List[Dict[str, Any]] = []

    # Render credential methods first (so the docstring example can reference one).
    # A connector may expose several credential widgets (e.g. dbt) — emit a method
    # per auth-type of each, targeting that widget's input field.
    used: set = set()
    cred_blocks: List[str] = []
    for target_field, cm2, config_name in creds:
        cred_props = _credential_props(cm2)
        for av in _auth_keys(cred_props):
            code, info = _render_credential_method(
                av, cred_props, target_field, config_name, used
            )
            auth_infos.append(info)
            cred_blocks.append("    # ── Step 1 · Credential ──")
            cred_blocks.append(code.replace("{cls}", cls))
            cred_blocks.append("")

    # Render metadata methods, collecting (name, sample) for the example.
    meta_used: set = set()
    meta_blocks: List[str] = []
    meta_samples: List[Tuple[str, str]] = []
    for snake, key, spec in _metadata_fields(cfg):
        code, mname, sample = _render_metadata_method(snake, key, spec, meta_used)
        meta_blocks.append(code.replace("{cls}", cls))
        meta_blocks.append("")
        meta_samples.append((mname, sample))

    # Apps that select an existing connection (e.g. miners) instead of creating one.
    selects_connection = any(
        _ui(s).get("widget") == "connectionSelector"
        for s in (cfg.get("properties") or {}).values()
        if isinstance(s, dict)
    )
    docstring = _builder_docstring(
        cls, app_id, ep, auth_infos, meta_samples, connector_name, selects_connection
    )
    # The direct-extraction method defaults to "direct"; some apps require another
    # value (e.g. bigquery-miner -> "query_history") via the configmap's
    # extraction-method default. Emit an override only when it differs.
    em_default = ((cfg.get("properties") or {}).get("extraction-method") or {}).get(
        "default"
    ) or "direct"
    lines = [
        f"class {cls}(AppBuilder):",
        docstring,
        "",
        f'    _APP_ID: ClassVar[str] = "{app_id}"',
        f"    _ENTRYPOINT: ClassVar[Optional[str]] = {ep!r}",
        f'    _CONNECTOR_NAME: ClassVar[str] = "{connector_name}"',
        f'    _CONNECTOR_CONFIG: ClassVar[str] = "{connector_config}"',
    ]
    if em_default != "direct":
        lines.append(f'    _EXTRACTION_METHOD: ClassVar[str] = "{em_default}"')
    lines += [
        f"    _INPUTS_CLASS = {inputs_cls}",
        f"    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {hidden!r}",
        "",
    ]
    lines.extend(cred_blocks)
    if meta_blocks:
        lines.append("    # ── Step 3 · Metadata ──")
        lines.extend(meta_blocks)
    return "\n".join(lines).rstrip() + "\n", auth_infos


def _builder_docstring(
    cls: str,
    app_id: str,
    ep: str,
    auth_infos: List[Dict[str, Any]],
    meta_samples: List[Tuple[str, str]],
    connector_name: str,
    selects_connection: bool,
) -> str:
    """A class docstring with a runnable usage example (first auth + first toggle)."""
    title = (
        f"Fluent, UI-equivalent builder for the `{app_id}`"
        + (f" / `{ep}`" if ep else "")
        + " app."
    )
    chain = [f"            {cls}(client)"]
    if selects_connection:
        # e.g. miners: select an existing connection by QN — the builder reuses
        # that connection's own credential automatically (no credential step).
        chain.append(
            f'            .connection(qualified_name="default/{connector_name}/1700000000")'
        )
    else:
        if auth_infos:
            a = auth_infos[0]
            args = ", ".join(f'{p}="..."' for p in a["required"])
            chain.append(f"            .{a['name']}({args})")
        else:
            chain.append('            .credential_guid("...")')
        chain.append('            .connection(name="my-connection", admins=["jdoe"])')
    if meta_samples:
        mname, sample = meta_samples[0]
        chain.append(f"            .{mname}({sample})")
    chain.append("            .run()")
    body = "\n".join(chain)
    return (
        f'    """{title}\n\n'
        "    Example::\n\n"
        "        resp = (\n"
        f"{body}\n"
        "        )\n"
        '    """'
    )


# --------------------------------------------------------------------------- #
# generated tests (one module per app — config assertions, like test_packages)
# --------------------------------------------------------------------------- #
_TEST_HEADER = (
    "# SPDX-License-Identifier: Apache-2.0\n"
    "# Copyright 2026 Atlan Pte. Ltd.\n"
    "# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.\n"
    "# Regenerate: uv run python -m pyatlan.generator.generate_apps\n"
    "from unittest.mock import Mock\n\n"
    "from pyatlan.model.apps import {builder}, {inputs}\n\n\n"
)


def _render_test_module(
    module: str,
    app_id: str,
    ep: str,
    cfg: Dict[str, Any],
    connector_name: str,
    connector_config: str,
    builder_cls: str,
    inputs_cls: str,
    auth_infos: List[Dict[str, Any]],
    hidden: Dict[str, Any],
) -> str:
    metadata = _metadata_fields(cfg)
    em_default = ((cfg.get("properties") or {}).get("extraction-method") or {}).get(
        "default"
    ) or "direct"
    out = [_TEST_HEADER.format(builder=builder_cls, inputs=inputs_cls)]

    # 1) inputs defaults match the configmap
    out.append(f"def test_{module}_inputs_defaults():")
    out.append(f"    i = {inputs_cls}()")
    out.append(f'    assert {inputs_cls}._APP_ID == "{app_id}"')
    out.append(f"    assert {inputs_cls}._ENTRYPOINT == {ep!r}")
    asserted = 0
    for snake, _key, spec in metadata:
        default = _default_repr(spec)
        if default != "None":
            out.append(f"    assert i.{snake} {_cmp(default)} {default}")
            asserted += 1
    if not asserted:
        out.append("    assert isinstance(i.to_inputs(), dict)")
    out.append("")
    out.append("")

    # 2) builder assembles the UI-equivalent payload (uniform connection+guid path)
    out.append(f"def test_{module}_builder_payload():")
    out.append(
        f"    out = {builder_cls}(Mock()).connection("
        'name="conn", admins=["u"]).credential_guid("g").preview()'
    )
    out.append(
        f'    assert out["connection"]["attributes"]["connectorName"] '
        f'== "{connector_name}"'
    )
    out.append('    assert out["credential_guid"] == "g"')
    out.append(f'    assert out["extraction_method"] == "{em_default}"')
    for hk, hv in hidden.items():
        out.append(f'    assert out["{hk}"] {_cmp(repr(hv))} {hv!r}')
    out.append("")
    out.append("")

    # 3) every generated credential method stages a credential
    for info in auth_infos:
        mname, required = info["name"], info["required"]
        # port params are typed int — use a number; everything else a string.
        args = ", ".join(f"{p}=443" if p == "port" else f'{p}="x"' for p in required)
        out.append(f"def test_{module}_credential_{mname}():")
        out.append(f"    b = {builder_cls}(Mock()).{mname}({args})")
        out.append("    assert b._raw_creds  # a credential was staged")
        out.append("    cred = next(iter(b._raw_creds.values()))")
        out.append("    assert cred.auth_type and cred.connector_config_name")
        out.append("")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _render_module(
    app_id: str,
    ep: str,
    cfg: Dict[str, Any],
    creds: List[Tuple[str, Dict[str, Any], str]],
    connector_name: str,
    connector_config: str,
) -> Tuple[str, str, str]:
    base = _class_base(app_id, ep)
    inputs_cls, builder_cls = f"{base}Inputs", base
    builder_code, auth_infos = _render_builder(
        builder_cls,
        inputs_cls,
        app_id,
        ep,
        cfg,
        creds,
        connector_name,
        connector_config,
    )
    code = (
        _render_inputs(inputs_cls, app_id, ep, cfg)
        + "\n\n"
        + builder_code
        + f'\n\n__all__ = ["{builder_cls}", "{inputs_cls}"]\n'
    )
    body = _module_header(code) + code
    module = _module_name(app_id, ep)
    test = _render_test_module(
        module,
        app_id,
        ep,
        cfg,
        connector_name,
        connector_config,
        builder_cls,
        inputs_cls,
        auth_infos,
        _hidden_defaults(cfg),
    )
    return builder_cls, body, test


# --------------------------------------------------------------------------- #
# discovery + orchestration
# --------------------------------------------------------------------------- #
def _credential_widgets(cfg: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Every credential widget in the inputs form, as (field_wire_key, credentialType).
    Most apps have one; some (e.g. dbt) have several with different credentialTypes."""
    out: List[Tuple[str, str]] = []
    for key, spec in (cfg.get("properties") or {}).items():
        if isinstance(spec, dict) and _ui(spec).get("widget") == "credential":
            ct = _ui(spec).get("credentialType")
            if ct:
                out.append((_snake(key), ct))
    return out


def discover_targets(client: AtlanClient) -> List[Tuple[str, Optional[str]]]:
    app_ids: set = set()
    cursor: Optional[str] = None
    for _ in range(50):
        page = client.app.get_all(limit=100, cursor=cursor)
        for w in page.workflows:
            dag = getattr(w, "dag", None)
            if isinstance(dag, dict):
                aid = ((dag.get("extract") or {}).get("inputs") or {}).get("app_id")
                if aid:
                    app_ids.add(aid)
        if not page.has_more:
            break
        cursor = page.next_cursor
    targets: List[Tuple[str, Optional[str]]] = []
    for app_id in sorted(app_ids):
        try:
            info = client.app.describe(app_id)
        except Exception as exc:  # noqa: BLE001
            print(f"  SKIP {app_id}: describe failed: {str(exc)[:50]}")
            continue
        if not info.native_ready:
            print(f"  SKIP {app_id}: not native-ready")
            continue
        eps: List[Optional[str]] = [e.name for e in info.entrypoints] or [None]
        targets.extend((app_id, ep) for ep in eps)
    print(f"discovered {len(app_ids)} apps -> {len(targets)} targets")
    return targets


def _build_one(
    cms: _ConfigMaps, app_id: str, ep: Optional[str]
) -> Optional[Tuple[str, str, str, str]]:
    """Return (module_name, class_name, content, test_content) or None on skip."""
    module = _module_name(app_id, ep or "")
    if module in _HAND_WRITTEN:
        return None
    cfg = cms.get(app_id, entrypoint=ep) if ep else cms.get(app_id)
    if not cfg:
        print(f"  SKIP {app_id} ({ep}): inputs configmap missing")
        return None
    widgets = _credential_widgets(cfg)
    # Fetch each credential widget's configmap -> (field, cm2, credentialType).
    creds: List[Tuple[str, Dict[str, Any], str]] = []
    for field, ct in widgets:
        cm2 = cms.get(ct, app_id=app_id)
        if cm2:
            creds.append((field, cm2, ct))
    primary_config = widgets[0][1] if widgets else ""
    if primary_config:
        connector_name = re.sub(r"^atlan-connectors-", "", primary_config)
    else:
        # No credential widget (e.g. miners select an existing connection) — derive
        # the connector from the app-id by stripping the atlan- prefix + role suffix.
        connector_name = re.sub(
            r"-(crawler|miner)$", "", re.sub(r"^atlan-", "", app_id)
        )
    cls, content, test = _render_module(
        app_id, ep or "", cfg, creds, connector_name, primary_config
    )
    n_meta = len(_metadata_fields(cfg))
    n_auth = sum(len(_auth_keys(_credential_props(cm2))) for _, cm2, _ in creds)
    print(
        f"  generated {module}.py :: {cls} "
        f"({n_meta} metadata, {n_auth} auth methods, {len(creds)} credential(s))"
    )
    return module, cls, content, test


def generate(
    client: AtlanClient, cms: _ConfigMaps
) -> Tuple[Dict[str, Tuple[str, str, str]], set]:
    """Return ({module: (cls, content, test)}, attempted_module_names).

    ``attempted`` is every module we tried (discovery ∪ manifest); main() keeps a
    transiently-failed target's existing file rather than deleting it.
    """
    discovered = discover_targets(client)
    # Union live discovery with the manifest (deployed-only discovery misses apps
    # that are installed but not currently running).
    seen = set(discovered)
    targets = list(discovered) + [t for t in MANIFEST if t not in seen]
    print(
        f"targets: {len(discovered)} discovered + "
        f"{len(targets) - len(discovered)} from manifest = {len(targets)}"
    )
    attempted = {_module_name(a, e or "") for a, e in targets} - _HAND_WRITTEN
    modules: Dict[str, Tuple[str, str, str]] = {}
    # Keep concurrency low — the configmap service throttles bursts.
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = pool.map(lambda t: _build_one(cms, t[0], t[1]), targets)
    for res in results:
        if res:
            module, cls, content, test = res
            modules[module] = (cls, content, test)
    failed = attempted - set(modules)
    if failed:
        print(
            f"WARNING: {len(failed)} target(s) failed this run (kept existing): {sorted(failed)}"
        )
    return modules, attempted


def _render_init(
    modules: Dict[str, Tuple[str, str, str]], hand: Dict[str, List[str]]
) -> str:
    lines = [
        "# SPDX-License-Identifier: Apache-2.0",
        "# Copyright 2026 Atlan Pte. Ltd.",
        '"""Typed models and fluent builders for app workflows.',
        "",
        "Each per-app builder mirrors the UI's 3-step wizard (Credential ->",
        "Connection -> Metadata); see ``pyatlan.generator.generate_apps``.",
        '"""',
        "",
        "from pyatlan.model.apps._base import AppBuilder, AppInput",
    ]
    exports = ["AppInput", "AppBuilder"]
    # hand-written modules first
    for module, names in sorted(hand.items()):
        lines.append(
            f"from pyatlan.model.apps.{module} import " + ", ".join(sorted(names))
        )
        exports.extend(names)
    for module, (cls, _content, _test) in sorted(modules.items()):
        lines.append(f"from pyatlan.model.apps.{module} import {cls}, {cls}Inputs")
        exports.extend([cls, f"{cls}Inputs"])
    lines.append("")
    lines.append("__all__ = [")
    for name in exports:
        lines.append(f'    "{name}",')
    lines.append("]")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_url = os.environ["ATLAN_BASE_URL"]
    api_key = os.environ["ATLAN_API_KEY"]
    client = AtlanClient(base_url=base_url, api_key=api_key)
    cms = _ConfigMaps(base_url, api_key)
    out_dir = Path(__file__).resolve().parents[1] / "model" / "apps"
    test_dir = Path(__file__).resolve().parents[2] / "tests" / "unit" / "apps"
    print(f"Generating modules into {out_dir} ...")
    modules, attempted = generate(client, cms)
    # All-or-nothing: if any target failed (e.g. throttled), don't touch any files
    # — a partial write would delete good modules and desync __init__.
    failed = attempted - set(modules)
    if failed:
        raise SystemExit(
            f"Aborting — {len(failed)} target(s) failed to fetch, no files changed. "
            f"Re-run (transient throttling): {sorted(failed)}"
        )
    # Clear stale generated modules (keep _base.py, __init__.py, hand-written).
    keep = {"_base.py", "__init__.py"} | {f"{m}.py" for m in _HAND_WRITTEN}
    for existing in out_dir.glob("*.py"):
        if existing.name not in keep:
            existing.unlink()
    test_dir.mkdir(parents=True, exist_ok=True)
    for existing in test_dir.glob("test_*.py"):
        existing.unlink()
    for module, (_cls, content, test) in modules.items():
        (out_dir / f"{module}.py").write_text(content)
        (test_dir / f"test_{module}.py").write_text(test)
    # __init__ also re-exports hand-written builders.
    hand = {"bigquery_crawler": ["BigqueryCrawler", "BigqueryCrawlerInputs"]}
    (out_dir / "__init__.py").write_text(_render_init(modules, hand))
    _format([out_dir, test_dir])
    print(
        f"done ({len(modules)} generated + {len(hand)} hand-written modules; "
        f"tests in {test_dir})"
    )


def _format(paths: List[Path]) -> None:
    """Format + lint-fix the generated code so the output is always clean and
    deterministic (no manual ruff pass needed)."""
    ruff = shutil.which("ruff")
    if not ruff:
        print("WARNING: ruff not found on PATH — skipping auto-format")
        return
    targets = [str(p) for p in paths]
    print("formatting generated code (ruff) ...")
    # check --fix first (drops any unused import, sorts), then format (style).
    subprocess.run([ruff, "check", "--fix", "--quiet", *targets], check=False)
    subprocess.run([ruff, "format", "--quiet", *targets], check=False)


if __name__ == "__main__":
    main()
