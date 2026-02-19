# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
SnowflakeDynamicTable asset model.

This module provides the SnowflakeDynamicTable flat asset class,
which extends Asset with Snowflake dynamic table-specific attributes.
In the legacy codebase, SnowflakeDynamicTable extends Table.
"""

from __future__ import annotations

from typing import Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.model.transform import register_asset

from .asset import Asset


@register_asset
class SnowflakeDynamicTable(Asset):
    """
    Instance of a Snowflake dynamic table in Atlan.
    """

    type_name: Union[str, UnsetType] = "SnowflakeDynamicTable"

    definition: Union[str, None, UnsetType] = UNSET
    """SQL statements used to define the dynamic table."""
