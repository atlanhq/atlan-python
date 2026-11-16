# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any

# The assets subpackage is lazy (lazy_loader): importing it loads only the
# eager base classes. Re-export its names through __getattr__ rather than
# ``from .assets import *`` — a star import resolves every name in __all__ and
# so loads every asset module while this package is still initialising. A
# thread that imports any ``pyatlan_v9.model.*`` submodule during that window
# holds the submodule's import lock while waiting for this package, and this
# package's initialisation waits for that submodule's lock: Python raises
# ``_DeadlockError`` or hands back a partially initialised module.
from . import assets as _assets

__all__ = list(_assets.__all__)


def __getattr__(name: str) -> Any:
    """Delegate lazy imports to the assets subpackage."""
    return getattr(_assets, name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
