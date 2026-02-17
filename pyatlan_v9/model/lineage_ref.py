# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Union

import msgspec


class LineageRef(msgspec.Struct, kw_only=True):
    """Reference to an asset within a lineage result."""

    qualified_name: Union[str, None] = None
    """Unique name of the asset being referenced."""

    name: Union[str, None] = None
    """Simple name of the asset being referenced."""

    guid: Union[str, None] = None
    """UUID of the asset being referenced."""
