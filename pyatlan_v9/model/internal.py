# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

"""
Internal model classes for pyatlan_v9, migrated from pyatlan/model/internal.py.
"""

from __future__ import annotations

import msgspec


class Internal(msgspec.Struct, kw_only=True):
    """For internal usage."""


class AtlasServer(msgspec.Struct, kw_only=True):
    """For internal usage."""
