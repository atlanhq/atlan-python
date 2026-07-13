# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
"""Regression gate for the asset-model import cost (CONNECT-49).

Importing the ``pydantic.v1`` asset models used to take ~8s (worse on slower /
Windows boxes, up to a hang) because pydantic.v1's metaclass deep-copies the
whole accumulated ``__fields__`` dict at every level of the hierarchy. A narrow
``smart_deepcopy`` optimization (:mod:`pyatlan._pydantic_v1_perf`) fixes that.

These tests fail if the optimization is removed or stops taking effect.
"""

import os
import subprocess
import sys
import time


def _run(code: str, env=None) -> str:
    return subprocess.check_output([sys.executable, "-c", code], text=True, env=env)


def test_import_optimization_is_active():
    # Deterministic (non-timing): after importing pyatlan, pydantic.v1's
    # smart_deepcopy is our narrow replacement in every module that bound it.
    out = _run(
        "import pyatlan\n"
        "import pydantic.v1.utils as u, pydantic.v1.main as m, pydantic.v1.fields as f\n"
        "mod = 'pyatlan._pydantic_v1_perf'\n"
        "assert u.smart_deepcopy.__module__ == mod, u.smart_deepcopy.__module__\n"
        "assert m.smart_deepcopy.__module__ == mod, m.smart_deepcopy.__module__\n"
        "assert f.smart_deepcopy.__module__ == mod, f.smart_deepcopy.__module__\n"
        "print('active')\n"
    )
    assert "active" in out


def test_cold_import_stays_well_under_pre_fix_cost():
    # Backstop: a fresh-process cold import of a heavy model must be far below the
    # ~8s pre-fix cost. Generous ceiling to stay non-flaky on loaded CI while
    # still catching a hang or the optimization being removed (which restores ~8s).
    start = time.perf_counter()
    subprocess.check_call(
        [sys.executable, "-c", "from pyatlan.model.assets import Column"]
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 6.0, (
        f"cold import took {elapsed:.1f}s; pre-fix was ~8s — the pydantic.v1 "
        f"import optimization may have regressed (see pyatlan._pydantic_v1_perf)."
    )


def test_models_are_correct_under_optimization():
    # The optimization must not change model behavior: field integrity,
    # construction, serialization, and per-instance default isolation.
    out = _run(
        "from pyatlan.model.assets import Column\n"
        "a = Column(name='a', qualified_name='qa')\n"
        "b = Column(name='b', qualified_name='qb')\n"
        "assert a.attributes is not b.attributes  # defaults isolated per instance\n"
        "assert 'attributes' in a.dict(by_alias=True)\n"
        "assert len(Column.__fields__) > 0\n"
        "print('ok')\n"
    )
    assert "ok" in out


def test_opt_out_env_restores_stock_behavior():
    # PYATLAN_DISABLE_IMPORT_PATCH=1 must fully disable the optimization.
    env = {**os.environ, "PYATLAN_DISABLE_IMPORT_PATCH": "1"}
    out = _run(
        "import pyatlan, pydantic.v1.utils as u\nprint(u.smart_deepcopy.__module__)\n",
        env=env,
    )
    assert "pyatlan._pydantic_v1_perf" not in out
