# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Generate typed ``*Inputs`` classes from apps' live input contracts (BLDX-1472).

For each (app_id, entrypoint) in MANIFEST, fetch the ``/v1/apps/{app}/inputs``
JSON Schema and emit a pydantic class extending ``AppInput`` into
``pyatlan/model/app_inputs/_generated.py``. The class mirrors the app's UI form:
typed fields, contract defaults, and the field ``title`` as its docstring.

Run (needs ATLAN_BASE_URL + ATLAN_API_KEY for a tenant with the apps deployed):

    uv run python -m pyatlan.generator.generate_app_inputs
"""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pyatlan.client.atlan import AtlanClient

# (app_id, entrypoint or None for default). Extend to cover more connectors.
MANIFEST: List[Tuple[str, str]] = [
    ("bigquery-crawler", "crawler"),
    ("bigquery-miner", "miner"),
    ("snowflake-crawler", "crawler"),
    ("oracle-crawler", "crawler"),
    ("postgres-crawler", "crawler"),
    ("atlan-mssql", "crawler"),
]

# Internal/infra fields the UI never surfaces — kept out of the typed classes so
# they mirror the user-facing form rather than the full data contract. (Handshake
# ids stripped server-side, plus output/checkpoint/publish/runtime-tuning knobs.)
_EXCLUDE = {
    "user-id",
    "user_id",
    "workflow_id",
    "correlation_id",
    "output_dir",
    "checkpoint_dir",
    "output_prefix",
    "output_path",
    "load_to_atlan",
    "publish_dry_run",
    "atlas_auth_type",
    "max_concurrent_activities",
    "max_activities_per_execution",
    "enable_continue_as_new",
    "schedule_to_start_timeout_secs",
}

_PRIMITIVE = {
    "boolean": "bool",
    "integer": "int",
    "number": "float",
    "string": "str",
    "object": "Dict[str, Any]",
    "array": "List[Any]",
}


def _py_type(spec: Dict[str, Any]) -> str:
    if not isinstance(spec, dict):
        return "Any"
    if "type" in spec and spec["type"] in _PRIMITIVE:
        return _PRIMITIVE[spec["type"]]
    if "anyOf" in spec:
        members = []
        for m in spec["anyOf"]:
            t = _py_type(m)
            if t not in members and t != "Any":
                members.append(t)
        if not members:
            return "Any"
        return members[0] if len(members) == 1 else f"Union[{', '.join(members)}]"
    return "Any"


def _render_default(value: Any) -> str:
    return repr(value)


def _camel(text: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[^0-9A-Za-z]+", text) if p)


def _class_name(app_id: str, entrypoint: str) -> str:
    base = _camel(app_id)
    ep = _camel(entrypoint or "")
    if ep and ep.lower() not in base.lower():
        base += ep
    return f"{base}Inputs"


def _render_class(
    name: str, app_id: str, entrypoint: str, contract: Dict[str, Any]
) -> str:
    props: Dict[str, Any] = contract.get("properties") or {}
    required = set(contract.get("required") or [])
    lines = [
        f"class {name}(AppInput):",
        f'    """Typed inputs for the `{app_id}`'
        + (f" / `{entrypoint}`" if entrypoint else "")
        + ' app (generated from its input contract)."""',
        "",
        f'    _APP_ID: ClassVar[str] = "{app_id}"',
        f"    _ENTRYPOINT: ClassVar[Optional[str]] = {entrypoint!r}",
        "",
    ]
    body = []
    for fname, spec in props.items():
        if fname in _EXCLUDE:
            continue
        spec = spec if isinstance(spec, dict) else {}
        ptype = _py_type(spec)
        valid_id = fname.isidentifier()
        attr = fname if valid_id else re.sub(r"[^0-9A-Za-z_]", "_", fname)
        has_default = "default" in spec and fname not in required
        if has_default:
            default = _render_default(spec["default"])
            field_args = [default] if valid_id else [f"default={default}"]
        else:
            ptype = f"Optional[{ptype}]"
            field_args = ["None"] if valid_id else ["default=None"]
        if not valid_id:
            field_args.append(f'alias="{fname}"')
        rhs = (
            field_args[0]
            if len(field_args) == 1 and valid_id
            else f"Field({', '.join(field_args)})"
        )
        body.append(f"    {attr}: {ptype} = {rhs}")
        title = spec.get("title")
        if title:
            body.append(f'    """{title}"""')
    lines.extend(body or ["    pass"])
    return "\n".join(lines) + "\n"


_MODULE_HEADER = (
    "# SPDX-License-Identifier: Apache-2.0\n"
    "# Copyright 2026 Atlan Pte. Ltd.\n"
    "# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.\n"
    "# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs\n"
    "from __future__ import annotations\n\n"
    "from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401\n\n"
    "from pydantic.v1 import Field  # noqa: F401\n\n"
    "from pyatlan.model.app_inputs._base import AppInput\n\n\n"
)


def _module_name(app_id: str, entrypoint: str) -> str:
    base = re.sub(r"[^0-9a-z]+", "_", app_id.lower()).strip("_")
    ep = re.sub(r"[^0-9a-z]+", "_", (entrypoint or "").lower()).strip("_")
    if ep and ep not in base:
        base = f"{base}_{ep}"
    return base


def discover_targets(client: AtlanClient) -> List[Tuple[str, Optional[str]]]:
    """Discover every app deployed on the tenant and resolve its entrypoints.

    There is no catalog endpoint, so we collect distinct ``app_id``s from the
    deployed workflows' DAGs, then describe each app for its entrypoints. Only
    native-ready apps are kept; an app with no named entrypoints yields one
    target with the default (``None``).
    """
    app_ids: set[str] = set()
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
            info = client.app.get_app(app_id)
        except Exception as exc:  # noqa: BLE001
            print(f"  SKIP {app_id}: describe failed: {str(exc)[:60]}")
            continue
        if not info.native_ready:
            print(f"  SKIP {app_id}: not native-ready")
            continue
        eps = [e.name for e in info.entrypoints] or [None]
        targets.extend((app_id, ep) for ep in eps)
    print(f"discovered {len(app_ids)} apps -> {len(targets)} targets")
    return targets


def _fetch_contract(
    client: AtlanClient, app_id: str, entrypoint: Optional[str]
) -> Tuple[str, Optional[str], Any, Any]:
    """Fetch one contract, trying the entrypoint then the default. Thread-safe."""
    last: Any = None
    for ep in (entrypoint, None) if entrypoint else (None,):
        try:
            return app_id, ep, client.app.get_input_contract(app_id, entrypoint=ep), None
        except Exception as exc:  # noqa: BLE001
            last = exc
    return app_id, entrypoint, None, last


def generate(
    client: AtlanClient, targets: Optional[List[Tuple[str, Optional[str]]]] = None
) -> Dict[str, Tuple[str, str]]:
    """Return {module_name: (class_name, file_content)} for each resolved app.

    ``targets`` defaults to live discovery of every app on the tenant. Contracts
    are fetched concurrently (the slow per-app step).
    """
    if targets is None:
        targets = discover_targets(client)
    modules: Dict[str, Tuple[str, str]] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(lambda t: _fetch_contract(client, t[0], t[1]), targets)
    for app_id, entrypoint, contract, last in results:
        if contract is None:
            print(f"  SKIP {app_id}: {str(last)[:80]}")
            continue
        class_name = _class_name(app_id, entrypoint or "")
        module = _module_name(app_id, entrypoint or "")
        content = _MODULE_HEADER + _render_class(
            class_name, app_id, entrypoint or "", contract.dict()
        )
        content += f'\n\n__all__ = ["{class_name}"]\n'
        modules[module] = (class_name, content)
        print(
            f"  generated {module}.py :: {class_name} ({len(contract.field_names())} fields)"
        )
    return modules


def _render_init(modules: Dict[str, Tuple[str, str]]) -> str:
    lines = [
        "# SPDX-License-Identifier: Apache-2.0",
        "# Copyright 2026 Atlan Pte. Ltd.",
        '"""Typed, contract-generated input models for native (v3) app workflows.',
        "",
        "``AppInput`` is the base; each ``*Inputs`` class is generated per app/entrypoint",
        "from the app's live input contract (see",
        "``pyatlan.generator.generate_app_inputs``). Pass an instance straight to",
        "``client.app.create(..., inputs=...)``.",
        '"""',
        "",
        "from pyatlan.model.app_inputs._base import AppInput",
    ]
    for module, (class_name, _) in sorted(modules.items()):
        lines.append(f"from pyatlan.model.app_inputs.{module} import {class_name}")
    lines.append("")
    lines.append("__all__ = [")
    lines.append('    "AppInput",')
    for _, (class_name, _content) in sorted(modules.items()):
        lines.append(f'    "{class_name}",')
    lines.append("]")
    return "\n".join(lines) + "\n"


def main() -> None:
    client = AtlanClient()
    out_dir = Path(__file__).resolve().parents[1] / "model" / "app_inputs"
    print(f"Generating modules into {out_dir} ...")
    modules = generate(client)
    # Clear stale generated modules (keep _base.py and __init__.py).
    for existing in out_dir.glob("*.py"):
        if existing.name not in {"_base.py", "__init__.py"}:
            existing.unlink()
    for module, (_class_name, content) in modules.items():
        (out_dir / f"{module}.py").write_text(content)
    (out_dir / "__init__.py").write_text(_render_init(modules))
    print(f"done ({len(modules)} modules)")


if __name__ == "__main__":
    main()
