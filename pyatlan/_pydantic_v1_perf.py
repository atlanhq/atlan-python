# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
"""Speed up importing pyatlan's ``pydantic.v1`` asset models (CONNECT-49).

The stable asset models live on the ``pydantic.v1`` compatibility shim. During
class creation pydantic.v1's metaclass copies the whole *accumulated* ``__fields__``
dict at every level of the hierarchy::

    # pydantic/v1/main.py, ModelMetaclass.__new__
    fields.update(smart_deepcopy(base.__fields__))

``smart_deepcopy`` falls through to ``copy.deepcopy``, which recurses into every
``ModelField`` (its ``field_info``, ``type_``, sub-fields, validators). Across
pyatlan's deep, wide *generated* model tree this is O(n^2) recursive deep-copy —
millions of ``deepcopy`` calls — so ``from pyatlan.model.assets import Column``
takes ~7-15s depending on single-thread speed (worst on slower / AV'd Windows
laptops, but ~8s even on a stock CI Linux box). See CONNECT-49.

Fix: install a **narrow** replacement for ``smart_deepcopy`` that optimizes only
that one case — copying a dict whose values are ``ModelField``\\ s. Each class
still gets its **own** ``ModelField`` + ``field_info`` (so no field state is
shared across the class tree), we just skip the deep recursion into
``type_``/sub-fields/validators that isn't needed for correctness. Every other
``smart_deepcopy`` call — notably the per-instance copy of mutable field
*defaults* — defers to the original, so default-isolation semantics are
unchanged for pyatlan **and** any other ``pydantic.v1`` user in the process.

Measured (cold ``import Column``, py3.12.3 / pydantic 2.13.4):
``windows-latest`` 7.6s -> 2.6s, ``ubuntu-latest`` 8.2s -> 2.8s (~2.9x), with
model construction, validation, serialization and default-isolation unchanged.

Opt out with ``PYATLAN_DISABLE_IMPORT_PATCH=1``.
"""

from __future__ import annotations

import os

_INSTALLED = False


def install() -> bool:
    """Install the narrow ``smart_deepcopy`` optimization (idempotent).

    Returns ``True`` if the optimization is active. Never raises: on any
    incompatibility (e.g. a future pydantic internal change) it silently
    no-ops so it can never break ``import pyatlan``.
    """
    global _INSTALLED
    if _INSTALLED:
        return True
    if os.getenv("PYATLAN_DISABLE_IMPORT_PATCH", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        return False
    try:
        import copy

        import pydantic.v1.fields as _fields
        import pydantic.v1.main as _main
        import pydantic.v1.utils as _utils
        from pydantic.v1.fields import ModelField

        _original_smart_deepcopy = _utils.smart_deepcopy

        def _smart_deepcopy(obj):
            # Fast path ONLY for the accumulated ``__fields__`` dict that
            # pydantic copies per subclass during class creation. Give each
            # class its own ModelField + field_info (shallow) rather than a full
            # recursive deep-copy of the field graph.
            if type(obj) is dict and obj:
                if type(next(iter(obj.values()))) is ModelField:
                    out = {}
                    for field_name, field in obj.items():
                        new_field = copy.copy(field)
                        new_field.field_info = copy.copy(field.field_info)
                        out[field_name] = new_field
                    return out
            # Everything else (field defaults, arbitrary values) keeps the
            # original deep-copy semantics.
            return _original_smart_deepcopy(obj)

        # pydantic.v1's ``main`` and ``fields`` modules bound ``smart_deepcopy``
        # by value (``from .utils import smart_deepcopy``), so patch all three.
        _utils.smart_deepcopy = _smart_deepcopy
        _main.smart_deepcopy = _smart_deepcopy
        _fields.smart_deepcopy = _smart_deepcopy
        _INSTALLED = True
        return True
    except Exception:  # pragma: no cover - defensive; must never block import
        return False
