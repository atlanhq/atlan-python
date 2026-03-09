# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any

# Re-export eagerly loaded base classes from the assets subpackage
from .assets import *  # noqa: F401, F403

# Re-export all names from the assets __all__
from .assets import __all__ as _assets_all

__all__ = list(_assets_all)


def __getattr__(name: str) -> Any:
    """Delegate lazy imports to the assets subpackage."""
    from . import assets

    return getattr(assets, name)
