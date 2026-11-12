# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""First-time imports of pyatlan_v9 model modules must be safe across threads.

A worker that loads ``pyatlan_v9`` lazily can import it from several threads at
once. If two of these modules import each other at module scope, one thread
holds module A's import lock while waiting for B and another holds B's while
waiting for A: Python raises ``_DeadlockError``, or a thread sees a partially
initialised module (``cannot import name 'Asset'``).

Each case runs in a fresh interpreter so ``sys.modules`` starts empty; the
import race only exists on a module's first import.
"""

import subprocess
import sys
import textwrap

import pytest

_MODULES = [
    "pyatlan_v9.model.assets",
    "pyatlan_v9.model.conversion_utils",
    "pyatlan_v9.model.transform",
    "pyatlan_v9.model.assets.asset",
    "pyatlan_v9.model.assets.referenceable",
]

_RACE = textwrap.dedent(
    """
    import sys
    import threading

    modules = sys.argv[1].split(",")
    barrier = threading.Barrier(len(modules))
    errors = []

    def load(name):
        barrier.wait()
        try:
            __import__(name)
        except BaseException as exc:  # noqa: BLE001 - report every failure
            errors.append(f"{name}: {type(exc).__name__}: {exc}")

    threads = [threading.Thread(target=load, args=(m,)) for m in modules]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    if errors:
        print("\\n".join(errors))
        sys.exit(1)
    """
)


@pytest.mark.parametrize("attempt", range(10))
def test_first_import_from_many_threads_does_not_deadlock(attempt):
    # Two threads per module, so every pair of modules races both ways.
    modules = ",".join(_MODULES * 2)
    result = subprocess.run(
        [sys.executable, "-c", _RACE, modules],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stdout + result.stderr
